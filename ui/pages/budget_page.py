"""Этап 9 — страница бюджетов и лимитов.

Лимит ставится на трёх уровнях: весь проект, текущая задача, отдельный агент.
Каждый — и по токенам, и по деньгам. Пустое поле означает «без ограничения»:
так же, как лимит токенов при постановке задачи.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from core.budget import SCOPE_TITLES, ScopeState, load_states
from core.events import Event, EventBus, EventType
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, info

#: цвет полосы в зависимости от того, насколько выбран бюджет
BAR_COLORS = [(1.0, "#ef5f6b"), (0.8, "#f0b429"), (0.0, "#6c8cff")]


def _bar_color(ratio: float) -> str:
    for threshold, colour in BAR_COLORS:
        if ratio >= threshold:
            return colour
    return BAR_COLORS[-1][1]


class LimitRow(Card):
    """Одна строка: уровень, расход и поля лимитов."""

    def __init__(self, parent: QWidget, state: ScopeState, on_change) -> None:
        super().__init__(parent, spacing=8)
        self.state = state
        self.on_change = on_change

        head = QHBoxLayout()
        name = QLabel(state.name)
        name.setObjectName("H2")
        head.addWidget(name)
        scope = QLabel(SCOPE_TITLES.get(state.scope, state.scope))
        scope.setObjectName("Dim")
        head.addWidget(scope)
        head.addStretch(1)

        spent = QLabel(tr("bud.spent",
                          tokens=f"{state.tokens:,}".replace(",", " "),
                          cost=f"{state.cost:.4f}"))
        spent.setObjectName("Dim")
        head.addWidget(spent)
        self.body.addLayout(head)

        if state.limit.is_set:
            ratio = min(state.ratio(), 1.0)
            bar = QProgressBar()
            bar.setTextVisible(False)
            bar.setValue(int(ratio * 100))
            colour = _bar_color(state.ratio())
            bar.setStyleSheet(
                f"QProgressBar::chunk {{ background: {colour}; border-radius: 6px; }}"
            )
            self.body.addWidget(bar)

            note = QLabel(tr("bud.used_pct", pct=f"{state.ratio() * 100:.0f}"))
            note.setStyleSheet(f"color: {colour};")
            if state.exceeded():
                note.setText(tr("bud.exceeded"))
            self.body.addWidget(note)

        fields = QHBoxLayout()
        tokens_col = QVBoxLayout()
        tokens_col.addWidget(QLabel(tr("bud.token_limit")))
        self.tokens_edit = QLineEdit(
            str(state.limit.token_limit) if state.limit.token_limit else ""
        )
        self.tokens_edit.setPlaceholderText(tr("bud.no_limit"))
        self.tokens_edit.editingFinished.connect(self._changed)
        tokens_col.addWidget(self.tokens_edit)
        fields.addLayout(tokens_col, 1)

        cost_col = QVBoxLayout()
        cost_col.addWidget(QLabel(tr("bud.cost_limit")))
        self.cost_edit = QLineEdit(
            f"{state.limit.cost_limit:g}" if state.limit.cost_limit else ""
        )
        self.cost_edit.setPlaceholderText(tr("bud.no_limit"))
        self.cost_edit.editingFinished.connect(self._changed)
        cost_col.addWidget(self.cost_edit)
        fields.addLayout(cost_col, 1)

        alert_col = QVBoxLayout()
        alert_col.addWidget(QLabel(tr("bud.alert_at")))
        self.alert_spin = QDoubleSpinBox()
        self.alert_spin.setRange(0.1, 1.0)
        self.alert_spin.setSingleStep(0.05)
        self.alert_spin.setDecimals(2)
        self.alert_spin.setValue(state.limit.alert_threshold or 0.8)
        self.alert_spin.valueChanged.connect(self._changed)
        alert_col.addWidget(self.alert_spin)
        fields.addLayout(alert_col)
        self.body.addLayout(fields)

    def _changed(self) -> None:
        self.on_change(self.state, self.values())

    def values(self) -> tuple[int | None, float | None, float]:
        return (_parse_int(self.tokens_edit.text()),
                _parse_float(self.cost_edit.text()),
                round(self.alert_spin.value(), 2))


class BudgetPage(QWidget):
    """Настройка лимитов и наблюдение за расходом."""

    def __init__(self, repos: Repos, bus: EventBus) -> None:
        super().__init__()
        self.repos = repos
        self.bus = bus
        self.workspace_id: int | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        self.header = Header(tr("bud.title"), tr("bud.subtitle"))
        refresh = QPushButton(tr("common.refresh"))
        refresh.clicked.connect(self.refresh)
        self.header.add_action(refresh)
        root.addWidget(self.header)

        self.alerts = QLabel("")
        self.alerts.setWordWrap(True)
        self.alerts.setVisible(False)
        root.addWidget(self.alerts)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        self.rows = QVBoxLayout(page)
        self.rows.setContentsMargins(0, 0, 0, 0)
        self.rows.setSpacing(10)

        self.bus.subscribe(self._on_event)

    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        while self.rows.count():
            item = self.rows.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.workspace_id is None:
            self.rows.addWidget(EmptyState(tr("ws.empty")))
            return

        states = load_states(self.repos, self.workspace_id)
        if not states:
            self.rows.addWidget(EmptyState(tr("bud.nothing")))
            return
        for state in states:
            self.rows.addWidget(LimitRow(self, state, self._save))
        self.rows.addStretch(1)

    def _save(self, state: ScopeState, values) -> None:
        """Сохраняет лимит. Пустые поля означают «ограничения нет»."""
        token_limit, cost_limit, threshold = values
        if token_limit is None and cost_limit is None:
            self.repos.budgets.delete_limit(state.scope, state.scope_id)
        else:
            self.repos.budgets.upsert(state.scope, state.scope_id,
                                      token_limit, cost_limit, threshold)
            self.repos.budgets.sync_used(state.scope, state.scope_id,
                                         state.tokens, state.cost)
        self.refresh()

    def _on_event(self, event: Event) -> None:
        if event.type not in (EventType.BUDGET_ALERT, EventType.BUDGET_EXCEEDED):
            return
        colour = "#ef5f6b" if event.type is EventType.BUDGET_EXCEEDED else "#f0b429"
        self.alerts.setText(event.message)
        self.alerts.setStyleSheet(
            f"color: {colour}; border: 1px solid {colour}; border-radius: 8px;"
            f"padding: 8px 12px;"
        )
        self.alerts.setVisible(True)
        self.refresh()


def _parse_int(raw: str) -> int | None:
    raw = (raw or "").replace(" ", "").strip()
    if not raw:
        return None
    try:
        value = int(raw)
    except ValueError:
        return None
    return value if value > 0 else None


def _parse_float(raw: str) -> float | None:
    raw = (raw or "").replace(",", ".").replace("$", "").strip()
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    return value if value > 0 else None

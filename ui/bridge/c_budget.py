"""Бюджеты: лимиты по токенам и деньгам на проект, задачу и каждого агента."""

from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.i18n import tr
from core.budget import load_states
from core.events import EventType
from ui.bridge.core import Controller, fmt_money, fmt_tokens
from ui.bridge.listmodel import DictListModel

SCOPE_ICONS = {"workspace": "layers", "task": "list-checks", "agent": "bot"}


def parse_int(raw: str) -> int | None:
    raw = (raw or "").replace(" ", "").replace("_", "").strip()
    if not raw:
        return None
    try:
        value = int(float(raw))
    except ValueError:
        return None
    return value if value > 0 else None


def parse_money(raw: str) -> float | None:
    raw = (raw or "").replace(",", ".").replace("$", "").replace(" ", "").strip()
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    return value if value > 0 else None


class BudgetController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._model = DictListModel(
            ["id", "scope", "scopeId", "scopeTitle", "icon", "name", "tokens", "cost",
             "tokenLimit", "costLimit", "threshold", "ratio", "exceeded", "isSet",
             "tokensText", "costText"], parent=self)
        self._set(alert="", alertTone="")

    alert = Property(str, lambda s: s._s.get("alert", ""), notify=changed)
    alertTone = Property(str, lambda s: s._s.get("alertTone", ""), notify=changed)

    def _get_model(self) -> QObject:
        return self._model

    model = Property(QObject, _get_model, constant=True)

    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            self._model.clear()
            return
        items = []
        for st in load_states(self.repos, self.ws_id):
            items.append({
                "id": f"{st.scope}:{st.scope_id}", "scope": st.scope, "scopeId": st.scope_id,
                "scopeTitle": tr(f"scope.{st.scope}"), "icon": SCOPE_ICONS.get(st.scope, "wallet"),
                "name": st.name, "tokens": st.tokens, "cost": st.cost,
                "tokenLimit": str(st.limit.token_limit) if st.limit.token_limit else "",
                "costLimit": f"{st.limit.cost_limit:g}" if st.limit.cost_limit else "",
                "threshold": float(st.limit.alert_threshold or 0.8),
                "ratio": float(st.ratio()), "exceeded": st.exceeded(),
                "isSet": st.limit.is_set, "tokensText": fmt_tokens(st.tokens),
                "costText": fmt_money(st.cost),
            })
        self._model.set_items(items)

    def reset(self) -> None:
        super().reset()
        self._model.clear()

    def on_event(self, event) -> None:
        if event.type in (EventType.BUDGET_ALERT, EventType.BUDGET_EXCEEDED,
                          EventType.BUDGET_EXTENDED):
            tone = {EventType.BUDGET_EXCEEDED: "error",
                    EventType.BUDGET_ALERT: "warning"}.get(event.type, "info")
            self._set(alert=event.message, alertTone=tone)
            self.refresh()
        elif event.type in (EventType.RUN_FINISHED, EventType.USAGE):
            # расход меняется во время прогона — но не чаще, чем пересчитает дашборд
            if event.type is EventType.RUN_FINISHED:
                self.refresh()

    @Slot(str, int, str, str, float, result=str)
    def save(self, scope: str, scope_id: int, token_limit: str, cost_limit: str,
             threshold: float) -> str:
        """Сохраняет лимит; пустые поля означают «без ограничения»."""
        tokens = parse_int(token_limit)
        cost = parse_money(cost_limit)
        if (token_limit or "").strip() and tokens is None:
            return tr("bud.bad_tokens")
        if (cost_limit or "").strip() and cost is None:
            return tr("bud.bad_cost")
        threshold = min(max(float(threshold or 0.8), 0.1), 1.0)
        if scope == "task":
            # Лимит токенов задачи живёт и в форме задачи — держим их в согласии.
            self.repos.tasks.update(scope_id, token_limit=tokens)
        if tokens is None and cost is None:
            self.repos.budgets.delete_limit(scope, scope_id)
        else:
            self.repos.budgets.upsert(scope, scope_id, tokens, cost, round(threshold, 2))
        # Идёт прогон — новый лимит действует сразу, а не со следующего запуска.
        orch = self.backend.orchestrator
        if orch is not None and orch.state.running and orch.budget is not None:
            orch.budget.reload_limits()
        self.refresh()
        self.backend.task.refresh()
        return ""

    @Slot()
    def dismissAlert(self) -> None:  # noqa: N802
        self._set(alert="", alertTone="")

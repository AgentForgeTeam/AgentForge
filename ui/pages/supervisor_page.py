"""Этап 5 — страница супервайзера.

Три раздела: кто сейчас работает супервайзером, лента анонимных сводок и
история инцидентов с возможностью закрыть эскалированный вручную.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.config import DEFAULT_WORKSPACE_SETTINGS
from app.i18n import tr
from core.events import Event, EventBus, EventType
from core.orchestrator import Orchestrator
from storage.db import local_time
from storage.models import Incident
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, warn
from utils.asyncutils import run_async

SEVERITY_COLORS = {"low": "#99a1b3", "medium": "#f0b429", "high": "#ef5f6b"}
SEVERITY_TITLES = {"low": "низкая", "medium": "средняя", "high": "высокая"}
STATUS_TITLES = {
    "open": "открыт",
    "auto_resolved": "разрешён автоматически",
    "escalated": "требует решения",
    "resolved": "закрыт",
}
REASON_LABELS = {
    "conflict": "Конфликт данных",
    "not_accepted": "Результат не принят",
    "low_confidence": "Низкая уверенность",
    "milestone": "Завершён этап",
}
KIND_TITLES = {
    "conflict": "конфликт данных",
    "factual_error": "фактическая ошибка",
    "contradiction": "противоречие",
    "off_scope": "выход за рамки задания",
}


class ResolveDialog(QDialog):
    """Ручное закрытие инцидента с объяснением решения."""

    def __init__(self, parent: QWidget, incident: Incident) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("sup.resolve"))
        self.setMinimumWidth(520)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        problem = QLabel(incident.description)
        problem.setWordWrap(True)
        lay.addWidget(problem)

        lay.addWidget(QLabel(tr("sup.resolution")))
        self.text = QPlainTextEdit(incident.resolution)
        self.text.setMinimumHeight(120)
        lay.addWidget(self.text)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def value(self) -> str:
        return self.text.toPlainText().strip()


class SupervisorPage(QWidget):
    """Сводки и инциденты текущего воркспейса."""

    def __init__(self, repos: Repos, bus: EventBus, orchestrator: Orchestrator) -> None:
        super().__init__()
        self.repos = repos
        self.bus = bus
        self.orchestrator = orchestrator
        self.workspace_id: int | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        self.header = Header(tr("sup.title"), tr("sup.subtitle"))
        self.btn_summary = QPushButton(tr("sup.make_summary"))
        self.btn_summary.setObjectName("Primary")
        self.btn_summary.clicked.connect(self._make_summary)
        self.header.add_action(self.btn_summary)
        root.addWidget(self.header)

        self.model_label = QLabel("")
        self.model_label.setObjectName("Dim")
        self.model_label.setWordWrap(True)
        root.addWidget(self.model_label)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)

        self.summaries_box, summaries_page = _scrollable()
        self.tabs.addTab(summaries_page, tr("sup.summaries"))

        self.incidents_box, incidents_page = _scrollable()
        self.tabs.addTab(incidents_page, tr("sup.incidents"))

        self.approvals_box, approvals_page = _scrollable()
        self.tabs.addTab(approvals_page, tr("sup.approvals"))

        self.bus.subscribe(self._on_event)

    # -- данные --------------------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        _clear(self.summaries_box)
        _clear(self.incidents_box)
        _clear(self.approvals_box)

        has_ws = self.workspace_id is not None
        self.btn_summary.setEnabled(has_ws and not self.orchestrator.state.running)
        if not has_ws:
            self.model_label.setText("")
            self.summaries_box.addWidget(EmptyState(tr("ws.empty")))
            self.incidents_box.addWidget(EmptyState(tr("ws.empty")))
            self.approvals_box.addWidget(EmptyState(tr("ws.empty")))
            return

        self.model_label.setText(self._describe_model())
        self._render_summaries()
        self._render_incidents()
        self._render_approvals()

    def _describe_model(self) -> str:
        ws = self.repos.workspaces.get(self.workspace_id)
        if ws is None:
            return ""
        s = {**DEFAULT_WORKSPACE_SETTINGS, **ws.settings}
        if s.get("supervisor_mode") == "local":
            return tr("sup.model_local",
                      model=s.get("supervisor_local_model", "—"),
                      url=s.get("supervisor_local_base_url", "—"))
        agent = self.repos.agents.get(int(s["supervisor_agent_id"])) \
            if s.get("supervisor_agent_id") else None
        if agent is None:
            agent = next((a for a in self.repos.agents.list(self.workspace_id)
                          if a.is_supervisor), None)
        if agent is None:
            return tr("sup.not_configured")
        return tr("sup.model_api", name=agent.name, model=agent.model)

    def _render_summaries(self) -> None:
        summaries = self.repos.reports.list_summaries(self.workspace_id, limit=30)
        if not summaries:
            self.summaries_box.addWidget(EmptyState(tr("sup.no_summaries")))
            return
        triggers = {"timer": tr("sup.by_timer"), "event": tr("sup.by_event"),
                    "manual": tr("sup.by_hand"), "final": tr("sup.by_final")}
        for item in summaries:
            card = Card(self, spacing=6)
            head = QHBoxLayout()
            when = QLabel(local_time(item.created_at))
            when.setObjectName("Dim")
            head.addWidget(when)
            trigger = QLabel(triggers.get(item.trigger, item.trigger))
            trigger.setObjectName("Dim")
            head.addWidget(trigger)
            head.addStretch(1)
            count = len([x for x in item.delivered_to.split(",") if x])
            recipients = QLabel(tr("sup.delivered", n=count))
            recipients.setObjectName("Dim")
            head.addWidget(recipients)
            card.body.addLayout(head)

            body = QLabel(item.content)
            body.setWordWrap(True)
            body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            card.body.addWidget(body)
            self.summaries_box.addWidget(card)
        self.summaries_box.addStretch(1)

    def _render_incidents(self) -> None:
        incidents = self.repos.incidents.list(self.workspace_id, limit=200)
        if not incidents:
            self.incidents_box.addWidget(EmptyState(tr("sup.no_incidents")))
            return
        for incident in incidents:
            self.incidents_box.addWidget(self._incident_card(incident))
        self.incidents_box.addStretch(1)

    def _incident_card(self, incident: Incident) -> Card:
        card = Card(self, spacing=6)
        row = QHBoxLayout()
        texts = QVBoxLayout()
        texts.setSpacing(3)

        head = QHBoxLayout()
        kind = QLabel(KIND_TITLES.get(incident.kind, incident.kind))
        kind.setObjectName("H2")
        head.addWidget(kind)

        color = SEVERITY_COLORS.get(incident.severity, SEVERITY_COLORS["medium"])
        severity = QLabel(SEVERITY_TITLES.get(incident.severity, incident.severity))
        severity.setStyleSheet(
            f"color: {color}; border: 1px solid {color}; border-radius: 9px;"
            f"padding: 1px 9px; font-size: 12px; font-weight: 600;"
        )
        head.addWidget(severity)
        head.addStretch(1)
        when = QLabel(local_time(incident.created_at))
        when.setObjectName("Dim")
        head.addWidget(when)
        texts.addLayout(head)

        description = QLabel(incident.description)
        description.setWordWrap(True)
        texts.addWidget(description)

        status = QLabel(f"{tr('common.status')}: "
                        f"{STATUS_TITLES.get(incident.status, incident.status)}")
        status.setObjectName("Dim")
        texts.addWidget(status)

        if incident.resolution:
            resolution = QLabel(f"{tr('sup.resolution')}: {incident.resolution}")
            resolution.setObjectName("Dim")
            resolution.setWordWrap(True)
            texts.addWidget(resolution)

        row.addLayout(texts, 1)
        if incident.status in ("open", "escalated"):
            button = QPushButton(tr("sup.resolve"))
            button.clicked.connect(lambda: self._resolve(incident))
            row.addWidget(button, 0, Qt.AlignmentFlag.AlignTop)
        card.body.addLayout(row)
        return card

    def _render_approvals(self) -> None:
        """История точек human-in-the-loop: что спросили и что ответили."""
        from core.hitl import parse_payload

        rows = self.repos.approvals.history(self.workspace_id, limit=60)
        if not rows:
            self.approvals_box.addWidget(EmptyState(tr("sup.no_approvals")))
            return

        titles = {"approve": tr("sup.d_approve"), "rework": tr("sup.d_rework"),
                  "skip": tr("sup.d_skip"), "abort": tr("sup.d_abort"),
                  "cancelled": tr("sup.d_cancelled"), "": tr("sup.d_pending")}
        colours = {"approve": "#3ecf8e", "rework": "#f0b429", "skip": "#99a1b3",
                   "abort": "#ef5f6b", "cancelled": "#99a1b3", "": "#6c8cff"}

        for row in rows:
            payload = parse_payload(row.get("payload_json", "{}"))
            card = Card(self, spacing=5)

            head = QHBoxLayout()
            reason = QLabel(REASON_LABELS.get(row["reason"], row["reason"]))
            reason.setObjectName("H2")
            head.addWidget(reason, 1)
            decision = row.get("decision", "")
            verdict = QLabel(titles.get(decision, decision))
            colour = colours.get(decision, "#99a1b3")
            verdict.setStyleSheet(
                f"color: {colour}; border: 1px solid {colour}; border-radius: 9px;"
                f"padding: 1px 9px; font-size: 12px; font-weight: 600;"
            )
            head.addWidget(verdict)
            card.body.addLayout(head)

            question = QLabel(payload.get("question", ""))
            question.setWordWrap(True)
            card.body.addWidget(question)

            meta_parts = [local_time(row["created_at"])]
            if payload.get("agent_name"):
                meta_parts.append(payload["agent_name"])
            if row.get("comment"):
                meta_parts.append(f"комментарий: {row['comment']}")
            meta = QLabel("  ·  ".join(meta_parts))
            meta.setObjectName("Dim")
            meta.setWordWrap(True)
            card.body.addWidget(meta)
            self.approvals_box.addWidget(card)
        self.approvals_box.addStretch(1)

    # -- действия ------------------------------------------------------------
    def _resolve(self, incident: Incident) -> None:
        dialog = ResolveDialog(self, incident)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        self.repos.incidents.resolve(incident.id, "resolved",
                                     dialog.value() or "Закрыто пользователем")
        self.refresh()

    def _make_summary(self) -> None:
        """Ручная сводка вне прогона — удобно, чтобы освежить контекст агентов."""
        if self.workspace_id is None:
            return
        task = self.repos.tasks.current(self.workspace_id)
        if task is None:
            warn(self, tr("task.no_task"))
            return

        ws = self.repos.workspaces.get(self.workspace_id)
        settings = {**DEFAULT_WORKSPACE_SETTINGS, **(ws.settings if ws else {})}
        from core.supervisor.supervisor import Supervisor

        supervisor = Supervisor(self.repos, self.bus, self.workspace_id, settings)
        if not supervisor.available():
            warn(self, tr("sup.not_configured"))
            return

        self.btn_summary.setEnabled(False)

        async def job() -> str:
            try:
                return await supervisor.make_summary(task, trigger="manual")
            finally:
                await supervisor.aclose()

        def done(content: str) -> None:
            self.btn_summary.setEnabled(True)
            if not content:
                warn(self, tr("sup.nothing_to_summarize"))
            self.refresh()

        def failed(exc: Exception) -> None:
            self.btn_summary.setEnabled(True)
            warn(self, str(exc))

        run_async(job(), done, failed)

    def _on_event(self, event: Event) -> None:
        if event.type in (EventType.SUMMARY_CREATED, EventType.INCIDENT_CREATED,
                          EventType.REPORT_REVIEWED, EventType.RUN_FINISHED,
                          EventType.APPROVAL_REQUESTED, EventType.APPROVAL_RESOLVED):
            self.refresh()


def _scrollable() -> tuple[QVBoxLayout, QWidget]:
    """Создаёт прокручиваемую страницу и возвращает её внутренний layout."""
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QScrollArea.Shape.NoFrame)
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(4, 8, 4, 8)
    layout.setSpacing(10)
    scroll.setWidget(container)
    return layout, scroll


def _clear(layout: QVBoxLayout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()

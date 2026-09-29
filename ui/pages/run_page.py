"""Этап 4 — страница выполнения: запуск агентов и наблюдение в реальном времени.

Слева — прогресс по подзадачам и статусы агентов, справа — лента событий:
шаги рассуждений, вызовы инструментов, отчёты, расход токенов.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from core.events import Event, EventBus, EventType
from core.hitl import Decision
from core.orchestrator import Orchestrator
from storage.repositories import Repos
from ui.theme import STATUS_COLORS, current_palette
from ui.widgets.approval_panel import ApprovalPanel
from ui.widgets.common import Card, EmptyState, Header, StatusBadge, confirm, warn
from utils.asyncutils import run_async

#: цвет строки в ленте для каждого типа события
FEED_COLORS = {
    EventType.RUN_STARTED: "#6c8cff",
    EventType.RUN_FINISHED: "#3ecf8e",
    EventType.RUN_PAUSED: "#f0b429",
    EventType.RUN_RESUMED: "#6c8cff",
    EventType.RUN_STOPPED: "#f0b429",
    EventType.AGENT_THINKING: "#99a1b3",
    EventType.AGENT_TOOL_CALL: "#b07cff",
    EventType.AGENT_TOOL_RESULT: "#7c8aa5",
    EventType.SUBTASK_STARTED: "#6c8cff",
    EventType.SUBTASK_FINISHED: "#3ecf8e",
    EventType.SUBTASK_FAILED: "#ef5f6b",
    EventType.REPORT_CREATED: "#3ecf8e",
    EventType.SUMMARY_CREATED: "#b07cff",
    EventType.INCIDENT_CREATED: "#ef5f6b",
    EventType.USAGE: "#5f6a7d",
    EventType.ERROR: "#ef5f6b",
}

#: события, которые не засоряют ленту при большом числе агентов
QUIET_EVENTS = {EventType.AGENT_STATUS}


class RunPage(QWidget):
    """Управление прогоном и живая телеметрия."""

    def __init__(self, repos: Repos, bus: EventBus, orchestrator: Orchestrator) -> None:
        super().__init__()
        self.repos = repos
        self.bus = bus
        self.orchestrator = orchestrator
        self.workspace_id: int | None = None
        self._feed_lines = 0

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        self.header = Header(tr("run.title"), tr("run.subtitle"))
        self.btn_start = QPushButton(tr("run.start"))
        self.btn_start.setObjectName("Primary")
        self.btn_start.clicked.connect(self._start)
        self.header.add_action(self.btn_start)

        self.btn_pause = QPushButton(tr("run.pause"))
        self.btn_pause.clicked.connect(self._toggle_pause)
        self.btn_pause.setEnabled(False)
        self.header.add_action(self.btn_pause)

        self.btn_stop = QPushButton(tr("run.stop"))
        self.btn_stop.setObjectName("Danger")
        self.btn_stop.clicked.connect(self._stop)
        self.btn_stop.setEnabled(False)
        self.header.add_action(self.btn_stop)
        root.addWidget(self.header)

        # --- полоса прогресса и счётчики ---
        top = Card(self, spacing=8)
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        top.body.addWidget(self.progress)
        self.summary_label = QLabel(tr("run.idle"))
        self.summary_label.setObjectName("Dim")
        top.body.addWidget(self.summary_label)
        root.addWidget(top)

        # --- запросы решений (human-in-the-loop) ---
        self.approvals = ApprovalPanel(self._decide)
        root.addWidget(self.approvals)

        # --- две колонки ---
        splitter = QSplitter(Qt.Orientation.Horizontal)
        root.addWidget(splitter, 1)

        left = QWidget()
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)
        left_lay.setSpacing(10)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        left_lay.addWidget(self.scroll, 1)
        self.panel = QWidget()
        self.panel_layout = QVBoxLayout(self.panel)
        self.panel_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_layout.setSpacing(8)
        self.scroll.setWidget(self.panel)
        splitter.addWidget(left)

        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        right_lay.setSpacing(8)
        feed_head = QHBoxLayout()
        feed_title = QLabel(tr("run.feed"))
        feed_title.setObjectName("H2")
        feed_head.addWidget(feed_title, 1)
        btn_clear = QPushButton(tr("run.clear_feed"))
        btn_clear.clicked.connect(lambda: (self.feed.clear(),
                                           setattr(self, "_feed_lines", 0)))
        feed_head.addWidget(btn_clear)
        right_lay.addLayout(feed_head)

        self.feed = QTextEdit()
        self.feed.setReadOnly(True)
        self.feed.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        right_lay.addWidget(self.feed, 1)
        splitter.addWidget(right)
        splitter.setSizes([520, 620])

        self.bus.subscribe(self._on_event)

    # -- данные --------------------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        self._clear_panel()
        running = self.orchestrator.state.running
        has_ws = self.workspace_id is not None
        self.btn_start.setEnabled(has_ws and not running)
        self.btn_pause.setEnabled(running)
        self.btn_stop.setEnabled(running)

        if not has_ws:
            self.panel_layout.addWidget(EmptyState(tr("ws.empty")))
            return

        task = self.repos.tasks.current(self.workspace_id)
        if task is None:
            self.panel_layout.addWidget(EmptyState(tr("task.no_task")))
            self.btn_start.setEnabled(False)
            return

        subtasks = self.repos.tasks.subtasks(task.id)
        agents = {a.id: a for a in self.repos.agents.list(self.workspace_id)}
        done = sum(1 for s in subtasks if s.status == "done")
        review = sum(1 for s in subtasks if s.status == "review")
        errors = sum(1 for s in subtasks if s.status == "error")
        total = len(subtasks) or 1
        self.progress.setMaximum(total)
        self.progress.setValue(done + review)

        tokens, cost = self.repos.budgets.workspace_totals(self.workspace_id)
        limit = f" / {task.token_limit}" if task.token_limit else " (без лимита)"
        self.summary_label.setText(
            tr("run.summary", done=done + review, total=len(subtasks), errors=errors)
            + f"  ·  {tokens}{limit} токенов  ·  ~${cost:.4f}"
        )

        # --- подзадачи ---
        head = QLabel(tr("task.subtasks"))
        head.setObjectName("H2")
        self.panel_layout.addWidget(head)
        if not subtasks:
            self.panel_layout.addWidget(EmptyState(tr("run.no_subtasks")))
        for i, st in enumerate(subtasks, 1):
            self.panel_layout.addWidget(self._subtask_row(i, st, agents))

        # --- агенты ---
        head2 = QLabel(tr("agents.title"))
        head2.setObjectName("H2")
        self.panel_layout.addWidget(head2)
        for agent in agents.values():
            row = QWidget()
            h = QHBoxLayout(row)
            h.setContentsMargins(4, 2, 4, 2)
            name = QLabel(agent.name + ("  ⭐" if agent.is_supervisor else ""))
            h.addWidget(name, 1)
            model = QLabel(agent.model)
            model.setObjectName("Dim")
            h.addWidget(model)
            h.addWidget(StatusBadge(agent.status))
            self.panel_layout.addWidget(row)
        self.panel_layout.addStretch(1)

    def _subtask_row(self, index: int, st, agents: dict) -> Card:
        card = Card(self, spacing=4)
        row = QHBoxLayout()
        texts = QVBoxLayout()
        texts.setSpacing(2)

        title = QLabel(f"{index}. {st.title}")
        title.setWordWrap(True)
        texts.addWidget(title)

        agent = agents.get(st.agent_id)
        meta = QLabel(f"{agent.name if agent else tr('task.unassigned')}"
                      f"  ·  {st.tokens_in + st.tokens_out} токенов"
                      f"  ·  ~${st.cost_usd:.4f}")
        meta.setObjectName("Dim")
        texts.addWidget(meta)

        if st.result:
            preview = QLabel(st.result[:200].replace("\n", " ")
                             + ("…" if len(st.result) > 200 else ""))
            preview.setObjectName("Dim")
            preview.setWordWrap(True)
            texts.addWidget(preview)

        row.addLayout(texts, 1)
        row.addWidget(StatusBadge(st.status), 0, Qt.AlignmentFlag.AlignTop)
        card.body.addLayout(row)
        return card

    def _clear_panel(self) -> None:
        while self.panel_layout.count():
            item = self.panel_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    # -- события -------------------------------------------------------------
    def _sync_approvals(self) -> None:
        """Перерисовывает панель из состояния ворот согласования."""
        gate = self.orchestrator.gate
        self.approvals.set_requests(gate.pending() if gate else [])

    def _decide(self, approval_id: int, decision: Decision, comment: str) -> None:
        """Передаёт решение пользователя в ядро."""
        gate = self.orchestrator.gate
        if gate is None or not gate.resolve(approval_id, decision, comment):
            # Вопрос уже снят (например, прогон остановлен) — просто обновляем вид.
            self._sync_approvals()
            return
        self._sync_approvals()

    def _on_event(self, event: Event) -> None:
        """Обработчик шины: пишет строку в ленту и обновляет панель."""
        if event.type in QUIET_EVENTS:
            return
        self._append_feed(event)

        if event.type in (EventType.APPROVAL_REQUESTED, EventType.APPROVAL_RESOLVED):
            self._sync_approvals()

        if event.type in (EventType.SUBTASK_STARTED, EventType.SUBTASK_FINISHED,
                          EventType.SUBTASK_FAILED, EventType.REPORT_CREATED,
                          EventType.RUN_STARTED, EventType.RUN_FINISHED,
                          EventType.RUN_STOPPED):
            self.refresh()

        if event.type in (EventType.RUN_FINISHED, EventType.RUN_STOPPED):
            # Прогон закончился — висящих вопросов быть не должно.
            self._sync_approvals()

        if event.type == EventType.RUN_FINISHED:
            self.btn_start.setEnabled(True)
            self.btn_pause.setEnabled(False)
            self.btn_stop.setEnabled(False)
            self.btn_pause.setText(tr("run.pause"))

    def _append_feed(self, event: Event) -> None:
        """Добавляет цветную строку; лента подрезается, чтобы не расти вечно."""
        if self._feed_lines > 1500:
            self.feed.clear()
            self._feed_lines = 0

        cursor = self.feed.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        dim = QTextCharFormat()
        dim.setForeground(QColor(STATUS_COLORS["idle"]))
        cursor.insertText(f"{event.time_short}  ", dim)

        if event.agent_name:
            name_fmt = QTextCharFormat()
            name_fmt.setForeground(QColor(current_palette()["text"]))
            cursor.insertText(f"[{event.agent_name}] ", name_fmt)

        body = QTextCharFormat()
        body.setForeground(QColor(FEED_COLORS.get(event.type, "#c8cedb")))
        cursor.insertText(f"{event.message}\n", body)

        self._feed_lines += 1
        self.feed.setTextCursor(cursor)
        self.feed.ensureCursorVisible()

    # -- действия ------------------------------------------------------------
    def _start(self) -> None:
        if self.workspace_id is None:
            return
        task = self.repos.tasks.current(self.workspace_id)
        if task is None:
            warn(self, tr("task.no_task"))
            return
        subtasks = self.repos.tasks.subtasks(task.id)
        if not subtasks:
            warn(self, tr("run.no_subtasks"))
            return
        missing = [s.title for s in subtasks if not s.agent_id and s.status != "done"]
        if missing:
            warn(self, tr("run.unassigned") + "\n· " + "\n· ".join(missing[:8]))
            return

        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(True)
        self.btn_stop.setEnabled(True)

        ws_id, task_id = self.workspace_id, task.id

        def failed(exc: Exception) -> None:
            self.btn_start.setEnabled(True)
            self.btn_pause.setEnabled(False)
            self.btn_stop.setEnabled(False)
            warn(self, str(exc))

        run_async(self.orchestrator.run_task(ws_id, task_id), None, failed)

    def _toggle_pause(self) -> None:
        if self.orchestrator.state.paused:
            self.orchestrator.resume()
            self.btn_pause.setText(tr("run.pause"))
        else:
            self.orchestrator.pause()
            self.btn_pause.setText(tr("run.resume"))

    def _stop(self) -> None:
        if confirm(self, tr("run.stop_confirm")):
            self.orchestrator.stop()

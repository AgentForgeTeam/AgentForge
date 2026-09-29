"""Этап 3 — постановка задачи и разбиение на подзадачи.

Здесь пользователь формулирует общую задачу воркспейса, задаёт лимит токенов
(пусто = без лимита, ответ на вопрос 7), выбирает формат результата и
раскладывает работу на подзадачи — руками или автоматически через ИИ.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from core.planner import match_agent_by_role, plan_subtasks
from storage.models import Subtask, Task
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, StatusBadge, confirm, warn
from utils.asyncutils import run_async

RESULT_FORMATS = [
    ("auto", "Определить автоматически"),
    ("markdown", "Markdown-документ"),
    ("docx", "Документ DOCX"),
    ("pdf", "Документ PDF"),
    ("zip", "ZIP-архив с файлами/кодом"),
]


class SubtaskDialog(QDialog):
    """Ручное создание/редактирование подзадачи и назначение исполнителя."""

    def __init__(self, parent: QWidget, repos: Repos, workspace_id: int,
                 subtask: Subtask | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("task.add_subtask"))
        self.setMinimumWidth(560)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        lay.addWidget(QLabel(tr("task.subtask_title")))
        self.title = QLineEdit(subtask.title if subtask else "")
        lay.addWidget(self.title)

        lay.addWidget(QLabel(tr("common.description")))
        self.description = QPlainTextEdit(subtask.description if subtask else "")
        self.description.setMinimumHeight(140)
        lay.addWidget(self.description)

        lay.addWidget(QLabel(tr("task.assignee")))
        self.assignee = QComboBox()
        self.assignee.addItem(tr("task.unassigned"), None)
        for agent in repos.agents.list(workspace_id):
            if not agent.is_supervisor:
                self.assignee.addItem(f"{agent.name} — {agent.model}", agent.id)
        if subtask and subtask.agent_id:
            idx = self.assignee.findData(subtask.agent_id)
            if idx >= 0:
                self.assignee.setCurrentIndex(idx)
        lay.addWidget(self.assignee)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def values(self) -> tuple[str, str, int | None]:
        return (self.title.text().strip(),
                self.description.toPlainText().strip(),
                self.assignee.currentData())


class TaskPage(QWidget):
    """Страница задачи текущего воркспейса."""

    task_changed = Signal()
    run_requested = Signal()   # пользователь нажал «Запустить агентов»

    def __init__(self, repos: Repos) -> None:
        super().__init__()
        self.repos = repos
        self.workspace_id: int | None = None
        self.task: Task | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        self.header = Header(tr("task.title"))
        root.addWidget(self.header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # --- карточка постановки задачи ---
        self.task_card = Card(self)
        lay.addWidget(self.task_card)

        self.task_card.body.addWidget(QLabel(tr("task.name")))
        self.title_edit = QLineEdit()
        self.task_card.body.addWidget(self.title_edit)

        self.task_card.body.addWidget(QLabel(tr("task.body")))
        self.body_edit = QPlainTextEdit()
        self.body_edit.setPlaceholderText(tr("task.placeholder"))
        self.body_edit.setMinimumHeight(220)
        self.task_card.body.addWidget(self.body_edit)

        options = QHBoxLayout()
        fmt_col = QVBoxLayout()
        fmt_col.addWidget(QLabel(tr("task.result_format")))
        self.format_box = QComboBox()
        for key, label in RESULT_FORMATS:
            self.format_box.addItem(label, key)
        fmt_col.addWidget(self.format_box)
        options.addLayout(fmt_col, 1)

        limit_col = QVBoxLayout()
        limit_col.addWidget(QLabel(tr("task.token_limit")))
        self.token_limit = QLineEdit()
        self.token_limit.setPlaceholderText(tr("task.token_limit_hint"))
        limit_col.addWidget(self.token_limit)
        options.addLayout(limit_col, 1)
        self.task_card.body.addLayout(options)

        buttons = QHBoxLayout()
        self.btn_save = QPushButton(tr("task.save"))
        self.btn_save.setObjectName("Primary")
        self.btn_save.clicked.connect(self._save_task)
        buttons.addWidget(self.btn_save)

        self.btn_run = QPushButton(tr("task.run"))
        self.btn_run.clicked.connect(self._request_run)
        buttons.addWidget(self.btn_run)
        buttons.addStretch(1)
        self.task_card.body.addLayout(buttons)

        # --- карточка подзадач ---
        self.subtasks_header = Header(tr("task.subtasks"))
        self.btn_add = QPushButton(tr("task.add_subtask"))
        self.btn_add.clicked.connect(self._add_subtask)
        self.subtasks_header.add_action(self.btn_add)
        self.btn_auto = QPushButton(tr("task.autosplit"))
        self.btn_auto.setObjectName("Primary")
        self.btn_auto.clicked.connect(self._autosplit)
        self.subtasks_header.add_action(self.btn_auto)
        lay.addWidget(self.subtasks_header)

        self.subtasks_box = QWidget()
        self.subtasks_layout = QVBoxLayout(self.subtasks_box)
        self.subtasks_layout.setContentsMargins(0, 0, 0, 0)
        self.subtasks_layout.setSpacing(8)
        lay.addWidget(self.subtasks_box)
        lay.addStretch(1)

    # -- загрузка ------------------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        enabled = self.workspace_id is not None
        for widget in (self.title_edit, self.body_edit, self.format_box,
                       self.token_limit, self.btn_save, self.btn_add,
                       self.btn_auto, self.btn_run):
            widget.setEnabled(enabled)
        if not enabled:
            self._clear_subtasks()
            self.subtasks_layout.addWidget(EmptyState(tr("ws.empty")))
            return

        self.task = self.repos.tasks.current(self.workspace_id)
        if self.task:
            self.title_edit.setText(self.task.title)
            self.body_edit.setPlainText(self.task.description)
            idx = self.format_box.findData(self.task.result_format)
            self.format_box.setCurrentIndex(max(0, idx))
            self.token_limit.setText(str(self.task.token_limit) if self.task.token_limit else "")
        else:
            self.title_edit.clear()
            self.body_edit.clear()
            self.format_box.setCurrentIndex(0)
            self.token_limit.clear()
        self._render_subtasks()

    def _clear_subtasks(self) -> None:
        while self.subtasks_layout.count():
            item = self.subtasks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _render_subtasks(self) -> None:
        self._clear_subtasks()
        if self.task is None:
            self.subtasks_layout.addWidget(EmptyState(tr("task.no_task")))
            return
        items = self.repos.tasks.subtasks(self.task.id)
        if not items:
            self.subtasks_layout.addWidget(EmptyState(tr("task.subtasks")))
            return
        agents = {a.id: a for a in self.repos.agents.list(self.workspace_id)}
        for position, st in enumerate(items):
            self.subtasks_layout.addWidget(
                self._build_subtask_card(st, position, len(items), agents)
            )

    def _build_subtask_card(self, st: Subtask, position: int, total: int,
                            agents: dict) -> Card:
        card = Card(self, spacing=6)
        row = QHBoxLayout()

        texts = QVBoxLayout()
        texts.setSpacing(2)
        head = QHBoxLayout()
        title = QLabel(f"{position + 1}. {st.title}")
        title.setObjectName("H2")
        title.setWordWrap(True)
        head.addWidget(title, 1)
        head.addWidget(StatusBadge(st.status))
        texts.addLayout(head)

        agent = agents.get(st.agent_id)
        meta = QLabel(f"{tr('task.assignee')}: "
                      f"{agent.name if agent else tr('task.unassigned')}")
        meta.setObjectName("Dim")
        texts.addWidget(meta)

        if st.description:
            desc = QLabel(st.description[:300] + ("…" if len(st.description) > 300 else ""))
            desc.setObjectName("Dim")
            desc.setWordWrap(True)
            texts.addWidget(desc)
        row.addLayout(texts, 1)

        controls = QVBoxLayout()
        controls.setSpacing(4)
        move_row = QHBoxLayout()
        btn_up = QPushButton("▲")
        btn_up.setObjectName("Icon")
        btn_up.setFixedWidth(36)
        btn_up.setEnabled(position > 0)
        btn_up.clicked.connect(lambda: self._move(st.id, -1))
        move_row.addWidget(btn_up)
        btn_down = QPushButton("▼")
        btn_down.setObjectName("Icon")
        btn_down.setFixedWidth(36)
        btn_down.setEnabled(position < total - 1)
        btn_down.clicked.connect(lambda: self._move(st.id, +1))
        move_row.addWidget(btn_down)
        controls.addLayout(move_row)

        btn_edit = QPushButton(tr("common.edit"))
        btn_edit.clicked.connect(lambda: self._edit_subtask(st))
        controls.addWidget(btn_edit)

        btn_del = QPushButton(tr("common.delete"))
        btn_del.setObjectName("Danger")
        btn_del.clicked.connect(lambda: self._delete_subtask(st))
        controls.addWidget(btn_del)

        row.addLayout(controls, 0)
        card.body.addLayout(row)
        return card

    # -- действия ------------------------------------------------------------
    def _parse_limit(self) -> int | None:
        raw = self.token_limit.text().strip()
        if not raw:
            return None       # пусто = лимита нет
        try:
            value = int(raw.replace(" ", ""))
            return value if value > 0 else None
        except ValueError:
            return None

    def _save_task(self) -> bool:
        if self.workspace_id is None:
            return False
        title = self.title_edit.text().strip() or "Без названия"
        body = self.body_edit.toPlainText().strip()
        if not body:
            warn(self, tr("task.placeholder"))
            return False
        fmt = self.format_box.currentData()
        limit = self._parse_limit()
        if self.task is None:
            self.task = self.repos.tasks.create(self.workspace_id, title, body, fmt, limit)
        else:
            self.repos.tasks.update(self.task.id, title=title, description=body,
                                    result_format=fmt, token_limit=limit)
            self.task = self.repos.tasks.get(self.task.id)
        self.task_changed.emit()
        self._render_subtasks()
        return True

    def _add_subtask(self) -> None:
        if self.task is None and not self._save_task():
            return
        dlg = SubtaskDialog(self, self.repos, self.workspace_id)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        title, description, agent_id = dlg.values()
        if not title:
            return
        self.repos.tasks.add_subtask(self.task.id, title, description, agent_id)
        self.task_changed.emit()
        self._render_subtasks()

    def _edit_subtask(self, st: Subtask) -> None:
        dlg = SubtaskDialog(self, self.repos, self.workspace_id, st)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        title, description, agent_id = dlg.values()
        if not title:
            return
        self.repos.tasks.update_subtask(st.id, title=title, description=description,
                                        agent_id=agent_id)
        self.task_changed.emit()
        self._render_subtasks()

    def _delete_subtask(self, st: Subtask) -> None:
        if not confirm(self, tr("common.delete") + "?"):
            return
        self.repos.tasks.delete_subtask(st.id)
        self.task_changed.emit()
        self._render_subtasks()

    def _move(self, subtask_id: int, delta: int) -> None:
        if self.task is None:
            return
        ids = [s.id for s in self.repos.tasks.subtasks(self.task.id)]
        i = ids.index(subtask_id)
        j = i + delta
        if 0 <= j < len(ids):
            ids[i], ids[j] = ids[j], ids[i]
            self.repos.tasks.reorder(ids)
            self._render_subtasks()

    def _autosplit(self) -> None:
        """Просит ИИ разбить задачу и сразу назначает исполнителей по ролям."""
        if not self._save_task() or self.task is None:
            return
        self.btn_auto.setEnabled(False)
        self.btn_auto.setText("…")

        task_id = self.task.id
        ws_id = self.workspace_id
        title, body = self.task.title, self.task.description

        async def job():
            return await plan_subtasks(self.repos, ws_id, title, body)

        def done(planned) -> None:
            self._reset_auto_button()
            for item in planned:
                agent_id = match_agent_by_role(self.repos, ws_id, item.assignee_role)
                self.repos.tasks.add_subtask(task_id, item.title, item.description, agent_id)
            self.task_changed.emit()
            self._render_subtasks()

        def failed(exc: Exception) -> None:
            self._reset_auto_button()
            warn(self, str(exc))

        run_async(job(), done, failed)

    def _request_run(self) -> None:
        """Сохраняет задачу и передаёт управление странице выполнения."""
        if self._save_task():
            self.run_requested.emit()

    def _reset_auto_button(self) -> None:
        self.btn_auto.setEnabled(True)
        self.btn_auto.setText(tr("task.autosplit"))

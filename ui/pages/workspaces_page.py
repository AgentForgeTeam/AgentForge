"""Этап 1 — страница воркспейсов (параллельных проектов).

Каждый воркспейс полностью изолирован: свой набор агентов, своя задача,
свой рабочий каталог на диске и свои настройки супервайзера.
"""

from __future__ import annotations

import shutil

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
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

from app.config import DEFAULT_WORKSPACE_SETTINGS, PATHS
from app.i18n import tr
from storage.db import local_time
from storage.models import Workspace
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, confirm


class WorkspaceDialog(QDialog):
    """Диалог создания/переименования воркспейса."""

    def __init__(self, parent: QWidget, workspace: Workspace | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("ws.new"))
        self.setMinimumWidth(440)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        lay.addWidget(QLabel(tr("ws.name")))
        self.name = QLineEdit(workspace.name if workspace else "")
        lay.addWidget(self.name)

        lay.addWidget(QLabel(tr("common.description")))
        self.description = QPlainTextEdit(workspace.description if workspace else "")
        self.description.setFixedHeight(90)
        lay.addWidget(self.description)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def values(self) -> tuple[str, str]:
        return self.name.text().strip(), self.description.toPlainText().strip()


class WorkspaceCard(Card):
    """Карточка одного воркспейса в списке."""

    def __init__(self, parent: QWidget, ws: Workspace, agents: int,
                 is_active: bool, on_select, on_edit, on_delete) -> None:
        super().__init__(parent, spacing=8)
        row = QHBoxLayout()
        texts = QVBoxLayout()
        texts.setSpacing(2)

        title = QLabel(ws.name + ("  ·  " + tr("ws.current") if is_active else ""))
        title.setObjectName("H2")
        texts.addWidget(title)

        meta = QLabel(f"{agents} {tr('ws.agents_count')}  ·  {local_time(ws.updated_at, '%Y-%m-%d %H:%M')}")
        meta.setObjectName("Dim")
        texts.addWidget(meta)

        if ws.description:
            desc = QLabel(ws.description)
            desc.setObjectName("Dim")
            desc.setWordWrap(True)
            texts.addWidget(desc)

        row.addLayout(texts, 1)

        btn_select = QPushButton(tr("ws.select"))
        btn_select.setObjectName("Primary")
        btn_select.setEnabled(not is_active)
        btn_select.clicked.connect(lambda: on_select(ws))
        row.addWidget(btn_select, 0, Qt.AlignmentFlag.AlignTop)

        btn_edit = QPushButton(tr("common.edit"))
        btn_edit.clicked.connect(lambda: on_edit(ws))
        row.addWidget(btn_edit, 0, Qt.AlignmentFlag.AlignTop)

        btn_delete = QPushButton(tr("common.delete"))
        btn_delete.setObjectName("Danger")
        btn_delete.clicked.connect(lambda: on_delete(ws))
        row.addWidget(btn_delete, 0, Qt.AlignmentFlag.AlignTop)

        self.body.addLayout(row)


class WorkspacesPage(QWidget):
    """Список воркспейсов с выбором активного."""

    workspace_selected = Signal(int)
    workspaces_changed = Signal()

    def __init__(self, repos: Repos) -> None:
        super().__init__()
        self.repos = repos
        self.active_id: int | None = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(16)

        self.header = Header(tr("ws.title"))
        btn_new = QPushButton(tr("ws.new"))
        btn_new.setObjectName("Primary")
        btn_new.clicked.connect(self._create)
        self.header.add_action(btn_new)
        lay.addWidget(self.header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        lay.addWidget(self.scroll, 1)

        self.container = QWidget()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        self.scroll.setWidget(self.container)

    # -- отрисовка -----------------------------------------------------------
    def refresh(self) -> None:
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        items = self.repos.workspaces.list(self.repos.session.user_id)
        if not items:
            self.list_layout.addWidget(EmptyState(tr("ws.empty")))
            return
        for ws in items:
            self.list_layout.addWidget(
                WorkspaceCard(
                    self, ws, self.repos.workspaces.agent_count(ws.id),
                    ws.id == self.active_id, self._select, self._edit, self._delete,
                )
            )
        self.list_layout.addStretch(1)

    def set_active(self, ws_id: int | None) -> None:
        self.active_id = ws_id
        self.refresh()

    # -- действия ------------------------------------------------------------
    def _create(self) -> None:
        dlg = WorkspaceDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        name, description = dlg.values()
        if not name:
            return
        ws = self.repos.workspaces.create(
            self.repos.session.user_id, name, description,
            dict(DEFAULT_WORKSPACE_SETTINGS),
        )
        PATHS.workspace_dir(ws.id).mkdir(parents=True, exist_ok=True)
        self.workspaces_changed.emit()
        self._select(ws)

    def _edit(self, ws: Workspace) -> None:
        dlg = WorkspaceDialog(self, ws)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        name, description = dlg.values()
        if name:
            self.repos.workspaces.update(ws.id, name=name, description=description)
            self.workspaces_changed.emit()
            self.refresh()

    def _delete(self, ws: Workspace) -> None:
        if not confirm(self, tr("ws.delete_confirm")):
            return
        self.repos.workspaces.delete(ws.id)
        shutil.rmtree(PATHS.workspace_dir(ws.id), ignore_errors=True)
        if self.active_id == ws.id:
            self.active_id = None
        self.workspaces_changed.emit()
        self.refresh()

    def _select(self, ws: Workspace) -> None:
        self.active_id = ws.id
        PATHS.workspace_dir(ws.id).mkdir(parents=True, exist_ok=True)
        self.workspace_selected.emit(ws.id)
        self.refresh()

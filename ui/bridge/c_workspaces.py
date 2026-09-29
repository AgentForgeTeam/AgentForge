"""Воркспейсы: параллельные проекты со своими агентами, задачей и настройками."""

from __future__ import annotations

import shutil

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.config import DEFAULT_WORKSPACE_SETTINGS, PATHS
from app.i18n import tr
from ui.bridge.core import Controller, fmt_money, fmt_tokens, when
from ui.bridge.listmodel import DictListModel


class WorkspacesController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._model = DictListModel(["id", "name", "description", "agents", "updated",
                                     "active", "tokens", "cost", "taskTitle"], parent=self)

    def _get_model(self) -> QObject:
        return self._model

    model = Property(QObject, _get_model, constant=True)

    @Slot()
    def refresh(self) -> None:
        if not self.ready:
            return
        items = []
        for ws in self.repos.workspaces.list(self.repos.session.user_id):
            tokens, cost = self.repos.budgets.workspace_totals(ws.id)
            task = self.repos.tasks.current(ws.id)
            items.append({
                "id": ws.id, "name": ws.name, "description": ws.description,
                "agents": self.repos.workspaces.agent_count(ws.id),
                "updated": when(ws.updated_at), "active": ws.id == self.ws_id,
                "tokens": fmt_tokens(tokens), "cost": fmt_money(cost),
                "taskTitle": task.title if task else "",
            })
        self._model.set_items(items)

    def reset(self) -> None:
        super().reset()
        self._model.clear()

    @Slot(str, str, result=str)
    def create(self, name: str, description: str) -> str:
        name = (name or "").strip()
        if not name:
            return tr("ws.need_name")
        ws = self.repos.workspaces.create(self.repos.session.user_id, name,
                                          (description or "").strip(),
                                          dict(DEFAULT_WORKSPACE_SETTINGS))
        PATHS.workspace_dir(ws.id).mkdir(parents=True, exist_ok=True)
        self.backend.select_workspace(ws.id)
        self.toast("success", tr("toast.ws_created"), name)
        return ""

    @Slot(int, str, str, result=str)
    def update(self, ws_id: int, name: str, description: str) -> str:
        name = (name or "").strip()
        if not name:
            return tr("ws.need_name")
        self.repos.workspaces.update(ws_id, name=name, description=(description or "").strip())
        self.backend._update_workspace_name()
        self.refresh()
        return ""

    @Slot(int)
    def remove(self, ws_id: int) -> None:
        if self.backend.orchestrator and self.backend.orchestrator.state.running \
                and ws_id == self.ws_id:
            self.toast("warning", tr("toast.run_active"), tr("toast.run_active_text"))
            return
        ws = self.repos.workspaces.get(ws_id)
        self.repos.workspaces.delete(ws_id)
        shutil.rmtree(PATHS.workspace_dir(ws_id), ignore_errors=True)
        if ws_id == self.ws_id:
            remaining = self.repos.workspaces.list(self.repos.session.user_id)
            self.backend.select_workspace(remaining[0].id if remaining else None)
        else:
            self.refresh()
        self.toast("info", tr("toast.ws_deleted"), ws.name if ws else "")

    @Slot(int)
    def select(self, ws_id: int) -> None:
        self.backend.select_workspace(ws_id)

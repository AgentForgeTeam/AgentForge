"""Сборка контроллеров страниц - в одном месте, чтобы Backend не знал деталей."""

from __future__ import annotations

from ui.bridge.c_agents import AgentsController
from ui.bridge.c_budget import BudgetController
from ui.bridge.c_dashboard import DashboardController
from ui.bridge.c_export import ExportController
from ui.bridge.c_keys import KeysController
from ui.bridge.c_prefs import PrefsController
from ui.bridge.c_run import RunController
from ui.bridge.c_supervisor import SupervisorController
from ui.bridge.c_task import TaskController
from ui.bridge.c_workspaces import WorkspacesController


def build_controllers(backend) -> dict:
    # Порядок важен: супервайзер описывает модель раньше, чем её спросит
    # карточка супервайзера на странице выполнения.
    return {
        "workspaces": WorkspacesController(backend),
        "keys": KeysController(backend),
        "agents": AgentsController(backend),
        "task": TaskController(backend),
        "supervisor": SupervisorController(backend),
        "run": RunController(backend),
        "dashboard": DashboardController(backend),
        "budget": BudgetController(backend),
        "exporter": ExportController(backend),
        "prefs": PrefsController(backend),
    }

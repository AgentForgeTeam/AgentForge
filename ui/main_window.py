"""Главное окно: боковая навигация + стек страниц.

Активный воркспейс — общее состояние окна: при его смене страницы агентов,
задачи, дашборда и настроек перезагружают свои данные.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_NAME, APP_VERSION, AppSettings
from app.i18n import tr
from core.events import EventBus
from core.orchestrator import Orchestrator
from core.security.crypto import Session
from storage.db import Database
from storage.repositories import Repos
from ui.pages.agents_page import AgentsPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.budget_page import BudgetPage
from ui.pages.export_page import ExportPage
from ui.pages.keys_page import KeysPage
from ui.pages.run_page import RunPage
from ui.pages.settings_page import SettingsPage
from ui.pages.supervisor_page import SupervisorPage
from ui.pages.task_page import TaskPage
from ui.pages.workspaces_page import WorkspacesPage
from ui.theme import stylesheet


class MainWindow(QMainWindow):
    """Основное окно приложения после успешного входа."""

    logged_out = Signal()
    #: язык сменился — окно нужно собрать заново (аргумент: индекс страницы)
    rebuild_requested = Signal(int)

    def __init__(self, db: Database, session: Session, app_settings: AppSettings) -> None:
        super().__init__()
        self.db = db
        self.session = session
        self.app_settings = app_settings
        self.repos = Repos(db, session)
        self.workspace_id: int | None = None

        # Шина событий и оркестратор живут на уровне окна: один прогон на окно.
        self.bus = EventBus()
        self.orchestrator = Orchestrator(self.repos, self.bus)

        self.setWindowTitle(f"{APP_NAME} — {session.username}")
        self.resize(1280, 820)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar())

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

        # --- страницы ---
        self.page_workspaces = WorkspacesPage(self.repos)
        self.page_keys = KeysPage(self.repos)
        self.page_agents = AgentsPage(self.repos)
        self.page_task = TaskPage(self.repos)
        self.page_run = RunPage(self.repos, self.bus, self.orchestrator)
        self.page_supervisor = SupervisorPage(self.repos, self.bus, self.orchestrator)
        self.page_dashboard = DashboardPage(self.repos, self.bus)
        self.page_budget = BudgetPage(self.repos, self.bus)
        self.page_export = ExportPage(self.repos)
        self.page_settings = SettingsPage(
            self.repos, app_settings,
            on_theme_change=self._apply_theme,
            on_language_change=lambda _: self._on_language_changed(),
        )
        for page in (self.page_workspaces, self.page_keys, self.page_agents,
                     self.page_task, self.page_run, self.page_supervisor,
                     self.page_dashboard, self.page_budget, self.page_export,
                     self.page_settings):
            self.stack.addWidget(page)

        # --- связи ---
        self.page_workspaces.workspace_selected.connect(self.set_workspace)
        self.page_workspaces.workspaces_changed.connect(self._update_workspace_label)
        self.page_keys.keys_changed.connect(self.page_agents.refresh)
        self.page_agents.agents_changed.connect(self.page_task.refresh)
        self.page_agents.agents_changed.connect(self.page_dashboard.refresh)
        self.page_task.task_changed.connect(self.page_dashboard.refresh)
        self.page_task.task_changed.connect(self.page_run.refresh)
        self.page_task.run_requested.connect(self._goto_run)
        self.page_agents.agents_changed.connect(self.page_run.refresh)

        self._select_page(0)
        self.page_workspaces.refresh()
        self.page_keys.refresh()
        self._restore_last_workspace()

    # -- построение ----------------------------------------------------------
    def _build_sidebar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("Sidebar")
        bar.setFixedWidth(230)
        lay = QVBoxLayout(bar)
        lay.setContentsMargins(14, 18, 14, 18)
        lay.setSpacing(6)

        logo = QLabel(APP_NAME)
        logo.setObjectName("H2")
        lay.addWidget(logo)
        version = QLabel(f"v{APP_VERSION} · {self.session.username}")
        version.setObjectName("Dim")
        lay.addWidget(version)
        lay.addSpacing(12)

        self.ws_label = QLabel(tr("ws.current") + ": —")
        self.ws_label.setObjectName("Dim")
        self.ws_label.setWordWrap(True)
        lay.addWidget(self.ws_label)
        lay.addSpacing(8)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        entries = [
            ("nav.workspaces", 0),
            ("nav.keys", 1),
            ("nav.agents", 2),
            ("nav.task", 3),
            ("nav.run", 4),
            ("nav.supervisor", 5),
            ("nav.dashboard", 6),
            ("nav.budget", 7),
            ("nav.export", 8),
            ("nav.settings", 9),
        ]
        for key, index in entries:
            button = QPushButton(tr(key))
            button.setObjectName("Nav")
            button.setCheckable(True)
            button.clicked.connect(lambda _=False, i=index: self._select_page(i))
            self.nav_group.addButton(button, index)
            lay.addWidget(button)

        lay.addStretch(1)
        logout = QPushButton(tr("nav.logout"))
        logout.clicked.connect(self._logout)
        lay.addWidget(logout)
        return bar

    # -- состояние -----------------------------------------------------------
    def _select_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        button = self.nav_group.button(index)
        if button:
            button.setChecked(True)
        widget = self.stack.currentWidget()
        if hasattr(widget, "refresh"):
            widget.refresh()

    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.page_workspaces.set_active(ws_id)
        self.page_agents.set_workspace(ws_id)
        self.page_task.set_workspace(ws_id)
        self.page_run.set_workspace(ws_id)
        self.page_supervisor.set_workspace(ws_id)
        self.page_budget.set_workspace(ws_id)
        self.page_export.set_workspace(ws_id)
        self.page_dashboard.set_workspace(ws_id)
        self.page_settings.set_workspace(ws_id)
        self._update_workspace_label()
        self._remember_workspace(ws_id)

    def _goto_run(self) -> None:
        """Переход на страницу выполнения по кнопке со страницы задачи."""
        self._select_page(4)

    def _update_workspace_label(self) -> None:
        ws = self.repos.workspaces.get(self.workspace_id) if self.workspace_id else None
        self.ws_label.setText(f"{tr('ws.current')}: {ws.name if ws else '—'}")

    def _remember_workspace(self, ws_id: int | None) -> None:
        user = self.repos.users.get(self.session.user_id)
        if user is None:
            return
        settings = dict(user.settings)
        settings["last_workspace_id"] = ws_id
        self.repos.users.save_settings(self.session.user_id, settings)

    def _restore_last_workspace(self) -> None:
        user = self.repos.users.get(self.session.user_id)
        last = (user.settings.get("last_workspace_id") if user else None)
        workspaces = self.repos.workspaces.list(self.session.user_id)
        ids = [w.id for w in workspaces]
        if last in ids:
            self.set_workspace(last)
        elif ids:
            self.set_workspace(ids[0])
        else:
            self.set_workspace(None)

    # -- прочее --------------------------------------------------------------
    def _apply_theme(self, theme: str) -> None:
        app = self.window().style().parent() if False else None  # noqa: SIM108
        from PySide6.QtWidgets import QApplication

        QApplication.instance().setStyleSheet(stylesheet(theme))

    def _on_language_changed(self) -> None:
        """Строки страниц берутся при построении, поэтому окно собирается заново.

        Во время прогона пересборка убила бы агентов — тогда язык применится
        при следующем входе.
        """
        if self.orchestrator.state.running:
            from ui.widgets.common import info

            info(self, tr("settings.lang_after_run"))
            return
        self.rebuild_requested.emit(self.stack.currentIndex())

    def select_page(self, index: int) -> None:
        """Открывает страницу по индексу — нужно после пересборки окна."""
        self._select_page(index)

    def closeEvent(self, event) -> None:  # noqa: N802 — сигнатура Qt
        """Корректно гасим фоновые задачи агентов при закрытии окна."""
        if self.orchestrator.state.running:
            self.orchestrator.stop()
        super().closeEvent(event)

    def _logout(self) -> None:
        if self.orchestrator.state.running:
            self.orchestrator.stop()
        self.session.wipe()
        self.logged_out.emit()
        self.close()

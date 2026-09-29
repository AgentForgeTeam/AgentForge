"""Корневой объект моста: профиль, воркспейс, события ядра, уведомления.

QML видит его как контекстное свойство ``backend``; контроллеры страниц
доступны как его свойства (``backend.agents``, ``backend.run`` …).
"""

from __future__ import annotations

import asyncio
import logging
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Property, QObject, QTimer, QUrl, Signal, Slot
from PySide6.QtGui import QDesktopServices

from app.config import APP_NAME, APP_VERSION, PATHS, AppSettings
from app.i18n import available_languages, set_language, tr
from core.events import Event, EventBus, EventType
from core.orchestrator import Orchestrator
from core.security.crypto import (
    Session,
    keyring_available,
    keyring_delete_password,
    keyring_get_password,
    keyring_store_password,
)
from storage.db import Database
from storage.repositories import Repos, UserRepo
from ui.bridge.core import StateObject, error_text, fmt_money, sprop
from utils.asyncutils import run_async

log = logging.getLogger("aiorc.ui")

MIN_PASSWORD_LEN = 8
MOTION_LEVELS = {"off": 0, "reduced": 1, "full": 2}


class Backend(StateObject):
    """Состояние приложения, общее для всех экранов."""

    changed = Signal()
    #: уведомление в углу окна: вид (success|info|warning|error), заголовок, текст
    toast = Signal(str, str, str)
    #: завершилась попытка входа или регистрации: ok, текст ошибки
    authFinished = Signal(bool, str)
    #: ядро прислало событие - для страниц, которым нужна живая лента
    coreEvent = Signal("QVariantMap")
    #: просьба интерфейсу открыть страницу
    navigateRequested = Signal(str)

    def __init__(self, db: Database, settings: AppSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.db = db
        self.settings = settings
        self.users = UserRepo(db)
        self.session: Session | None = None
        self.repos: Repos | None = None
        self.bus: EventBus | None = None
        self.orchestrator: Orchestrator | None = None
        self.workspace_id: int | None = None

        from ui.bridge.pages import build_controllers

        self._controllers = build_controllers(self)
        for name, controller in self._controllers.items():
            setattr(self, f"_c_{name}", controller)

        self._state_timer = QTimer(self)
        self._state_timer.setInterval(1000)
        self._state_timer.timeout.connect(self._tick)

        self._set(loggedIn=False, username="", workspaceId=-1, workspaceName="",
                  running=False, paused=False, pendingApprovals=0, authBusy=False,
                  runElapsed="", runTokens="0", runCost="$0",
                  motion=settings.motion if settings.motion in MOTION_LEVELS else "full")
        self.refresh_profiles()

    # -- свойства -------------------------------------------------------------
    loggedIn = sprop(bool, "loggedIn", False, changed)
    username = sprop(str, "username", "", changed)
    profiles = sprop("QVariantList", "profiles", [], changed)
    lastUsername = sprop(str, "lastUsername", "", changed)
    rememberDefault = sprop(bool, "rememberDefault", False, changed)
    authBusy = sprop(bool, "authBusy", False, changed)
    workspaceId = sprop(int, "workspaceId", -1, changed)
    workspaceName = sprop(str, "workspaceName", "", changed)
    running = sprop(bool, "running", False, changed)
    paused = sprop(bool, "paused", False, changed)
    pendingApprovals = sprop(int, "pendingApprovals", 0, changed)
    runElapsed = sprop(str, "runElapsed", "", changed)
    runTokens = sprop(str, "runTokens", "0", changed)
    runCost = sprop(str, "runCost", "$0", changed)
    motion = sprop(str, "motion", "full", changed)

    def _motion_level(self) -> int:
        return MOTION_LEVELS.get(self._s.get("motion", "full"), 2)

    motionLevel = Property(int, _motion_level, notify=changed)

    def _const(value):  # noqa: N805 - фабрика константных свойств
        return Property(str, lambda self: value, constant=True)

    appName = _const(APP_NAME)
    appVersion = _const(APP_VERSION)
    dataRoot = _const(str(PATHS.home))

    def _keyring(self) -> bool:
        return keyring_available()

    keyringAvailable = Property(bool, _keyring, constant=True)

    def _controller(name: str):  # noqa: N805
        return Property(QObject, lambda self: self._controllers[name], constant=True)

    workspaces = _controller("workspaces")
    keys = _controller("keys")
    agents = _controller("agents")
    task = _controller("task")
    run = _controller("run")
    supervisor = _controller("supervisor")
    dashboard = _controller("dashboard")
    budget = _controller("budget")
    exporter = _controller("exporter")
    prefs = _controller("prefs")

    # -- профиль --------------------------------------------------------------
    def refresh_profiles(self) -> None:
        names = self.users.list_usernames()
        last = self.settings.last_username if self.settings.last_username in names else \
            (names[0] if names else "")
        self._set(profiles=names, lastUsername=last,
                  rememberDefault=bool(self.settings.remember_master_password))

    @Slot(str, result=str)
    def savedPassword(self, username: str) -> str:  # noqa: N802
        """Пароль из хранилища ОС, если пользователь просил его запомнить."""
        if username and self.settings.remember_master_password and keyring_available():
            return keyring_get_password(username) or ""
        return ""

    @Slot(str, str, bool)
    def signIn(self, username: str, password: str, remember: bool) -> None:  # noqa: N802
        username = (username or "").strip()
        if not username or not password:
            self.authFinished.emit(False, tr("login.bad_credentials"))
            return
        self._set(authBusy=True)

        async def job() -> Session | None:
            # Argon2id занимает десятые доли секунды - в отдельном потоке,
            # чтобы индикатор на кнопке не замирал.
            return await asyncio.to_thread(self.users.authenticate, username, password)

        def done(session: Session | None) -> None:
            self._set(authBusy=False)
            if session is None:
                self.authFinished.emit(False, tr("login.bad_credentials"))
                return
            self.settings.last_username = username
            self.settings.remember_master_password = bool(remember)
            self.settings.save()
            if remember:
                keyring_store_password(username, password)
            else:
                keyring_delete_password(username)
            self._open_session(session)
            self.authFinished.emit(True, "")

        def failed(exc: Exception) -> None:
            self._set(authBusy=False)
            self.authFinished.emit(False, error_text(exc))

        run_async(job(), done, failed)

    @Slot(str, str, str)
    def signUp(self, username: str, password: str, password2: str) -> None:  # noqa: N802
        username = (username or "").strip()
        error = ""
        if not username:
            error = tr("login.need_username")
        elif self.users.exists(username):
            error = tr("login.user_exists")
        elif len(password) < MIN_PASSWORD_LEN:
            error = tr("login.password_short")
        elif password != password2:
            error = tr("login.password_mismatch")
        if error:
            self.authFinished.emit(False, error)
            return
        self._set(authBusy=True)

        async def job() -> Session:
            return await asyncio.to_thread(self.users.create, username, password)

        def done(session: Session) -> None:
            self._set(authBusy=False)
            self.settings.last_username = username
            self.settings.save()
            self.refresh_profiles()
            self._open_session(session)
            self.authFinished.emit(True, "")
            self.toast.emit("success", tr("toast.profile_created"), username)

        def failed(exc: Exception) -> None:
            self._set(authBusy=False)
            self.authFinished.emit(False, error_text(exc))

        run_async(job(), done, failed)

    @Slot(str, result=int)
    def passwordStrength(self, password: str) -> int:  # noqa: N802
        """Оценка 0..4 для индикатора надёжности при создании профиля."""
        if not password:
            return 0
        score = 0
        if len(password) >= MIN_PASSWORD_LEN:
            score += 1
        if len(password) >= 12:
            score += 1
        classes = sum(bool(f(password)) for f in (
            lambda p: any(c.islower() for c in p), lambda p: any(c.isupper() for c in p),
            lambda p: any(c.isdigit() for c in p), lambda p: any(not c.isalnum() for c in p)))
        if classes >= 2:
            score += 1
        if classes >= 3 and len(password) >= 10:
            score += 1
        return min(score, 4)

    def _open_session(self, session: Session) -> None:
        self.session = session
        self.repos = Repos(self.db, session)
        fixed = self.repos.recover_interrupted_runs()
        if fixed:
            log.info("После аварийного завершения исправлено статусов: %s", fixed)
        self.bus = EventBus()
        self.bus.subscribe(self._on_event)
        self.orchestrator = Orchestrator(self.repos, self.bus)
        self._set(loggedIn=True, username=session.username)
        self._restore_workspace()
        self._state_timer.start()
        if fixed:
            self.toast.emit("info", tr("toast.recovered"), tr("toast.recovered_text"))

    @Slot()
    def logout(self) -> None:
        if self.orchestrator and self.orchestrator.state.running:
            self.orchestrator.stop()
        self._state_timer.stop()
        # Остановленный прогон ещё досылает события о завершении; экраны
        # вышедшего профиля их получать не должны.
        if self.bus is not None:
            self.bus.unsubscribe(self._on_event)
        if self.session:
            self.session.wipe()
        self.session = None
        self.repos = None
        self.bus = None
        self.orchestrator = None
        self.workspace_id = None
        for controller in self._controllers.values():
            controller.reset()
        self._set(loggedIn=False, username="", workspaceId=-1, workspaceName="",
                  running=False, paused=False, pendingApprovals=0)
        self.refresh_profiles()

    def change_password(self, old: str, new1: str, new2: str) -> str:
        """Смена пароля; возвращает текст ошибки или пустую строку."""
        if self.repos is None or self.session is None:
            return tr("login.bad_credentials")
        if len(new1) < MIN_PASSWORD_LEN:
            return tr("login.password_short")
        if new1 != new2:
            return tr("login.password_mismatch")
        if not self.repos.users.change_password(self.session, old, new1):
            return tr("login.bad_credentials")
        # Сохранённый в хранилище ОС пароль иначе перестал бы подходить.
        if self.settings.remember_master_password and keyring_available():
            keyring_store_password(self.session.username, new1)
        return ""

    # -- воркспейс --------------------------------------------------------------
    def _restore_workspace(self) -> None:
        assert self.repos is not None and self.session is not None
        user = self.repos.users.get(self.session.user_id)
        last = user.settings.get("last_workspace_id") if user else None
        ids = [w.id for w in self.repos.workspaces.list(self.session.user_id)]
        self.select_workspace(last if last in ids else (ids[0] if ids else None))

    def select_workspace(self, ws_id: int | None) -> None:
        if self.repos is None or self.session is None:
            return
        if self.orchestrator and self.orchestrator.state.running and ws_id != self.workspace_id:
            self.toast.emit("warning", tr("toast.run_active"), tr("toast.run_active_text"))
            return
        self.workspace_id = ws_id
        if ws_id is not None:
            PATHS.workspace_dir(ws_id).mkdir(parents=True, exist_ok=True)
            user = self.repos.users.get(self.session.user_id)
            if user is not None:
                settings = dict(user.settings)
                settings["last_workspace_id"] = ws_id
                self.repos.users.save_settings(self.session.user_id, settings)
        self._update_workspace_name()
        for controller in self._controllers.values():
            try:
                controller.on_workspace_changed()
            except Exception:  # noqa: BLE001 - одна страница не должна ломать остальные
                log.exception("Контроллер %s не обновился", type(controller).__name__)

    def _update_workspace_name(self) -> None:
        ws = self.repos.workspaces.get(self.workspace_id) if (self.repos and self.workspace_id) else None
        self._set(workspaceId=ws.id if ws else -1, workspaceName=ws.name if ws else "")

    @Slot(int)
    def selectWorkspace(self, ws_id: int) -> None:  # noqa: N802
        self.select_workspace(ws_id if ws_id >= 0 else None)

    # -- настройки приложения ---------------------------------------------------
    @Slot(str)
    def setLanguage(self, code: str) -> None:  # noqa: N802
        if code not in {c for c, _ in available_languages()}:
            return
        set_language(code)
        self.settings.language = code
        self.settings.save()
        # Статусы и подписи, собранные в Python, тоже на новом языке.
        for controller in self._controllers.values():
            if self.repos is not None:
                try:
                    controller.refresh()
                except Exception:  # noqa: BLE001
                    log.exception("Не обновился после смены языка: %s", controller)

    @Slot(str)
    def setMotion(self, level: str) -> None:  # noqa: N802
        if level not in MOTION_LEVELS:
            return
        self.settings.motion = level
        self.settings.save()
        self._set(motion=level)

    @Slot(str)
    def navigate(self, page: str) -> None:
        self.navigateRequested.emit(page)

    @Slot(str)
    def openPath(self, path: str) -> None:  # noqa: N802
        """Открывает файл или каталог в системном проводнике."""
        target = Path(path)
        if not target.exists():
            self.toast.emit("warning", tr("toast.not_found"), str(target))
            return
        if sys.platform == "win32" and target.is_file():
            subprocess.Popen(["explorer", "/select,", str(target)])  # noqa: S603, S607
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(target if target.is_dir() else target.parent)))

    @Slot(str)
    def copyText(self, text: str) -> None:  # noqa: N802
        from PySide6.QtGui import QGuiApplication

        QGuiApplication.clipboard().setText(text or "")
        self.toast.emit("info", tr("toast.copied"), "")

    # -- события ядра --------------------------------------------------------------
    def _on_event(self, event: Event) -> None:
        if event.workspace_id is not None and self.workspace_id is not None \
                and event.workspace_id != self.workspace_id:
            return
        for controller in self._controllers.values():
            try:
                controller.on_event(event)
            except Exception:  # noqa: BLE001
                log.exception("Сбой обработки события %s", event.type)
        self._sync_run_state()
        self._toast_for(event)
        if event.type is not EventType.AGENT_DELTA:
            self.coreEvent.emit({"type": event.type.value, "message": event.message,
                                 "agent": event.agent_name})

    def _sync_run_state(self) -> None:
        orch = self.orchestrator
        if orch is None:
            return
        gate = orch.gate
        self._set(running=orch.state.running, paused=orch.state.paused,
                  pendingApprovals=len(gate.pending()) if gate else 0)

    def _tick(self) -> None:
        """Раз в секунду: таймер прогона и живые счётчики расхода."""
        orch = self.orchestrator
        if orch is None or not orch.state.running:
            if self._s.get("runElapsed"):
                self._set(runElapsed="")
            return
        from datetime import datetime, timezone

        try:
            started = datetime.fromisoformat(orch.state.started_at)
            seconds = int((datetime.now(timezone.utc) - started).total_seconds())
        except ValueError:
            seconds = 0
        minutes, sec = divmod(max(seconds, 0), 60)
        hours, minutes = divmod(minutes, 60)
        elapsed = f"{hours}:{minutes:02d}:{sec:02d}" if hours else f"{minutes:02d}:{sec:02d}"
        from ui.bridge.core import fmt_tokens

        self._set(runElapsed=elapsed, runTokens=fmt_tokens(orch.state.tokens),
                  runCost=fmt_money(orch.state.cost))

    def _toast_for(self, event: Event) -> None:
        kind = event.type
        if kind is EventType.RUN_FINISHED:
            p = event.payload
            if p.get("stopped"):
                self.toast.emit("warning", tr("toast.run_stopped"), event.message)
            elif p.get("failed"):
                self.toast.emit("error", tr("toast.run_failed"), event.message)
            elif p.get("escalated"):
                self.toast.emit("warning", tr("toast.run_review"), event.message)
            else:
                self.toast.emit("success", tr("toast.run_done"), event.message)
        elif kind is EventType.APPROVAL_REQUESTED:
            self.toast.emit("warning", tr("toast.need_decision"), event.message)
        elif kind is EventType.BUDGET_ALERT:
            self.toast.emit("warning", tr("toast.budget_alert"), event.message)
        elif kind is EventType.BUDGET_EXCEEDED:
            self.toast.emit("error", tr("toast.budget_exceeded"), event.message)
        elif kind is EventType.BUDGET_EXTENDED:
            self.toast.emit("info", tr("toast.budget_extended"), event.message)
        elif kind is EventType.SUBTASK_FAILED:
            who = f"{event.agent_name}: " if event.agent_name else ""
            self.toast.emit("error", tr("toast.subtask_failed"), who + event.message)

    # -- служебное -----------------------------------------------------------------
    def shutdown(self) -> None:
        """Закрытие окна: гасим агентов, чтобы не оставить висящих запросов."""
        if self.orchestrator and self.orchestrator.state.running:
            self.orchestrator.stop()


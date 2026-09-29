"""Настройки воркспейса: human-in-the-loop, супервайзер, выполнение, инструменты,
песочница, доступные каталоги и безопасность профиля."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Property, Signal, Slot

from app.config import DEFAULT_WORKSPACE_SETTINGS
from app.i18n import tr
from core.tools.base import TOOL_GROUPS
from core.tools.sandbox import docker_available_async
from ui.bridge.core import Controller
from utils.asyncutils import run_async

#: допустимые диапазоны числовых настроек: (минимум, максимум)
RANGES = {
    "hitl_confidence_threshold": (0.0, 1.0),
    "summary_interval_minutes": (0, 600),
    "agent_max_steps": (1, 50),
    "max_rework_rounds": (0, 10),
    "max_parallel_agents": (1, 32),
    "sandbox_timeout_sec": (5, 600),
    "sandbox_memory_mb": (64, 8192),
}
#: группы инструментов, которые можно включать на уровне воркспейса
TOOL_SWITCHES = ["web_search", "files", "code_exec"]


class PrefsController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._set(ws={}, supervisorOptions=[], docker="unknown", hasSearchKey=False)

    ws = Property("QVariantMap", lambda s: s._s.get("ws", {}), notify=changed)
    supervisorOptions = Property("QVariantList", lambda s: s._s.get("supervisorOptions", []),
                                 notify=changed)
    docker = Property(str, lambda s: s._s.get("docker", "unknown"), notify=changed)
    hasSearchKey = Property(bool, lambda s: s._s.get("hasSearchKey", False),
                            notify=changed)

    def _tool_switches(self) -> list[dict]:
        return [{"key": k, "title": tr(f"toolgroup.{k}")} for k in TOOL_SWITCHES]

    toolSwitches = Property("QVariantList", _tool_switches, notify=changed)

    def _settings(self) -> dict:
        ws = self.repos.workspaces.get(self.ws_id) if self.ws_id else None
        return {**DEFAULT_WORKSPACE_SETTINGS, **(ws.settings if ws else {})}

    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            self._set(ws={}, supervisorOptions=[], hasSearchKey=False)
            return
        s = self._settings()
        view = {k: v for k, v in s.items() if k != "search_api_key"}
        view["tools_enabled"] = self._groups(s.get("tools_enabled") or [])
        view["extra_allowed_paths"] = [str(p) for p in s.get("extra_allowed_paths") or []]
        view["supervisor_agent_id"] = int(s.get("supervisor_agent_id") or -1)
        options = [{"id": -1, "title": tr("prefs.sup_auto")}] + [
            {"id": a.id, "title": f"{a.name} · {a.model}"}
            for a in self.repos.agents.list(self.ws_id)]
        self._set(ws=view, supervisorOptions=options,
                  hasSearchKey=bool(s.get("search_api_key")))
        if self._s.get("docker") == "unknown":
            self.checkDocker()

    @staticmethod
    def _groups(names: list[str]) -> list[str]:
        """Настройка хранит смесь групп и имён инструментов — приводим к группам."""
        groups = []
        for group in TOOL_SWITCHES:
            members = TOOL_GROUPS.get(group, [group])
            if group in names or any(m in names for m in members):
                groups.append(group)
        return groups

    def _save(self, **changes) -> None:
        s = self._settings()
        s.update(changes)
        self.repos.workspaces.update(self.ws_id, settings=s)
        self.refresh()

    @Slot(str, "QVariant")
    def setValue(self, key: str, value) -> None:  # noqa: N802
        if self.ws_id is None or key not in DEFAULT_WORKSPACE_SETTINGS or key == "search_api_key":
            return
        default = DEFAULT_WORKSPACE_SETTINGS[key]
        if key == "supervisor_agent_id":
            value = int(value) if value is not None and int(value) >= 0 else None
        elif isinstance(default, bool):
            value = bool(value)
        elif isinstance(default, int):
            value = int(round(float(value)))
        elif isinstance(default, float):
            value = round(float(value), 2)
        elif isinstance(default, str):
            value = str(value or "").strip()
        if key in RANGES and isinstance(value, (int, float)):
            low, high = RANGES[key]
            value = min(max(value, low), high)
        self._save(**{key: value})
        if key.startswith("supervisor"):
            self.backend.supervisor.refresh()

    @Slot(str, bool)
    def setTool(self, group: str, enabled: bool) -> None:  # noqa: N802
        groups = set(self._s.get("ws", {}).get("tools_enabled", []))
        if enabled:
            groups.add(group)
        else:
            groups.discard(group)
        self._save(tools_enabled=[g for g in TOOL_SWITCHES if g in groups])

    @Slot(str)
    def setSearchKey(self, secret: str) -> None:  # noqa: N802
        """Ключ Tavily/Brave хранится зашифрованным мастер-ключом профиля."""
        self._save(search_api_key=self.repos.secrets.seal((secret or "").strip()))
        self.toast("success" if secret else "info",
                   tr("toast.search_key_saved") if secret else tr("toast.search_key_removed"), "")

    @Slot()
    def addPath(self) -> None:  # noqa: N802
        from PySide6.QtWidgets import QFileDialog

        folder = QFileDialog.getExistingDirectory(None, tr("prefs.add_path"), str(Path.home()))
        if folder:
            paths = list(self._s.get("ws", {}).get("extra_allowed_paths", []))
            if folder not in paths:
                paths.append(folder)
                self._save(extra_allowed_paths=paths)

    @Slot(str)
    def removePath(self, path: str) -> None:  # noqa: N802
        paths = [p for p in self._s.get("ws", {}).get("extra_allowed_paths", []) if p != path]
        self._save(extra_allowed_paths=paths)

    @Slot()
    def checkDocker(self) -> None:  # noqa: N802
        self._set(docker="checking")
        run_async(docker_available_async(),
                  lambda ok: self._set(docker="yes" if ok else "no"),
                  lambda exc: self._set(docker="no"))

    @Slot(str, str, str, result=str)
    def changePassword(self, old: str, new1: str, new2: str) -> str:  # noqa: N802
        error = self.backend.change_password(old, new1, new2)
        if not error:
            self.toast("success", tr("toast.password_changed"), tr("toast.password_changed_text"))
        return error

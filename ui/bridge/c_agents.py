"""Агенты воркспейса: роли, модели, инструменты, системные промпты."""

from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.i18n import current_language, tr
from core.agents.roles import COMMON_RULES, TEMPLATES, by_key, title as role_title
from core.tools.base import default_registry, expand_tool_names
from providers.factory import build_provider, model_price
from providers.presets import preset
from ui.bridge.core import Controller, as_float, as_int, elide, error_text, status_title
from ui.bridge.listmodel import DictListModel
from utils.asyncutils import run_async

#: подписи инструментов в интерфейсе
TOOL_TITLES = {
    "web_search": "tool.web_search", "fetch_url": "tool.fetch_url",
    "read_file": "tool.read_file", "write_file": "tool.write_file",
    "list_dir": "tool.list_dir", "code_exec": "tool.code_exec",
}

ROLE_ICONS = {
    "analyst": "chart-line", "developer": "terminal", "tester": "badge-check",
    "critic": "scale", "documenter": "file-text", "researcher": "book-open",
    "supervisor": "shield-check", "custom": "sparkles",
}


class AgentsController(Controller):
    changed = Signal()

    #: список моделей загружен с сервера провайдера: id ключа, модели, ошибка
    modelsLoaded = Signal(int, "QVariantList", str)

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._model = DictListModel(
            ["id", "name", "role", "roleTitle", "icon", "provider", "providerTitle",
             "modelName", "keyId", "keyLabel", "temperature", "maxTokens", "tools",
             "toolTitles", "prompt", "promptPreview", "isSupervisor", "status",
             "statusTitle", "enabled", "price"], parent=self)
        self._set(hasKeys=False, keyOptions=[], supervisorId=-1)

    hasKeys = Property(bool, lambda self: self._s.get("hasKeys", False),
                       notify=changed)
    keyOptions = Property("QVariantList", lambda self: self._s.get("keyOptions", []),
                          notify=changed)

    def _get_model(self) -> QObject:
        return self._model

    model = Property(QObject, _get_model, constant=True)

    def _templates(self) -> list[dict]:
        lang = current_language()
        return [{"key": t.key, "title": role_title(t, lang), "icon": ROLE_ICONS.get(t.key, "bot"),
                 "tools": expand_tool_names(t.suggested_tools)} for t in TEMPLATES]

    templates = Property("QVariantList", _templates, notify=changed)

    def _tools(self) -> list[dict]:
        return [{"name": n, "title": tr(TOOL_TITLES.get(n, n))} for n in default_registry().names()]

    tools = Property("QVariantList", _tools, notify=changed)

    @Slot()
    def refresh(self) -> None:
        if not self.ready:
            return
        keys = self.repos.keys.list()
        key_by_id = {k.id: k for k in keys}
        self._set(hasKeys=bool(keys), keyOptions=[
            {"id": k.id, "title": f"{k.label} · {preset(k.provider).title}",
             "provider": k.provider} for k in keys])
        if self.ws_id is None:
            self._model.clear()
            self.changed.emit()
            return
        lang = current_language()
        items = []
        for a in self.repos.agents.list(self.ws_id):
            key = key_by_id.get(a.api_key_id or -1)
            tools = expand_tool_names(a.tools)
            p_in, p_out = model_price(a.provider, a.model) if a.model else (0.0, 0.0)
            items.append({
                "id": a.id, "name": a.name, "role": a.role or "custom",
                "roleTitle": role_title(by_key(a.role or "custom"), lang),
                "icon": ROLE_ICONS.get(a.role or "custom", "bot"),
                "provider": a.provider, "providerTitle": preset(a.provider).title if a.provider else "",
                "modelName": a.model, "keyId": a.api_key_id or -1,
                "keyLabel": key.label if key else tr("agents.key_missing"),
                "temperature": a.temperature, "maxTokens": a.max_tokens,
                "tools": tools, "toolTitles": [tr(TOOL_TITLES.get(t, t)) for t in tools],
                "prompt": a.system_prompt, "promptPreview": elide(a.system_prompt, 150),
                "isSupervisor": a.is_supervisor, "status": a.status,
                "statusTitle": status_title(a.status), "enabled": a.enabled,
                "price": (f"${p_in:g} / ${p_out:g}" if (p_in or p_out)
                          else (tr("agents.free") if a.provider and preset(a.provider).local else "")),
            })
        self._model.set_items(items)
        self.changed.emit()

    def reset(self) -> None:
        super().reset()
        self._model.clear()

    def on_event(self, event) -> None:
        from core.events import EventType

        if event.type is EventType.AGENT_STATUS and event.agent_id:
            status = event.payload.get("status", event.message)
            self._model.update_row(event.agent_id, status=status,
                                   statusTitle=status_title(status))
        elif event.type in (EventType.RUN_FINISHED, EventType.RUN_STOPPED):
            self.refresh()

    # -- форма агента ---------------------------------------------------------
    @Slot(str, result="QVariantMap")
    def templateInfo(self, key: str) -> dict:  # noqa: N802
        template = by_key(key)
        prompt = (template.prompt + "\n\n" + COMMON_RULES.strip()) if template.prompt else ""
        return {"name": role_title(template, current_language()), "prompt": prompt,
                "tools": expand_tool_names(template.suggested_tools)}

    @Slot(int, result="QVariantList")
    def modelsForKey(self, key_id: int) -> list[str]:  # noqa: N802
        """Кэш последней проверки ключа, иначе популярные модели пресета."""
        key = self.repos.keys.get(key_id) if self.ready and key_id >= 0 else None
        if key is None:
            return []
        return list(key.meta.get("models") or preset(key.provider).suggested_models)

    @Slot(int)
    def loadModels(self, key_id: int) -> None:  # noqa: N802
        key = self.repos.keys.get(key_id)
        if key is None:
            self.modelsLoaded.emit(key_id, [], tr("keys.not_found"))
            return

        async def job() -> list[str]:
            provider = build_provider(key.provider, self.repos.keys.reveal(key.id),
                                      key.base_url, timeout=20)
            try:
                return await provider.list_models()
            finally:
                await provider.aclose()

        def done(models: list[str]) -> None:
            if self.ready:
                # Только кэш моделей: подпись и адрес за время запроса могли
                # поменять, и старые значения их бы затёрли.
                self.repos.keys.update_meta(key.id, models=models[:300])
            self.modelsLoaded.emit(key_id, models[:300], "")

        def failed(exc: Exception) -> None:
            self.modelsLoaded.emit(key_id, [], tr("keys.test_fail", err=error_text(exc)))

        run_async(job(), done, failed)

    @Slot("QVariantMap", result=str)
    def save(self, data: dict) -> str:
        """Создаёт или обновляет агента. Возвращает текст ошибки или пустую строку."""
        if self.ws_id is None:
            return tr("ws.empty")
        name = str(data.get("name") or "").strip()
        model = str(data.get("model") or "").strip()
        key_id = as_int(data.get("keyId"))
        key = self.repos.keys.get(key_id) if key_id >= 0 else None
        if not name:
            return tr("agents.need_name")
        if key is None:
            return tr("agents.need_key")
        if not model:
            return tr("agents.need_model")
        tools = [t for t in (data.get("tools") or []) if t in default_registry().names()]
        fields = dict(
            name=name, role=str(data.get("role") or "custom"),
            system_prompt=str(data.get("prompt") or "").strip(),
            api_key_id=key.id, provider=key.provider, model=model,
            params={"temperature": round(min(max(as_float(data.get("temperature"), 0.7), 0.0), 2.0), 2),
                    "max_tokens": max(1, as_int(data.get("maxTokens"), 2048)), "tools": tools},
            is_supervisor=bool(data.get("isSupervisor", False)),
        )
        agent_id = as_int(data.get("id"))
        if agent_id >= 0:
            self.repos.agents.update(agent_id, **fields)
            self.toast("success", tr("toast.agent_saved"), name)
        else:
            self.repos.agents.create(self.ws_id, **fields)
            self.toast("success", tr("toast.agent_created"), name)
        self._after_change()
        return ""

    @Slot(int)
    def remove(self, agent_id: int) -> None:
        if self.backend.running:
            # Агент мог быть занят подзадачей: его история и отчёт ссылаются
            # на запись, которой больше нет, и прогон падает на сохранении.
            self.toast("warning", tr("toast.run_active"), tr("toast.run_active_text"))
            return
        agent = self.repos.agents.get(agent_id)
        self.repos.agents.delete(agent_id)
        self._after_change()
        self.toast("info", tr("toast.agent_deleted"), agent.name if agent else "")

    @Slot(int, bool)
    def setEnabled(self, agent_id: int, enabled: bool) -> None:  # noqa: N802
        self.repos.agents.update(agent_id, enabled=enabled)
        self._model.update_row(agent_id, enabled=enabled)

    @Slot(int)
    def duplicate(self, agent_id: int) -> None:
        a = self.repos.agents.get(agent_id)
        if a is None:
            return
        self.repos.agents.create(a.workspace_id, a.name + " 2", a.role, a.system_prompt,
                                 a.api_key_id, a.provider, a.model, dict(a.params), False)
        self._after_change()

    def _after_change(self) -> None:
        self.refresh()
        self.backend.task.refresh()
        self.backend.prefs.refresh()
        self.backend.dashboard.schedule()

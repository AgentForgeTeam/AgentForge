"""API-ключи провайдеров: общие для всех воркспейсов профиля."""

from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.i18n import tr
from providers.factory import build_provider
from providers.presets import preset, preset_list
from ui.bridge.core import Controller, error_text, when
from ui.bridge.listmodel import DictListModel
from utils.asyncutils import run_async


class KeysController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._model = DictListModel(
            ["id", "label", "provider", "providerTitle", "baseUrl", "hasSecret",
             "local", "free", "models", "testState", "testMessage", "created"],
            parent=self)
        self._presets = [
            {"key": p.key, "title": p.title, "baseUrl": p.base_url,
             "requiresKey": p.requires_key, "free": p.free_tier, "local": p.local,
             "notes": p.notes, "docsUrl": p.docs_url,
             "models": ", ".join(p.suggested_models[:3])}
            for p in preset_list()
        ]
        #: результаты проверок живут до выхода из профиля
        self._tests: dict[int, tuple[str, str]] = {}

    def _get_model(self) -> QObject:
        return self._model

    model = Property(QObject, _get_model, constant=True)

    def _get_presets(self) -> list:
        return self._presets

    presets = Property("QVariantList", _get_presets, constant=True)

    @Slot()
    def refresh(self) -> None:
        if not self.ready:
            return
        items = []
        for key in self.repos.keys.list():
            p = preset(key.provider)
            state, message = self._tests.get(key.id, ("", ""))
            items.append({
                "id": key.id, "label": key.label, "provider": key.provider,
                "providerTitle": p.title, "baseUrl": key.base_url or p.base_url,
                "hasSecret": key.has_secret, "local": p.local, "free": p.free_tier,
                "models": len(key.meta.get("models") or []),
                "testState": state, "testMessage": message, "created": when(key.created_at),
            })
        self._model.set_items(items)

    def reset(self) -> None:
        super().reset()
        self._tests.clear()
        self._model.clear()

    @Slot(str, str, str, str, result=str)
    def create(self, provider: str, label: str, base_url: str, secret: str) -> str:
        p = preset(provider)
        secret = (secret or "").strip()
        if p.requires_key and not secret:
            return tr("keys.need_secret")
        if p.key == "custom" and not (base_url or "").strip():
            return tr("keys.need_url")
        key = self.repos.keys.create((label or "").strip() or p.title, provider, secret,
                                     (base_url or "").strip())
        self.refresh()
        self.backend.agents.refresh()
        self.toast("success", tr("toast.key_saved"), key.label)
        self.test(key.id)
        return ""

    @Slot(int, str, str, str, result=str)
    def update(self, key_id: int, label: str, base_url: str, secret: str) -> str:
        key = self.repos.keys.get(key_id)
        if key is None:
            return tr("keys.not_found")
        self.repos.keys.update(key_id, (label or "").strip() or key.label,
                               (base_url or "").strip(), (secret or "").strip() or None)
        self._tests.pop(key_id, None)
        self.refresh()
        self.backend.agents.refresh()
        return ""

    @Slot(int)
    def remove(self, key_id: int) -> None:
        key = self.repos.keys.get(key_id)
        self.repos.keys.delete(key_id)
        self._tests.pop(key_id, None)
        self.refresh()
        self.backend.agents.refresh()
        self.toast("info", tr("toast.key_deleted"), key.label if key else "")

    @Slot(int)
    def test(self, key_id: int) -> None:
        """Реальный запрос списка моделей: проверяет и ключ, и адрес сервера."""
        key = self.repos.keys.get(key_id)
        if key is None:
            return
        self._tests[key_id] = ("testing", "")
        self._model.update_row(key_id, testState="testing", testMessage="")

        async def job() -> list[str]:
            secret = self.repos.keys.reveal(key.id)
            provider = build_provider(key.provider, secret, key.base_url, timeout=20)
            try:
                return await provider.test()
            finally:
                await provider.aclose()

        def done(models: list[str]) -> None:
            message = tr("keys.test_ok", n=len(models))
            self._tests[key_id] = ("ok", message)
            meta = dict(key.meta)
            meta["models"] = models[:300]    # кэш для выпадающего списка моделей
            self.repos.keys.update(key.id, key.label, key.base_url, None, meta)
            self._model.update_row(key_id, testState="ok", testMessage=message,
                                   models=len(models))
            self.backend.agents.refresh()

        def failed(exc: Exception) -> None:
            message = tr("keys.test_fail", err=error_text(exc))
            self._tests[key_id] = ("fail", message)
            self._model.update_row(key_id, testState="fail", testMessage=message)

        run_async(job(), done, failed)

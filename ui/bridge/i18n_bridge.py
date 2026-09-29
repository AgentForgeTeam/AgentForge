"""Локализация для QML.

Словарь строк текущего языка отдаётся в QML свойством ``t``; биндинги вида
``text: i18n.t["login.title"]`` зависят от этого свойства, поэтому при смене
языка весь интерфейс перерисовывается сам - без пересборки окна, как было
в версии на виджетах.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Property, QObject, Signal, Slot

from app import i18n as catalog


class I18n(QObject):
    changed = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._strings: dict[str, str] = {}
        self._rebuild()
        catalog.on_language_changed(self._on_catalog_changed)

    def _rebuild(self) -> None:
        # Русский словарь - базовый: если в английском чего-то нет, строка
        # всё равно не пропадёт из интерфейса.
        merged = dict(catalog.RU)
        merged.update(catalog.catalog_for(catalog.current_language()))
        self._strings = merged

    def _on_catalog_changed(self) -> None:
        self._rebuild()
        self.changed.emit()

    def _t(self) -> dict[str, str]:
        return self._strings

    t = Property("QVariantMap", _t, notify=changed)

    def _lang(self) -> str:
        return catalog.current_language()

    lang = Property(str, _lang, notify=changed)

    def _languages(self) -> list[dict[str, str]]:
        return [{"code": c, "title": t} for c, t in catalog.available_languages()]

    languages = Property("QVariantList", _languages, constant=True)

    @Slot(str, "QVariantMap", result=str)
    def fmt(self, template: str, args: dict[str, Any]) -> str:
        """Подставляет ``{placeholders}``; сломанный шаблон возвращается как есть."""
        try:
            return (template or "").format(**(args or {}))
        except (KeyError, IndexError, ValueError):
            return template or ""

    @Slot(str, result=str)
    def status(self, code: str) -> str:
        return self._strings.get(f"status.{code}", code)

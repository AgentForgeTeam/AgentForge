"""Общие кирпичики моста: объект состояния, контроллер страницы, форматтеры."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.i18n import tr
from storage.db import local_time

if TYPE_CHECKING:  # pragma: no cover
    from core.events import Event
    from storage.repositories import Repos
    from ui.bridge.backend import Backend


class StateObject(QObject):
    """QObject, у которого все свойства лежат в одном словаре.

    Одного сигнала ``changed`` хватает всем свойствам: QML перечитывает
    только те биндинги, что зависят от объекта, а объектов немного. Это
    избавляет от десятков однотипных сигналов и сеттеров.

    Важно: сигнал ``changed = Signal()`` объявляет КАЖДЫЙ конечный класс, а
    не этот базовый. PySide6 связывает ``notify`` свойства только с сигналом
    того же класса; с унаследованным сигналом свойство становится
    «неуведомляемым», и биндинги QML перестают обновляться.
    """

    changed: Signal  # объявляется в подклассе

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._s: dict[str, Any] = {}

    def _set(self, **values: Any) -> None:
        dirty = False
        for name, value in values.items():
            if self._s.get(name, _MISSING) != value:
                self._s[name] = value
                dirty = True
        if dirty:
            self.changed.emit()


_MISSING = object()


def sprop(type_: Any, name: str, default: Any, signal: Signal) -> Property:
    """Свойство, читающее ``self._s[name]`` и уведомляющее сигналом класса."""

    def getter(self: StateObject) -> Any:
        return self._s.get(name, default)

    return Property(type_, getter, notify=signal)


class Controller(StateObject):
    """Контроллер одной страницы: данные для QML и действия пользователя."""

    def __init__(self, backend: "Backend") -> None:
        super().__init__(backend)
        self.backend = backend

    @property
    def repos(self) -> "Repos":
        assert self.backend.repos is not None, "контроллер вызван до входа в профиль"
        return self.backend.repos

    @property
    def ws_id(self) -> int | None:
        return self.backend.workspace_id

    @property
    def ready(self) -> bool:
        return self.backend.repos is not None

    def toast(self, kind: str, title: str, message: str = "") -> None:
        self.backend.toast.emit(kind, title, message)

    # -- переопределяемое ---------------------------------------------------
    @Slot()
    def refresh(self) -> None:
        """Перечитать данные из хранилища."""

    def on_workspace_changed(self) -> None:
        self.refresh()

    def on_event(self, event: "Event") -> None:
        """Реакция на событие ядра (по умолчанию ничего)."""

    def reset(self) -> None:
        """Сброс при выходе из профиля."""
        self._s.clear()
        self.changed.emit()


# -- форматтеры -------------------------------------------------------------------


def fmt_tokens(value: int | float) -> str:
    value = int(value or 0)
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 10_000:
        return f"{value / 1000:.1f}k"
    return f"{value:,}".replace(",", " ")


def fmt_money(value: float) -> str:
    """Сумма с точностью, при которой копеечные расходы не превращаются в $0.00."""
    value = float(value or 0)
    if value >= 100:
        return f"${value:,.0f}".replace(",", " ")
    if value >= 1:
        return f"${value:.2f}"
    if value >= 0.01:
        return f"${value:.3f}"
    if value == 0:
        return "$0"
    return f"${value:.4f}"


def when(iso: str | None, fmt: str = "%d.%m %H:%M") -> str:
    return local_time(iso or "", fmt) if iso else ""


def elide(text: str, limit: int) -> str:
    text = (text or "").strip().replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def error_text(exc: BaseException) -> str:
    from providers.base import ProviderError

    if isinstance(exc, (ProviderError, RuntimeError, ValueError)):
        return str(exc)
    return f"{type(exc).__name__}: {exc}"


def status_title(code: str) -> str:
    return tr(f"status.{code}") if code else ""

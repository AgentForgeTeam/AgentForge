"""Запуск интерфейса на Qt Quick.

Порядок: приложение Qt → шрифты → мост (Backend, I18n) → QML-движок →
главное окно → общий цикл asyncio (qasync).
"""

from __future__ import annotations

import ctypes
import logging
import sys
from pathlib import Path

from PySide6.QtCore import QtMsgType, qInstallMessageHandler
from PySide6.QtGui import QFontDatabase, QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

from app.config import AppSettings
from storage.db import Database

log = logging.getLogger("aiorc.qml")

UI_DIR = Path(__file__).resolve().parent
QML_DIR = UI_DIR / "qml"
FONTS_DIR = UI_DIR / "assets" / "fonts"

#: сообщения QML, собранные за сессию (смоук-тест интерфейса проверяет,
#: что среди них нет ошибок)
QML_MESSAGES: list[tuple[str, str]] = []


def _qt_message(mode: QtMsgType, context, message: str) -> None:
    level = {QtMsgType.QtWarningMsg: "warning", QtMsgType.QtCriticalMsg: "error",
             QtMsgType.QtFatalMsg: "error"}.get(mode, "info")
    if "Cannot find font directory" in message:
        level = "info"    # платформа без системных шрифтов; свои шрифты мы приносим сами
    QML_MESSAGES.append((level, message))
    if level == "info":
        log.debug(message)
    else:
        log.warning("Qt: %s", message)


def ensure_qt_dll_path() -> None:
    """Помогает Windows найти DLL Qt для QML-плагинов.

    Плагины (например, стиль Basic для Qt Quick Controls) лежат в подкаталогах
    PySide6 и зависят от DLL в его корне. В части окружений (venv, запуск не
    из консоли Python) Windows их не находит, и загрузка QML падает с
    «Не найден указанный модуль». Явное добавление каталога это лечит.
    """
    if sys.platform != "win32":
        return
    import os

    import PySide6

    qt_dir = os.path.dirname(PySide6.__file__)
    try:
        os.add_dll_directory(qt_dir)
    except (OSError, AttributeError):
        pass
    if qt_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = qt_dir + os.pathsep + os.environ.get("PATH", "")


def load_fonts() -> dict[str, str]:
    """Регистрирует шрифты из комплекта и возвращает имена семейств для QML."""
    families = {"sans": "Segoe UI", "mono": "Consolas", "icons": "lucide"}
    found: dict[str, str] = {}
    for path in sorted(FONTS_DIR.glob("*.ttf")):
        font_id = QFontDatabase.addApplicationFont(str(path))
        names = QFontDatabase.applicationFontFamilies(font_id) if font_id >= 0 else []
        if not names:
            log.warning("Не удалось загрузить шрифт %s", path.name)
            continue
        if path.name.startswith("Inter"):
            found["sans"] = names[0]
        elif path.name.startswith("JetBrains"):
            found["mono"] = names[0]
        elif path.name.startswith("lucide"):
            found["icons"] = names[0]
    families.update(found)
    return families


def apply_dark_titlebar(window) -> None:
    """Тёмный системный заголовок окна на Windows 10/11, в цвет фона приложения."""
    if sys.platform != "win32" or window is None:
        return
    try:
        hwnd = int(window.winId())
        dwm = ctypes.windll.dwmapi
        value = ctypes.c_int(1)
        # DWMWA_USE_IMMERSIVE_DARK_MODE: 20 (новые сборки) и 19 (старые)
        for attr in (20, 19):
            if dwm.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(value), ctypes.sizeof(value)) == 0:
                break
        # DWMWA_CAPTION_COLOR (Windows 11): цвет заголовка = цвет фона (BGR)
        caption = ctypes.c_int(0x0F0809)
        dwm.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(caption), ctypes.sizeof(caption))
    except Exception:  # noqa: BLE001 - косметика, не повод падать
        log.debug("Тёмный заголовок окна недоступен", exc_info=True)


class UiApp:
    """Собранное приложение: держит ссылки, чтобы их не собрал сборщик мусора."""

    def __init__(self, settings: AppSettings, db: Database | None = None) -> None:
        from ui.bridge.backend import Backend
        from ui.bridge.i18n_bridge import I18n

        ensure_qt_dll_path()
        qInstallMessageHandler(_qt_message)
        QQuickStyle.setStyle("Basic")
        self.app = QGuiApplication.instance()
        assert self.app is not None, "QApplication должно быть создано до UiApp"
        icon = UI_DIR / "assets" / "icon.png"
        if icon.exists():
            self.app.setWindowIcon(QIcon(str(icon)))

        self.fonts = load_fonts()
        self.backend = Backend(db or Database(), settings)
        self.i18n = I18n()
        self.engine = QQmlApplicationEngine()
        self.engine.addImportPath(str(QML_DIR))
        ctx = self.engine.rootContext()
        ctx.setContextProperty("backend", self.backend)
        ctx.setContextProperty("i18n", self.i18n)
        ctx.setContextProperty("fonts", self.fonts)
        self.engine.load(str(QML_DIR / "Main.qml"))
        if not self.engine.rootObjects():
            raise RuntimeError("Не удалось загрузить интерфейс (Main.qml). Подробности в логе.")
        self.window = self.engine.rootObjects()[0]
        apply_dark_titlebar(self.window)

    def dispose(self) -> None:
        """Порядок важен: сначала гасим агентов и QML, потом мост.

        Если мост уничтожить раньше движка, биндинги QML успевают обратиться
        к уже удалённым объектам и засыпают лог ошибками «of null».

        Вызывается явно после выхода из цикла событий, а не по
        ``aboutToQuit``: qasync выходит из цикла Qt и в служебных случаях
        (``run_until_complete``), и окно пропадало бы посреди работы.
        """
        self.backend.shutdown()
        # Движок принадлежит Python: снятие ссылки удаляет его сразу, вместе
        # с деревом QML, пока мост ещё жив.
        self.window = None
        self.engine = None

"""Точка входа Agent Forge.

Запуск::

    python main.py

Цикл событий Qt и asyncio объединяются через qasync - это даёт один общий
луп, в котором живут и интерфейс, и параллельно работающие агенты.
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

# Чтобы приложение запускалось из любого каталога.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.config import APP_NAME, PATHS, AppSettings  # noqa: E402
from app.i18n import set_language  # noqa: E402

# Шрифты и геометрия Qt Quick лучше выглядят без принудительного округления
# масштаба на дисплеях 125-175 %.
os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
from utils.logging_setup import setup_logging  # noqa: E402

log = logging.getLogger("aiorc.main")


def _check_dependencies() -> None:
    """Понятное сообщение вместо стектрейса, если зависимости не установлены."""
    missing: list[str] = []
    for module, package in (("PySide6", "PySide6"), ("qasync", "qasync"),
                            ("httpx", "httpx"), ("cryptography", "cryptography")):
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    if missing:
        print(f"Не установлены зависимости: {', '.join(missing)}\n"
              f"Выполните:  pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    _check_dependencies()

    import qasync
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    from storage.db import Database
    from ui.app import UiApp

    setup_logging()
    PATHS.ensure()
    log.info("Старт %s, каталог данных: %s", APP_NAME, PATHS.home)

    settings = AppSettings.load()
    set_language(settings.language)

    # QApplication, а не QGuiApplication: системные диалоги выбора файлов
    # и папок (экспорт, разрешённые каталоги) живут в QtWidgets.
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("AgentForge")

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    ui = UiApp(settings, Database())

    with loop:
        code = loop.run_forever() or 0
        ui.dispose()
    return code


if __name__ == "__main__":
    sys.exit(main())

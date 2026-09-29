"""Точка входа AI Orchestrator.

Запуск::

    python main.py

Цикл событий Qt и asyncio объединяются через qasync — это даёт один общий
луп, в котором живут и интерфейс, и параллельно работающие агенты.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

# Чтобы приложение запускалось из любого каталога.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.config import APP_NAME, PATHS, AppSettings  # noqa: E402
from app.i18n import set_language  # noqa: E402
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


def start_ui(db, settings: AppSettings) -> dict[str, object]:
    """Связывает окна: вход → главное окно → выход или смена языка.

    Возвращает словарь с текущими окнами (ключи ``login`` и ``main``) —
    по нему смоук-тест интерфейса ходит по тому же пути, что и приложение.
    """
    from ui.login_window import LoginWindow
    from ui.main_window import MainWindow

    windows: dict[str, object] = {}

    def show_login() -> None:
        login = LoginWindow(db, settings)
        login.logged_in.connect(lambda session: on_login(login, session))
        windows["login"] = login
        login.show()

    def open_main(session, page: int = 0) -> None:
        window = MainWindow(db, session, settings)
        window.logged_out.connect(show_login)
        window.rebuild_requested.connect(lambda index: rebuild_main(window, index))
        windows["main"] = window
        window.select_page(page)
        window.show()

    def rebuild_main(old: MainWindow, page: int) -> None:
        """Пересобирает главное окно после смены языка, сохраняя сессию."""
        geometry = old.saveGeometry()
        open_main(old.session, page)
        windows["main"].restoreGeometry(geometry)
        old.close()
        old.deleteLater()

    def on_login(login: LoginWindow, session) -> None:
        login.close()
        open_main(session)

    show_login()
    return windows


def main() -> int:
    _check_dependencies()

    import qasync
    from PySide6.QtWidgets import QApplication

    from storage.db import Database
    from ui.theme import stylesheet

    setup_logging()
    PATHS.ensure()
    log.info("Старт %s, каталог данных: %s", APP_NAME, PATHS.home)

    settings = AppSettings.load()
    set_language(settings.language)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet(stylesheet(settings.theme))

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    windows = start_ui(Database(), settings)  # noqa: F841 — держит окна живыми

    with loop:
        return loop.run_forever() or 0


if __name__ == "__main__":
    sys.exit(main())

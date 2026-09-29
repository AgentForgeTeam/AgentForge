"""Настройка логирования: файл с ротацией + консоль."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler

from app.config import PATHS

_FORMAT = "%(asctime)s  %(levelname)-7s  %(name)-22s  %(message)s"


def setup_logging(level: int = logging.INFO) -> None:
    PATHS.ensure()
    root = logging.getLogger()
    if root.handlers:  # уже настроено
        return
    root.setLevel(level)

    file_handler = RotatingFileHandler(
        PATHS.logs_dir / "app.log", maxBytes=2_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(_FORMAT))
    root.addHandler(file_handler)

    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(logging.Formatter(_FORMAT))
    root.addHandler(console)

    # Библиотеки не должны заливать лог.
    for noisy in ("httpx", "httpcore", "urllib3", "asyncio"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

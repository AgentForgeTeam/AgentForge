"""Общая настройка pytest: изолированный каталог данных и путь к проекту.

Каталог данных задаётся ДО импорта модулей приложения: ``app.config``
вычисляет пути при импорте, и тесты не должны трогать реальный профиль.
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

_HOME = Path(tempfile.mkdtemp(prefix="aiorc_pytest_"))
os.environ["AIORC_HOME"] = str(_HOME)


def pytest_sessionfinish(session, exitstatus):  # noqa: ARG001
    shutil.rmtree(_HOME, ignore_errors=True)

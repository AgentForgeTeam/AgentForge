"""Интерфейс на Qt Quick: загрузка всех экранов и живой прогон без сети.

Тур запускается отдельным процессом: у Qt и qasync свой цикл событий, и
смешивать его с циклом pytest-asyncio в одном процессе ненадёжно.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_bridge_properties_notify_qml():
    """Каждое свойство моста либо константное, либо с сигналом изменения.

    Иначе биндинги QML молча перестают обновляться (так было с сигналом,
    унаследованным от базового класса).
    """
    from ui.bridge import (backend, c_agents, c_budget, c_dashboard, c_export, c_keys,
                           c_prefs, c_run, c_supervisor, c_task, c_workspaces, i18n_bridge,
                           listmodel)

    modules = (c_agents, c_budget, c_dashboard, c_export, c_keys, c_prefs, c_run,
               c_supervisor, c_task, c_workspaces)
    classes = [backend.Backend, i18n_bridge.I18n, listmodel.DictListModel] + [
        getattr(m, n) for m in modules for n in dir(m)
        if n.endswith("Controller") and n != "Controller"]
    silent = []
    for cls in classes:
        mo = cls.staticMetaObject
        for i in range(mo.propertyOffset(), mo.propertyCount()):
            prop = mo.property(i)
            if not prop.hasNotifySignal() and not prop.isConstant():
                silent.append(f"{cls.__name__}.{prop.name()}")
    assert not silent, silent


def test_translation_keys_exist_in_both_languages():
    import re

    from app import i18n

    used = set()
    for f in (ROOT / "ui" / "qml").rglob("*.qml"):
        used |= set(re.findall(r'i18n\.t\["([^"]+)"\]', f.read_text("utf-8")))
    missing_ru = sorted(k for k in used if k not in i18n.RU)
    missing_en = sorted(k for k in i18n.RU if k not in i18n.EN)
    assert not missing_ru, missing_ru
    assert not missing_en, missing_en


def test_toggles_show_saved_state_after_click():
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen")
    proc = subprocess.run([sys.executable, str(ROOT / "tests" / "qml_controls_check.py")],
                          cwd=ROOT, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=120)
    assert proc.returncode == 0, proc.stdout[-3000:] + proc.stderr[-3000:]


def test_ui_tour_runs_without_qml_errors(tmp_path):
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen",
               AGENTFORGE_HOME=str(tmp_path / "data"))
    proc = subprocess.run([sys.executable, str(ROOT / "tests" / "ui_tour.py"),
                           str(tmp_path / "shots")],
                          cwd=ROOT, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=300)
    assert proc.returncode == 0, proc.stdout[-3000:] + proc.stderr[-3000:]
    shots = sorted(p.name for p in (tmp_path / "shots").glob("*.png"))
    assert len(shots) >= 15, shots

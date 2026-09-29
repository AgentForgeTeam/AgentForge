"""Смоук-прогон интерфейса: полный пользовательский сценарий без сети.

Запуск::

    python tests/ui_smoke.py              # без окон (offscreen), скриншоты в temp
    python tests/ui_smoke.py --show       # с настоящими окнами
    python tests/ui_smoke.py --out DIR    # куда сложить скриншоты

Сценарий: создание профиля → воркспейс → ключ → агенты → задача и
автоматическое разбиение → прогон с паузой human-in-the-loop → супервайзер,
дашборд, бюджеты → экспорт во все форматы → смена темы и языка.

Модальные диалоги подменяются заполнителями, модели — фейковым провайдером.
Любое исключение в слоте Qt, в обработчике шины или в фоновой задаче
считается провалом.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

parser = argparse.ArgumentParser()
parser.add_argument("--show", action="store_true", help="показывать настоящие окна")
parser.add_argument("--out", default="", help="каталог для скриншотов")
ARGS = parser.parse_args()

if not ARGS.show:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    # offscreen-платформа сама системные шрифты не находит — без этого
    # на скриншотах вместо текста квадраты
    if sys.platform == "win32":
        os.environ.setdefault("QT_QPA_FONTDIR", os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts"))
    elif sys.platform == "darwin":
        os.environ.setdefault("QT_QPA_FONTDIR", "/System/Library/Fonts")
    else:
        os.environ.setdefault("QT_QPA_FONTDIR", "/usr/share/fonts")
_TEMP_HOME = Path(tempfile.mkdtemp(prefix="aiorc_ui_"))
os.environ["AIORC_HOME"] = str(_TEMP_HOME)
SHOTS = Path(ARGS.out) if ARGS.out else _TEMP_HOME / "shots"
SHOTS.mkdir(parents=True, exist_ok=True)

import qasync  # noqa: E402
import shiboken6  # noqa: E402
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox, QPushButton  # noqa: E402

from app.config import PATHS, AppSettings  # noqa: E402
from app.i18n import set_language  # noqa: E402
from core.hitl import DECISION_TITLES, Decision  # noqa: E402
from providers.base import CompletionResult, LLMProvider, ToolCall, Usage  # noqa: E402
from storage.db import Database  # noqa: E402
from ui.theme import stylesheet  # noqa: E402

# ---------------------------------------------------------------------------
# Сбор ошибок
# ---------------------------------------------------------------------------

ERRORS: list[str] = []
_passed: list[str] = []
_failed: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    mark = "OK  " if condition else "FAIL"
    print(f"  [{mark}] {name}" + (f" — {detail}" if detail else ""))
    (_passed if condition else _failed).append(name)


def _excepthook(kind, value, tb) -> None:
    ERRORS.append("".join(traceback.format_exception(kind, value, tb)))


class _ErrorLog(logging.Handler):
    """Ошибки, которые ядро глотает и пишет в лог (шина, run_async)."""

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= logging.ERROR:
            text = record.getMessage()
            if record.exc_info:
                text += "\n" + "".join(traceback.format_exception(*record.exc_info))
            ERRORS.append(text)


sys.excepthook = _excepthook
logging.getLogger().addHandler(_ErrorLog())
logging.getLogger().setLevel(logging.INFO)

# ---------------------------------------------------------------------------
# Фейковая модель: одна на всех, роль определяется по промпту
# ---------------------------------------------------------------------------


class FakeModel(LLMProvider):
    calls: dict[str, int] = {}

    async def list_models(self) -> list[str]:
        return ["fake-mini", "fake-large"]

    async def aclose(self) -> None:
        return None

    async def complete(self, model, messages, *, temperature=0.7,
                       max_tokens=2048, tools=None):
        await asyncio.sleep(0.05)
        system, user = messages[0].content, messages[-1].content
        joined = "\n".join(m.content for m in messages)
        if "планировщик работ" in system:
            return CompletionResult(
                text='{"subtasks": ['
                     '{"title": "Собрать требования", "description": "Опросить источники", '
                     '"assignee_role": "analyst"},'
                     '{"title": "Написать скрипт", "description": "Сохранить main.py", '
                     '"assignee_role": "developer"}]}',
                usage=Usage(300, 120))
        if "ПРОВЕРЯЕМАЯ ПОДЗАДАЧА" in joined:
            return CompletionResult(text='{"verdict":"ok","notes":"","issues":[]}',
                                    usage=Usage(150, 20))
        if "Сравни результаты" in system:
            return CompletionResult(
                text='{"conflicts":[{"description":"Сроки в отчётах расходятся",'
                     '"severity":"medium","labels":[],"auto_resolvable":true,'
                     '"resolution":"Берём более поздний срок"}]}',
                usage=Usage(120, 40))
        if "Составь краткую сводку" in system:
            return CompletionResult(
                text="ФАКТЫ:\nтребования собраны\nРАСХОЖДЕНИЯ:\nнет\nОТКРЫТЫЕ ВОПРОСЫ:\nнет",
                usage=Usage(120, 50))

        # Исполнитель: разработчик сначала пишет файл, аналитик один раз
        # отвечает неуверенно — это должно остановить прогон.
        wants_file = "Сохранить main.py" in joined
        if wants_file and tools and not self.calls.get("file"):
            self.calls["file"] = 1
            return CompletionResult(
                text="Сохраняю файл.",
                tool_calls=[ToolCall("c1", "write_file",
                                     {"path": "main.py", "content": "print('hello')\n"})],
                usage=Usage(250, 60))
        low = "Собрать требования" in joined and not self.calls.get("low")
        if low:
            self.calls["low"] = 1
        confidence = "0.3" if low else "0.9"
        return CompletionResult(
            text=f"Готово.\nCONFIDENCE: {confidence}\nRESULT:\nИтог работы по «{user[:60]}».",
            usage=Usage(400, 150))


def fake_build_provider(*_args, **_kwargs) -> LLMProvider:
    return FakeModel()


import core.orchestrator  # noqa: E402
import core.planner  # noqa: E402
import core.supervisor.supervisor  # noqa: E402
import ui.pages.agents_page  # noqa: E402
import ui.pages.keys_page  # noqa: E402

for module in (core.orchestrator, core.planner, core.supervisor.supervisor,
               ui.pages.agents_page, ui.pages.keys_page):
    module.build_provider = fake_build_provider

# ---------------------------------------------------------------------------
# Подмена модальных окон
# ---------------------------------------------------------------------------

FILLERS: dict[str, object] = {}
MESSAGES: list[str] = []


def _fake_exec(self) -> int:
    filler = FILLERS.pop(type(self).__name__, None)
    if filler is None:
        ERRORS.append(f"неожиданный диалог {type(self).__name__}")
        return QDialog.DialogCode.Rejected
    self.show()
    filler(self)
    self.layout().activate()
    self.grab().save(str(SHOTS / f"dialog_{type(self).__name__}.png"))
    self.hide()
    return QDialog.DialogCode.Accepted


QDialog.exec = _fake_exec
QMessageBox.warning = staticmethod(lambda _p, _t, text, *a, **k: MESSAGES.append(text))
QMessageBox.information = staticmethod(lambda _p, _t, text, *a, **k: MESSAGES.append(text))

import ui.widgets.common as common  # noqa: E402

_yes = lambda *_a, **_k: True  # noqa: E731
common.confirm = _yes
for name in ("workspaces_page", "keys_page", "agents_page", "task_page", "run_page"):
    setattr(sys.modules.get(f"ui.pages.{name}") or __import__(f"ui.pages.{name}",
            fromlist=["x"]), "confirm", _yes)


# ---------------------------------------------------------------------------
# Сценарий
# ---------------------------------------------------------------------------


def shot(widget, name: str) -> None:
    # processEvents() здесь нельзя: внутри корутины он повторно входит в луп
    # qasync и ломает чужие таски. Отрисовку дают паузы settle().
    widget.grab().save(str(SHOTS / f"{name}.png"))


async def settle(seconds: float = 0.2) -> None:
    await asyncio.sleep(seconds)


async def wait_for(predicate, timeout: float = 20.0) -> bool:
    loop = asyncio.get_event_loop()
    end = loop.time() + timeout
    while loop.time() < end:
        if predicate():
            return True
        await settle(0.05)
    return False


async def scenario(app: QApplication) -> None:
    from main import start_ui

    settings = AppSettings.load()
    db = Database()

    # Та же связка окон, что в приложении: вход → главное окно → выход → вход.
    windows = start_ui(db, settings)

    print("\n[1] Вход")
    login = windows["login"]
    login.resize(520, 640)
    await settle()
    shot(login, "01_signup")
    check("без профилей открыт экран регистрации", login.stack.currentIndex() == 1)

    login.su_username.setText("tester")
    login.su_password.setText("short")
    login.su_password2.setText("short")
    login._do_signup()
    check("короткий пароль отвергнут", "main" not in windows and login.su_error.isVisible())
    login.su_password.setText("password123")
    login.su_password2.setText("password123")
    login._do_signup()
    check("профиль создан", "main" in windows)

    print("\n[2] Главное окно")
    window = windows["main"]
    await settle(0.5)
    check("приложение не закрылось при переходе из окна входа",
          asyncio.get_event_loop().is_running() and window.isVisible())
    for i in range(window.stack.count()):
        window._select_page(i)
        await settle(0.05)
        shot(window, f"02_empty_{i:02d}")
    check("все страницы открываются без воркспейса", not ERRORS)

    print("\n[3] Воркспейс, ключ, агенты")
    window._select_page(0)

    def fill_ws(dlg):
        dlg.name.setText("Демо-проект")
        dlg.description.setPlainText("Проверка интерфейса")
    FILLERS["WorkspaceDialog"] = fill_ws
    window.page_workspaces._create()
    await settle()
    check("воркспейс создан и выбран", window.workspace_id is not None)
    shot(window, "03_workspaces")

    window._select_page(1)

    def fill_key(dlg):
        dlg.provider.setCurrentIndex(dlg.provider.findData("openai"))
        dlg.secret.setText("sk-test-123")
    FILLERS["KeyDialog"] = fill_key
    window.page_keys._create()
    await settle()
    keys = window.repos.keys.list()
    check("ключ сохранён", len(keys) == 1)
    for button in window.page_keys.findChildren(QPushButton):
        if button.text() == common.tr("common.test"):
            button.click()
    await settle(0.5)
    shot(window, "04_keys")
    check("проверка ключа закэшировала модели",
          window.repos.keys.get(keys[0].id).meta.get("models") == ["fake-mini", "fake-large"])

    window._select_page(2)
    for role, is_sup in (("analyst", False), ("developer", False), ("supervisor", True)):
        def fill_agent(dlg, role=role, is_sup=is_sup):
            idx = dlg.template.findData(role)
            if idx < 0:
                idx = 0
            dlg.template.setCurrentIndex(idx)
            dlg._load_models()
            dlg.model.setCurrentText("fake-mini")
            dlg.is_supervisor.setChecked(is_sup)
        FILLERS["AgentDialog"] = fill_agent
        window.page_agents._create()
        await settle(0.2)
    agents = window.repos.agents.list(window.workspace_id)
    check("три агента созданы", len(agents) == 3, ", ".join(a.name for a in agents))
    shot(window, "05_agents")

    print("\n[4] Задача")
    window._select_page(3)
    page = window.page_task
    page.title_edit.setText("Демо-задача")
    page.body_edit.setPlainText("Подготовить демо: требования и небольшой скрипт")
    page.token_limit.setText("100 000")
    page._autosplit()
    ok = await wait_for(lambda: page.btn_auto.isEnabled())
    subtasks = window.repos.tasks.subtasks(page.task.id)
    check("автоматическое разбиение", ok and len(subtasks) == 2,
          f"подзадач: {len(subtasks)}")
    check("исполнители назначены по ролям", all(s.agent_id for s in subtasks))

    def fill_sub(dlg):
        dlg.title.setText("Проверить итог")
        dlg.description.setPlainText("Свести результаты")
        dlg.assignee.setCurrentIndex(1)
    FILLERS["SubtaskDialog"] = fill_sub
    page._add_subtask()
    await settle()
    page._move(window.repos.tasks.subtasks(page.task.id)[-1].id, -1)
    await settle()
    shot(window, "06_task")
    check("подзадача добавлена вручную",
          len(window.repos.tasks.subtasks(page.task.id)) == 3)

    print("\n[5] Настройки воркспейса")
    window._select_page(9)
    sp = window.page_settings
    sp.hitl.setChecked(True)
    sp.hitl_threshold.setValue(0.5)
    idx = sp.sup_agent.findData(next(a.id for a in agents if a.is_supervisor))
    sp.sup_agent.setCurrentIndex(idx)
    await settle()
    ws = window.repos.workspaces.get(window.workspace_id)
    check("human-in-the-loop включён", ws.settings.get("human_in_the_loop") is True)
    supervisor_id = next(a.id for a in agents if a.is_supervisor)
    check("список агентов в настройках актуален", idx >= 0, f"индекс: {idx}")
    check("супервайзер выбран", ws.settings.get("supervisor_agent_id") == supervisor_id)
    shot(window, "07_settings")

    print("\n[6] Прогон")
    window.page_task._request_run()
    await settle()
    check("кнопка «Запустить» переводит на страницу выполнения",
          window.stack.currentWidget() is window.page_run)
    window.page_run.btn_start.click()
    run = window.page_run
    paused = await wait_for(lambda: run.approvals.isVisible(), 20)
    await settle(0.3)
    shot(window, "08_run_paused")
    confidences = [r.confidence for r in window.repos.reports.list_reports(window.workspace_id)]
    check("появилась панель решения", paused, f"уверенность в отчётах: {confidences}")

    window._select_page(6)
    await settle(1.3)
    shot(window, "09_dashboard_live")
    window._select_page(4)

    approve = DECISION_TITLES[Decision.APPROVE]
    for _ in range(10):
        buttons = [b for b in run.approvals.findChildren(QPushButton)
                   if b.text() == approve and b.isEnabled() and b.isVisible()]
        if not buttons:
            if not window.orchestrator.state.running:
                break
            await settle(0.2)
            continue
        buttons[0].click()
        await settle(0.3)
    finished = await wait_for(lambda: not window.orchestrator.state.running, 30)
    await settle(0.5)
    shot(window, "10_run_done")
    statuses = [s.status for s in window.repos.tasks.subtasks(page.task.id)]
    check("прогон завершён", finished, f"статусы: {statuses}")
    check("все подзадачи выполнены", all(s == "done" for s in statuses))
    check("разработчик записал файл инструментом write_file",
          (PATHS.workspace_dir(window.workspace_id) / "main.py").exists())
    check("кнопки вернулись в исходное состояние",
          run.btn_start.isEnabled() and not run.btn_stop.isEnabled())

    print("\n[7] Супервайзер, дашборд, бюджеты")
    window._select_page(5)
    for i in range(window.page_supervisor.tabs.count()):
        window.page_supervisor.tabs.setCurrentIndex(i)
        await settle(0.05)
        shot(window, f"11_supervisor_{i}")
    check("история решений не пуста",
          bool(window.repos.approvals.history(window.workspace_id)))

    window._select_page(6)
    await settle(1.2)
    dash = window.page_dashboard
    shot(window, "12_dashboard")
    check("график расходов получил точки", len(dash.cost_chart._points) >= 2,
          f"точек: {len(dash.cost_chart._points)}")
    check("распределение по агентам заполнено", len(dash.agent_chart._bars) >= 1)

    window._select_page(7)
    await settle()
    rows = [w for w in window.page_budget.findChildren(
        sys.modules["ui.pages.budget_page"].LimitRow)]
    check("бюджеты отображаются по уровням", len(rows) >= 3, f"строк: {len(rows)}")
    if rows:
        rows[0].tokens_edit.setText("5000")
        rows[0].tokens_edit.editingFinished.emit()
        await settle()
    shot(window, "13_budget")

    print("\n[8] Экспорт")
    window._select_page(8)
    await settle()
    ep = window.page_export
    auto_fmt = ep.format_box.currentData()
    check("формат определён автоматически", auto_fmt == "zip", f"формат: {auto_fmt}")
    shot(window, "14_export")
    for fmt in ("markdown", "docx", "pdf", "zip"):
        ep.format_box.setCurrentIndex(ep.format_box.findData(fmt))
        ep.opt_reports.setChecked(True)
        ep.opt_summaries.setChecked(True)
        ep.opt_decisions.setChecked(True)
        before = len(MESSAGES)
        ep._export()
        path = Path(ep.path_edit.text())
        check(f"экспорт {fmt}", path.exists() and path.stat().st_size > 0
              and len(MESSAGES) == before,
              MESSAGES[-1] if len(MESSAGES) > before else path.name)

    print("\n[9] Тема и язык")
    window._select_page(9)
    sp.theme_box.setCurrentIndex(1)
    await settle()
    for i in (6, 4, 9):
        window._select_page(i)
        await settle(0.1)
        shot(window, f"15_light_{i:02d}")
    sp.theme_box.setCurrentIndex(0)
    sp.lang_box.setCurrentIndex(sp.lang_box.findData("en"))
    await settle(0.5)
    rebuilt = windows["main"]
    nav = rebuilt.nav_group.button(0).text() if rebuilt is not window else ""
    check("смена языка пересобрала окно", rebuilt is not window and rebuilt.isVisible()
          and not shiboken6.isValid(window) and nav == "Workspaces",
          f"кнопка навигации: {nav!r}")
    check("после пересборки открыта та же страница",
          rebuilt.stack.currentWidget() is rebuilt.page_settings)
    shot(rebuilt, "16_main_en")

    rebuilt._logout()
    await settle(0.5)
    login2 = windows["login"]
    check("после выхода снова открыто окно входа",
          login2 is not login and login2.isVisible()
          and login2.stack.currentIndex() == 0)
    shot(login2, "17_login_en")
    login2.password.setText("password123")
    login2._do_signin()
    await settle(0.5)
    check("повторный вход по паролю",
          windows["main"] is not rebuilt and windows["main"].isVisible())
    shot(windows["main"], "18_main_after_login")
    set_language("ru")


def main() -> int:
    settings = AppSettings.load()
    set_language(settings.language)
    PATHS.ensure()
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet(settings.theme))
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        try:
            loop.run_until_complete(asyncio.wait_for(scenario(app), 120))
        except Exception:  # noqa: BLE001
            ERRORS.append(traceback.format_exc())

    print(f"\nСкриншоты: {SHOTS}")
    if ERRORS:
        print(f"\nОШИБКИ ({len(ERRORS)}):")
        for text in dict.fromkeys(ERRORS):
            print("-" * 66)
            print(text.rstrip())
    print("\n" + "=" * 66)
    total = len(_passed) + len(_failed)
    if _failed or ERRORS:
        print(f"ПРОВАЛЕНО: {len(_failed)} из {total}, ошибок в слотах: {len(ERRORS)}")
        for name in _failed:
            print(f"  - {name}")
        return 1
    print(f"ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ: {total} из {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

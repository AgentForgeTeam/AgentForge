"""Смоук-тесты ядра: все девять этапов MVP без сети и без GUI.

Запуск::

    python tests/smoke.py

Модели подменяются фейковыми провайдерами, поэтому тесты не ходят в интернет,
не тратят токены и выполняются за секунды. Проверяется именно логика ядра:
шифрование, изоляция агентов, конвейер выполнения, супервайзер, паузы,
экспорт и бюджеты. Интерфейс сюда не входит - его надо смотреть глазами.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Изолированный каталог данных, чтобы не трогать реальный профиль.
_TEMP_HOME = Path(tempfile.mkdtemp(prefix="aiorc_smoke_"))
os.environ["AGENTFORGE_HOME"] = str(_TEMP_HOME)

from app.config import PATHS  # noqa: E402
from core.budget import load_states  # noqa: E402
from core.events import EventBus, EventType  # noqa: E402
from core.export.bundle import ExportOptions, collect, detect_format  # noqa: E402
from core.export.exporters import export, suggest_filename  # noqa: E402
from core.hitl import Decision  # noqa: E402
from core.orchestrator import Orchestrator  # noqa: E402

_passed: list[str] = []
_failed: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    """Печатает результат одной проверки и копит статистику."""
    mark = "OK  " if condition else "FAIL"
    print(f"  [{mark}] {name}" + (f" - {detail}" if detail else ""))
    (_passed if condition else _failed).append(name)


# Подменные провайдеры и каркас сценариев вынесены в tests/fakes.py:
# их же используют pytest-тесты.
from tests.fakes import (  # noqa: E402
    SupervisorProvider,
    Worker,
    build_project,
    drive,
    patch_supervisor,
)


# ---------------------------------------------------------------------------
# Сценарии
# ---------------------------------------------------------------------------


def test_storage_and_crypto() -> None:
    print("\n[1-3] Хранилище, шифрование ключей, задачи")
    repos, workspace, task, agents, key = build_project()

    check("профиль создан и пароль проверяется",
          repos.users.authenticate(repos.session.username, "password123") is not None)
    check("неверный пароль отвергается",
          repos.users.authenticate(repos.session.username, "wrong") is None)

    row = repos.db.query_one("SELECT secret_blob FROM api_keys WHERE id = ?", (key.id,))
    check("секрет не лежит в БД открытым текстом",
          b"sk-secret-value" not in row["secret_blob"])
    check("секрет расшифровывается", repos.keys.reveal(key.id) == "sk-secret-value")

    repos.users.change_password(repos.session, "password123", "newpassword456")
    check("после смены пароля ключ читается",
          repos.keys.reveal(key.id) == "sk-secret-value",
          "перешифровка выполнена")

    check("подзадачи привязаны к агентам",
          all(s.agent_id for s in repos.tasks.subtasks(task.id)))


async def test_pipeline() -> None:
    print("\n[4] Конвейер: ReAct, инструменты, зависимости, изоляция")
    repos, workspace, task, agents, _ = build_project(subtask_count=2)
    subtasks = repos.tasks.subtasks(task.id)
    repos.tasks.update_subtask(subtasks[1].id, depends_on=str(subtasks[0].id))

    bus = EventBus()
    seen: list[tuple] = []
    bus.subscribe(lambda e: seen.append((e.type, e.subtask_id)))

    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, bus)
    workers = {a.id: Worker(a.name, use_tool=(i == 0))
               for i, a in enumerate(agents)}
    orch._provider_for = lambda agent: workers.get(agent.id, Worker(agent.name))

    state = await drive(orch, workspace.id, task.id)

    check("обе подзадачи выполнены", state.finished == 2 and state.failed == 0,
          f"finished={state.finished}, failed={state.failed}")
    check("результаты сохранены",
          all(s.result.strip() for s in repos.tasks.subtasks(task.id)))
    check("инструмент code_exec отработал", workers[agents[0].id].calls >= 2,
          f"вызовов модели: {workers[agents[0].id].calls}")

    started = [s for t, s in seen if t is EventType.SUBTASK_STARTED]
    finished = [s for t, s in seen if t is EventType.SUBTASK_FINISHED]
    check("зависимость соблюдена",
          finished and started.index(subtasks[1].id) > 0
          and subtasks[0].id in finished[:started.index(subtasks[1].id) + 1])

    history_one = repos.messages.history(agents[0].id)
    history_two = repos.messages.history(agents[1].id)
    check("истории агентов изолированы",
          bool(history_one) and bool(history_two)
          and all(m["agent_id"] == agents[1].id for m in history_two),
          f"{len(history_one)} и {len(history_two)} сообщений")
    check("отчёты созданы", len(repos.reports.list_reports(workspace.id)) == 2)


async def test_supervisor() -> None:
    print("\n[5] Супервайзер: доработка, анонимизация, конфликты")
    repos, workspace, task, agents, _ = build_project(subtask_count=2)
    repos.agents.update(agents[0].id, name="Аналитик Пётр")
    repos.agents.update(agents[1].id, name="Критик Анна")

    provider = SupervisorProvider(
        verdicts=['{"verdict":"rework","notes":"Нет источников.",'
                  '"issues":[{"kind":"factual_error","severity":"high",'
                  '"description":"Цифры без источника"}]}'],
        conflicts='{"conflicts":[{"description":"Оценки расходятся",'
                  '"severity":"high","labels":[],"auto_resolvable":false,'
                  '"resolution":""},'
                  '{"description":"Мелкое расхождение в дате",'
                  '"severity":"low","labels":[],"auto_resolvable":true,'
                  '"resolution":"Верна более свежая дата"}]}',
    )
    patch_supervisor(provider)
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: Worker(agent.name)

    state = await drive(orch, workspace.id, task.id)

    check("доработка назначена и выполнена", state.reworks == 1,
          f"reworks={state.reworks}")
    check("после доработки результат принят",
          all(s.status == "done" for s in repos.tasks.subtasks(task.id)))

    summaries = repos.reports.list_summaries(workspace.id)
    leaked = [s for s in summaries if "Пётр" in s.content or "Анна" in s.content]
    check("имена агентов не утекают в сводки", not leaked and bool(summaries),
          f"сводок: {len(summaries)}")

    incidents = repos.incidents.list(workspace.id)
    auto = [i for i in incidents if i.status == "auto_resolved"]
    escalated = [i for i in incidents if i.status == "escalated"]
    closed = [i for i in incidents if i.status == "resolved"]
    check("конфликт разрешён автоматически", len(auto) == 1)
    check("неразрешимый конфликт эскалирован", len(escalated) == 1)
    check("замечание закрыто после доработки", len(closed) >= 1)


async def test_hitl() -> None:
    print("\n[7] Human-in-the-loop: пауза, доработка, остановка")
    repos, workspace, task, agents, _ = build_project(
        subtask_count=1,
        settings={"human_in_the_loop": True, "hitl_confidence_threshold": 0.9,
                  "max_rework_rounds": 0},
    )
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, EventBus())
    worker = Worker("Агент", confidence="0.4")
    orch._provider_for = lambda agent: worker

    await drive(orch, workspace.id, task.id,
               answers=[(Decision.REWORK, "Добавь источники"),
                        (Decision.APPROVE, "теперь годится")])
    subtask = repos.tasks.subtasks(task.id)[0]
    check("пауза по низкой уверенности сработала", worker.calls == 2,
          f"вызовов модели: {worker.calls}")
    check("решение пользователя дало круг доработки", subtask.rework_count == 1)
    check("после подтверждения подзадача закрыта", subtask.status == "done")
    check("история решений записана",
          len(repos.approvals.history(workspace.id)) == 2)

    # Защита от бесконечного цикла: человек возвращает работу снова и снова.
    repos2, ws2, task2, agents2, _ = build_project(
        subtask_count=1,
        settings={"human_in_the_loop": True, "hitl_confidence_threshold": 0.9,
                  "max_rework_rounds": 0},
    )
    patch_supervisor(SupervisorProvider())
    orch2 = Orchestrator(repos2, EventBus())
    stubborn = Worker("Агент", confidence="0.4")
    orch2._provider_for = lambda agent: stubborn
    await drive(orch2, ws2.id, task2.id, fallback=Decision.REWORK)
    check("потолок доработок человека держится", stubborn.calls == 4,
          f"вызовов модели: {stubborn.calls} (1 + 3 круга)")

    # Остановка прогона решением пользователя.
    repos3, ws3, task3, agents3, _ = build_project(
        subtask_count=3,
        settings={"human_in_the_loop": True, "hitl_confidence_threshold": 0.9,
                  "max_rework_rounds": 0},
    )
    patch_supervisor(SupervisorProvider())
    orch3 = Orchestrator(repos3, EventBus())
    orch3._provider_for = lambda agent: Worker(agent.name, confidence="0.4")
    state3 = await drive(orch3, ws3.id, task3.id, fallback=Decision.ABORT)
    statuses = [s.status for s in repos3.tasks.subtasks(task3.id)]
    check("остановка прогона работает",
          state3.finished == 0 and statuses.count("idle") >= 1,
          f"статусы: {statuses}")


async def test_budget() -> None:
    print("\n[9] Бюджеты: блокировка и алерты")
    repos, workspace, task, agents, _ = build_project(subtask_count=3, agent_count=1)
    subtasks = repos.tasks.subtasks(task.id)
    for previous, current in zip(subtasks, subtasks[1:]):
        repos.tasks.update_subtask(current.id, depends_on=str(previous.id))

    repos.budgets.upsert("agent", agents[0].id, 400, None, 0.5)

    events: list[str] = []
    bus = EventBus()
    bus.subscribe(lambda e: events.append(e.type.value)
                  if e.type in (EventType.BUDGET_ALERT, EventType.BUDGET_EXCEEDED)
                  else None)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, bus)
    worker = Worker("Агент", tokens=(300, 100))
    orch._provider_for = lambda agent: worker

    await drive(orch, workspace.id, task.id)
    statuses = [s.status for s in repos.tasks.subtasks(task.id)]

    check("лимит остановил работу", worker.calls == 1,
          f"вызовов модели: {worker.calls}")
    check("заблокированные подзадачи помечены ошибкой",
          statuses.count("error") == 2, f"статусы: {statuses}")
    check("событие о превышении опубликовано", "budget_exceeded" in events)

    states = load_states(repos, workspace.id)
    scopes = {s.scope for s in states}
    check("бюджет считается на трёх уровнях",
          {"workspace", "task", "agent"} <= scopes, f"уровни: {sorted(scopes)}")


async def test_export() -> None:
    print("\n[8] Экспорт результата")
    repos, workspace, task, agents, _ = build_project(subtask_count=2)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: Worker(agent.name)
    await drive(orch, workspace.id, task.id)

    bundle = collect(repos, workspace.id)
    fmt, reason = detect_format(bundle)
    check("формат определяется автоматически", bool(fmt) and bool(reason),
          f"{fmt}: {reason}")

    out = _TEMP_HOME / "exports"
    out.mkdir(parents=True, exist_ok=True)
    options = ExportOptions(include_reports=True, include_summaries=True)

    result = export(bundle, options, "markdown", out / suggest_filename(bundle, "markdown"))
    body = result.path.read_text("utf-8")
    check("markdown собран", result.size > 0 and "# " in body, f"{result.size} байт")
    check("результаты подзадач попали в документ", "Результат" in body)

    for optional, module in (("docx", "docx"), ("pdf", "reportlab")):
        try:
            __import__(module)
        except ImportError:
            print(f"  [SKIP] {optional} - пакет {module} не установлен")
            continue
        result = export(bundle, options, optional,
                        out / suggest_filename(bundle, optional))
        check(f"{optional} собран", result.size > 0, f"{result.size} байт")

    # ZIP: в рабочем каталоге появляются файлы проекта
    workspace_dir = PATHS.workspace_dir(workspace.id)
    (workspace_dir / "src").mkdir(parents=True, exist_ok=True)
    (workspace_dir / "src" / "main.py").write_text("print('привет')\n", "utf-8")
    (workspace_dir / ".sandbox").mkdir(exist_ok=True)
    (workspace_dir / ".sandbox" / "junk.py").write_text("мусор", "utf-8")

    bundle = collect(repos, workspace.id)
    fmt, _ = detect_format(bundle)
    check("появление кода переключает формат на архив", fmt == "zip", fmt)

    result = export(bundle, options, "zip", out / suggest_filename(bundle, "zip"))
    import zipfile

    with zipfile.ZipFile(result.path) as archive:
        names = archive.namelist()
    check("архив содержит отчёт и манифест",
          "RESULT.md" in names and "manifest.json" in names)
    check("файлы проекта вложены", "files/src/main.py" in names)
    check("служебные каталоги исключены",
          not any(".sandbox" in name for name in names))


# ---------------------------------------------------------------------------


async def main() -> int:
    print("=" * 66)
    print("Смоук-тесты Agent Forge (без сети, без GUI)")
    print(f"Временный каталог данных: {_TEMP_HOME}")
    print("=" * 66)

    test_storage_and_crypto()
    await test_pipeline()
    await test_supervisor()
    await test_export()
    await test_hitl()
    await test_budget()

    print("\n" + "=" * 66)
    total = len(_passed) + len(_failed)
    if _failed:
        print(f"ПРОВАЛЕНО {len(_failed)} из {total}:")
        for name in _failed:
            print(f"  · {name}")
        return 1
    print(f"ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ: {total} из {total}")
    return 0


if __name__ == "__main__":
    code = 0
    try:
        code = asyncio.run(main())
    finally:
        shutil.rmtree(_TEMP_HOME, ignore_errors=True)
    sys.exit(code)

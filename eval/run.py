"""Прогон набора задач через Agent Forge и проверка ответов.

Две архитектуры на одном наборе:

* ``single`` - один агент получает задачу целиком, супервайзера нет;
* ``team`` - планировщик разбивает задачу на подзадачи с зависимостями,
  их выполняют агенты разных ролей, каждый отчёт проверяет супервайзер.

Ядро работает так же, как в приложении (оркестратор, инструменты, бюджет),
только без окна и в отдельном временном каталоге данных. Ключ модели берётся
из переменной окружения и нигде не сохраняется::

    set GEMINI_API_KEY=...
    python -m eval.run --arch single team --out eval/results/kp2
    python -m eval.report eval/results/kp2

Прогон можно прервать и запустить снова: готовые задачи пропускаются.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import secrets
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    provider: str = "gemini"
    agent_model: str = "gemini-3.5-flash-lite"
    supervisor_model: str = "gemini-3.1-flash-lite"
    judge_model: str = "gemini-3.1-flash-lite-preview"
    max_steps: int = 6
    max_tokens: int = 4096
    token_limit: int = 300_000
    task_timeout: int = 900
    rework_rounds: int = 1
    parallel: int = 3
    archs: list[str] = field(default_factory=lambda: ["single", "team"])


SINGLE_ROLE = {"research": "researcher", "math": "analyst", "code": "developer"}
TEAM = [("Исследователь", "researcher", ["web_search"]),
        ("Аналитик", "analyst", ["web_search", "code_exec"]),
        ("Разработчик", "developer", ["code_exec"]),
        ("Критик", "critic", ["web_search"])]
TOOLS_BY_KIND = {"research": ["web_search"], "math": ["code_exec"], "code": ["code_exec"]}
# так ядро сообщает, что у модели кончилась квота (providers/retry.py)
QUOTA_MARK = "Квота модели исчерпана"


class Harness:
    """Профиль, ключ и воркспейсы замера во временном каталоге данных."""

    def __init__(self, cfg: Config, api_key: str) -> None:
        from storage.db import Database
        from storage.repositories import Repos, UserRepo

        self.cfg = cfg
        db = Database()
        session = UserRepo(db).create("eval", secrets.token_urlsafe(16))
        self.repos = Repos(db, session)
        self.user_id = session.user_id
        self.key = self.repos.keys.create("Замер", cfg.provider, api_key, "")

    def _prompt(self, role: str) -> str:
        from core.agents.roles import COMMON_RULES, by_key

        return by_key(role).prompt + "\n\n" + COMMON_RULES.strip()

    def _agent(self, ws_id: int, name: str, role: str, tools: list[str],
               model: str | None = None, supervisor: bool = False):
        params = {"temperature": 0.2, "max_tokens": self.cfg.max_tokens, "tools": tools}
        return self.repos.agents.create(
            ws_id, name, role, self._prompt(role), self.key.id, self.cfg.provider,
            model or self.cfg.agent_model, params, is_supervisor=supervisor)

    def workspace(self, task, arch: str):
        """Воркспейс под одну задачу: своя история агентов, свои сводки."""
        from app.config import DEFAULT_WORKSPACE_SETTINGS

        settings = {**DEFAULT_WORKSPACE_SETTINGS,
                    "human_in_the_loop": False, "summary_interval_minutes": 0,
                    "summary_on_event": False, "agent_max_steps": self.cfg.max_steps,
                    "max_rework_rounds": self.cfg.rework_rounds,
                    "max_parallel_agents": self.cfg.parallel,
                    "tools_enabled": ["web_search", "code_exec"],
                    "sandbox_backend": "subprocess", "supervisor_mode": "api",
                    "supervisor_agent_id": None}
        ws = self.repos.workspaces.create(self.user_id, f"{arch}: {task.id}", "", settings)
        if arch == "single":
            role = SINGLE_ROLE[task.kind]
            agent = self._agent(ws.id, "Исполнитель", role, TOOLS_BY_KIND[task.kind])
            return ws, [agent]
        agents = [self._agent(ws.id, name, role, tools) for name, role, tools in TEAM]
        sup = self._agent(ws.id, "Супервайзер", "supervisor", [],
                          model=self.cfg.supervisor_model, supervisor=True)
        self.repos.workspaces.update(ws.id, settings={**settings, "supervisor_agent_id": sup.id})
        return ws, agents


def final_answer(subtasks) -> str:
    """Итог задачи: результат последней подзадачи, от которой никто не зависит."""
    referenced = set()
    for s in subtasks:
        referenced |= {int(t) for t in (s.depends_on or "").split(",") if t.strip().isdigit()}
    with_result = [s for s in subtasks if (s.result or "").strip()]
    sinks = [s for s in with_result if s.id not in referenced]
    chosen = (sinks or with_result)
    return chosen[-1].result if chosen else ""


async def run_one(harness: Harness, task, arch: str, judge_provider) -> dict:
    from core.events import EventBus
    from core.orchestrator import Orchestrator
    from core.planner import create_planned_subtasks, plan_subtasks
    from core.verify.links import check_links
    from eval import scoring

    cfg, repos = harness.cfg, harness.repos
    ws, agents = harness.workspace(task, arch)
    prompt = task.prompt()
    record = repos.tasks.create(ws.id, task.title, prompt, "markdown", cfg.token_limit)
    started = time.monotonic()
    row: dict = {"task_id": task.id, "source": task.source, "kind": task.kind, "arch": arch,
                 "gold": task.answer if task.check != "tests" else "", "error": ""}

    try:
        if arch == "single":
            repos.tasks.add_subtask(record.id, "Решить задачу целиком",
                                    "Выполни общую задачу проекта полностью и дай итог "
                                    "в требуемом формате.", agents[0].id)
        else:
            planned = await plan_subtasks(repos, ws.id, record.title, prompt)
            ids = create_planned_subtasks(repos, ws.id, record.id, planned)
            fallback = next(a for a in agents if a.role == SINGLE_ROLE[task.kind])
            for sid in ids:
                if repos.tasks.get_subtask(sid).agent_id is None:
                    repos.tasks.update_subtask(sid, agent_id=fallback.id)
        bus = EventBus()
        # Подзадача могла упасть из-за квоты модели, а не из-за ответа: такую
        # задачу замер не засчитывает, а перезапускает позже.
        bus.subscribe(lambda event: QUOTA_MARK in (event.message or "")
                      and row.setdefault("quota", event.message[:300]))
        orchestrator = Orchestrator(repos, bus)
        try:
            await asyncio.wait_for(orchestrator.run_task(ws.id, record.id), cfg.task_timeout)
        except asyncio.TimeoutError:
            orchestrator.stop()
            row["error"] = f"прогон не уложился в {cfg.task_timeout} с"
    except Exception as exc:  # noqa: BLE001 - ошибка задачи не должна ронять весь замер
        row["error"] = f"{type(exc).__name__}: {exc}"[:500]
    row["seconds"] = round(time.monotonic() - started, 1)

    subtasks = repos.tasks.subtasks(record.id)
    answer = final_answer(subtasks)
    row["answer"] = answer[:6000]
    row["plan"] = [{"title": s.title, "status": s.status, "depends_on": s.depends_on,
                    "reworks": s.rework_count} for s in subtasks]
    tokens, cost = repos.budgets.task_totals(record.id)
    usage = repos.budgets.usage_by_agent(ws.id)
    supervisor_ids = {a.id for a in repos.agents.list(ws.id) if a.is_supervisor}
    row.update(tokens=tokens, cost=round(cost, 6),
               supervisor_tokens=sum(t for aid, t, _ in usage if aid is None),
               planner_tokens=sum(t for aid, t, _ in usage if aid in supervisor_ids),
               limit_exceeded=tokens > cfg.token_limit)

    try:
        if task.check == "number":
            score = scoring.check_number(answer, task.answer)
        elif task.check == "tests":
            score = await scoring.check_tests(answer, task.entry_point, task.tests)
        else:
            score, judge_usage = await scoring.judge(judge_provider, cfg.judge_model,
                                                     task.question, task.answer, answer)
            row["judge_tokens"] = judge_usage.total
            row["contains_gold"] = scoring.contains_gold(answer, task.answer)
        row.update(correct=score.correct, detail=score.detail, extracted=score.extracted[:500])
        if task.kind == "research":
            row["links"] = (await check_links(answer)).as_dict()
    except Exception as exc:  # noqa: BLE001 - сбой проверки повторяется через --retry-errors
        row.update(correct=False, detail="", extracted="",
                   error=row["error"] or f"проверка не выполнена: {type(exc).__name__}: {exc}"[:500])
    return row


def plain_dashes(text: str) -> str:
    """Модели любят длинные тире; в файлах проекта везде обычный дефис."""
    return text.replace("\u2014", "-").replace("\u2013", "-")


def done_keys(path: Path, retry_errors: bool) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    if not path.exists():
        return keys
    for line in path.read_text("utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            if retry_errors and row.get("error"):
                continue
            keys.add((row["task_id"], row["arch"]))
    return keys


async def run_all(cfg: Config, out: Path, only: list[str] | None, limit: int | None,
                  retry_errors: bool, api_key: str) -> None:
    from eval.tasks import load_tasks
    from providers.factory import build_provider
    from utils.logging_setup import setup_logging

    setup_logging()
    tasks = load_tasks(only=only, limit=limit)
    out.mkdir(parents=True, exist_ok=True)
    results = out / "results.jsonl"
    (out / "config.json").write_text(json.dumps(asdict(cfg), ensure_ascii=False, indent=2),
                                     "utf-8", newline="\n")
    skip = done_keys(results, retry_errors)
    if retry_errors and results.exists():
        kept = [line for line in results.read_text("utf-8").splitlines()
                if line.strip() and not json.loads(line).get("error")]
        results.write_text("".join(f"{line}\n" for line in kept), "utf-8", newline="\n")

    harness = Harness(cfg, api_key)
    judge_provider = build_provider(cfg.provider, api_key, "", timeout=180)
    total = len(tasks) * len(cfg.archs)
    step = 0
    try:
        for task in tasks:
            for arch in cfg.archs:
                step += 1
                if (task.id, arch) in skip:
                    continue
                print(f"[{step}/{total}] {arch:6} {task.id} ...", flush=True)
                row = await run_one(harness, task, arch, judge_provider)
                if row.get("quota") or QUOTA_MARK in row.get("error", ""):
                    print(f"Квота модели исчерпана, замер остановлен. Запустите ту же команду "
                          f"позже, готовые задачи пропустятся.\n{row.get('quota') or row['error']}",
                          flush=True)
                    return
                mark = "верно" if row.get("correct") else "неверно"
                print(f"    {mark}: {row.get('detail', '')[:100]} | {row['tokens']} ток., "
                      f"{row['seconds']} с {('| ' + row['error'][:120]) if row['error'] else ''}",
                      flush=True)
                with results.open("a", encoding="utf-8", newline="\n") as f:
                    f.write(plain_dashes(json.dumps(row, ensure_ascii=False)) + "\n")
    finally:
        await judge_provider.aclose()


def main() -> int:
    parser = argparse.ArgumentParser(description="Замер качества Agent Forge на наборе задач")
    parser.add_argument("--out", type=Path, default=ROOT / "eval" / "results" / "latest")
    parser.add_argument("--arch", nargs="+", choices=["single", "team"], default=["single", "team"])
    parser.add_argument("--only", nargs="*", help="источники (frames, gsm8k, humaneval) или id задач")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--key-env", default="GEMINI_API_KEY",
                        help="переменная окружения с ключом провайдера")
    parser.add_argument("--provider", default=Config.provider)
    parser.add_argument("--agent-model", default=Config.agent_model)
    parser.add_argument("--supervisor-model", default=Config.supervisor_model)
    parser.add_argument("--judge-model", default=Config.judge_model)
    parser.add_argument("--retry-errors", action="store_true",
                        help="перезапустить задачи, которые закончились ошибкой")
    args = parser.parse_args()

    api_key = os.environ.get(args.key_env, "").strip()
    if not api_key:
        print(f"Нет ключа: задайте переменную окружения {args.key_env}", file=sys.stderr)
        return 1
    cfg = Config(provider=args.provider, agent_model=args.agent_model,
                 supervisor_model=args.supervisor_model, judge_model=args.judge_model,
                 archs=args.arch)
    # Отдельный каталог данных: замер не трогает профиль пользователя.
    # Задаётся до импорта модулей приложения - они читают его при импорте.
    os.environ["AGENTFORGE_HOME"] = tempfile.mkdtemp(prefix="af_eval_")
    sys.path.insert(0, str(ROOT))
    asyncio.run(run_all(cfg, args.out, args.only, args.limit, args.retry_errors, api_key))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

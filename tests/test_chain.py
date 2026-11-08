"""Место подзадачи в цепочке: пометка для агента и супервайзера."""

from __future__ import annotations

from core.chain import chain_note
from core.events import EventBus
from core.orchestrator import Orchestrator
from storage.models import Subtask
from tests.fakes import SupervisorProvider, Worker, build_project, drive, patch_supervisor


def _sub(sid: int, title: str, depends_on: str = "") -> Subtask:
    return Subtask(id=sid, task_id=1, title=title, description="", agent_id=None,
                   status="pending", order_index=sid, depends_on=depends_on, result="",
                   rework_count=0, tokens_in=0, tokens_out=0, cost_usd=0.0,
                   created_at="", updated_at="")


def test_note_depends_on_place_in_chain():
    boxes, cost, alone = _sub(1, "Коробки"), _sub(2, "Стоимость", "1"), _sub(3, "Отдельно")
    chain = [boxes, cost, alone]

    first = chain_note(chain, boxes, for_supervisor=True)
    assert "промежуточный" in first and "«Стоимость»" in first and "ANSWER" in first
    last = chain_note(chain, cost, for_supervisor=True)
    assert "итоговый" in last and "«Коробки»" in last
    assert "промежуточный" in chain_note(chain, boxes, for_supervisor=False)
    # подзадача вне цепочки: пометки нет, тексты для модели прежние
    assert chain_note(chain, alone, for_supervisor=True) == ""
    assert chain_note(chain, alone, for_supervisor=False) == ""


class RecordingSupervisor(SupervisorProvider):
    def __init__(self) -> None:
        super().__init__()
        self.prompts: list[str] = []

    async def complete(self, model, messages, **kwargs):
        if "ПРОВЕРЯЕМАЯ ПОДЗАДАЧА" in messages[1].content:
            self.prompts.append(messages[1].content)
        return await super().complete(model, messages, **kwargs)


class RecordingWorker(Worker):
    def __init__(self) -> None:
        super().__init__("A")
        self.briefings: list[str] = []

    async def complete(self, model, messages, **kwargs):
        self.briefings.append(next(m.content for m in messages if m.role == "user"))
        return await super().complete(model, messages, **kwargs)


async def _run(subtask_count: int, chained: bool):
    repos, ws, task, _, _ = build_project(subtask_count=subtask_count, agent_count=1)
    subs = repos.tasks.subtasks(task.id)
    if chained:
        repos.tasks.update_subtask(subs[1].id, depends_on=str(subs[0].id))
    supervisor, worker = RecordingSupervisor(), RecordingWorker()
    patch_supervisor(supervisor)
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: worker
    await drive(orch, ws.id, task.id)
    return supervisor, worker


async def test_agent_and_supervisor_see_the_stage():
    supervisor, worker = await _run(2, chained=True)
    first = next(p for p in supervisor.prompts if "Подзадача 1" in p)
    second = next(p for p in supervisor.prompts if "Подзадача 2\n" in p)
    assert "промежуточный этап" in first and "«Подзадача 2»" in first
    assert "итоговый этап" in second
    assert any("МЕСТО В ЦЕПОЧКЕ: это промежуточный этап" in b for b in worker.briefings)
    assert any("МЕСТО В ЦЕПОЧКЕ: это итоговый этап" in b for b in worker.briefings)


async def test_single_subtask_prompts_are_unchanged():
    supervisor, worker = await _run(1, chained=False)
    assert supervisor.prompts and worker.briefings
    assert not any("МЕСТО В ЦЕПОЧКЕ" in p for p in supervisor.prompts + worker.briefings)

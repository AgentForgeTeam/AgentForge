"""Оценка качества: набор задач, проверка ответов, сводка метрик."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from eval import scoring
from eval.report import summarize, wilson
from eval.run import final_answer
from eval.tasks import load_tasks
from providers.base import CompletionResult, LLMProvider, Usage


def test_dataset_has_forty_tasks_from_three_benchmarks():
    tasks = load_tasks()
    assert len(tasks) == 40
    by_source = {}
    for t in tasks:
        by_source[t.source] = by_source.get(t.source, 0) + 1
    assert by_source == {"frames": 14, "gsm8k": 13, "humaneval": 13}
    assert len({t.id for t in tasks}) == 40
    for t in tasks:
        assert t.source_url.startswith("https://") and t.license
        assert t.answer
        if t.kind == "code":
            assert t.entry_point and "def check" in t.tests


def test_prompt_never_contains_the_reference_answer():
    for t in load_tasks():
        if t.kind == "code":
            assert t.tests not in t.prompt()
        elif len(t.answer) > 3:
            assert t.answer not in t.prompt(), t.id


@pytest.mark.parametrize("text, gold, ok", [
    ("Решение...\nANSWER: 1,490", "1490", True),
    ("**ANSWER:** $64.00", "64", True),
    ("ANSWER: 16 (а не 12)", "12", False),     # в строке ANSWER берётся первое число
    ("Итого 8 батончиков", "8", True),          # без строки ANSWER берётся последнее число
    ("не знаю", "5", False),
])
def test_number_check(text, gold, ok):
    assert scoring.check_number(text, gold).correct is ok


def test_code_is_taken_from_the_block_with_the_function():
    text = ("Пример вызова:\n```python\nprint(add(1, 2))\n```\n"
            "Итог:\n```python\ndef add(x, y):\n    return x + y\n```")
    assert "return x + y" in scoring.extract_code(text, "add")


async def test_humaneval_tests_pass_for_reference_and_fail_for_wrong_code():
    task = next(t for t in load_tasks() if t.kind == "code")
    reference = f"```python\n{task.question}{task.answer}\n```"
    assert (await scoring.check_tests(reference, task.entry_point, task.tests)).correct
    wrong = f"```python\ndef {task.entry_point}(*args, **kwargs):\n    return None\n```"
    result = await scoring.check_tests(wrong, task.entry_point, task.tests)
    assert not result.correct and "не прошли" in result.detail
    missing = await scoring.check_tests("кода нет", task.entry_point, task.tests)
    assert not missing.correct


class Judge(LLMProvider):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.prompt = ""

    async def complete(self, model, messages, **kwargs):
        self.prompt = messages[-1].content
        return CompletionResult(text=self.text, usage=Usage(120, 10))

    async def list_models(self):
        return []


async def test_judge_reads_verdict_and_sees_only_the_answer_line():
    judge = Judge('{"correct": true, "reason": "совпадает"}')
    score, usage = await scoring.judge(judge, "m", "Кто первый?", "McDonald's in 1940",
                                       "Долго искал...\nANSWER: McDonald's")
    assert score.correct and usage.total == 130
    assert "ANSWER" not in judge.prompt.split("ОТВЕТ СИСТЕМЫ:")[1]
    bad, _ = await scoring.judge(Judge("не уверен"), "m", "q", "a", "b")
    assert not bad.correct


def test_contains_gold():
    assert scoring.contains_gold("It was Tony Blair.", "Tony Blair")
    assert not scoring.contains_gold("John Major", "Tony Blair")


def test_final_answer_is_the_last_sink():
    subtasks = [
        SimpleNamespace(id=1, depends_on="", result="данные"),
        SimpleNamespace(id=2, depends_on="", result="ещё данные"),
        SimpleNamespace(id=3, depends_on="1,2", result="ANSWER: 42"),
    ]
    assert final_answer(subtasks) == "ANSWER: 42"
    subtasks[2].result = ""
    assert final_answer(subtasks) == "ещё данные"
    assert final_answer([]) == ""


def test_wilson_interval():
    lo, hi = wilson(30, 40)
    assert 0.59 < lo < 0.62 and 0.85 < hi < 0.88
    assert wilson(0, 0) == (0.0, 0.0)


def test_summary_metrics():
    rows = [
        {"task_id": "a", "source": "gsm8k", "arch": "single", "correct": True, "tokens": 100,
         "cost": 0.001, "seconds": 2, "supervisor_tokens": 0, "planner_tokens": 0},
        {"task_id": "a", "source": "gsm8k", "arch": "team", "correct": False, "tokens": 400,
         "cost": 0.004, "seconds": 9, "supervisor_tokens": 100, "planner_tokens": 20,
         "plan": [{"status": "review"}, {"status": "error"}]},
        {"task_id": "b", "source": "frames", "arch": "team", "correct": True, "tokens": 600,
         "cost": 0.006, "seconds": 20, "supervisor_tokens": 200, "planner_tokens": 30,
         "links": {"total": 4, "fabricated": 1}, "plan": [{"status": "done"}, {"status": "done"}]},
    ]
    s = summarize(rows)
    team = s["architectures"]["team"]
    assert team["correct"] == 1 and team["n"] == 2
    assert team["stalled"] == 1
    assert team["supervisor_share"] == pytest.approx(0.3)
    assert team["links_fabricated_share"] == pytest.approx(0.25)
    assert s["paired"]["only_single"] == ["a"]

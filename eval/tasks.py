"""Набор задач и формулировки, с которыми задача уходит в Agent Forge."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

TASKS_FILE = Path(__file__).resolve().parent / "data" / "tasks.jsonl"


@dataclass
class EvalTask:
    id: str
    source: str
    kind: str          # research | math | code
    check: str         # judge | number | tests
    question: str
    answer: str
    source_url: str = ""
    license: str = ""
    entry_point: str = ""
    tests: str = ""
    links: list[str] = field(default_factory=list)
    reasoning_types: str = ""

    @property
    def title(self) -> str:
        head = " ".join(self.question.split())[:70]
        return f"{self.source}: {head}"

    def prompt(self) -> str:
        """Формулировка задачи для системы. Эталон в неё, конечно, не входит."""
        if self.kind == "math":
            return (f"{self.question}\n\n"
                    "Реши задачу и проверь расчёт. В конце итога напиши отдельной "
                    "строкой ANSWER: <число> - только число, без единиц измерения.")
        if self.kind == "code":
            return ("Реализуй функцию на Python по сигнатуре и описанию ниже. "
                    "Решение будет проверено скрытыми тестами.\n\n"
                    f"```python\n{self.question.rstrip()}\n```\n\n"
                    "Итог после строки RESULT: должен содержать полный код функции "
                    "вместе с нужными импортами одним блоком ```python```.")
        return (f"{self.question}\n\n"
                "Найди ответ с помощью поиска и чтения страниц (лучше Википедии). "
                "В конце итога дай краткий ответ отдельной строкой ANSWER: <ответ> "
                "и приведи блок ИСТОЧНИКИ.")


def load_tasks(path: Path = TASKS_FILE, only: list[str] | None = None,
               limit: int | None = None) -> list[EvalTask]:
    tasks: list[EvalTask] = []
    known = set(EvalTask.__dataclass_fields__)
    for line in path.read_text("utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        task = EvalTask(**{k: v for k, v in row.items() if k in known})
        if only and task.source not in only and task.id not in only:
            continue
        tasks.append(task)
    return tasks[:limit] if limit else tasks

"""Проверка ответов системы против эталонов бенчмарков.

* число (GSM8K) - сравнение с эталоном, без модели;
* код (HumanEval) - запуск тестов авторов в песочнице;
* исследовательский вопрос (FRAMES) - LLM-судья сравнивает ответ с эталоном
  по смыслу: «McDonald's в 1940 году» и «McDonald's» - один и тот же ответ.
"""

from __future__ import annotations

import json
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path

_ANSWER_RE = re.compile(r"^\s*\**\s*ANSWER\s*\**\s*[:=]\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
_NUMBER_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?|-?\.\d+")
_CODE_RE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


@dataclass
class Score:
    correct: bool
    detail: str = ""
    extracted: str = ""


def answer_line(text: str) -> str:
    """Содержимое последней строки ``ANSWER: ...`` (или пустая строка)."""
    found = _ANSWER_RE.findall(text or "")
    return found[-1].strip() if found else ""


def parse_number(text: str) -> float | None:
    """Первое число в строке: "$1,490.00" -> 1490.0, "ответ: 8 кг" -> 8.0."""
    match = _NUMBER_RE.search((text or "").replace(" ", " "))
    if not match:
        return None
    raw = match.group(0).replace(",", "").replace(" ", "")
    try:
        return float(raw)
    except ValueError:
        return None


def check_number(result: str, gold: str) -> Score:
    line = answer_line(result)
    value = parse_number(line) if line else None
    if value is None:
        # Ответ без строки ANSWER: берём последнее число в тексте.
        numbers = _NUMBER_RE.findall(result or "")
        value = parse_number(numbers[-1]) if numbers else None
    expected = parse_number(gold)
    if value is None or expected is None:
        return Score(False, "в ответе нет числа", line)
    ok = abs(value - expected) < 1e-6
    return Score(ok, f"ответ {value:g}, эталон {expected:g}", line or f"{value:g}")


def extract_code(text: str, entry_point: str) -> str:
    """Код решения из ответа: последний блок с нужной функцией."""
    blocks = _CODE_RE.findall(text or "")
    for block in reversed(blocks):
        if re.search(rf"def\s+{re.escape(entry_point)}\s*\(", block):
            return block
    if blocks:
        return blocks[-1]
    return text or ""


async def check_tests(result: str, entry_point: str, tests: str, timeout: int = 30) -> Score:
    """Запускает тесты HumanEval в той же песочнице, что и код агентов."""
    from core.tools.sandbox import SubprocessSandbox

    code = extract_code(result, entry_point)
    if f"def {entry_point}" not in code:
        return Score(False, f"в ответе нет функции {entry_point}", "")
    program = f"{code}\n\n{tests}\n\ncheck({entry_point})\n"
    with tempfile.TemporaryDirectory(prefix="af_eval_") as tmp:
        run = await SubprocessSandbox().run(program, "python", Path(tmp), timeout, 512, False)
    if run.timed_out:
        return Score(False, "тесты не уложились во время", code)
    if run.exit_code != 0:
        tail = (run.stderr or run.stdout).strip().splitlines()[-1:] or ["ошибка"]
        return Score(False, f"тесты не прошли: {tail[0][:200]}", code)
    return Score(True, "все тесты прошли", code)


JUDGE_SYSTEM = """\
Ты проверяешь ответы на вопросы викторины. Тебе дают вопрос, эталонный ответ \
и ответ системы. Ответ системы верен, если по смыслу совпадает с эталоном: \
допустимы другие формулировки, лишние пояснения и другой язык, но не другой \
факт, не другое число и не список вариантов, среди которых есть правильный. \
Если эталон уточнён (например, «McDonald's в 1940»), достаточно главного: \
того, о чём спрашивали.

Ответь строго одним JSON-объектом: {"correct": true или false, "reason": "кратко"}
"""


async def judge(provider, model: str, question: str, gold: str, result: str) -> tuple[Score, object]:
    """LLM-судья. Возвращает оценку и расход вызова."""
    from providers.base import ChatMessage

    answer = answer_line(result) or (result or "")[-1500:]
    prompt = (f"ВОПРОС:\n{question}\n\nЭТАЛОН:\n{gold}\n\n"
              f"ОТВЕТ СИСТЕМЫ:\n{answer}")
    reply = await provider.complete(
        model, [ChatMessage("system", JUDGE_SYSTEM), ChatMessage("user", prompt)],
        temperature=0.0, max_tokens=1024)
    raw = (reply.text or "").strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        data = json.loads(match.group(0)) if match else {}
    except ValueError:
        data = {}
    flag = data.get("correct")
    correct = flag is True or str(flag).strip().lower() in ("true", "1", "yes", "да")
    return Score(correct, str(data.get("reason", raw[:200])), answer[:300]), reply.usage


def contains_gold(result: str, gold: str) -> bool:
    """Грубая проверка без модели: эталон встречается в ответе дословно."""
    norm = lambda s: re.sub(r"\W+", " ", (s or "").lower()).strip()  # noqa: E731
    g = norm(gold)
    return bool(g) and g in norm(result)

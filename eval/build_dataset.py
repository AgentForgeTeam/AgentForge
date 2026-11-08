"""Сборка набора задач из открытых бенчмарков.

Задачи не придуманы командой: они взяты из опубликованных наборов вместе с
эталонными ответами авторов.

* FRAMES (Google, Apache-2.0) - многошаговые вопросы по Википедии, для
  ответа нужно найти и связать несколько статей;
* GSM8K (OpenAI, MIT) - текстовые задачи с расчётом, ответ - число;
* HumanEval (OpenAI, MIT) - функции на Python, проверяются тестами авторов.

Выборка детерминирована (фиксированное зерно), поэтому любой участник
получит тот же файл ``eval/data/tasks.jsonl``::

    python -m eval.build_dataset
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import random
import time
from pathlib import Path

import httpx

DATA = Path(__file__).resolve().parent / "data"
TASKS_FILE = DATA / "tasks.jsonl"
SEED = 2026
COUNTS = {"frames": 14, "gsm8k": 13, "humaneval": 13}

SOURCES = {
    "frames": {
        "title": "FRAMES (Google)",
        "license": "Apache-2.0",
        "home": "https://huggingface.co/datasets/google/frames-benchmark",
        "url": "https://huggingface.co/datasets/google/frames-benchmark/resolve/main/test.tsv",
    },
    "gsm8k": {
        "title": "GSM8K (OpenAI)",
        "license": "MIT",
        "home": "https://github.com/openai/grade-school-math",
        "url": "https://raw.githubusercontent.com/openai/grade-school-math/master/"
               "grade_school_math/data/test.jsonl",
    },
    "humaneval": {
        "title": "HumanEval (OpenAI)",
        "license": "MIT",
        "home": "https://github.com/openai/human-eval",
        "url": "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz",
    },
}


def _get(client: httpx.Client, url: str, attempts: int = 3) -> httpx.Response:
    for attempt in range(1, attempts + 1):
        try:
            resp = client.get(url)
            resp.raise_for_status()
            return resp
        except httpx.HTTPError:
            if attempt == attempts:
                raise
            time.sleep(2 * attempt)
    raise AssertionError("unreachable")


def load_frames(client: httpx.Client) -> list[dict]:
    text = _get(client, SOURCES["frames"]["url"]).text
    rows = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    out = []
    for row in rows:
        links = [row.get(f"wikipedia_link_{i}") for i in range(1, 11)] + [row.get("wikipedia_link_11+")]
        out.append({
            "source_id": str(row.get("Unnamed: 0") or row.get("") or "").strip(),
            "question": row["Prompt"].strip(),
            "answer": str(row["Answer"]).strip(),
            "links": [u for u in links if u and u != "None"],
            "reasoning_types": row.get("reasoning_types", ""),
        })
    return out


def load_gsm8k(client: httpx.Client) -> list[dict]:
    out = []
    for i, line in enumerate(_get(client, SOURCES["gsm8k"]["url"]).text.splitlines()):
        if not line.strip():
            continue
        row = json.loads(line)
        solution, _, final = row["answer"].rpartition("####")
        out.append({"source_id": str(i), "question": row["question"].strip(),
                    "answer": final.strip().replace(",", ""), "solution": solution.strip()})
    return out


def load_humaneval(client: httpx.Client) -> list[dict]:
    raw = gzip.decompress(_get(client, SOURCES["humaneval"]["url"]).content).decode("utf-8")
    out = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        out.append({"source_id": row["task_id"], "question": row["prompt"],
                    "entry_point": row["entry_point"], "tests": row["test"],
                    "answer": row["canonical_solution"]})
    return out


KIND = {"frames": ("research", "judge"), "gsm8k": ("math", "number"),
        "humaneval": ("code", "tests")}


def build(counts: dict[str, int] = COUNTS, seed: int = SEED) -> list[dict]:
    loaders = {"frames": load_frames, "gsm8k": load_gsm8k, "humaneval": load_humaneval}
    rng = random.Random(seed)
    tasks: list[dict] = []
    with httpx.Client(timeout=60, follow_redirects=True) as client:
        for source, count in counts.items():
            pool = loaders[source](client)
            kind, check = KIND[source]
            for item in sorted(rng.sample(pool, count), key=lambda r: r["source_id"]):
                tasks.append({
                    "id": f"{source}-{item['source_id'].replace('/', '_')}",
                    "source": source, "kind": kind, "check": check,
                    "source_url": SOURCES[source]["home"],
                    "license": SOURCES[source]["license"],
                    **item,
                })
    return tasks


def main() -> int:
    parser = argparse.ArgumentParser(description="Сборка набора задач для оценки")
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--out", type=Path, default=TASKS_FILE)
    args = parser.parse_args()
    tasks = build(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="\n") as f:
        for task in tasks:
            f.write(json.dumps(task, ensure_ascii=False) + "\n")
    by_source: dict[str, int] = {}
    for task in tasks:
        by_source[task["source"]] = by_source.get(task["source"], 0) + 1
    print(f"Задач: {len(tasks)} {by_source} -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

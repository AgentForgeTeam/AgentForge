"""Сводка метрик по результатам прогона ``eval.run``.

    python -m eval.report eval/results/kp2

Пишет рядом ``summary.json`` и ``summary.md``. Точность показана с 95%
интервалом Уилсона: на 40 задачах разница в несколько процентов между
архитектурами может оказаться шумом, и интервал это честно показывает.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

SOURCES = ["frames", "gsm8k", "humaneval"]
TITLES = {"single": "Один агент", "team": "Команда + супервайзер",
          "frames": "FRAMES (исследование)", "gsm8k": "GSM8K (расчёт)",
          "humaneval": "HumanEval (код)"}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% доверительный интервал доли успехов."""
    if n == 0:
        return 0.0, 0.0
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centre - half), min(1.0, centre + half)


def load(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]
    # При повторных запусках остаётся последняя запись по паре (задача, архитектура).
    latest: dict[tuple[str, str], dict] = {}
    for row in rows:
        latest[(row["task_id"], row["arch"])] = row
    return list(latest.values())


def summarize(rows: list[dict]) -> dict:
    by_arch: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_arch[row["arch"]].append(row)
    out: dict = {"architectures": {}}
    for arch, items in by_arch.items():
        n = len(items)
        k = sum(1 for r in items if r.get("correct"))
        lo, hi = wilson(k, n)
        tokens = sum(r.get("tokens", 0) for r in items)
        links_total = sum((r.get("links") or {}).get("total", 0) for r in items)
        links_bad = sum((r.get("links") or {}).get("fabricated", 0) for r in items)
        by_source = {}
        for source in SOURCES:
            part = [r for r in items if r["source"] == source]
            if part:
                ks = sum(1 for r in part if r.get("correct"))
                by_source[source] = {"n": len(part), "correct": ks, "accuracy": ks / len(part)}
        out["architectures"][arch] = {
            "n": n, "correct": k, "accuracy": k / n if n else 0.0, "ci95": [lo, hi],
            "by_source": by_source,
            "tokens_total": tokens, "tokens_per_task": tokens / n if n else 0,
            "cost_total": round(sum(r.get("cost", 0) for r in items), 4),
            "cost_per_task": (sum(r.get("cost", 0) for r in items) / n) if n else 0,
            "seconds_per_task": (sum(r.get("seconds", 0) for r in items) / n) if n else 0,
            "supervisor_share": (sum(r.get("supervisor_tokens", 0) for r in items) / tokens) if tokens else 0,
            "planner_share": (sum(r.get("planner_tokens", 0) for r in items) / tokens) if tokens else 0,
            "links_total": links_total, "links_fabricated": links_bad,
            "links_fabricated_share": (links_bad / links_total) if links_total else None,
            "limit_exceeded": sum(1 for r in items if r.get("limit_exceeded")),
            "errors": sum(1 for r in items if r.get("error")),
            # подзадача осталась непринятой или не запустилась из-за неё
            "stalled": sum(1 for r in items
                           if any(p.get("status") != "done" for p in r.get("plan", []))),
        }
    if {"single", "team"} <= set(by_arch):
        single = {r["task_id"]: bool(r.get("correct")) for r in by_arch["single"]}
        team = {r["task_id"]: bool(r.get("correct")) for r in by_arch["team"]}
        common = sorted(set(single) & set(team))
        out["paired"] = {
            "tasks": len(common),
            "both": sum(1 for t in common if single[t] and team[t]),
            "only_single": [t for t in common if single[t] and not team[t]],
            "only_team": [t for t in common if team[t] and not single[t]],
            "neither": sum(1 for t in common if not single[t] and not team[t]),
        }
    return out


def _pct(x: float | None) -> str:
    return "-" if x is None else f"{x * 100:.0f}%"


def markdown(summary: dict, rows: list[dict], config: dict) -> str:
    archs = [a for a in ("single", "team") if a in summary["architectures"]]
    s = summary["architectures"]
    lines = ["# Замер качества Agent Forge", ""]
    if config:
        lines += [f"Модели: агенты `{config.get('agent_model')}`, супервайзер и планировщик "
                  f"`{config.get('supervisor_model')}`, судья `{config.get('judge_model')}`. "
                  f"До {config.get('max_steps')} шагов на подзадачу, до "
                  f"{config.get('rework_rounds')} доработки, лимит {config.get('token_limit')} "
                  "токенов на задачу.", ""]
    head = "| Метрика | " + " | ".join(TITLES[a] for a in archs) + " |"
    lines += [head, "|---|" + "---|" * len(archs)]

    def row(name: str, fn) -> None:
        lines.append(f"| {name} | " + " | ".join(fn(s[a]) for a in archs) + " |")

    row("Решено задач", lambda x: f"{x['correct']} из {x['n']}")
    row("Успешность (95% интервал)",
        lambda x: f"{_pct(x['accuracy'])} ({_pct(x['ci95'][0])}-{_pct(x['ci95'][1])})")
    for source in SOURCES:
        row(TITLES[source], lambda x, src=source: (
            f"{x['by_source'][src]['correct']} из {x['by_source'][src]['n']}"
            if src in x["by_source"] else "-"))
    row("Токенов на задачу", lambda x: f"{x['tokens_per_task']:.0f}")
    row("Стоимость по прайсу, на задачу", lambda x: f"${x['cost_per_task']:.4f}")
    row("Время на задачу", lambda x: f"{x['seconds_per_task']:.0f} с")
    row("Доля супервайзера в токенах", lambda x: _pct(x["supervisor_share"]))
    row("Доля планировщика в токенах", lambda x: _pct(x["planner_share"]))
    row("Выдуманные ссылки",
        lambda x: f"{x['links_fabricated']} из {x['links_total']} ({_pct(x['links_fabricated_share'])})")
    row("Превышение лимита", lambda x: str(x["limit_exceeded"]))
    row("Прогонов с ошибкой", lambda x: str(x["errors"]))
    row("Цепочка остановлена", lambda x: f"{x['stalled']} из {x['n']}")
    lines.append("")

    if "paired" in summary:
        p = summary["paired"]
        lines += ["## Попарное сравнение", "",
                  f"Из {p['tasks']} задач обе архитектуры решили {p['both']}, ни одна - "
                  f"{p['neither']}. Только один агент: {len(p['only_single'])} "
                  f"({', '.join(p['only_single']) or 'нет'}). Только команда: "
                  f"{len(p['only_team'])} ({', '.join(p['only_team']) or 'нет'}).", ""]

    lines += ["## Задачи", "", "| Задача | Архитектура | Итог | Токены | Время | Комментарий |",
              "|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: (x["task_id"], x["arch"])):
        mark = "верно" if r.get("correct") else "неверно"
        note = (r.get("error") or r.get("detail") or "").replace("|", "/").replace("\n", " ")[:110]
        lines.append(f"| {r['task_id']} | {r['arch']} | {mark} | {r.get('tokens', 0)} | "
                     f"{r.get('seconds', 0):.0f} с | {note} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Сводка метрик замера")
    parser.add_argument("folder", type=Path)
    args = parser.parse_args()
    rows = load(args.folder / "results.jsonl")
    summary = summarize(rows)
    config_file = args.folder / "config.json"
    config = json.loads(config_file.read_text("utf-8")) if config_file.exists() else {}
    (args.folder / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), "utf-8", newline="\n")
    (args.folder / "summary.md").write_text(markdown(summary, rows, config), "utf-8",
                                            newline="\n")
    print((args.folder / "summary.md").read_text("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

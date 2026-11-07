"""Замер фильтра prompt injection на наборе ``eval/data/injections.jsonl``.

Считается для каждого слоя защиты отдельно и для их комбинации:

* доля пойманных атак (непрямые BIPIA, прямые deepset);
* доля ложных срабатываний на чистых текстах.

Эвристика проверяется без сети. Для модели-классификатора нужен ключ::

    set GEMINI_API_KEY=...
    python -m eval.injection_eval --out eval/results/kp2
    python -m eval.injection_eval --out eval/results/kp2 --no-llm   # только эвристика

Ответы модели кэшируются в ``injections_llm.jsonl``: прерванный замер
продолжается с места остановки.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).resolve().parent / "data" / "injections.jsonl"


def load(path: Path = DATA) -> list[dict]:
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]


def rates(items: list[dict], flagged: dict[str, bool]) -> dict:
    """Доли срабатываний по частям набора."""
    def share(part: list[dict]) -> dict:
        hit = sum(1 for i in part if flagged.get(i["id"]))
        return {"n": len(part), "flagged": hit, "share": hit / len(part) if part else None}

    return {
        "bipia_attacks_caught": share([i for i in items if i["set"] == "bipia"]),
        "deepset_attacks_caught": share([i for i in items if i["set"] == "deepset" and i["label"] == 1]),
        "clean_false_alarms": share([i for i in items if i["set"] == "clean"]),
        "deepset_benign_false_alarms": share([i for i in items if i["set"] == "deepset" and i["label"] == 0]),
        "all_attacks_caught": share([i for i in items if i["label"] == 1]),
        "all_benign_false_alarms": share([i for i in items if i["label"] == 0]),
    }


async def llm_verdicts(items: list[dict], provider_key: str, model: str, api_key: str,
                       cache: Path, concurrency: int = 4) -> dict[str, bool]:
    from core.security.injection import classify_with_llm
    from providers.factory import build_provider

    done: dict[str, bool] = {}
    if cache.exists():
        for line in cache.read_text("utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                done[row["id"]] = row["injection"]
    todo = [i for i in items if i["id"] not in done]
    provider = build_provider(provider_key, api_key, "", timeout=120)
    limit = asyncio.Semaphore(concurrency)

    async def one(item: dict) -> None:
        async with limit:
            try:
                flag, reason, _ = await classify_with_llm(provider, model, item["text"])
            except Exception as exc:  # noqa: BLE001 - пропуск запишется и повторится
                print(f"  {item['id']}: ошибка {exc}", flush=True)
                return
        done[item["id"]] = flag
        with cache.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({"id": item["id"], "injection": flag, "reason": reason},
                               ensure_ascii=False) + "\n")

    try:
        await asyncio.gather(*(one(i) for i in todo))
    finally:
        await provider.aclose()
    return done


def _pct(part: dict) -> str:
    return "-" if part["share"] is None else f"{part['flagged']} из {part['n']} ({part['share'] * 100:.0f}%)"


def markdown(results: dict, model: str) -> str:
    layers = [k for k in ("heuristic", "llm", "combined") if k in results]
    titles = {"heuristic": "Эвристика", "llm": f"Модель ({model})",
              "combined": "Эвристика + модель"}
    rows = [("Пойманы непрямые атаки (BIPIA)", "bipia_attacks_caught"),
            ("Пойманы прямые атаки (deepset)", "deepset_attacks_caught"),
            ("Пойманы все атаки", "all_attacks_caught"),
            ("Ложные срабатывания: абзацы Википедии", "clean_false_alarms"),
            ("Ложные срабатывания: обычные запросы (deepset)", "deepset_benign_false_alarms")]
    lines = ["# Замер фильтра prompt injection", "",
             "| Метрика | " + " | ".join(titles[k] for k in layers) + " |",
             "|---|" + "---|" * len(layers)]
    for title, key in rows:
        lines.append(f"| {title} | " + " | ".join(_pct(results[k][key]) for k in layers) + " |")
    return "\n".join(lines) + "\n"


async def run(out: Path, use_llm: bool, provider_key: str, model: str, api_key: str) -> dict:
    from core.security.injection import scan

    items = load()
    heuristic = {i["id"]: scan(i["text"]).suspicious for i in items}
    results = {"heuristic": rates(items, heuristic)}
    if use_llm:
        llm = await llm_verdicts(items, provider_key, model, api_key, out / "injections_llm.jsonl")
        results["llm"] = rates([i for i in items if i["id"] in llm], llm)
        combined = {k: heuristic[k] or llm.get(k, False) for k in heuristic if k in llm}
        results["combined"] = rates([i for i in items if i["id"] in combined], combined)
    out.mkdir(parents=True, exist_ok=True)
    (out / "injections.json").write_text(json.dumps(results, ensure_ascii=False, indent=2),
                                         "utf-8", newline="\n")
    (out / "injections.md").write_text(markdown(results, model), "utf-8", newline="\n")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Замер фильтра prompt injection")
    parser.add_argument("--out", type=Path, default=ROOT / "eval" / "results" / "latest")
    parser.add_argument("--no-llm", action="store_true", help="только эвристика, без модели")
    parser.add_argument("--provider", default="gemini")
    parser.add_argument("--model", default="gemini-3.1-flash-lite")
    parser.add_argument("--key-env", default="GEMINI_API_KEY")
    args = parser.parse_args()
    api_key = os.environ.get(args.key_env, "").strip()
    use_llm = not args.no_llm
    if use_llm and not api_key:
        print(f"Нет ключа в {args.key_env}: замер только эвристики (--no-llm)", file=sys.stderr)
        use_llm = False
    sys.path.insert(0, str(ROOT))
    asyncio.run(run(args.out, use_llm, args.provider, args.model, api_key))
    print((args.out / "injections.md").read_text("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

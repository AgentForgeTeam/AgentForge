"""Набор для замера фильтра prompt injection.

Атаки взяты из открытых наборов, а не придуманы:

* BIPIA (Microsoft, MIT) - 75 инструкций для непрямых атак: злоумышленник
  прячет их в текст страницы или документа, который читает агент. Каждая
  вставляется в абзац из Википедии (в начало, середину или конец), а тот же
  абзац без вставки служит чистым примером. Так проверяется, что фильтр
  реагирует на атаку, а не на тему текста;
* deepset/prompt-injections (Apache-2.0), тестовая часть - 116 размеченных
  текстов: прямые атаки и обычные запросы.

    python -m eval.build_injections
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from urllib.parse import quote

import httpx

DATA = Path(__file__).resolve().parent / "data"
OUT = DATA / "injections.jsonl"
SEED = 2026

BIPIA_URL = "https://raw.githubusercontent.com/microsoft/BIPIA/main/benchmark/text_attack_test.json"
DEEPSET_ROWS = ("https://datasets-server.huggingface.co/rows?dataset=deepset/prompt-injections"
                "&config=default&split=test&offset={offset}&length=100")
WIKI_EXTRACT = ("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1"
                "&exintro=1&format=json&redirects=1&titles={title}")

# нейтральные статьи: из их вступлений берутся абзацы-носители
ARTICLES = [
    "Photosynthesis", "Mount Everest", "Python (programming language)", "Great Barrier Reef",
    "Johann Sebastian Bach", "Roman Empire", "Volcano", "Honey bee", "Saturn", "Tea",
    "Antarctica", "Printing press", "Olympic Games", "Coffee", "Amazon River", "Chess",
    "Leonardo da Vinci", "Penicillin", "Internet", "Silk Road", "Tokyo", "Jazz",
    "Moon", "Bicycle", "Pyramids of Giza", "Library of Alexandria", "Electricity",
    "Rainforest", "Marie Curie", "Wind power", "Desert", "Eiffel Tower",
]


def _json(client: httpx.Client, url: str) -> dict:
    resp = client.get(url)
    resp.raise_for_status()
    return resp.json()


def wiki_paragraphs(client: httpx.Client, count: int, rng: random.Random) -> list[dict]:
    paragraphs: list[dict] = []
    for title in ARTICLES:
        data = _json(client, WIKI_EXTRACT.format(title=quote(title)))
        for page in data.get("query", {}).get("pages", {}).values():
            for para in (page.get("extract") or "").split("\n"):
                # длинные тире Википедии заменяются дефисом, как во всём проекте
                para = para.strip().replace("\u2014", "-").replace("\u2013", "-")
                if 250 <= len(para) <= 1500:
                    paragraphs.append({"text": para, "origin": f"https://en.wikipedia.org/wiki/{quote(title)}"})
    rng.shuffle(paragraphs)
    if len(paragraphs) < count:
        raise RuntimeError(f"мало абзацев: {len(paragraphs)} < {count}")
    return paragraphs[:count]


def insert(paragraph: str, attack: str, where: str) -> str:
    if where == "start":
        return f"{attack} {paragraph}"
    if where == "end":
        return f"{paragraph} {attack}"
    sentences = paragraph.split(". ")
    middle = max(1, len(sentences) // 2)
    return ". ".join(sentences[:middle]) + f". {attack} " + ". ".join(sentences[middle:])


def build() -> list[dict]:
    rng = random.Random(SEED)
    items: list[dict] = []
    headers = {"User-Agent": "AgentForge/1.2 (+https://github.com/AgentForgeTeam/AgentForge; dataset builder)"}
    with httpx.Client(timeout=60, follow_redirects=True, headers=headers) as client:
        attacks = [(category, text) for category, texts in _json(client, BIPIA_URL).items()
                   for text in texts]
        carriers = wiki_paragraphs(client, len(attacks), rng)
        for i, ((category, attack), carrier) in enumerate(zip(attacks, carriers)):
            where = ("start", "middle", "end")[i % 3]
            items.append({"id": f"bipia-{i:03d}", "set": "bipia", "label": 1,
                          "category": category, "position": where,
                          "text": insert(carrier["text"], attack, where),
                          "source": "https://github.com/microsoft/BIPIA", "carrier": carrier["origin"]})
            items.append({"id": f"clean-{i:03d}", "set": "clean", "label": 0,
                          "category": "", "position": "", "text": carrier["text"],
                          "source": carrier["origin"], "carrier": carrier["origin"]})
        offset = 0
        while True:
            data = _json(client, DEEPSET_ROWS.format(offset=offset))
            rows = data.get("rows", [])
            for r in rows:
                row = r["row"]
                items.append({"id": f"deepset-{r['row_idx']:03d}", "set": "deepset",
                              "label": int(row["label"]), "category": "", "position": "",
                              "text": row["text"], "carrier": "",
                              "source": "https://huggingface.co/datasets/deepset/prompt-injections"})
            offset += len(rows)
            if not rows or offset >= data.get("num_rows_total", 0):
                break
    return items


def main() -> int:
    items = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    counts: dict[str, int] = {}
    for item in items:
        key = f"{item['set']}:{item['label']}"
        counts[key] = counts.get(key, 0) + 1
    print(f"Примеров: {len(items)} {counts} -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

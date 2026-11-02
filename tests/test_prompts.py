"""Промпты ролей и формат ответа агента.

Ответ агента читают программы: оркестратор берёт итог из блока RESULT,
human-in-the-loop смотрит на CONFIDENCE, проверка ссылок разбирает блок
ИСТОЧНИКИ. Тесты держат промпты и разбор ответа в согласии.
"""

from __future__ import annotations

from core.agents.roles import ANSWER_MARKERS, COMMON_RULES, TEMPLATES, by_key
from core.agents.runner import parse_confidence, parse_result
from core.verify.links import extract_citations

# Ответ, написанный строго по правилам из COMMON_RULES.
SAMPLE = """Проверил численность населения по двум источникам.

RESULT:
Население Парижа на 2023 год - около 2,1 млн человек.

ИСТОЧНИКИ:
- https://en.wikipedia.org/wiki/Paris | "The City of Paris has an estimated population of 2,102,650"
- https://www.insee.fr/en/statistiques/2011101?geo=COM-75056 | "Population en 2021 : 2 133 111"

CONFIDENCE: 0.85
"""


def test_common_rules_name_every_marker():
    for marker in ANSWER_MARKERS:
        assert marker.rstrip(":") in COMMON_RULES, marker


def test_rules_keep_code_inside_the_result_block():
    # Всё, что стоит до RESULT:, в итог подзадачи не попадает.
    assert "помещай внутрь него" in COMMON_RULES


def test_rules_forbid_made_up_links():
    text = COMMON_RULES.lower()
    assert "не" in text and "придумывай" in text
    assert "дословная цитата" in text


def test_every_role_has_a_prompt_except_custom():
    for template in TEMPLATES:
        if template.key == "custom":
            assert template.prompt == ""
        else:
            assert len(template.prompt) > 80, template.key
            assert template.title_ru and template.title_en


def test_answer_in_the_contract_format_is_parsed():
    result = parse_result(SAMPLE)
    assert result.startswith("Население Парижа")
    assert "CONFIDENCE" not in result
    assert parse_confidence(SAMPLE) == 0.85
    citations = extract_citations(result)
    assert [c.url for c in citations] == [
        "https://en.wikipedia.org/wiki/Paris",
        "https://www.insee.fr/en/statistiques/2011101?geo=COM-75056",
    ]
    assert citations[1].quote == "Population en 2021 : 2 133 111"


def test_analyst_and_researcher_work_with_sources():
    assert "ссылк" in by_key("analyst").prompt
    assert "первоисточник" in by_key("researcher").prompt

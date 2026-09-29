"""Пресеты подключения к провайдерам «из коробки».

Пользователю достаточно выбрать провайдера и вставить свой ключ - base URL,
формат API и список популярных моделей подставляются автоматически.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProviderPreset:
    key: str
    title: str
    base_url: str
    api_style: str              # "openai" | "anthropic" | "gemini"
    requires_key: bool = True
    free_tier: bool = False     # бесплатный/условно-бесплатный доступ
    local: bool = False         # работает без интернета
    docs_url: str = ""
    suggested_models: list[str] = field(default_factory=list)
    notes: str = ""


PRESETS: dict[str, ProviderPreset] = {
    "openai": ProviderPreset(
        key="openai",
        title="OpenAI",
        base_url="https://api.openai.com/v1",
        api_style="openai",
        docs_url="https://platform.openai.com/api-keys",
        suggested_models=["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "o4-mini"],
    ),
    "anthropic": ProviderPreset(
        key="anthropic",
        title="Anthropic (Claude)",
        base_url="https://api.anthropic.com/v1",
        api_style="anthropic",
        docs_url="https://console.anthropic.com/settings/keys",
        suggested_models=[
            "claude-sonnet-4-5", "claude-opus-4-1", "claude-3-7-sonnet-latest",
            "claude-3-5-haiku-latest",
        ],
    ),
    "gemini": ProviderPreset(
        key="gemini",
        title="Google Gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        api_style="gemini",
        free_tier=True,
        docs_url="https://aistudio.google.com/app/apikey",
        suggested_models=["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"],
        notes="Есть бесплатная квота в AI Studio.",
    ),
    "groq": ProviderPreset(
        key="groq",
        title="Groq",
        base_url="https://api.groq.com/openai/v1",
        api_style="openai",
        free_tier=True,
        docs_url="https://console.groq.com/keys",
        suggested_models=[
            "llama-3.3-70b-versatile", "llama-3.1-8b-instant",
            "qwen/qwen3-32b", "deepseek-r1-distill-llama-70b",
        ],
        notes="Очень быстрый инференс, щедрый бесплатный лимит.",
    ),
    "openrouter": ProviderPreset(
        key="openrouter",
        title="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        api_style="openai",
        free_tier=True,
        docs_url="https://openrouter.ai/keys",
        suggested_models=[
            "deepseek/deepseek-chat", "qwen/qwen-2.5-72b-instruct",
            "meta-llama/llama-3.3-70b-instruct", "google/gemma-3-27b-it:free",
        ],
        notes="Единый ключ к десяткам моделей, часть из них бесплатна (суффикс :free).",
    ),
    "ollama": ProviderPreset(
        key="ollama",
        title="Ollama (локально)",
        base_url="http://localhost:11434/v1",
        api_style="openai",
        requires_key=False,
        free_tier=True,
        local=True,
        docs_url="https://ollama.com/download",
        suggested_models=["qwen2.5:7b-instruct", "qwen2.5:14b-instruct",
                          "llama3.1:8b", "mistral-nemo", "gemma3:12b"],
        notes="Работает офлайн. Ключ не нужен - достаточно запущенного сервера Ollama.",
    ),
    "huggingface": ProviderPreset(
        key="huggingface",
        title="Hugging Face Inference",
        base_url="https://router.huggingface.co/v1",
        api_style="openai",
        free_tier=True,
        docs_url="https://huggingface.co/settings/tokens",
        suggested_models=["Qwen/Qwen2.5-72B-Instruct", "meta-llama/Llama-3.3-70B-Instruct"],
        notes="Router HF совместим с OpenAI API. Бесплатная квота ограничена.",
    ),
    "custom": ProviderPreset(
        key="custom",
        title="Свой OpenAI-совместимый endpoint",
        base_url="",
        api_style="openai",
        requires_key=False,
        notes="LM Studio, vLLM, llama.cpp server, корпоративный шлюз и т.п.",
    ),
}


def preset(key: str) -> ProviderPreset:
    """Возвращает пресет; неизвестный ключ трактуется как «custom»."""
    return PRESETS.get(key, PRESETS["custom"])


def preset_list() -> list[ProviderPreset]:
    return list(PRESETS.values())

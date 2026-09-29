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
        # Только модели, которые вызывают инструменты через Chat Completions.
        # gpt-6-astra и gpt-6.1-sol умеют это лишь через Responses API: их
        # можно вписать вручную для агентов без инструментов или взять
        # через OpenRouter.
        suggested_models=["gpt-5.4-mini", "gpt-5.4-nano", "gpt-5.4", "gpt-6-luna",
                          "gpt-6-sol", "gpt-4.1", "gpt-4.1-mini", "gpt-4o-mini"],
        notes="Запросы платные: нужен пополненный баланс в Billing.",
    ),
    "anthropic": ProviderPreset(
        key="anthropic",
        title="Anthropic (Claude)",
        base_url="https://api.anthropic.com/v1",
        api_style="anthropic",
        docs_url="https://console.anthropic.com/settings/keys",
        suggested_models=[
            "claude-sonnet-5-5", "claude-opus-5-5", "claude-fable-5-1",
            "claude-haiku-4-5-20251001",
        ],
    ),
    "gemini": ProviderPreset(
        key="gemini",
        title="Google Gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        api_style="gemini",
        free_tier=True,
        docs_url="https://aistudio.google.com/app/apikey",
        # Модели 2.5 Google открыл только тем, кто пользовался ими раньше,
        # 2.0 отключены: новым ключам они отвечают ошибкой.
        suggested_models=[
            "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash",
            "gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite",
            "gemini-3.1-pro-preview", "gemini-3-flash-preview", "gemini-flash-latest",
        ],
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
            "openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b",
            "llama-3.3-70b-versatile", "llama-3.1-8b-instant",
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
            "google/gemini-3.8-flash", "openai/gpt-6-luna", "openai/gpt-6-astra",
            "anthropic/claude-sonnet-5.5", "deepseek/deepseek-v4.1-flash",
            "moonshotai/kimi-k3", "qwen/qwen3.8-27b:free", "google/gemma-4-31b-it:free",
            "nvidia/nemotron-3-super-120b-a12b:free",
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
        suggested_models=["qwen3.8:27b", "qwen3.6:27b", "granite4.1:8b", "lfm2.5:8b",
                          "qwen2.5:7b-instruct", "llama3.1:8b"],
        notes="Работает офлайн. Ключ не нужен - достаточно запущенного сервера Ollama.",
    ),
    "huggingface": ProviderPreset(
        key="huggingface",
        title="Hugging Face Inference",
        base_url="https://router.huggingface.co/v1",
        api_style="openai",
        free_tier=True,
        docs_url="https://huggingface.co/settings/tokens",
        suggested_models=[
            "Qwen/Qwen3.8-27B", "deepseek-ai/DeepSeek-V4.1-Flash", "openai/gpt-oss-120b",
            "moonshotai/Kimi-K3", "google/gemma-4-31B-it", "meta-llama/Llama-3.3-70B-Instruct",
        ],
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

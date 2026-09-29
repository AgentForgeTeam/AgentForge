"""Провайдер Google Gemini (generativeLanguage API).

Особенности, скрытые внутри класса:
* роли называются ``user``/``model``, системный промпт — ``systemInstruction``;
* ключ передаётся заголовком ``x-goog-api-key``;
* инструменты описываются как ``functionDeclarations``.
"""

from __future__ import annotations

import uuid
from typing import Any

import httpx

from providers.base import (
    ChatMessage,
    CompletionResult,
    LLMProvider,
    ProviderError,
    ToolCall,
    ToolSpec,
    Usage,
)


class GeminiProvider(LLMProvider):
    key = "gemini"

    def __init__(self, api_key: str = "", base_url: str = "",
                 timeout: float = 120.0) -> None:
        super().__init__(
            api_key, base_url or "https://generativelanguage.googleapis.com/v1beta", timeout
        )
        self._client: httpx.AsyncClient | None = None

    def _headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json", "x-goog-api-key": self.api_key}

    def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @staticmethod
    def _split(messages: list[ChatMessage]) -> tuple[str, list[dict[str, Any]]]:
        system_parts: list[str] = []
        contents: list[dict[str, Any]] = []
        for m in messages:
            if m.role == "system":
                system_parts.append(m.content)
            elif m.role == "tool":
                contents.append({
                    "role": "user",
                    "parts": [{"functionResponse": {"name": m.name or "tool",
                                                    "response": {"result": m.content}}}],
                })
            elif m.role == "assistant":
                parts: list[dict[str, Any]] = []
                if m.content:
                    parts.append({"text": m.content})
                parts += [{"functionCall": {"name": tc.name, "args": tc.arguments}}
                          for tc in m.tool_calls]
                contents.append({"role": "model", "parts": parts or [{"text": ""}]})
            else:
                contents.append({"role": "user", "parts": [{"text": m.content}]})
        return "\n\n".join(p for p in system_parts if p), contents

    async def complete(self, model: str, messages: list[ChatMessage], *,
                       temperature: float = 0.7, max_tokens: int = 2048,
                       tools: list[ToolSpec] | None = None) -> CompletionResult:
        system, contents = self._split(messages)
        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {"temperature": temperature,
                                 "maxOutputTokens": max_tokens},
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        if tools:
            payload["tools"] = [{
                "functionDeclarations": [
                    {"name": t.name, "description": t.description, "parameters": t.parameters}
                    for t in tools
                ]
            }]

        url = f"{self.base_url}/models/{model}:generateContent"
        try:
            resp = await self._http().post(url, headers=self._headers(), json=payload)
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)

        data = resp.json()
        candidate = (data.get("candidates") or [{}])[0]
        text_parts, calls = [], []
        for part in (candidate.get("content") or {}).get("parts", []):
            if "text" in part:
                text_parts.append(part["text"])
            elif "functionCall" in part:
                fc = part["functionCall"]
                calls.append(ToolCall(id=uuid.uuid4().hex[:12], name=fc.get("name", ""),
                                      arguments=fc.get("args") or {}))
        u = data.get("usageMetadata") or {}
        return CompletionResult(
            text="".join(text_parts),
            tool_calls=calls,
            usage=Usage(int(u.get("promptTokenCount", 0)),
                        int(u.get("candidatesTokenCount", 0))),
            finish_reason=candidate.get("finishReason", ""),
            model=model,
            raw=data,
        )

    async def list_models(self) -> list[str]:
        try:
            resp = await self._http().get(f"{self.base_url}/models", headers=self._headers())
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)
        names = []
        for m in resp.json().get("models", []):
            name = (m.get("name") or "").removeprefix("models/")
            if name and "generateContent" in (m.get("supportedGenerationMethods") or
                                              ["generateContent"]):
                names.append(name)
        return sorted(names)


def _error_text(resp: httpx.Response) -> str:
    try:
        err = resp.json().get("error") or {}
        return f"{resp.status_code}: {err.get('message', resp.text[:200])}"
    except Exception:  # noqa: BLE001
        return f"{resp.status_code}: {resp.text[:200]}"

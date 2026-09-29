"""Провайдер для всех OpenAI-совместимых API.

Покрывает OpenAI, Groq, OpenRouter, Ollama, Hugging Face Router и любой
локальный сервер (LM Studio, vLLM, llama.cpp) — различается только base_url.
"""

from __future__ import annotations

import json
from typing import Any, AsyncIterator

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


class OpenAICompatProvider(LLMProvider):
    """Реализация протокола ``/chat/completions``."""

    key = "openai"

    def __init__(self, api_key: str = "", base_url: str = "",
                 timeout: float = 120.0, extra_headers: dict | None = None) -> None:
        super().__init__(api_key, base_url or "https://api.openai.com/v1", timeout)
        self._extra_headers = extra_headers or {}
        self._client: httpx.AsyncClient | None = None

    # -- служебное -----------------------------------------------------------
    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", **self._extra_headers}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @staticmethod
    def _to_wire(messages: list[ChatMessage]) -> list[dict[str, Any]]:
        """Конвертирует нейтральные сообщения в формат OpenAI."""
        out: list[dict[str, Any]] = []
        for m in messages:
            if m.role == "tool":
                out.append({"role": "tool", "tool_call_id": m.tool_call_id,
                            "content": m.content})
                continue
            item: dict[str, Any] = {"role": m.role, "content": m.content}
            if m.tool_calls:
                item["tool_calls"] = [
                    {"id": tc.id, "type": "function",
                     "function": {"name": tc.name,
                                  "arguments": json.dumps(tc.arguments, ensure_ascii=False)}}
                    for tc in m.tool_calls
                ]
                # OpenAI требует content=None, когда есть tool_calls
                item["content"] = m.content or None
            out.append(item)
        return out

    @staticmethod
    def _tools_payload(tools: list[ToolSpec] | None) -> list[dict] | None:
        if not tools:
            return None
        return [
            {"type": "function",
             "function": {"name": t.name, "description": t.description,
                          "parameters": t.parameters}}
            for t in tools
        ]

    # -- API -----------------------------------------------------------------
    async def complete(self, model: str, messages: list[ChatMessage], *,
                       temperature: float = 0.7, max_tokens: int = 2048,
                       tools: list[ToolSpec] | None = None) -> CompletionResult:
        payload: dict[str, Any] = {
            "model": model,
            "messages": self._to_wire(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        tool_payload = self._tools_payload(tools)
        if tool_payload:
            payload["tools"] = tool_payload
            payload["tool_choice"] = "auto"

        try:
            resp = await self._http().post(
                f"{self.base_url}/chat/completions", headers=self._headers(), json=payload
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc

        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)

        data = resp.json()
        choice = (data.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        calls = [
            ToolCall(id=c.get("id", ""),
                     name=(c.get("function") or {}).get("name", ""),
                     arguments=ToolCall.parse_args((c.get("function") or {}).get("arguments")))
            for c in (msg.get("tool_calls") or [])
        ]
        u = data.get("usage") or {}
        return CompletionResult(
            text=msg.get("content") or "",
            tool_calls=calls,
            usage=Usage(int(u.get("prompt_tokens", 0)), int(u.get("completion_tokens", 0))),
            finish_reason=choice.get("finish_reason", ""),
            model=data.get("model", model),
            raw=data,
        )

    async def stream(self, model: str, messages: list[ChatMessage], *,
                     temperature: float = 0.7,
                     max_tokens: int = 2048) -> AsyncIterator[str]:
        payload = {
            "model": model,
            "messages": self._to_wire(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        try:
            async with self._http().stream(
                "POST", f"{self.base_url}/chat/completions",
                headers=self._headers(), json=payload
            ) as resp:
                if resp.status_code >= 400:
                    await resp.aread()
                    raise ProviderError(_error_text(resp), resp.status_code)
                async for line in resp.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    chunk = line[5:].strip()
                    if chunk in ("", "[DONE]"):
                        continue
                    try:
                        delta = json.loads(chunk)["choices"][0].get("delta", {})
                    except (ValueError, KeyError, IndexError):
                        continue
                    if delta.get("content"):
                        yield delta["content"]
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc

    async def list_models(self) -> list[str]:
        try:
            resp = await self._http().get(f"{self.base_url}/models", headers=self._headers())
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)
        data = resp.json()
        items = data.get("data", data if isinstance(data, list) else [])
        names = [it.get("id") or it.get("name", "") for it in items if isinstance(it, dict)]
        return sorted(n for n in names if n)


def _error_text(resp: httpx.Response) -> str:
    """Достаёт понятное сообщение об ошибке из ответа провайдера."""
    try:
        data = resp.json()
        err = data.get("error")
        if isinstance(err, dict):
            return f"{resp.status_code}: {err.get('message', resp.text[:200])}"
        if isinstance(err, str):
            return f"{resp.status_code}: {err}"
        if "message" in data:
            return f"{resp.status_code}: {data['message']}"
    except Exception:  # noqa: BLE001
        pass
    return f"{resp.status_code}: {resp.text[:200]}"

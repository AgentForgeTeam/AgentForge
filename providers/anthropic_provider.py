"""Провайдер Anthropic Messages API.

Отличия от OpenAI, которые здесь скрываются:
* системный промпт передаётся отдельным полем ``system``;
* результат инструмента — блок ``tool_result`` внутри сообщения роли ``user``;
* заголовки ``x-api-key`` и ``anthropic-version``.
"""

from __future__ import annotations

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

ANTHROPIC_VERSION = "2023-06-01"


class AnthropicProvider(LLMProvider):
    key = "anthropic"

    def __init__(self, api_key: str = "", base_url: str = "",
                 timeout: float = 120.0) -> None:
        super().__init__(api_key, base_url or "https://api.anthropic.com/v1", timeout)
        self._client: httpx.AsyncClient | None = None

    def _headers(self) -> dict[str, str]:
        return {
            "content-type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": ANTHROPIC_VERSION,
        }

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
        """Отделяет system-промпт и собирает тело диалога."""
        system_parts: list[str] = []
        wire: list[dict[str, Any]] = []
        for m in messages:
            if m.role == "system":
                system_parts.append(m.content)
            elif m.role == "tool":
                wire.append({
                    "role": "user",
                    "content": [{"type": "tool_result",
                                 "tool_use_id": m.tool_call_id,
                                 "content": m.content}],
                })
            elif m.role == "assistant" and m.tool_calls:
                blocks: list[dict[str, Any]] = []
                if m.content:
                    blocks.append({"type": "text", "text": m.content})
                blocks += [{"type": "tool_use", "id": tc.id, "name": tc.name,
                            "input": tc.arguments} for tc in m.tool_calls]
                wire.append({"role": "assistant", "content": blocks})
            else:
                wire.append({"role": m.role, "content": m.content})
        return "\n\n".join(p for p in system_parts if p), wire

    async def complete(self, model: str, messages: list[ChatMessage], *,
                       temperature: float = 0.7, max_tokens: int = 2048,
                       tools: list[ToolSpec] | None = None) -> CompletionResult:
        system, wire = self._split(messages)
        payload: dict[str, Any] = {
            "model": model,
            "messages": wire,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system:
            payload["system"] = system
        if tools:
            payload["tools"] = [
                {"name": t.name, "description": t.description, "input_schema": t.parameters}
                for t in tools
            ]

        try:
            resp = await self._http().post(
                f"{self.base_url}/messages", headers=self._headers(), json=payload
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)

        data = resp.json()
        text_parts: list[str] = []
        calls: list[ToolCall] = []
        for block in data.get("content", []):
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                calls.append(ToolCall(id=block.get("id", ""), name=block.get("name", ""),
                                      arguments=block.get("input") or {}))
        u = data.get("usage") or {}
        return CompletionResult(
            text="".join(text_parts),
            tool_calls=calls,
            usage=Usage(int(u.get("input_tokens", 0)), int(u.get("output_tokens", 0))),
            finish_reason=data.get("stop_reason", ""),
            model=data.get("model", model),
            raw=data,
        )

    async def stream(self, model: str, messages: list[ChatMessage], *,
                     temperature: float = 0.7,
                     max_tokens: int = 2048) -> AsyncIterator[str]:
        import json as _json

        system, wire = self._split(messages)
        payload: dict[str, Any] = {
            "model": model, "messages": wire, "max_tokens": max_tokens,
            "temperature": temperature, "stream": True,
        }
        if system:
            payload["system"] = system
        try:
            async with self._http().stream(
                "POST", f"{self.base_url}/messages", headers=self._headers(), json=payload
            ) as resp:
                if resp.status_code >= 400:
                    await resp.aread()
                    raise ProviderError(_error_text(resp), resp.status_code)
                async for line in resp.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    try:
                        event = _json.loads(line[5:].strip())
                    except ValueError:
                        continue
                    if event.get("type") == "content_block_delta":
                        piece = (event.get("delta") or {}).get("text")
                        if piece:
                            yield piece
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc

    async def list_models(self) -> list[str]:
        try:
            resp = await self._http().get(f"{self.base_url}/models", headers=self._headers())
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)
        return sorted(it.get("id", "") for it in resp.json().get("data", []) if it.get("id"))


def _error_text(resp: httpx.Response) -> str:
    try:
        err = resp.json().get("error") or {}
        return f"{resp.status_code}: {err.get('message', resp.text[:200])}"
    except Exception:  # noqa: BLE001
        return f"{resp.status_code}: {resp.text[:200]}"

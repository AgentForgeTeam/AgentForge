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
    DeltaHandler,
    LLMProvider,
    ProviderError,
    ToolCall,
    ToolSpec,
    Usage,
    estimate_tokens,
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

    async def stream_complete(self, model: str, messages: list[ChatMessage], *,
                              temperature: float = 0.7, max_tokens: int = 2048,
                              tools: list[ToolSpec] | None = None,
                              on_delta: DeltaHandler | None = None) -> CompletionResult:
        """Потоковый ``/chat/completions`` с разбором вызовов инструментов.

        Аргументы вызова инструмента приходят кусками JSON в нескольких
        чанках, поэтому они склеиваются по ``index`` и разбираются в конце.
        Расход токенов сервер присылает последним чанком, если попросить
        ``stream_options.include_usage``; часть совместимых серверов этот
        параметр не знает — тогда запрос повторяется без него.
        """
        payload: dict[str, Any] = {
            "model": model,
            "messages": self._to_wire(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        tool_payload = self._tools_payload(tools)
        if tool_payload:
            payload["tools"] = tool_payload
            payload["tool_choice"] = "auto"
        try:
            return await self._stream_once(payload, model, messages, on_delta)
        except ProviderError as exc:
            if exc.status == 400 and "stream_options" in str(exc):
                payload.pop("stream_options", None)
                return await self._stream_once(payload, model, messages, on_delta)
            raise

    async def _stream_once(self, payload: dict[str, Any], model: str,
                           messages: list[ChatMessage],
                           on_delta: DeltaHandler | None) -> CompletionResult:
        text_parts: list[str] = []
        reasoning_parts: list[str] = []
        calls: dict[int, dict[str, str]] = {}
        usage: dict[str, Any] = {}
        finish_reason = ""
        model_name = model
        try:
            async with self._http().stream(
                "POST", f"{self.base_url}/chat/completions",
                headers=self._headers(), json=payload,
            ) as resp:
                if resp.status_code >= 400:
                    await resp.aread()
                    raise ProviderError(_error_text(resp), resp.status_code)
                async for line in resp.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    raw = line[5:].strip()
                    if not raw or raw == "[DONE]":
                        continue
                    try:
                        chunk = json.loads(raw)
                    except ValueError:
                        continue
                    if chunk.get("error"):
                        err = chunk["error"]
                        raise ProviderError(err.get("message", str(err))
                                            if isinstance(err, dict) else str(err))
                    model_name = chunk.get("model") or model_name
                    usage = (chunk.get("usage")
                             or (chunk.get("x_groq") or {}).get("usage")
                             or usage)
                    for choice in chunk.get("choices") or []:
                        delta = choice.get("delta") or {}
                        piece = delta.get("content")
                        if piece:
                            text_parts.append(piece)
                            if on_delta:
                                on_delta(piece, "text")
                        thought = delta.get("reasoning_content") or delta.get("reasoning")
                        if isinstance(thought, str) and thought:
                            reasoning_parts.append(thought)
                            if on_delta:
                                on_delta(thought, "reasoning")
                        for tc in delta.get("tool_calls") or []:
                            slot = calls.setdefault(int(tc.get("index", len(calls))),
                                                    {"id": "", "name": "", "args": ""})
                            slot["id"] = tc.get("id") or slot["id"]
                            fn = tc.get("function") or {}
                            slot["name"] = fn.get("name") or slot["name"]
                            slot["args"] += fn.get("arguments") or ""
                        finish_reason = choice.get("finish_reason") or finish_reason
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc

        text = "".join(text_parts)
        tool_calls = [
            ToolCall(id=slot["id"] or f"call_{index}", name=slot["name"],
                     arguments=ToolCall.parse_args(slot["args"]))
            for index, slot in sorted(calls.items()) if slot["name"]
        ]
        if usage:
            result_usage = Usage(int(usage.get("prompt_tokens", 0)),
                                 int(usage.get("completion_tokens", 0)))
        else:
            prompt = sum(len(m.content or "") for m in messages)
            output = text + "".join(reasoning_parts) + "".join(
                c["args"] for c in calls.values())
            result_usage = Usage(prompt // 4, estimate_tokens(output))
        return CompletionResult(text=text, tool_calls=tool_calls, usage=result_usage,
                                finish_reason=finish_reason, model=model_name)

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

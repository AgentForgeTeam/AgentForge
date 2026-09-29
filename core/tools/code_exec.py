"""Инструмент исполнения кода в песочнице."""

from __future__ import annotations

from typing import Any

from core.tools.base import Tool, ToolContext, ToolError
from core.tools.sandbox import LANG_COMMANDS, get_sandbox


class CodeExecTool(Tool):
    name = "code_exec"
    description = (
        "Выполнить фрагмент кода в изолированной песочнице и получить stdout/stderr. "
        "Сеть внутри песочницы отключена, файловая система одноразовая. "
        "Используй для проверки гипотез, расчётов и прогона тестов."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Исходный код целиком"},
            "language": {
                "type": "string",
                "enum": list(LANG_COMMANDS),
                "description": "Язык исполнения",
                "default": "python",
            },
        },
        "required": ["code"],
    }

    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        code = (kwargs.get("code") or "").strip()
        language = (kwargs.get("language") or "python").lower()
        if not code:
            raise ToolError("Пустой код - нечего исполнять")
        if language not in LANG_COMMANDS:
            raise ToolError(f"Язык «{language}» не поддерживается")

        sandbox = await get_sandbox(ctx.sandbox_backend)
        result = await sandbox.run(
            code=code,
            language=language,
            workdir=ctx.workspace_dir / ".sandbox",
            timeout=ctx.sandbox_timeout_sec,
            memory_mb=ctx.sandbox_memory_mb,
            network=ctx.allow_network_in_sandbox,
        )
        return result.as_text()

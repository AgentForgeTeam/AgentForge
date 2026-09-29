"""Файловые инструменты агента.

Права ограничены каталогом воркспейса плюс каталогами, которые пользователь
явно добавил в настройках (ответ на вопрос 10). Проверка пути централизована
в ``ToolContext.resolve``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.tools.base import Tool, ToolContext, ToolError

MAX_READ_BYTES = 200_000
MAX_WRITE_BYTES = 2_000_000


class FileReadTool(Tool):
    name = "read_file"
    description = (
        "Прочитать текстовый файл из рабочего каталога проекта "
        "или из каталога, разрешённого пользователем."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Путь относительно рабочего каталога"},
            "max_bytes": {"type": "integer",
                          "description": f"Сколько байт прочитать (по умолчанию {MAX_READ_BYTES})"},
        },
        "required": ["path"],
    }

    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        path = ctx.resolve(str(kwargs.get("path", "")), must_exist=True)
        if path.is_dir():
            raise ToolError(f"«{path.name}» - каталог, используй list_dir")
        try:
            limit = min(max(1, int(kwargs.get("max_bytes") or MAX_READ_BYTES)), MAX_READ_BYTES)
        except (TypeError, ValueError):
            limit = MAX_READ_BYTES
        # Читаем только нужный кусок: файл на гигабайт не должен целиком
        # попадать в память ради первых 200 КБ.
        with path.open("rb") as fh:
            data = fh.read(limit)
        text = data.decode("utf-8", "replace")
        suffix = "\n\n(файл обрезан)" if path.stat().st_size > limit else ""
        return f"Файл: {path}\n\n{text}{suffix}"


class FileWriteTool(Tool):
    name = "write_file"
    description = (
        "Создать или перезаписать текстовый файл в рабочем каталоге проекта. "
        "Промежуточные каталоги создаются автоматически."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Путь относительно рабочего каталога"},
            "content": {"type": "string", "description": "Содержимое файла"},
            "append": {"type": "boolean", "description": "Дописать в конец вместо перезаписи",
                       "default": False},
        },
        "required": ["path", "content"],
    }

    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        content = str(kwargs.get("content", ""))
        if len(content.encode("utf-8")) > MAX_WRITE_BYTES:
            raise ToolError("Слишком большой файл (лимит 2 МБ)")
        path = ctx.resolve(str(kwargs.get("path", "")))
        path.parent.mkdir(parents=True, exist_ok=True)
        if kwargs.get("append"):
            with path.open("a", encoding="utf-8") as fh:
                fh.write(content)
            action = "дописан"
        else:
            path.write_text(content, "utf-8")
            action = "записан"
        return f"Файл {action}: {path} ({len(content)} символов)"


class ListDirTool(Tool):
    name = "list_dir"
    description = "Показать содержимое каталога внутри разрешённой зоны."
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Каталог (по умолчанию корень проекта)",
                     "default": "."},
        },
    }

    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        path = ctx.resolve(str(kwargs.get("path") or "."), must_exist=True)
        if not path.is_dir():
            raise ToolError(f"«{path.name}» - не каталог")
        lines: list[str] = []
        for item in sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
            if item.name.startswith("."):
                continue
            lines.append(f"{'DIR ' if item.is_dir() else 'FILE'}  {item.name}"
                         + ("" if item.is_dir() else f"  ({_human(item)})"))
        return f"Каталог: {path}\n" + ("\n".join(lines) if lines else "(пусто)")


def _human(path: Path) -> str:
    try:
        size = path.stat().st_size
    except OSError:          # битая ссылка или файл исчез между листингом и stat
        return "?"
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024
    return f"{size:.1f} ТБ"

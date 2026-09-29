"""Датаклассы предметной области — типизированное представление строк БД."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from typing import Any


def _json(raw: str | None) -> dict:
    try:
        return json.loads(raw) if raw else {}
    except (TypeError, ValueError):
        return {}


# ---------------------------------------------------------------------------


@dataclass
class User:
    id: int
    username: str
    created_at: str
    settings: dict = field(default_factory=dict)

    @staticmethod
    def from_row(r: sqlite3.Row) -> "User":
        return User(r["id"], r["username"], r["created_at"], _json(r["settings_json"]))


@dataclass
class Workspace:
    id: int
    user_id: int
    name: str
    description: str
    settings: dict
    archived: bool
    created_at: str
    updated_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Workspace":
        return Workspace(
            r["id"], r["user_id"], r["name"], r["description"],
            _json(r["settings_json"]), bool(r["archived"]),
            r["created_at"], r["updated_at"],
        )


@dataclass
class ApiKey:
    """Метаданные ключа. Сам секрет в объект не попадает — только по запросу."""

    id: int
    user_id: int
    label: str
    provider: str
    base_url: str
    has_secret: bool
    meta: dict
    created_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "ApiKey":
        return ApiKey(
            r["id"], r["user_id"], r["label"], r["provider"], r["base_url"],
            r["secret_blob"] is not None, _json(r["meta_json"]), r["created_at"],
        )


@dataclass
class Agent:
    id: int
    workspace_id: int
    name: str
    role: str
    system_prompt: str
    api_key_id: int | None
    provider: str
    model: str
    params: dict
    enabled: bool
    status: str
    is_supervisor: bool
    created_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Agent":
        return Agent(
            r["id"], r["workspace_id"], r["name"], r["role"], r["system_prompt"],
            r["api_key_id"], r["provider"], r["model"], _json(r["params_json"]),
            bool(r["enabled"]), r["status"], bool(r["is_supervisor"]), r["created_at"],
        )

    # Параметры лежат в JSON и могли быть поправлены руками или старой
    # версией: битое значение не должно ронять запуск агента.
    @property
    def temperature(self) -> float:
        try:
            return float(self.params.get("temperature", 0.7))
        except (TypeError, ValueError):
            return 0.7

    @property
    def max_tokens(self) -> int:
        try:
            return max(1, int(self.params.get("max_tokens", 2048)))
        except (TypeError, ValueError):
            return 2048

    @property
    def tools(self) -> list[str]:
        raw = self.params.get("tools")
        return [str(t) for t in raw] if isinstance(raw, list) else []


@dataclass
class Task:
    id: int
    workspace_id: int
    title: str
    description: str
    status: str
    result_format: str
    token_limit: int | None
    created_at: str
    updated_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Task":
        return Task(
            r["id"], r["workspace_id"], r["title"], r["description"], r["status"],
            r["result_format"], r["token_limit"], r["created_at"], r["updated_at"],
        )


@dataclass
class Subtask:
    id: int
    task_id: int
    agent_id: int | None
    title: str
    description: str
    status: str
    order_index: int
    depends_on: str
    result: str
    rework_count: int
    tokens_in: int
    tokens_out: int
    cost_usd: float
    created_at: str
    updated_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Subtask":
        return Subtask(
            r["id"], r["task_id"], r["agent_id"], r["title"], r["description"],
            r["status"], r["order_index"], r["depends_on"], r["result"],
            r["rework_count"], r["tokens_in"], r["tokens_out"], r["cost_usd"],
            r["created_at"], r["updated_at"],
        )


@dataclass
class Report:
    id: int
    workspace_id: int
    task_id: int | None
    subtask_id: int | None
    agent_id: int | None
    content: str
    confidence: float | None
    tokens_in: int
    tokens_out: int
    cost_usd: float
    reviewed: bool
    review_verdict: str
    review_notes: str
    created_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Report":
        return Report(
            r["id"], r["workspace_id"], r["task_id"], r["subtask_id"], r["agent_id"],
            r["content"], r["confidence"], r["tokens_in"], r["tokens_out"],
            r["cost_usd"], bool(r["reviewed"]), r["review_verdict"],
            r["review_notes"], r["created_at"],
        )


@dataclass
class Summary:
    id: int
    workspace_id: int
    task_id: int | None
    content: str
    trigger: str
    delivered_to: str
    created_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Summary":
        return Summary(
            r["id"], r["workspace_id"], r["task_id"], r["content"],
            r["trigger"], r["delivered_to"], r["created_at"],
        )


@dataclass
class Incident:
    id: int
    workspace_id: int
    task_id: int | None
    subtask_id: int | None
    report_id: int | None
    kind: str
    severity: str
    description: str
    status: str
    resolution: str
    created_at: str
    resolved_at: str | None

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Incident":
        return Incident(
            r["id"], r["workspace_id"], r["task_id"], r["subtask_id"], r["report_id"],
            r["kind"], r["severity"], r["description"], r["status"], r["resolution"],
            r["created_at"], r["resolved_at"],
        )


@dataclass
class Budget:
    id: int
    scope: str
    scope_id: int
    token_limit: int | None
    cost_limit_usd: float | None
    tokens_used: int
    cost_used_usd: float
    alert_threshold: float
    alerted: bool
    updated_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Budget":
        return Budget(
            r["id"], r["scope"], r["scope_id"], r["token_limit"], r["cost_limit_usd"],
            r["tokens_used"], r["cost_used_usd"], r["alert_threshold"],
            bool(r["alerted"]), r["updated_at"],
        )

    def ratio(self) -> float:
        """Доля израсходованного бюджета (максимум из токенов и денег)."""
        parts: list[float] = []
        if self.token_limit:
            parts.append(self.tokens_used / self.token_limit)
        if self.cost_limit_usd:
            parts.append(self.cost_used_usd / self.cost_limit_usd)
        return max(parts) if parts else 0.0


def dumps(obj: Any) -> str:
    """Безопасная сериализация словарей настроек в TEXT-колонки."""
    return json.dumps(obj, ensure_ascii=False)

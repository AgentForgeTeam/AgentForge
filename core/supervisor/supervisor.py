"""Этап 5 — служба супервайзера.

Обязанности:
* проверять отчёты агентов по чек-листу и выносить вердикт;
* возвращать работу на доработку (не более ``max_rework_rounds`` раз);
* составлять анонимные сводки и рассылать их всем агентам;
* находить противоречия между результатами и заводить инциденты;
* эскалировать пользователю то, что не разрешается автоматически.

Модель супервайзера выбирается в настройках воркспейса: либо один из
подключённых агентов со своим API-ключом, либо локальная модель через
OpenAI-совместимый endpoint (Ollama, по умолчанию Qwen) — она работает
офлайн и ничего не стоит.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from core.events import Event, EventBus, EventType
from core.supervisor.checklist import (
    CONFLICT_SYSTEM,
    REVIEW_SYSTEM,
    REVIEW_USER,
    SUMMARY_SYSTEM,
    SUMMARY_USER,
    Anonymizer,
    Conflict,
    Verdict,
    parse_conflicts,
    parse_verdict,
)
from providers.base import ChatMessage, LLMProvider, ProviderError
from providers.factory import build_provider, estimate_cost
from storage.models import Report, Subtask, Task
from storage.repositories import Repos

log = logging.getLogger("aiorc.supervisor")

#: сколько последних результатов подмешивать в контекст проверки
CONTEXT_REPORTS = 6
#: предел длины одного отчёта в промпте супервайзера
REPORT_CLIP = 6000


@dataclass
class SupervisorModel:
    """Чем именно работает супервайзер в этом прогоне."""

    provider: LLMProvider
    model: str
    provider_key: str
    source: str          # "api" | "local"
    label: str


class Supervisor:
    """Проверяющий над командой агентов."""

    def __init__(self, repos: Repos, bus: EventBus, workspace_id: int,
                 settings: dict) -> None:
        self.repos = repos
        self.bus = bus
        self.workspace_id = workspace_id
        self.settings = settings
        self.anon = Anonymizer()
        self._model: SupervisorModel | None = None
        self._summary_task: asyncio.Task | None = None
        self._stop = asyncio.Event()

    # -- модель --------------------------------------------------------------
    def available(self) -> bool:
        """Можно ли вообще запустить супервайзера с текущими настройками."""
        try:
            return self._resolve_model() is not None
        except Exception:  # noqa: BLE001
            return False

    def _resolve_model(self) -> SupervisorModel | None:
        """Создаёт провайдера супервайзера один раз на прогон."""
        if self._model is not None:
            return self._model

        mode = self.settings.get("supervisor_mode", "api")

        if mode == "local":
            base_url = (self.settings.get("supervisor_local_base_url")
                        or "http://localhost:11434/v1")
            model_name = self.settings.get("supervisor_local_model") or "qwen2.5:7b-instruct"
            provider = build_provider("ollama", "", base_url, timeout=180)
            self._model = SupervisorModel(provider, model_name, "ollama", "local",
                                          f"локальная модель {model_name}")
            return self._model

        agent_id = self.settings.get("supervisor_agent_id")
        agent = self.repos.agents.get(int(agent_id)) if agent_id else None
        if agent is None:
            # Запасной вариант: агент, помеченный звёздочкой в списке.
            agent = next((a for a in self.repos.agents.list(self.workspace_id)
                          if a.is_supervisor), None)
        if agent is None or not agent.model or not agent.api_key_id:
            return None

        key = self.repos.keys.get(agent.api_key_id)
        if key is None:
            return None
        secret = self.repos.keys.reveal(agent.api_key_id)
        provider = build_provider(agent.provider, secret, key.base_url, timeout=180)
        self._model = SupervisorModel(provider, agent.model, agent.provider, "api",
                                      f"{agent.name} ({agent.model})")
        return self._model

    async def aclose(self) -> None:
        self._stop.set()
        if self._summary_task:
            self._summary_task.cancel()
            self._summary_task = None
        if self._model is not None:
            try:
                await self._model.provider.aclose()
            except Exception:  # noqa: BLE001
                pass
            self._model = None

    # -- вызов модели --------------------------------------------------------
    async def _ask(self, system: str, user: str, task_id: int | None,
                   max_tokens: int = 1600) -> str:
        """Один вызов модели супервайзера с учётом расхода."""
        model = self._resolve_model()
        if model is None:
            raise RuntimeError(
                "Супервайзер не настроен: выберите агента или локальную модель "
                "на вкладке «Настройки»."
            )
        result = await model.provider.complete(
            model.model,
            [ChatMessage("system", system), ChatMessage("user", user)],
            temperature=0.2,          # проверка требует предсказуемости
            max_tokens=max_tokens,
        )
        cost = estimate_cost(model.provider_key, model.model,
                             result.usage.input_tokens, result.usage.output_tokens)
        self.repos.budgets.log_call(
            self.workspace_id, task_id, None, None,
            model.provider_key, model.model,
            result.usage.input_tokens, result.usage.output_tokens, cost,
        )
        return result.text

    def _emit(self, kind: EventType, message: str, **payload) -> None:
        self.bus.emit(Event(kind, workspace_id=self.workspace_id,
                            agent_name="Супервайзер", message=message,
                            payload=payload))

    # -- проверка отчёта -----------------------------------------------------
    async def review(self, task: Task, subtask: Subtask, report: Report) -> Verdict:
        """Проверяет отчёт по чек-листу и возвращает вердикт."""
        label = self.anon.label(report.agent_id)
        context = self._accepted_context(task.id, exclude_subtask=subtask.id)

        user = REVIEW_USER.format(
            task=f"{task.title}\n{task.description}"[:4000],
            subtask=f"{subtask.title}\n{subtask.description}"[:2000],
            label=label,
            confidence=(f"{report.confidence:.2f}" if report.confidence is not None
                        else "не указана"),
            report=report.content[:REPORT_CLIP],
            context=(f"\nРАНЕЕ ПРИНЯТЫЕ РЕЗУЛЬТАТЫ ПРОЕКТА\n{context}" if context else ""),
        )

        self._emit(EventType.AGENT_THINKING, f"проверяю «{subtask.title}»")
        try:
            raw = await self._ask(REVIEW_SYSTEM, user, task.id)
        except ProviderError as exc:
            log.warning("Супервайзер недоступен: %s", exc)
            # Недоступность проверяющего не должна ронять весь прогон:
            # отчёт принимается, но факт пропуска проверки фиксируется.
            self._emit(EventType.ERROR, f"проверка пропущена: {exc}")
            return Verdict(verdict="ok", notes=f"Проверка не выполнена: {exc}")

        verdict = parse_verdict(raw)
        self.repos.reports.mark_reviewed(report.id, verdict.verdict, verdict.notes)

        for issue in verdict.issues:
            incident_id = self.repos.incidents.add(
                self.workspace_id, kind=issue.kind, description=issue.description,
                severity=issue.severity, task_id=task.id, subtask_id=subtask.id,
                report_id=report.id,
            )
            self._emit(EventType.INCIDENT_CREATED,
                       f"{issue.kind}: {issue.description[:120]}",
                       incident_id=incident_id, severity=issue.severity)

        message = {
            "ok": f"принято: «{subtask.title}»",
            "rework": f"на доработку: «{subtask.title}»",
            "conflict": f"конфликт данных: «{subtask.title}»",
        }.get(verdict.verdict, verdict.verdict)
        self._emit(EventType.REPORT_REVIEWED, message,
                   verdict=verdict.verdict, subtask_id=subtask.id)
        return verdict

    def _accepted_context(self, task_id: int, exclude_subtask: int | None = None) -> str:
        """Обезличенная выжимка уже принятых результатов проекта."""
        chunks: list[str] = []
        for st in self.repos.tasks.subtasks(task_id):
            if st.id == exclude_subtask or not st.result:
                continue
            if st.status not in ("done", "review"):
                continue
            chunks.append(f"[{self.anon.label(st.agent_id)}] {st.title}:\n"
                          f"{st.result[:1200]}")
        return "\n\n".join(chunks[-CONTEXT_REPORTS:])

    # -- сводки --------------------------------------------------------------
    async def make_summary(self, task: Task, trigger: str = "manual") -> str:
        """Составляет анонимную сводку и «рассылает» её всем агентам.

        Рассылка означает запись в таблицу ``summaries``: каждый агент
        подхватывает последнюю сводку при следующем запуске, не зная,
        кто из коллег что написал.
        """
        materials = self._summary_materials(task.id)
        if not materials:
            return ""

        self._emit(EventType.AGENT_THINKING, "составляю сводку")
        try:
            raw = await self._ask(
                SUMMARY_SYSTEM,
                SUMMARY_USER.format(task=f"{task.title}\n{task.description}"[:3000],
                                    reports=materials),
                task.id,
                max_tokens=1200,
            )
        except (ProviderError, RuntimeError) as exc:
            self._emit(EventType.ERROR, f"сводка не составлена: {exc}")
            return ""

        # Страховка: вычищаем имена агентов, если модель их всё-таки назвала.
        names = {a.id: a.name for a in self.repos.agents.list(self.workspace_id)}
        content = self.anon.scrub(raw.strip(), names)
        if not content:
            return ""

        recipients = [a.id for a in self.repos.agents.list(self.workspace_id)
                      if a.enabled and not a.is_supervisor]
        summary_id = self.repos.reports.add_summary(
            self.workspace_id, task.id, content, trigger, recipients
        )
        self._emit(EventType.SUMMARY_CREATED,
                   f"сводка разослана ({len(recipients)} получателей, {trigger})",
                   summary_id=summary_id, trigger=trigger)
        return content

    def _summary_materials(self, task_id: int) -> str:
        """Обезличенные материалы для сводки."""
        chunks: list[str] = []
        for st in self.repos.tasks.subtasks(task_id):
            if not st.result:
                continue
            chunks.append(f"[{self.anon.label(st.agent_id)}] {st.title}:\n"
                          f"{st.result[:2500]}")
        return "\n\n".join(chunks[-CONTEXT_REPORTS:])

    def start_timer(self, task: Task) -> None:
        """Запускает периодическую рассылку сводок по таймеру."""
        minutes = int(self.settings.get("summary_interval_minutes", 15) or 0)
        if minutes <= 0 or self._summary_task is not None:
            return

        async def loop() -> None:
            try:
                while not self._stop.is_set():
                    await asyncio.sleep(minutes * 60)
                    if self._stop.is_set():
                        return
                    await self.make_summary(task, trigger="timer")
            except asyncio.CancelledError:
                raise
            except Exception:  # noqa: BLE001
                log.exception("Сбой периодической сводки")

        self._summary_task = asyncio.ensure_future(loop())
        self._emit(EventType.LOG, f"сводки по таймеру: раз в {minutes} мин")

    # -- конфликты -----------------------------------------------------------
    async def find_conflicts(self, task: Task) -> list[Conflict]:
        """Ищет прямые противоречия между результатами подзадач.

        Противоречие требует как минимум двух результатов, поэтому при одном
        готовом результате вызов модели пропускается — это экономит токены,
        а не срезает проверку.
        """
        with_results = [s for s in self.repos.tasks.subtasks(task.id) if s.result.strip()]
        if len(with_results) < 2:
            return []
        materials = self._summary_materials(task.id)
        if not materials:
            return []

        try:
            raw = await self._ask(
                CONFLICT_SYSTEM,
                SUMMARY_USER.format(task=f"{task.title}\n{task.description}"[:3000],
                                    reports=materials),
                task.id,
                max_tokens=1200,
            )
        except (ProviderError, RuntimeError) as exc:
            self._emit(EventType.ERROR, f"поиск конфликтов пропущен: {exc}")
            return []

        conflicts = parse_conflicts(raw)
        for conflict in conflicts:
            resolved = conflict.auto_resolvable and bool(conflict.resolution)
            incident_id = self.repos.incidents.add(
                self.workspace_id, kind="conflict", description=conflict.description,
                severity=conflict.severity, task_id=task.id,
            )
            if resolved:
                self.repos.incidents.resolve(incident_id, "auto_resolved",
                                             conflict.resolution)
                self._emit(EventType.INCIDENT_CREATED,
                           f"конфликт разрешён автоматически: {conflict.description[:100]}",
                           incident_id=incident_id, resolved=True)
            else:
                self.repos.incidents.resolve(incident_id, "escalated",
                                             "Требуется решение пользователя")
                self._emit(EventType.INCIDENT_CREATED,
                           f"конфликт эскалирован: {conflict.description[:100]}",
                           incident_id=incident_id, resolved=False,
                           severity=conflict.severity)
        if conflicts:
            self._emit(EventType.LOG, f"найдено расхождений: {len(conflicts)}")
        return conflicts

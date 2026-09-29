"""Этап 6 — дашборд реального времени.

Собирает в одном месте всё, что происходит в воркспейсе: статус каждого
агента, прогресс по задаче и подзадачам, кривые расхода токенов и денег,
объединённую ленту отчётов и сводок, историю инцидентов.

Обновление идёт по событиям шины, но с троттлингом: во время прогона
события летят пачками, и перерисовывать всё на каждое — лишняя работа.
Таймер собирает их в один апдейт не чаще раза в секунду.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from core.events import Event, EventBus, EventType
from storage.db import local_time
from storage.repositories import Repos
from ui.pages.supervisor_page import KIND_TITLES
from ui.theme import STATUS_COLORS
from ui.widgets.charts import Bar, BarChart, LineChart, SegmentBar, SeriesPoint
from ui.widgets.common import Card, EmptyState, Header, StatusBadge

#: не чаще одного перерисовывания в секунду
REFRESH_THROTTLE_MS = 1000
#: сколько записей показывать в ленте
FEED_LIMIT = 40
#: точек на кривой расхода
SERIES_LIMIT = 300

AGENT_COLORS = ["#6c8cff", "#3ecf8e", "#f0b429", "#b07cff", "#ef5f6b",
                "#4fc3f7", "#ff9e64", "#7ee787"]


class Metric(QWidget):
    """Одна крупная цифра с подписью."""

    def __init__(self, caption: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(1)
        self.value = QLabel("—")
        self.value.setObjectName("H1")
        lay.addWidget(self.value)
        self.caption = QLabel(caption)
        self.caption.setObjectName("Dim")
        lay.addWidget(self.caption)

    def set(self, value: str, colour: str = "") -> None:
        self.value.setText(value)
        self.value.setStyleSheet(f"color: {colour};" if colour else "")

    def set_caption(self, caption: str) -> None:
        self.caption.setText(caption)


class DashboardPage(QWidget):
    """Сводная картина по активному воркспейсу."""

    def __init__(self, repos: Repos, bus: EventBus) -> None:
        super().__init__()
        self.repos = repos
        self.bus = bus
        self.workspace_id: int | None = None

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(REFRESH_THROTTLE_MS)
        self._timer.timeout.connect(self.refresh)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        self.header = Header(tr("dash.title"), tr("dash.subtitle"))
        refresh_button = QPushButton(tr("common.refresh"))
        refresh_button.clicked.connect(self.refresh)
        self.header.add_action(refresh_button)
        root.addWidget(self.header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        body = QVBoxLayout(page)
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(14)

        body.addWidget(self._build_metrics())
        body.addWidget(self._build_progress())

        charts_row = QHBoxLayout()
        charts_row.setSpacing(14)
        charts_row.addWidget(self._build_cost_chart(), 1)
        charts_row.addWidget(self._build_agents_chart(), 1)
        body.addLayout(charts_row)

        body.addWidget(self._build_agents_card())

        feeds_row = QHBoxLayout()
        feeds_row.setSpacing(14)
        feeds_row.addWidget(self._build_feed_card(), 3)
        feeds_row.addWidget(self._build_incidents_card(), 2)
        body.addLayout(feeds_row)
        body.addStretch(1)

        self.bus.subscribe(self._on_event)

    # -- построение ----------------------------------------------------------
    def _build_metrics(self) -> Card:
        card = Card(self)
        grid = QGridLayout()
        grid.setSpacing(18)
        self.m_agents = Metric(tr("dash.m_agents"))
        self.m_subtasks = Metric(tr("dash.m_subtasks"))
        self.m_tokens = Metric(tr("dash.m_tokens"))
        self.m_cost = Metric(tr("dash.m_cost"))
        self.m_reworks = Metric(tr("dash.m_reworks"))
        self.m_open = Metric(tr("dash.m_open_incidents"))
        for i, metric in enumerate((self.m_agents, self.m_subtasks, self.m_tokens,
                                    self.m_cost, self.m_reworks, self.m_open)):
            grid.addWidget(metric, 0, i)
        card.body.addLayout(grid)
        return card

    def _build_progress(self) -> Card:
        card = Card(self, spacing=8)
        row = QHBoxLayout()
        self.task_title = QLabel(tr("task.no_task"))
        self.task_title.setObjectName("H2")
        self.task_title.setWordWrap(True)
        row.addWidget(self.task_title, 1)
        self.progress_label = QLabel("")
        self.progress_label.setObjectName("Dim")
        row.addWidget(self.progress_label)
        card.body.addLayout(row)

        self.progress_bar = SegmentBar()
        card.body.addWidget(self.progress_bar)

        self.legend = QLabel("")
        self.legend.setObjectName("Dim")
        self.legend.setWordWrap(True)
        card.body.addWidget(self.legend)
        return card

    def _build_cost_chart(self) -> Card:
        card = Card(self, spacing=6)
        self.cost_chart = LineChart(tr("dash.cost_chart"), unit="usd")
        self.cost_chart.empty_text = tr("dash.no_usage")
        card.body.addWidget(self.cost_chart)
        self.tokens_chart = LineChart(tr("dash.tokens_chart"), unit="tokens")
        self.tokens_chart.empty_text = tr("dash.no_usage")
        card.body.addWidget(self.tokens_chart)
        return card

    def _build_agents_chart(self) -> Card:
        card = Card(self, spacing=6)
        self.agent_chart = BarChart(tr("dash.by_agent"), unit="tokens")
        self.agent_chart.empty_text = tr("dash.no_usage")
        card.body.addWidget(self.agent_chart)
        return card

    def _build_agents_card(self) -> Card:
        card = Card(self, spacing=8)
        title = QLabel(tr("dash.agents"))
        title.setObjectName("H2")
        card.body.addWidget(title)
        self.agents_box = QVBoxLayout()
        self.agents_box.setSpacing(4)
        card.body.addLayout(self.agents_box)
        return card

    def _build_feed_card(self) -> Card:
        card = Card(self, spacing=8)
        title = QLabel(tr("dash.feed"))
        title.setObjectName("H2")
        card.body.addWidget(title)
        self.feed_box = QVBoxLayout()
        self.feed_box.setSpacing(6)
        card.body.addLayout(self.feed_box)
        return card

    def _build_incidents_card(self) -> Card:
        card = Card(self, spacing=8)
        title = QLabel(tr("dash.incidents"))
        title.setObjectName("H2")
        card.body.addWidget(title)
        self.incidents_box = QVBoxLayout()
        self.incidents_box.setSpacing(6)
        card.body.addLayout(self.incidents_box)
        return card

    # -- данные --------------------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        _clear(self.agents_box)
        _clear(self.feed_box)
        _clear(self.incidents_box)

        if self.workspace_id is None:
            self.task_title.setText(tr("ws.empty"))
            self.progress_label.setText("")
            self.legend.setText("")
            self.progress_bar.set_segments([])
            for metric in (self.m_agents, self.m_subtasks, self.m_tokens,
                           self.m_cost, self.m_reworks, self.m_open):
                metric.set("—")
            self.cost_chart.set_points([])
            self.tokens_chart.set_points([])
            self.agent_chart.set_bars([])
            self.agents_box.addWidget(EmptyState(tr("ws.empty")))
            return

        agents = self.repos.agents.list(self.workspace_id)
        task = self.repos.tasks.current(self.workspace_id)
        subtasks = self.repos.tasks.subtasks(task.id) if task else []

        self._fill_metrics(agents, task, subtasks)
        self._fill_progress(task, subtasks)
        self._fill_charts(agents)
        self._fill_agents(agents, subtasks)
        self._fill_feed()
        self._fill_incidents()

    def _fill_metrics(self, agents, task, subtasks) -> None:
        tokens, cost = self.repos.budgets.workspace_totals(self.workspace_id)
        counts = self.repos.budgets.incident_counts(self.workspace_id)
        open_count = counts.get("open", 0) + counts.get("escalated", 0)
        done = sum(1 for s in subtasks if s.status == "done")
        reworks = sum(s.rework_count for s in subtasks)

        self.m_agents.set(str(len(agents)))
        self.m_subtasks.set(f"{done} / {len(subtasks)}" if subtasks else "—")
        self.m_tokens.set(f"{tokens:,}".replace(",", " "))
        self.m_cost.set(f"${cost:.4f}" if cost < 1 else f"${cost:,.2f}".replace(",", " "))
        self.m_reworks.set(str(reworks), STATUS_COLORS["rework"] if reworks else "")
        self.m_open.set(str(open_count), STATUS_COLORS["error"] if open_count else "")

        if task and task.token_limit:
            share = tokens / task.token_limit
            self.m_tokens.set_caption(
                tr("dash.m_tokens_limit", pct=f"{share * 100:.0f}",
                   limit=f"{task.token_limit:,}".replace(",", " "))
            )
        else:
            self.m_tokens.set_caption(tr("dash.m_tokens"))

    def _fill_progress(self, task, subtasks) -> None:
        if task is None:
            self.task_title.setText(tr("task.no_task"))
            self.progress_label.setText("")
            self.legend.setText("")
            self.progress_bar.set_segments([])
            return

        self.task_title.setText(task.title or tr("task.title"))
        order = ["done", "review", "rework", "running", "error", "paused", "idle"]
        buckets = {key: 0 for key in order}
        for subtask in subtasks:
            buckets[subtask.status] = buckets.get(subtask.status, 0) + 1

        self.progress_bar.set_segments(
            [(tr(f"status.{key}"), buckets.get(key, 0), STATUS_COLORS.get(key, "#888"))
             for key in order]
        )
        done = buckets.get("done", 0)
        total = len(subtasks)
        percent = (done / total * 100) if total else 0
        self.progress_label.setText(f"{done} / {total}  ·  {percent:.0f}%")
        self.legend.setText("   ".join(
            f"{tr(f'status.{key}')}: {buckets[key]}" for key in order if buckets.get(key)
        ) or tr("task.subtasks"))

    def _fill_charts(self, agents) -> None:
        series = self.repos.budgets.usage_series(self.workspace_id, SERIES_LIMIT)
        cost_points: list[SeriesPoint] = []
        token_points: list[SeriesPoint] = []
        cost_acc = 0.0
        token_acc = 0
        for created_at, tokens, cost in series:
            cost_acc += cost
            token_acc += tokens
            label = local_time(created_at, "%H:%M")
            cost_points.append(SeriesPoint(label, cost_acc))
            token_points.append(SeriesPoint(label, float(token_acc)))
        self.cost_chart.set_points(cost_points)
        self.tokens_chart.set_points(token_points)

        names = {a.id: a.name for a in agents}
        bars: list[Bar] = []
        for i, (agent_id, tokens, _cost) in enumerate(
            self.repos.budgets.usage_by_agent(self.workspace_id)
        ):
            if not tokens:
                continue
            label = names.get(agent_id) if agent_id else tr("dash.supervisor_line")
            bars.append(Bar(label or tr("dash.supervisor_line"), float(tokens),
                            AGENT_COLORS[i % len(AGENT_COLORS)]))
        self.agent_chart.set_bars(bars[:10])

    def _fill_agents(self, agents, subtasks) -> None:
        if not agents:
            self.agents_box.addWidget(EmptyState(tr("agents.empty")))
            return
        usage = {agent_id: (tokens, cost) for agent_id, tokens, cost
                 in self.repos.budgets.usage_by_agent(self.workspace_id)}
        assigned: dict[int, str] = {}
        for subtask in subtasks:
            if subtask.agent_id and subtask.status in ("running", "rework"):
                assigned[subtask.agent_id] = subtask.title

        for agent in agents:
            row = QWidget()
            line = QHBoxLayout(row)
            line.setContentsMargins(0, 0, 0, 0)
            line.setSpacing(10)

            name = QLabel(agent.name + ("  ⭐" if agent.is_supervisor else ""))
            line.addWidget(name)

            current = assigned.get(agent.id)
            if current:
                doing = QLabel("→ " + _elide(current, 38))
                doing.setObjectName("Dim")
                line.addWidget(doing)
            line.addStretch(1)

            tokens, cost = usage.get(agent.id, (0, 0.0))
            spent = QLabel(f"{tokens:,}".replace(",", " ") + f" · ${cost:.4f}")
            spent.setObjectName("Dim")
            line.addWidget(spent)
            line.addWidget(StatusBadge(agent.status))
            self.agents_box.addWidget(row)

    def _fill_feed(self) -> None:
        """Объединённая лента отчётов и сводок, новое сверху."""
        entries: list[tuple[str, str, str, str]] = []   # (время, метка, текст, цвет)
        names = {a.id: a.name for a in self.repos.agents.list(self.workspace_id)}

        for report in self.repos.reports.list_reports(self.workspace_id, limit=FEED_LIMIT):
            verdict = {"ok": tr("dash.v_ok"), "rework": tr("dash.v_rework"),
                       "conflict": tr("dash.v_conflict")}.get(report.review_verdict, "")
            colour = {"ok": STATUS_COLORS["done"], "rework": STATUS_COLORS["rework"],
                      "conflict": STATUS_COLORS["error"]}.get(
                          report.review_verdict, STATUS_COLORS["idle"])
            confidence = (f"  ·  {tr('dash.confidence')} {report.confidence:.2f}"
                          if report.confidence is not None else "")
            entries.append((
                report.created_at,
                names.get(report.agent_id, tr("dash.unknown_agent")),
                f"{_elide(report.content.strip().replace(chr(10), ' '), 150)}"
                f"{confidence}{('  ·  ' + verdict) if verdict else ''}",
                colour,
            ))

        for summary in self.repos.reports.list_summaries(self.workspace_id,
                                                         limit=FEED_LIMIT):
            entries.append((
                summary.created_at,
                tr("dash.summary_line"),
                _elide(summary.content.strip().replace("\n", " "), 150),
                "#b07cff",
            ))

        entries.sort(key=lambda e: e[0], reverse=True)
        if not entries:
            self.feed_box.addWidget(EmptyState(tr("dash.no_feed")))
            return

        for created_at, who, text, colour in entries[:FEED_LIMIT]:
            item = QWidget()
            lay = QVBoxLayout(item)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(1)

            head = QHBoxLayout()
            author = QLabel(who)
            author.setStyleSheet(f"color: {colour}; font-weight: 600;")
            head.addWidget(author)
            head.addStretch(1)
            when = QLabel(local_time(created_at, "%H:%M:%S"))
            when.setObjectName("Dim")
            head.addWidget(when)
            lay.addLayout(head)

            body = QLabel(text)
            body.setObjectName("Dim")
            body.setWordWrap(True)
            lay.addWidget(body)
            self.feed_box.addWidget(item)

    def _fill_incidents(self) -> None:
        incidents = self.repos.incidents.list(self.workspace_id, limit=FEED_LIMIT)
        if not incidents:
            self.incidents_box.addWidget(EmptyState(tr("sup.no_incidents")))
            return
        severity_colours = {"low": STATUS_COLORS["idle"], "medium": STATUS_COLORS["rework"],
                            "high": STATUS_COLORS["error"]}
        statuses = {"open": tr("dash.i_open"), "escalated": tr("dash.i_escalated"),
                    "auto_resolved": tr("dash.i_auto"), "resolved": tr("dash.i_resolved")}
        for incident in incidents:
            item = QWidget()
            lay = QVBoxLayout(item)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(1)

            head = QHBoxLayout()
            kind = QLabel(KIND_TITLES.get(incident.kind, incident.kind))
            kind.setStyleSheet(
                f"color: {severity_colours.get(incident.severity, '#888')}; font-weight: 600;"
            )
            head.addWidget(kind)
            head.addStretch(1)
            status = QLabel(statuses.get(incident.status, incident.status))
            status.setObjectName("Dim")
            head.addWidget(status)
            lay.addLayout(head)

            description = QLabel(_elide(incident.description, 140))
            description.setObjectName("Dim")
            description.setWordWrap(True)
            lay.addWidget(description)
            self.incidents_box.addWidget(item)

    # -- реакция на события --------------------------------------------------
    def _on_event(self, event: Event) -> None:
        """Ставит обновление в очередь, а не перерисовывает всё немедленно."""
        if event.type in (EventType.AGENT_THINKING, EventType.AGENT_TOOL_CALL,
                          EventType.AGENT_TOOL_RESULT):
            return
        if not self._timer.isActive():
            self._timer.start()


def _elide(text: str, limit: int) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _clear(layout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()

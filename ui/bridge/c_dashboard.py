"""Дашборд: метрики, прогресс, кривые расхода, агенты, лента и инциденты.

Во время прогона события идут пачками, поэтому перерисовка собирается
таймером не чаще раза в секунду; шаги рассуждений дашборд не интересуют.
"""

from __future__ import annotations

from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot

from app.i18n import tr
from core.events import EventType
from ui.bridge.c_agents import ROLE_ICONS
from ui.bridge.core import Controller, elide, fmt_money, fmt_tokens, status_title, when
from ui.bridge.listmodel import DictListModel

THROTTLE_MS = 1000
SERIES_LIMIT = 300
FEED_LIMIT = 40
STATUS_ORDER = ["done", "review", "rework", "running", "paused", "error", "idle"]
QUIET = {EventType.AGENT_THINKING, EventType.AGENT_DELTA, EventType.AGENT_TOOL_CALL,
         EventType.AGENT_TOOL_RESULT}


class DashboardController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._agents = DictListModel(["id", "name", "icon", "status", "statusTitle",
                                      "doing", "tokens", "cost", "share", "isSupervisor"],
                                     parent=self)
        self._feed = DictListModel(["id", "who", "when", "text", "tone", "badge",
                                    "confidence"], parent=self)
        self._incidents = DictListModel(["id", "kindTitle", "tone", "statusTitle",
                                         "description", "when"], parent=self)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(THROTTLE_MS)
        self._timer.timeout.connect(self.refresh)
        self._set(agentsCount=0, done=0, total=0, tokens=0, tokensText="0", cost=0.0,
                  costText="$0", reworks=0, openIncidents=0, limitPct=-1.0,
                  taskTitle="", segments=[], costSeries=[], tokenSeries=[], bars=[],
                  supervisorShare=0.0)

    def _p(name, type_=str, default="", sig=changed):  # noqa: N805
        return Property(type_, lambda self: self._s.get(name, default), notify=sig)

    agentsCount = _p("agentsCount", int, 0)
    done = _p("done", int, 0)
    total = _p("total", int, 0)
    tokens = _p("tokens", float, 0.0)
    tokensText = _p("tokensText")
    cost = _p("cost", float, 0.0)
    costText = _p("costText")
    reworks = _p("reworks", int, 0)
    openIncidents = _p("openIncidents", int, 0)
    limitPct = _p("limitPct", float, -1.0)
    taskTitle = _p("taskTitle")
    supervisorShare = _p("supervisorShare", float, 0.0)
    segments = _p("segments", "QVariantList", [])
    costSeries = _p("costSeries", "QVariantList", [])
    tokenSeries = _p("tokenSeries", "QVariantList", [])
    bars = _p("bars", "QVariantList", [])

    def _m(attr):  # noqa: N805
        return Property(QObject, lambda self: getattr(self, attr), constant=True)

    agentsModel = _m("_agents")
    feed = _m("_feed")
    incidents = _m("_incidents")

    def schedule(self) -> None:
        if self.ready and not self._timer.isActive():
            self._timer.start()

    def on_event(self, event) -> None:
        if event.type not in QUIET:
            self.schedule()

    def reset(self) -> None:
        super().reset()
        self._timer.stop()
        for m in (self._agents, self._feed, self._incidents):
            m.clear()

    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            for m in (self._agents, self._feed, self._incidents):
                m.clear()
            self._set(agentsCount=0, done=0, total=0, tokens=0.0, tokensText="0",
                      cost=0.0, costText="$0", reworks=0, openIncidents=0, limitPct=-1.0,
                      taskTitle="", segments=[], costSeries=[], tokenSeries=[], bars=[],
                      supervisorShare=0.0)
            return
        ws_id = self.ws_id
        agents = self.repos.agents.list(ws_id)
        task = self.repos.tasks.current(ws_id)
        subtasks = self.repos.tasks.subtasks(task.id) if task else []
        tokens, cost = self.repos.budgets.workspace_totals(ws_id)
        counts = self.repos.budgets.incident_counts(ws_id)

        buckets = {k: 0 for k in STATUS_ORDER}
        for s in subtasks:
            buckets[s.status] = buckets.get(s.status, 0) + 1
        segments = [{"status": k, "title": status_title(k), "count": buckets[k]}
                    for k in STATUS_ORDER if buckets.get(k)]

        series = self.repos.budgets.usage_series(ws_id, SERIES_LIMIT)
        cost_acc = token_acc = 0.0
        cost_series, token_series = [], []
        for created, t, c in series:
            cost_acc += c
            token_acc += t
            label = when(created, "%H:%M")
            cost_series.append({"label": label, "value": round(cost_acc, 6)})
            token_series.append({"label": label, "value": token_acc})

        names = {a.id: a for a in agents}
        usage = self.repos.budgets.usage_by_agent(ws_id)
        total_tokens = sum(t for _, t, _ in usage) or 1
        bars = []
        for agent_id, t, c in usage:
            if not t:
                continue
            a = names.get(agent_id) if agent_id else None
            label = a.name if a else (tr("dash.supervisor_line") if agent_id is None
                                      else tr("dash.unknown_agent"))
            bars.append({"label": label, "value": t, "text": fmt_tokens(t),
                         "cost": fmt_money(c), "supervisor": agent_id is None})
        supervisor_tokens = sum(t for aid, t, _ in usage if aid is None)

        limit_pct = -1.0
        if task and task.token_limit:
            task_tokens, _ = self.repos.budgets.task_totals(task.id)
            limit_pct = min(task_tokens / task.token_limit, 9.99)

        self._set(agentsCount=len(agents), done=buckets.get("done", 0), total=len(subtasks),
                  tokens=float(tokens), tokensText=fmt_tokens(tokens), cost=float(cost),
                  costText=fmt_money(cost), reworks=sum(s.rework_count for s in subtasks),
                  openIncidents=counts.get("open", 0) + counts.get("escalated", 0),
                  limitPct=limit_pct, taskTitle=task.title if task else "",
                  segments=segments, costSeries=cost_series, tokenSeries=token_series,
                  bars=bars[:10], supervisorShare=supervisor_tokens / total_tokens)

        per_agent = {aid: (t, c) for aid, t, c in usage}
        doing = {s.agent_id: s.title for s in subtasks
                 if s.agent_id and s.status in ("running", "rework")}
        self._agents.set_items([
            {"id": a.id, "name": a.name, "icon": ROLE_ICONS.get(a.role or "custom", "bot"),
             "status": a.status, "statusTitle": status_title(a.status),
             "doing": doing.get(a.id, ""),
             "tokens": fmt_tokens(per_agent.get(a.id, (0, 0))[0]),
             "cost": fmt_money(per_agent.get(a.id, (0, 0.0))[1]),
             "share": per_agent.get(a.id, (0, 0))[0] / total_tokens,
             "isSupervisor": a.is_supervisor}
            for a in agents])
        self._fill_feed(names)
        self._incidents.set_items([
            {"id": i.id, "kindTitle": tr(f"kind.{i.kind}"),
             "tone": {"low": "muted", "medium": "warning", "high": "error"}.get(i.severity, "warning"),
             "statusTitle": tr(f"inc.{i.status}"), "description": elide(i.description, 160),
             "when": when(i.created_at)}
            for i in self.repos.incidents.list(ws_id, limit=FEED_LIMIT)])

    def _fill_feed(self, names: dict) -> None:
        entries = []
        verdicts = {"ok": ("dash.v_ok", "success"), "rework": ("dash.v_rework", "warning"),
                    "conflict": ("dash.v_conflict", "error"),
                    "unverified": ("dash.v_unverified", "error")}
        for r in self.repos.reports.list_reports(self.ws_id, limit=FEED_LIMIT):
            badge, tone = verdicts.get(r.review_verdict, ("", "muted"))
            agent = names.get(r.agent_id)
            entries.append({"id": f"r{r.id}", "who": agent.name if agent else tr("dash.unknown_agent"),
                            "when_raw": r.created_at, "when": when(r.created_at, "%H:%M:%S"),
                            "text": elide(r.content, 180), "tone": tone,
                            "badge": tr(badge) if badge else "",
                            "confidence": f"{r.confidence:.2f}" if r.confidence is not None else ""})
        for s in self.repos.reports.list_summaries(self.ws_id, limit=FEED_LIMIT):
            entries.append({"id": f"s{s.id}", "who": tr("dash.summary_line"),
                            "when_raw": s.created_at, "when": when(s.created_at, "%H:%M:%S"),
                            "text": elide(s.content, 180), "tone": "violet", "badge": "",
                            "confidence": ""})
        entries.sort(key=lambda e: e["when_raw"], reverse=True)
        for e in entries:
            e.pop("when_raw", None)
        self._feed.set_items(entries[:FEED_LIMIT])

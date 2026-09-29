"""Экспорт результата: формат с объяснением выбора, состав, путь сохранения."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Property, Signal, Slot

from app.config import PATHS
from app.i18n import tr
from core.export.bundle import ExportOptions, collect, detect_format
from core.export.exporters import ExportError, export, suggest_filename
from ui.bridge.core import Controller, error_text

FORMATS = [("markdown", "file-text"), ("docx", "file-type"), ("pdf", "book-open"),
           ("zip", "file-archive")]
OPTIONS = ["results", "reports", "summaries", "incidents", "decisions", "stats",
           "files", "anon"]
DEFAULT_OPTIONS = {"results": True, "reports": False, "summaries": False,
                   "incidents": True, "decisions": False, "stats": True,
                   "files": True, "anon": False}


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024:
            return f"{value:.0f} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


class ExportController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._bundle = None
        self._set(format="markdown", recommended="markdown", reason="", stats="",
                  path="", canExport=False, options=dict(DEFAULT_OPTIONS),
                  lastPath="", lastInfo="", exporting=False, nothing=True)

    def _p(name, type_=str, default="", sig=changed):  # noqa: N805
        return Property(type_, lambda self: self._s.get(name, default), notify=sig)

    format = _p("format")
    recommended = _p("recommended")
    reason = _p("reason")
    stats = _p("stats")
    path = _p("path")
    canExport = _p("canExport", bool, False)
    options = _p("options", "QVariantMap", {})
    lastPath = _p("lastPath")
    lastInfo = _p("lastInfo")
    exporting = _p("exporting", bool, False)
    nothing = _p("nothing", bool, True)

    def _formats(self) -> list[dict]:
        return [{"key": k, "title": tr(f"exp.f_{k}"), "hint": tr(f"exp.fh_{k}"), "icon": icon}
                for k, icon in FORMATS]

    formats = Property("QVariantList", _formats, notify=changed)

    def _option_list(self) -> list[dict]:
        return [{"key": k, "title": tr(f"exp.opt_{k}")} for k in OPTIONS]

    optionList = Property("QVariantList", _option_list, notify=changed)

    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            self._bundle = None
            self._set(canExport=False, stats="", reason="", nothing=True)
            return
        try:
            self._bundle = collect(self.repos, self.ws_id)
        except ValueError as exc:
            self._bundle = None
            self._set(canExport=False, reason=str(exc), nothing=True)
            return
        b = self._bundle
        done = sum(1 for s in b.subtasks if s.result.strip())
        nothing = done == 0 and not b.files
        fmt, reason = detect_format(b)
        self._set(stats=tr("exp.stats", results=done, total=len(b.subtasks),
                           files=len(b.files), reports=len(b.reports)),
                  recommended=fmt, reason=reason, nothing=nothing,
                  canExport=not nothing)
        self.setFormat(fmt)

    def reset(self) -> None:
        super().reset()
        self._bundle = None
        self._set(format="markdown", options=dict(DEFAULT_OPTIONS), lastPath="", lastInfo="")

    @Slot(str)
    def setFormat(self, fmt: str) -> None:  # noqa: N802
        if fmt not in dict(FORMATS):
            return
        path = ""
        if self._bundle is not None:
            PATHS.ensure()
            path = str(PATHS.exports_dir / suggest_filename(self._bundle, fmt))
        self._set(format=fmt, path=path)

    @Slot(str, bool)
    def setOption(self, key: str, value: bool) -> None:  # noqa: N802
        options = dict(self._s.get("options", DEFAULT_OPTIONS))
        options[key] = bool(value)
        self._set(options=options)

    @Slot(str)
    def setPath(self, path: str) -> None:  # noqa: N802
        self._set(path=(path or "").strip())

    @Slot()
    def browse(self) -> None:
        from PySide6.QtWidgets import QFileDialog

        current = self._s.get("path") or str(PATHS.exports_dir)
        chosen, _ = QFileDialog.getSaveFileName(None, tr("exp.output"), current)
        if chosen:
            self._set(path=chosen)

    @Slot()
    def exportNow(self) -> None:  # noqa: N802
        if self._bundle is None:
            return
        raw = (self._s.get("path") or "").strip()
        if not raw:
            self.toast("warning", tr("exp.no_path"), "")
            return
        o = self._s.get("options", DEFAULT_OPTIONS)
        fmt = self._s.get("format", "markdown")
        options = ExportOptions(
            include_results=o.get("results", True), include_reports=o.get("reports", False),
            include_summaries=o.get("summaries", False),
            include_incidents=o.get("incidents", True),
            include_decisions=o.get("decisions", False),
            include_files=o.get("files", True) and fmt == "zip",
            include_stats=o.get("stats", True), anonymize=o.get("anon", False))
        self._set(exporting=True)
        try:
            result = export(self._bundle, options, fmt, Path(raw).expanduser())
        except ExportError as exc:
            self.toast("error", tr("toast.export_failed"), str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            self.toast("error", tr("toast.export_failed"), error_text(exc))
            return
        finally:
            self._set(exporting=False)
        info = f"{result.path.name} · {human_size(result.size)}"
        if result.note:
            info += f" · {result.note}"
        self._set(lastPath=str(result.path), lastInfo=info)
        self.toast("success", tr("toast.exported"), info)

    @Slot()
    def openFolder(self) -> None:  # noqa: N802
        if self._s.get("lastPath"):
            self.backend.openPath(self._s["lastPath"])

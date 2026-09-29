"""Этап 8 — страница экспорта результата.

Формат подбирается автоматически по типу задачи и по тому, что реально
наработано, но выбор всегда остаётся за пользователем: рядом с подсказкой
написано, **почему** предложен именно этот формат.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.config import PATHS
from app.i18n import tr
from core.export.bundle import FORMAT_TITLES, ExportOptions, collect, detect_format
from core.export.exporters import (
    ExportError,
    ExportResult,
    export,
    open_folder,
    suggest_filename,
)
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, warn


class ExportPage(QWidget):
    """Сборка и выгрузка финального результата."""

    def __init__(self, repos: Repos) -> None:
        super().__init__()
        self.repos = repos
        self.workspace_id: int | None = None
        self._bundle = None
        self._last: ExportResult | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        self.header = Header(tr("exp.title"), tr("exp.subtitle"))
        self.btn_refresh = QPushButton(tr("common.refresh"))
        self.btn_refresh.clicked.connect(self.refresh)
        self.header.add_action(self.btn_refresh)
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

        body.addWidget(self._build_format_card())
        body.addWidget(self._build_content_card())
        body.addWidget(self._build_output_card())
        body.addStretch(1)

    # -- карточки ------------------------------------------------------------
    def _build_format_card(self) -> Card:
        card = Card(self, spacing=10)
        title = QLabel(tr("exp.format"))
        title.setObjectName("H2")
        card.body.addWidget(title)

        row = QHBoxLayout()
        self.format_box = QComboBox()
        for key, label in FORMAT_TITLES.items():
            self.format_box.addItem(label, key)
        self.format_box.currentIndexChanged.connect(self._on_format_changed)
        row.addWidget(self.format_box, 1)

        self.btn_auto = QPushButton(tr("exp.use_auto"))
        self.btn_auto.clicked.connect(self._apply_auto)
        row.addWidget(self.btn_auto)
        card.body.addLayout(row)

        self.hint = QLabel("")
        self.hint.setObjectName("Dim")
        self.hint.setWordWrap(True)
        card.body.addWidget(self.hint)

        self.stats = QLabel("")
        self.stats.setObjectName("Dim")
        self.stats.setWordWrap(True)
        card.body.addWidget(self.stats)
        return card

    def _build_content_card(self) -> Card:
        card = Card(self, spacing=8)
        title = QLabel(tr("exp.content"))
        title.setObjectName("H2")
        card.body.addWidget(title)

        self.opt_results = QCheckBox(tr("exp.opt_results"))
        self.opt_results.setChecked(True)
        self.opt_reports = QCheckBox(tr("exp.opt_reports"))
        self.opt_summaries = QCheckBox(tr("exp.opt_summaries"))
        self.opt_incidents = QCheckBox(tr("exp.opt_incidents"))
        self.opt_incidents.setChecked(True)
        self.opt_decisions = QCheckBox(tr("exp.opt_decisions"))
        self.opt_stats = QCheckBox(tr("exp.opt_stats"))
        self.opt_stats.setChecked(True)
        self.opt_files = QCheckBox(tr("exp.opt_files"))
        self.opt_files.setChecked(True)
        self.opt_anon = QCheckBox(tr("exp.opt_anon"))
        self.opt_anon.setToolTip(tr("exp.opt_anon_hint"))

        for box in (self.opt_results, self.opt_reports, self.opt_summaries,
                    self.opt_incidents, self.opt_decisions, self.opt_stats,
                    self.opt_files, self.opt_anon):
            card.body.addWidget(box)
        return card

    def _build_output_card(self) -> Card:
        card = Card(self, spacing=10)
        title = QLabel(tr("exp.output"))
        title.setObjectName("H2")
        card.body.addWidget(title)

        row = QHBoxLayout()
        self.path_edit = QLineEdit()
        row.addWidget(self.path_edit, 1)
        browse = QPushButton(tr("exp.browse"))
        browse.clicked.connect(self._browse)
        row.addWidget(browse)
        card.body.addLayout(row)

        buttons = QHBoxLayout()
        self.btn_export = QPushButton(tr("exp.export"))
        self.btn_export.setObjectName("Primary")
        self.btn_export.clicked.connect(self._export)
        buttons.addWidget(self.btn_export)

        self.btn_open = QPushButton(tr("exp.open_folder"))
        self.btn_open.setEnabled(False)
        self.btn_open.clicked.connect(self._open_folder)
        buttons.addWidget(self.btn_open)
        buttons.addStretch(1)
        card.body.addLayout(buttons)

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        card.body.addWidget(self.result_label)

        self.empty = EmptyState(tr("exp.nothing"))
        self.empty.setVisible(False)
        card.body.addWidget(self.empty)
        return card

    # -- данные --------------------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        enabled = self.workspace_id is not None
        for widget in (self.format_box, self.btn_auto, self.btn_export,
                       self.path_edit):
            widget.setEnabled(enabled)
        if not enabled:
            self.hint.setText(tr("ws.empty"))
            self.stats.setText("")
            return

        try:
            self._bundle = collect(self.repos, self.workspace_id)
        except ValueError as exc:
            self.hint.setText(str(exc))
            return

        done = sum(1 for s in self._bundle.subtasks if s.result.strip())
        self.stats.setText(tr(
            "exp.stats",
            results=done,
            total=len(self._bundle.subtasks),
            files=len(self._bundle.files),
            reports=len(self._bundle.reports),
        ))

        nothing = done == 0 and not self._bundle.files
        self.empty.setVisible(nothing)
        self.btn_export.setEnabled(not nothing)

        self._apply_auto()

    def _apply_auto(self) -> None:
        """Подставляет автоопределённый формат и объясняет выбор."""
        if self._bundle is None:
            return
        fmt, reason = detect_format(self._bundle)
        index = self.format_box.findData(fmt)
        if index >= 0:
            self.format_box.setCurrentIndex(index)
        self.hint.setText(tr("exp.auto_hint", reason=reason))
        self._suggest_path()

    def _on_format_changed(self) -> None:
        self._suggest_path()
        fmt = self.format_box.currentData()
        # Файлы проекта имеют смысл только в архиве: в документ их не вложить.
        self.opt_files.setEnabled(fmt == "zip")
        if fmt != "zip":
            self.opt_files.setToolTip(tr("exp.files_zip_only"))
        else:
            self.opt_files.setToolTip("")

    def _suggest_path(self) -> None:
        if self._bundle is None:
            return
        fmt = self.format_box.currentData()
        PATHS.ensure()
        self.path_edit.setText(
            str(PATHS.exports_dir / suggest_filename(self._bundle, fmt))
        )

    def _options(self) -> ExportOptions:
        return ExportOptions(
            include_results=self.opt_results.isChecked(),
            include_reports=self.opt_reports.isChecked(),
            include_summaries=self.opt_summaries.isChecked(),
            include_incidents=self.opt_incidents.isChecked(),
            include_decisions=self.opt_decisions.isChecked(),
            include_files=self.opt_files.isChecked(),
            include_stats=self.opt_stats.isChecked(),
            anonymize=self.opt_anon.isChecked(),
        )

    # -- действия ------------------------------------------------------------
    def _browse(self) -> None:
        current = Path(self.path_edit.text() or str(PATHS.exports_dir))
        chosen, _ = QFileDialog.getSaveFileName(
            self, tr("exp.output"), str(current)
        )
        if chosen:
            self.path_edit.setText(chosen)

    def _export(self) -> None:
        if self._bundle is None:
            return
        raw = self.path_edit.text().strip()
        if not raw:
            warn(self, tr("exp.no_path"))
            return

        fmt = self.format_box.currentData()
        path = Path(raw).expanduser()
        self.btn_export.setEnabled(False)
        try:
            result = export(self._bundle, self._options(), fmt, path)
        except ExportError as exc:
            warn(self, str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            warn(self, f"{type(exc).__name__}: {exc}")
            return
        finally:
            self.btn_export.setEnabled(True)

        self._last = result
        self.btn_open.setEnabled(True)
        note = f"\n{result.note}" if result.note else ""
        self.result_label.setText(
            tr("exp.done", path=str(result.path), size=_human(result.size)) + note
        )
        self.result_label.setObjectName("Ok")
        self.result_label.setStyleSheet("color: #3ecf8e;")

    def _open_folder(self) -> None:
        if self._last is None:
            return
        if not open_folder(self._last.path):
            warn(self, tr("exp.open_failed", path=str(self._last.path.parent)))


def _human(size: int) -> str:
    value = float(size)
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if value < 1024:
            return f"{value:.0f} {unit}"
        value /= 1024
    return f"{value:.1f} ТБ"

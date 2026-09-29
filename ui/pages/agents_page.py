"""Этап 2 — страница агентов воркспейса.

Количество агентов не ограничено: список прокручивается, а карточки
компактны, поэтому 2 агента и 15+ агентов выглядят одинаково опрятно.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.i18n import current_language, tr
from core.agents.roles import COMMON_RULES, TEMPLATES, by_key, title as role_title
from core.tools.base import default_registry, expand_tool_names
from providers.base import ProviderError
from providers.factory import build_provider
from providers.presets import preset
from storage.models import Agent
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, StatusBadge, confirm, warn
from utils.asyncutils import run_async


class AgentDialog(QDialog):
    """Форма создания/редактирования агента."""

    def __init__(self, parent: QWidget, repos: Repos, agent: Agent | None = None) -> None:
        super().__init__(parent)
        self.repos = repos
        self.agent = agent
        self.setWindowTitle(tr("agents.new"))
        self.setMinimumSize(620, 700)

        root = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        lay = QVBoxLayout(page)
        lay.setSpacing(10)

        lay.addWidget(QLabel(tr("agents.name")))
        self.name = QLineEdit(agent.name if agent else "")
        lay.addWidget(self.name)
        #: имя, подставленное из шаблона; пока пользователь его не менял,
        #: смена шаблона меняет и имя
        self._auto_name = ""
        self._auto_prompt = ""

        lay.addWidget(QLabel(tr("agents.template")))
        self.template = QComboBox()
        lang = current_language()
        for t in TEMPLATES:
            self.template.addItem(role_title(t, lang), t.key)
        self.template.currentIndexChanged.connect(self._apply_template)
        lay.addWidget(self.template)

        lay.addWidget(QLabel(tr("agents.provider_key")))
        self.key_box = QComboBox()
        self.keys = self.repos.keys.list()
        for k in self.keys:
            self.key_box.addItem(f"{k.label} — {preset(k.provider).title}", k.id)
        self.key_box.currentIndexChanged.connect(self._on_key_changed)
        lay.addWidget(self.key_box)

        model_row = QHBoxLayout()
        model_col = QVBoxLayout()
        model_col.addWidget(QLabel(tr("agents.model")))
        self.model = QComboBox()
        self.model.setEditable(True)   # можно вписать модель вручную
        model_col.addWidget(self.model)
        model_row.addLayout(model_col, 1)
        self.btn_models = QPushButton(tr("agents.load_models"))
        self.btn_models.clicked.connect(self._load_models)
        model_row.addWidget(self.btn_models, 0, Qt.AlignmentFlag.AlignBottom)
        lay.addLayout(model_row)

        params_row = QHBoxLayout()
        temp_col = QVBoxLayout()
        temp_col.addWidget(QLabel(tr("agents.temperature")))
        self.temperature = QDoubleSpinBox()
        self.temperature.setRange(0.0, 2.0)
        self.temperature.setSingleStep(0.1)
        self.temperature.setValue(agent.temperature if agent else 0.7)
        temp_col.addWidget(self.temperature)
        params_row.addLayout(temp_col)

        tok_col = QVBoxLayout()
        tok_col.addWidget(QLabel(tr("agents.max_tokens")))
        self.max_tokens = QSpinBox()
        self.max_tokens.setRange(256, 32768)
        self.max_tokens.setSingleStep(256)
        self.max_tokens.setValue(agent.max_tokens if agent else 2048)
        tok_col.addWidget(self.max_tokens)
        params_row.addLayout(tok_col)
        lay.addLayout(params_row)

        lay.addWidget(QLabel("Инструменты"))
        tools_row = QHBoxLayout()
        self.tool_boxes: dict[str, QCheckBox] = {}
        enabled_tools = set(expand_tool_names(agent.tools)) if agent else set()
        for tool_name in default_registry().names():
            box = QCheckBox(tool_name)
            box.setChecked(tool_name in enabled_tools)
            self.tool_boxes[tool_name] = box
            tools_row.addWidget(box)
        tools_row.addStretch(1)
        lay.addLayout(tools_row)

        lay.addWidget(QLabel(tr("agents.prompt")))
        self.prompt = QPlainTextEdit(agent.system_prompt if agent else "")
        self.prompt.setMinimumHeight(180)
        lay.addWidget(self.prompt)

        note = QLabel(tr("agents.isolated_note"))
        note.setObjectName("Dim")
        note.setWordWrap(True)
        lay.addWidget(note)

        self.is_supervisor = QCheckBox(tr("settings.supervisor"))
        self.is_supervisor.setChecked(agent.is_supervisor if agent else False)
        lay.addWidget(self.is_supervisor)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

        if agent is not None:
            idx = self.template.findData(agent.role or "custom")
            self.template.blockSignals(True)
            self.template.setCurrentIndex(max(0, idx))
            self.template.blockSignals(False)
            idx = self.key_box.findData(agent.api_key_id)
            if idx >= 0:
                self.key_box.setCurrentIndex(idx)
            self._on_key_changed()
            self.model.setCurrentText(agent.model)
        else:
            self._apply_template()
            self._on_key_changed()

    # -- реакции -------------------------------------------------------------
    def _apply_template(self) -> None:
        template = by_key(self.template.currentData())
        # Промпт, который пользователь успел поправить руками, не затираем.
        prompt = self.prompt.toPlainText().strip()
        if template.prompt and (not prompt or prompt == self._auto_prompt):
            self._auto_prompt = template.prompt + "\n\n" + COMMON_RULES.strip()
            self.prompt.setPlainText(self._auto_prompt)
        current = self.name.text().strip()
        if not current or current == self._auto_name:
            self._auto_name = role_title(template, current_language())
            self.name.setText(self._auto_name)
        suggested = expand_tool_names(template.suggested_tools)
        for name, box in self.tool_boxes.items():
            box.setChecked(name in suggested)

    def _on_key_changed(self) -> None:
        """Подставляет в список моделей кэш последней проверки или пресет."""
        key_id = self.key_box.currentData()
        key = next((k for k in self.keys if k.id == key_id), None)
        if key is None:
            return
        current = self.model.currentText()
        cached = key.meta.get("models") or []
        models = cached or preset(key.provider).suggested_models
        self.model.clear()
        self.model.addItems(models)
        if current:
            self.model.setCurrentText(current)
        elif models:
            self.model.setCurrentIndex(0)

    def _load_models(self) -> None:
        key_id = self.key_box.currentData()
        key = next((k for k in self.keys if k.id == key_id), None)
        if key is None:
            return
        self.btn_models.setEnabled(False)

        async def job() -> list[str]:
            secret = self.repos.keys.reveal(key.id)
            provider = build_provider(key.provider, secret, key.base_url, timeout=20)
            try:
                return await provider.list_models()
            finally:
                await provider.aclose()

        def done(models: list[str]) -> None:
            self.btn_models.setEnabled(True)
            current = self.model.currentText()
            self.model.clear()
            self.model.addItems(models)
            if current:
                self.model.setCurrentText(current)
            meta = dict(key.meta)
            meta["models"] = models[:300]
            self.repos.keys.update(key.id, key.label, key.base_url, None, meta)

        def failed(exc: Exception) -> None:
            self.btn_models.setEnabled(True)
            message = str(exc) if isinstance(exc, ProviderError) else f"{type(exc).__name__}: {exc}"
            warn(self, tr("keys.test_fail", err=message))

        run_async(job(), done, failed)

    def values(self) -> dict:
        key_id = self.key_box.currentData()
        key = next((k for k in self.keys if k.id == key_id), None)
        return {
            "name": self.name.text().strip(),
            "role": self.template.currentData(),
            "system_prompt": self.prompt.toPlainText().strip(),
            "api_key_id": key_id,
            "provider": key.provider if key else "",
            "model": self.model.currentText().strip(),
            "params": {
                "temperature": self.temperature.value(),
                "max_tokens": self.max_tokens.value(),
                "tools": [n for n, b in self.tool_boxes.items() if b.isChecked()],
            },
            "is_supervisor": self.is_supervisor.isChecked(),
        }


class AgentsPage(QWidget):
    """Список агентов текущего воркспейса."""

    agents_changed = Signal()

    def __init__(self, repos: Repos) -> None:
        super().__init__()
        self.repos = repos
        self.workspace_id: int | None = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(16)

        self.header = Header(tr("agents.title"), tr("agents.isolated_note"))
        self.btn_new = QPushButton(tr("agents.new"))
        self.btn_new.setObjectName("Primary")
        self.btn_new.clicked.connect(self._create)
        self.header.add_action(self.btn_new)
        lay.addWidget(self.header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        lay.addWidget(self.scroll, 1)

        self.container = QWidget()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        self.scroll.setWidget(self.container)

    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.workspace_id is None:
            self.btn_new.setEnabled(False)
            self.list_layout.addWidget(EmptyState(tr("ws.empty")))
            return
        self.btn_new.setEnabled(True)

        if not self.repos.keys.list():
            self.list_layout.addWidget(EmptyState(tr("agents.no_keys")))
            return

        agents = self.repos.agents.list(self.workspace_id)
        if not agents:
            self.list_layout.addWidget(EmptyState(tr("agents.empty")))
            return
        for agent in agents:
            self.list_layout.addWidget(self._build_card(agent))
        self.list_layout.addStretch(1)

    def _build_card(self, agent: Agent) -> Card:
        card = Card(self, spacing=6)
        row = QHBoxLayout()

        texts = QVBoxLayout()
        texts.setSpacing(2)
        head = QHBoxLayout()
        name = QLabel(agent.name + ("  ⭐" if agent.is_supervisor else ""))
        name.setObjectName("H2")
        head.addWidget(name)
        head.addWidget(StatusBadge(agent.status))
        head.addStretch(1)
        texts.addLayout(head)

        p = preset(agent.provider)
        meta = QLabel(f"{role_title(by_key(agent.role), current_language())}  ·  "
                      f"{p.title}  ·  {agent.model or '—'}"
                      f"  ·  T={agent.temperature}  ·  max={agent.max_tokens}")
        meta.setObjectName("Dim")
        texts.addWidget(meta)

        if agent.tools:
            tools = QLabel("Инструменты: " + ", ".join(agent.tools))
            tools.setObjectName("Dim")
            texts.addWidget(tools)

        prompt_preview = agent.system_prompt.replace("\n", " ")[:160]
        if prompt_preview:
            preview = QLabel(prompt_preview + ("…" if len(agent.system_prompt) > 160 else ""))
            preview.setObjectName("Dim")
            preview.setWordWrap(True)
            texts.addWidget(preview)

        row.addLayout(texts, 1)

        btn_edit = QPushButton(tr("common.edit"))
        btn_edit.clicked.connect(lambda: self._edit(agent))
        row.addWidget(btn_edit, 0, Qt.AlignmentFlag.AlignTop)

        btn_del = QPushButton(tr("common.delete"))
        btn_del.setObjectName("Danger")
        btn_del.clicked.connect(lambda: self._delete(agent))
        row.addWidget(btn_del, 0, Qt.AlignmentFlag.AlignTop)

        card.body.addLayout(row)
        return card

    # -- действия ------------------------------------------------------------
    def _create(self) -> None:
        if self.workspace_id is None:
            return
        if not self.repos.keys.list():
            warn(self, tr("agents.no_keys"))
            return
        dlg = AgentDialog(self, self.repos)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        data = dlg.values()
        if not data["name"] or not data["model"]:
            warn(self, tr("agents.model"))
            return
        self.repos.agents.create(self.workspace_id, **data)
        self.agents_changed.emit()
        self.refresh()

    def _edit(self, agent: Agent) -> None:
        dlg = AgentDialog(self, self.repos, agent)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        self.repos.agents.update(agent.id, **dlg.values())
        self.agents_changed.emit()
        self.refresh()

    def _delete(self, agent: Agent) -> None:
        if not confirm(self, tr("agents.delete_confirm")):
            return
        self.repos.agents.delete(agent.id)
        self.agents_changed.emit()
        self.refresh()

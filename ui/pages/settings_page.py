"""Страница настроек: приложение + настройки активного воркспейса.

Здесь же выбирается режим супервайзера (ответ на вопрос 8): либо один из
подключённых API-ключей/агентов, либо локальная модель через Ollama —
например Qwen, которая работает офлайн и ничего не стоит.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.config import DEFAULT_WORKSPACE_SETTINGS, AppSettings
from app.i18n import available_languages, current_language, set_language, tr
from core.tools.sandbox import docker_available
from storage.repositories import Repos
from ui.widgets.common import Card, Header, info, warn

MIN_PASSWORD_LEN = 8


class PasswordDialog(QDialog):
    """Смена пароля профиля с перешифровкой всех API-ключей."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("settings.change_password"))
        self.setMinimumWidth(420)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        lay.addWidget(QLabel("Текущий пароль"))
        self.old = QLineEdit()
        self.old.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.old)

        lay.addWidget(QLabel(tr("login.password")))
        self.new1 = QLineEdit()
        self.new1.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.new1)

        lay.addWidget(QLabel(tr("login.password2")))
        self.new2 = QLineEdit()
        self.new2.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.new2)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def values(self) -> tuple[str, str, str]:
        return self.old.text(), self.new1.text(), self.new2.text()


class SettingsPage(QWidget):
    """Настройки приложения и текущего воркспейса."""

    theme_changed = object  # заменяется сигналом в main_window через callback

    def __init__(self, repos: Repos, app_settings: AppSettings,
                 on_theme_change=None, on_language_change=None) -> None:
        super().__init__()
        self.repos = repos
        self.app_settings = app_settings
        self.on_theme_change = on_theme_change
        self.on_language_change = on_language_change
        self.workspace_id: int | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)
        root.addWidget(Header(tr("settings.title")))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        lay.addWidget(self._build_app_card())
        self.ws_card = self._build_workspace_card()
        lay.addWidget(self.ws_card)
        lay.addWidget(self._build_security_card())
        lay.addStretch(1)

    # -- карточки ------------------------------------------------------------
    def _build_app_card(self) -> Card:
        card = Card(self)
        title = QLabel("Приложение")
        title.setObjectName("H2")
        card.body.addWidget(title)

        row = QHBoxLayout()
        lang_col = QVBoxLayout()
        lang_col.addWidget(QLabel(tr("settings.language")))
        self.lang_box = QComboBox()
        for code, label in available_languages():
            self.lang_box.addItem(label, code)
        idx = self.lang_box.findData(current_language())
        self.lang_box.setCurrentIndex(max(0, idx))
        self.lang_box.currentIndexChanged.connect(self._change_language)
        lang_col.addWidget(self.lang_box)
        row.addLayout(lang_col)

        theme_col = QVBoxLayout()
        theme_col.addWidget(QLabel(tr("settings.theme")))
        self.theme_box = QComboBox()
        self.theme_box.addItem("Тёмная", "dark")
        self.theme_box.addItem("Светлая", "light")
        self.theme_box.setCurrentIndex(0 if self.app_settings.theme == "dark" else 1)
        self.theme_box.currentIndexChanged.connect(self._change_theme)
        theme_col.addWidget(self.theme_box)
        row.addLayout(theme_col)
        row.addStretch(1)
        card.body.addLayout(row)

        note = QLabel(tr("settings.restart_note"))
        note.setObjectName("Dim")
        card.body.addWidget(note)
        return card

    def _build_workspace_card(self) -> Card:
        card = Card(self)
        title = QLabel("Воркспейс")
        title.setObjectName("H2")
        card.body.addWidget(title)

        self.hitl = QCheckBox(tr("settings.hitl"))
        self.hitl.stateChanged.connect(self._on_hitl_toggled)
        card.body.addWidget(self.hitl)

        hitl_row = QHBoxLayout()
        conf_col = QVBoxLayout()
        conf_col.addWidget(QLabel(tr("settings.hitl_threshold")))
        self.hitl_threshold = QDoubleSpinBox()
        self.hitl_threshold.setRange(0.0, 1.0)
        self.hitl_threshold.setSingleStep(0.05)
        self.hitl_threshold.setDecimals(2)
        self.hitl_threshold.setToolTip(tr("settings.hitl_threshold_hint"))
        self.hitl_threshold.valueChanged.connect(self._save_workspace)
        conf_col.addWidget(self.hitl_threshold)
        hitl_row.addLayout(conf_col)
        hitl_row.addStretch(1)
        card.body.addLayout(hitl_row)

        self.hitl_milestone = QCheckBox(tr("settings.hitl_milestone"))
        self.hitl_milestone.setToolTip(tr("settings.hitl_milestone_hint"))
        self.hitl_milestone.stateChanged.connect(self._save_workspace)
        card.body.addWidget(self.hitl_milestone)

        card.body.addWidget(QLabel(tr("settings.supervisor_mode")))
        self.sup_mode = QComboBox()
        self.sup_mode.addItem(tr("settings.supervisor_api"), "api")
        self.sup_mode.addItem(tr("settings.supervisor_local"), "local")
        self.sup_mode.currentIndexChanged.connect(self._on_sup_mode)
        card.body.addWidget(self.sup_mode)

        self.sup_agent = QComboBox()
        card.body.addWidget(self.sup_agent)
        self.sup_agent.currentIndexChanged.connect(self._save_workspace)

        local_row = QHBoxLayout()
        local_col = QVBoxLayout()
        local_col.addWidget(QLabel("Локальная модель (Ollama)"))
        self.sup_local_model = QLineEdit()
        self.sup_local_model.editingFinished.connect(self._save_workspace)
        local_col.addWidget(self.sup_local_model)
        local_row.addLayout(local_col, 1)

        url_col = QVBoxLayout()
        url_col.addWidget(QLabel("Base URL"))
        self.sup_local_url = QLineEdit()
        self.sup_local_url.editingFinished.connect(self._save_workspace)
        url_col.addWidget(self.sup_local_url)
        local_row.addLayout(url_col, 1)
        card.body.addLayout(local_row)

        interval_row = QHBoxLayout()
        int_col = QVBoxLayout()
        int_col.addWidget(QLabel(tr("settings.summary_interval")))
        self.summary_interval = QSpinBox()
        self.summary_interval.setRange(1, 600)
        self.summary_interval.valueChanged.connect(self._save_workspace)
        int_col.addWidget(self.summary_interval)
        interval_row.addLayout(int_col)

        steps_col = QVBoxLayout()
        steps_col.addWidget(QLabel("Шагов ReAct на подзадачу"))
        self.max_steps = QSpinBox()
        self.max_steps.setRange(1, 50)
        self.max_steps.valueChanged.connect(self._save_workspace)
        steps_col.addWidget(self.max_steps)
        interval_row.addLayout(steps_col)
        interval_row.addStretch(1)
        card.body.addLayout(interval_row)

        self.summary_on_event = QCheckBox(tr("settings.summary_on_event"))
        self.summary_on_event.stateChanged.connect(self._save_workspace)
        card.body.addWidget(self.summary_on_event)

        # --- песочница ---
        sandbox_title = QLabel(tr("settings.sandbox"))
        sandbox_title.setObjectName("H2")
        card.body.addWidget(sandbox_title)

        sandbox_row = QHBoxLayout()
        back_col = QVBoxLayout()
        back_col.addWidget(QLabel("Бэкенд"))
        self.sandbox_backend = QComboBox()
        self.sandbox_backend.addItem("Авто", "auto")
        self.sandbox_backend.addItem("Отдельный процесс", "subprocess")
        self.sandbox_backend.addItem("Docker", "docker")
        self.sandbox_backend.currentIndexChanged.connect(self._save_workspace)
        back_col.addWidget(self.sandbox_backend)
        sandbox_row.addLayout(back_col, 1)

        to_col = QVBoxLayout()
        to_col.addWidget(QLabel("Таймаут, с"))
        self.sandbox_timeout = QSpinBox()
        self.sandbox_timeout.setRange(5, 600)
        self.sandbox_timeout.valueChanged.connect(self._save_workspace)
        to_col.addWidget(self.sandbox_timeout)
        sandbox_row.addLayout(to_col)

        mem_col = QVBoxLayout()
        mem_col.addWidget(QLabel("Память, МБ"))
        self.sandbox_memory = QSpinBox()
        self.sandbox_memory.setRange(64, 8192)
        self.sandbox_memory.setSingleStep(64)
        self.sandbox_memory.valueChanged.connect(self._save_workspace)
        mem_col.addWidget(self.sandbox_memory)
        sandbox_row.addLayout(mem_col)
        card.body.addLayout(sandbox_row)

        self.docker_note = QLabel("")
        self.docker_note.setObjectName("Dim")
        self.docker_note.setWordWrap(True)
        card.body.addWidget(self.docker_note)

        # --- разрешённые каталоги ---
        paths_title = QLabel(tr("settings.allowed_paths"))
        paths_title.setObjectName("H2")
        card.body.addWidget(paths_title)

        self.paths_list = QListWidget()
        self.paths_list.setMaximumHeight(120)
        card.body.addWidget(self.paths_list)

        paths_buttons = QHBoxLayout()
        btn_add_path = QPushButton(tr("settings.add_path"))
        btn_add_path.clicked.connect(self._add_path)
        paths_buttons.addWidget(btn_add_path)
        btn_del_path = QPushButton(tr("common.delete"))
        btn_del_path.setObjectName("Danger")
        btn_del_path.clicked.connect(self._remove_path)
        paths_buttons.addWidget(btn_del_path)
        paths_buttons.addStretch(1)
        card.body.addLayout(paths_buttons)

        warning = QLabel(
            "Агенты получают доступ на чтение и запись в эти каталоги. "
            "Не добавляйте сюда системные папки и каталоги с личными данными."
        )
        warning.setObjectName("Dim")
        warning.setWordWrap(True)
        card.body.addWidget(warning)
        return card

    def _build_security_card(self) -> Card:
        card = Card(self)
        title = QLabel("Безопасность")
        title.setObjectName("H2")
        card.body.addWidget(title)

        text = QLabel(
            "API-ключи зашифрованы AES-256-GCM. Ключ шифрования выводится из пароля "
            "профиля функцией Argon2id и существует только в оперативной памяти."
        )
        text.setObjectName("Dim")
        text.setWordWrap(True)
        card.body.addWidget(text)

        btn = QPushButton(tr("settings.change_password"))
        btn.clicked.connect(self._change_password)
        card.body.addWidget(btn)
        return card

    # -- загрузка/сохранение -------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.ws_card.setEnabled(ws_id is not None)
        if ws_id is None:
            return
        ws = self.repos.workspaces.get(ws_id)
        if ws is None:
            return
        s = {**DEFAULT_WORKSPACE_SETTINGS, **ws.settings}

        self._loading = True
        self.hitl.setChecked(bool(s["human_in_the_loop"]))
        self.hitl_threshold.setValue(float(s.get("hitl_confidence_threshold", 0.5)))
        self.hitl_milestone.setChecked(bool(s.get("hitl_pause_on_milestone", False)))
        self._sync_hitl_enabled()
        self.sup_mode.setCurrentIndex(0 if s["supervisor_mode"] == "api" else 1)

        self.sup_agent.clear()
        self.sup_agent.addItem(tr("common.none"), None)
        for agent in self.repos.agents.list(ws_id):
            self.sup_agent.addItem(f"{agent.name} — {agent.model}", agent.id)
        idx = self.sup_agent.findData(s.get("supervisor_agent_id"))
        self.sup_agent.setCurrentIndex(max(0, idx))

        self.sup_local_model.setText(str(s["supervisor_local_model"]))
        self.sup_local_url.setText(str(s["supervisor_local_base_url"]))
        self.summary_interval.setValue(int(s["summary_interval_minutes"]))
        self.summary_on_event.setChecked(bool(s["summary_on_event"]))
        self.max_steps.setValue(int(s["agent_max_steps"]))

        i = self.sandbox_backend.findData(s["sandbox_backend"])
        self.sandbox_backend.setCurrentIndex(max(0, i))
        self.sandbox_timeout.setValue(int(s["sandbox_timeout_sec"]))
        self.sandbox_memory.setValue(int(s["sandbox_memory_mb"]))

        self.paths_list.clear()
        self.paths_list.addItems([str(p) for p in s.get("extra_allowed_paths", [])])

        self.docker_note.setText(
            "Docker найден — доступна полная изоляция сети и файловой системы."
            if docker_available() else
            "Docker не найден. Будет использован режим отдельного процесса: "
            "ограничены CPU, память, размер файлов и переменные окружения, "
            "но это не полная изоляция."
        )
        self._on_sup_mode()
        self._loading = False

    def refresh(self) -> None:
        """Перечитывает настройки: список агентов мог измениться после входа на страницу."""
        self.set_workspace(self.workspace_id)

    def _save_workspace(self) -> None:
        if self.workspace_id is None or getattr(self, "_loading", False):
            return
        ws = self.repos.workspaces.get(self.workspace_id)
        if ws is None:
            return
        s = {**DEFAULT_WORKSPACE_SETTINGS, **ws.settings}
        s.update({
            "human_in_the_loop": self.hitl.isChecked(),
            "hitl_confidence_threshold": round(self.hitl_threshold.value(), 2),
            "hitl_pause_on_milestone": self.hitl_milestone.isChecked(),
            "supervisor_mode": self.sup_mode.currentData(),
            "supervisor_agent_id": self.sup_agent.currentData(),
            "supervisor_local_model": self.sup_local_model.text().strip(),
            "supervisor_local_base_url": self.sup_local_url.text().strip(),
            "summary_interval_minutes": self.summary_interval.value(),
            "summary_on_event": self.summary_on_event.isChecked(),
            "agent_max_steps": self.max_steps.value(),
            "sandbox_backend": self.sandbox_backend.currentData(),
            "sandbox_timeout_sec": self.sandbox_timeout.value(),
            "sandbox_memory_mb": self.sandbox_memory.value(),
            "extra_allowed_paths": [self.paths_list.item(i).text()
                                    for i in range(self.paths_list.count())],
        })
        self.repos.workspaces.update(self.workspace_id, settings=s)

    def _on_hitl_toggled(self) -> None:
        self._sync_hitl_enabled()
        self._save_workspace()

    def _sync_hitl_enabled(self) -> None:
        """Настройки пауз бессмысленны при выключенном human-in-the-loop."""
        enabled = self.hitl.isChecked()
        self.hitl_threshold.setEnabled(enabled)
        self.hitl_milestone.setEnabled(enabled)

    def _on_sup_mode(self) -> None:
        local = self.sup_mode.currentData() == "local"
        self.sup_agent.setVisible(not local)
        self.sup_local_model.setEnabled(local)
        self.sup_local_url.setEnabled(local)
        self._save_workspace()

    # -- действия ------------------------------------------------------------
    def _change_language(self) -> None:
        code = self.lang_box.currentData()
        set_language(code)
        self.app_settings.language = code
        self.app_settings.save()
        if self.on_language_change:
            self.on_language_change(code)

    def _change_theme(self) -> None:
        theme = self.theme_box.currentData()
        self.app_settings.theme = theme
        self.app_settings.save()
        if self.on_theme_change:
            self.on_theme_change(theme)

    def _add_path(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, tr("settings.add_path"),
                                                  str(Path.home()))
        if folder:
            self.paths_list.addItem(folder)
            self._save_workspace()

    def _remove_path(self) -> None:
        for item in self.paths_list.selectedItems():
            self.paths_list.takeItem(self.paths_list.row(item))
        self._save_workspace()

    def _change_password(self) -> None:
        dlg = PasswordDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        old, new1, new2 = dlg.values()
        if len(new1) < MIN_PASSWORD_LEN:
            warn(self, tr("login.password_short"))
            return
        if new1 != new2:
            warn(self, tr("login.password_mismatch"))
            return
        if self.repos.users.change_password(self.repos.session, old, new1):
            info(self, "Пароль изменён, API-ключи перешифрованы.")
        else:
            warn(self, tr("login.bad_credentials"))

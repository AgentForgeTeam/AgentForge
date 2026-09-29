"""Этап 2 — страница API-ключей.

Ключи хранятся зашифрованными (AES-256-GCM на мастер-ключе профиля).
Кнопка «Проверить» делает реальный запрос списка моделей — это заодно
подтверждает, что ключ и base URL рабочие.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from providers.base import ProviderError
from providers.factory import build_provider
from providers.presets import preset, preset_list
from storage.models import ApiKey
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, confirm, info, warn
from utils.asyncutils import run_async


class KeyDialog(QDialog):
    """Создание/редактирование ключа с автоподстановкой base URL из пресета."""

    def __init__(self, parent: QWidget, repos: Repos, key: ApiKey | None = None) -> None:
        super().__init__(parent)
        self.repos = repos
        self.key = key
        self.setWindowTitle(tr("keys.new"))
        self.setMinimumWidth(520)

        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        lay.addWidget(QLabel(tr("keys.provider")))
        self.provider = QComboBox()
        for p in preset_list():
            suffix = []
            if p.free_tier:
                suffix.append("free")
            if p.local:
                suffix.append("local")
            label = p.title + (f"  ({', '.join(suffix)})" if suffix else "")
            self.provider.addItem(label, p.key)
        self.provider.currentIndexChanged.connect(self._on_provider)
        self.provider.setEnabled(key is None)   # провайдер не меняем после создания
        lay.addWidget(self.provider)

        self.notes = QLabel("")
        self.notes.setObjectName("Dim")
        self.notes.setWordWrap(True)
        lay.addWidget(self.notes)

        lay.addWidget(QLabel(tr("keys.label")))
        self.label = QLineEdit(key.label if key else "")
        lay.addWidget(self.label)

        lay.addWidget(QLabel(tr("keys.base_url")))
        self.base_url = QLineEdit(key.base_url if key else "")
        lay.addWidget(self.base_url)

        self.key_label = QLabel(tr("keys.key"))
        lay.addWidget(self.key_label)
        self.secret = QLineEdit()
        self.secret.setEchoMode(QLineEdit.EchoMode.Password)
        self.secret.setPlaceholderText("sk-..." if key is None else "оставьте пустым, чтобы не менять")
        lay.addWidget(self.secret)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

        if key is not None:
            idx = self.provider.findData(key.provider)
            if idx >= 0:
                self.provider.setCurrentIndex(idx)
        self._on_provider()

    def _on_provider(self) -> None:
        p = preset(self.provider.currentData())
        if self.key is None:
            self.base_url.setText(p.base_url)
            if not self.label.text():
                self.label.setText(p.title)
        self.secret.setEnabled(p.requires_key or p.key == "custom")
        hint = p.notes
        if not p.requires_key:
            hint = (hint + " " if hint else "") + tr("keys.no_key_needed")
        if p.docs_url:
            hint = (hint + "  " if hint else "") + p.docs_url
        self.notes.setText(hint)

    def values(self) -> tuple[str, str, str, str]:
        return (
            self.provider.currentData(),
            self.label.text().strip() or preset(self.provider.currentData()).title,
            self.base_url.text().strip(),
            self.secret.text().strip(),
        )


class KeysPage(QWidget):
    """Список ключей пользователя (общий для всех воркспейсов)."""

    keys_changed = Signal()

    def __init__(self, repos: Repos) -> None:
        super().__init__()
        self.repos = repos

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(16)

        self.header = Header(tr("keys.title"), tr("keys.subtitle"))
        btn_new = QPushButton(tr("keys.new"))
        btn_new.setObjectName("Primary")
        btn_new.clicked.connect(self._create)
        self.header.add_action(btn_new)
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

    def refresh(self) -> None:
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        keys = self.repos.keys.list()
        if not keys:
            self.list_layout.addWidget(EmptyState(tr("keys.empty")))
            return
        for key in keys:
            self.list_layout.addWidget(self._build_card(key))
        self.list_layout.addStretch(1)

    def _build_card(self, key: ApiKey) -> Card:
        p = preset(key.provider)
        card = Card(self, spacing=8)
        row = QHBoxLayout()

        texts = QVBoxLayout()
        texts.setSpacing(2)
        title = QLabel(f"{key.label}")
        title.setObjectName("H2")
        texts.addWidget(title)
        meta = QLabel(f"{p.title}  ·  {key.base_url or p.base_url or '—'}  ·  "
                      + ("ключ сохранён" if key.has_secret else "без ключа"))
        meta.setObjectName("Dim")
        texts.addWidget(meta)
        status = QLabel("")
        status.setObjectName("Dim")
        status.setWordWrap(True)
        texts.addWidget(status)
        row.addLayout(texts, 1)

        btn_test = QPushButton(tr("common.test"))
        btn_test.clicked.connect(lambda: self._test(key, btn_test, status))
        row.addWidget(btn_test, 0, Qt.AlignmentFlag.AlignTop)

        btn_edit = QPushButton(tr("common.edit"))
        btn_edit.clicked.connect(lambda: self._edit(key))
        row.addWidget(btn_edit, 0, Qt.AlignmentFlag.AlignTop)

        btn_del = QPushButton(tr("common.delete"))
        btn_del.setObjectName("Danger")
        btn_del.clicked.connect(lambda: self._delete(key))
        row.addWidget(btn_del, 0, Qt.AlignmentFlag.AlignTop)

        card.body.addLayout(row)
        return card

    # -- действия ------------------------------------------------------------
    def _create(self) -> None:
        dlg = KeyDialog(self, self.repos)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        provider, label, base_url, secret = dlg.values()
        p = preset(provider)
        if p.requires_key and not secret:
            warn(self, tr("keys.key"))
            return
        self.repos.keys.create(label, provider, secret, base_url)
        self.keys_changed.emit()
        self.refresh()

    def _edit(self, key: ApiKey) -> None:
        dlg = KeyDialog(self, self.repos, key)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        _, label, base_url, secret = dlg.values()
        self.repos.keys.update(key.id, label, base_url, secret if secret else None)
        self.keys_changed.emit()
        self.refresh()

    def _delete(self, key: ApiKey) -> None:
        if not confirm(self, tr("keys.delete_confirm")):
            return
        self.repos.keys.delete(key.id)
        self.keys_changed.emit()
        self.refresh()

    def _test(self, key: ApiKey, button: QPushButton, status: QLabel) -> None:
        """Асинхронная проверка соединения без блокировки интерфейса."""
        button.setEnabled(False)
        status.setText("…")

        async def job() -> list[str]:
            secret = self.repos.keys.reveal(key.id)
            provider = build_provider(key.provider, secret, key.base_url, timeout=20)
            try:
                return await provider.test()
            finally:
                await provider.aclose()

        def done(models: list[str]) -> None:
            button.setEnabled(True)
            status.setText(tr("keys.test_ok", n=len(models)))
            meta = dict(key.meta)
            meta["models"] = models[:300]   # кэш для выпадающего списка в агентах
            self.repos.keys.update(key.id, key.label, key.base_url, None, meta)
            self.keys_changed.emit()

        def failed(exc: Exception) -> None:
            button.setEnabled(True)
            message = str(exc) if isinstance(exc, ProviderError) else f"{type(exc).__name__}: {exc}"
            status.setText(tr("keys.test_fail", err=message))

        run_async(job(), done, failed)

"""Этап 1 — окно локальной авторизации.

Поддерживает несколько профилей на одном устройстве. Пароль профиля
одновременно является мастер-паролем для расшифровки API-ключей, поэтому
при создании профиля показывается предупреждение о невозможности восстановления.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_NAME, APP_VERSION, AppSettings
from app.i18n import available_languages, current_language, set_language, tr
from core.security.crypto import (
    Session,
    keyring_available,
    keyring_delete_password,
    keyring_get_password,
    keyring_store_password,
)
from storage.db import Database
from storage.repositories import UserRepo
from ui.widgets.common import Card, PageSwitcher

MIN_PASSWORD_LEN = 8


class LoginWindow(QWidget):
    """Окно входа. При успехе эмитит ``logged_in`` с открытой сессией."""

    logged_in = Signal(object)  # Session

    def __init__(self, db: Database, settings: AppSettings) -> None:
        super().__init__()
        self.db = db
        self.settings = settings
        self.users = UserRepo(db)

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(460, 560)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(40, 32, 40, 32)
        outer.addStretch(1)

        self.card = Card(self, spacing=14)
        # Фиксированная ширина, а не максимальная: при выравнивании по центру
        # layout отдаёт карточке ширину sizeHint, и перенос строк в
        # предупреждении считался бы не от той ширины — текст обрезался.
        self.card.setFixedWidth(420)
        outer.addWidget(self.card, 0, Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch(1)

        self.footer = QLabel(f"{APP_NAME} {APP_VERSION} · локальное хранение данных")
        self.footer.setObjectName("Dim")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(self.footer)

        self.stack = PageSwitcher()
        self.card.body.addWidget(self.stack)
        self.stack.addWidget(self._build_signin())
        self.stack.addWidget(self._build_signup())

        self._refresh_profiles()

    # -- построение экранов --------------------------------------------------
    def _build_signin(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        lang_row = QHBoxLayout()
        lang_row.addStretch(1)
        self.lang_box = QComboBox()
        for code, label in available_languages():
            self.lang_box.addItem(label, code)
        self.lang_box.setCurrentIndex(
            max(0, [c for c, _ in available_languages()].index(current_language()))
        )
        self.lang_box.currentIndexChanged.connect(self._on_language)
        self.lang_box.setMaximumWidth(140)
        lang_row.addWidget(self.lang_box)
        lay.addLayout(lang_row)

        self.title = QLabel(tr("login.title"))
        self.title.setObjectName("H1")
        lay.addWidget(self.title)
        self.subtitle = QLabel(tr("login.subtitle"))
        self.subtitle.setObjectName("Dim")
        self.subtitle.setWordWrap(True)
        lay.addWidget(self.subtitle)

        self.lbl_user = QLabel(tr("login.username"))
        lay.addWidget(self.lbl_user)
        self.profile_box = QComboBox()
        self.profile_box.setEditable(False)
        self.profile_box.currentTextChanged.connect(self._on_profile_changed)
        lay.addWidget(self.profile_box)

        self.lbl_pass = QLabel(tr("login.password"))
        lay.addWidget(self.lbl_pass)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.returnPressed.connect(self._do_signin)
        lay.addWidget(self.password)

        self.remember = QCheckBox(tr("login.remember"))
        self.remember.setEnabled(keyring_available())
        self.remember.setChecked(self.settings.remember_master_password)
        if not keyring_available():
            self.remember.setToolTip("Установите пакет keyring, чтобы включить эту опцию")
        lay.addWidget(self.remember)

        self.error = QLabel("")
        self.error.setObjectName("Error")
        self.error.setWordWrap(True)
        self.error.setVisible(False)
        lay.addWidget(self.error)

        self.btn_signin = QPushButton(tr("login.signin"))
        self.btn_signin.setObjectName("Primary")
        self.btn_signin.clicked.connect(self._do_signin)
        lay.addWidget(self.btn_signin)

        self.btn_to_signup = QPushButton(tr("login.create"))
        self.btn_to_signup.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        lay.addWidget(self.btn_to_signup)
        return page

    def _build_signup(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        self.su_title = QLabel(tr("login.create_title"))
        self.su_title.setObjectName("H1")
        lay.addWidget(self.su_title)

        self.su_warning = QLabel(tr("login.warning"))
        self.su_warning.setObjectName("Dim")
        self.su_warning.setWordWrap(True)
        lay.addWidget(self.su_warning)

        self.su_lbl_user = QLabel(tr("login.username"))
        lay.addWidget(self.su_lbl_user)
        self.su_username = QLineEdit()
        lay.addWidget(self.su_username)

        self.su_lbl_pass = QLabel(tr("login.password"))
        lay.addWidget(self.su_lbl_pass)
        self.su_password = QLineEdit()
        self.su_password.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.su_password)

        self.su_lbl_pass2 = QLabel(tr("login.password2"))
        lay.addWidget(self.su_lbl_pass2)
        self.su_password2 = QLineEdit()
        self.su_password2.setEchoMode(QLineEdit.EchoMode.Password)
        self.su_password2.returnPressed.connect(self._do_signup)
        lay.addWidget(self.su_password2)

        self.su_error = QLabel("")
        self.su_error.setObjectName("Error")
        self.su_error.setWordWrap(True)
        self.su_error.setVisible(False)
        lay.addWidget(self.su_error)

        self.su_btn_create = QPushButton(tr("login.create"))
        self.su_btn_create.setObjectName("Primary")
        self.su_btn_create.clicked.connect(self._do_signup)
        lay.addWidget(self.su_btn_create)

        self.su_btn_back = QPushButton(tr("common.cancel"))
        self.su_btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        lay.addWidget(self.su_btn_back)
        return page

    # -- логика --------------------------------------------------------------
    def _refresh_profiles(self) -> None:
        names = self.users.list_usernames()
        self.profile_box.clear()
        self.profile_box.addItems(names)
        if not names:
            self._show_error(tr("login.no_profiles"))
            self.stack.setCurrentIndex(1)
            return
        if self.settings.last_username in names:
            self.profile_box.setCurrentText(self.settings.last_username)
        self._on_profile_changed(self.profile_box.currentText())

    def _on_profile_changed(self, username: str) -> None:
        """Подставляет сохранённый пароль, если пользователь просил его запомнить."""
        self.password.clear()
        if username and self.settings.remember_master_password and keyring_available():
            saved = keyring_get_password(username)
            if saved:
                self.password.setText(saved)

    def _on_language(self) -> None:
        code = self.lang_box.currentData()
        set_language(code)
        self.settings.language = code
        self.settings.save()
        self._retranslate()

    def _retranslate(self) -> None:
        self.title.setText(tr("login.title"))
        self.subtitle.setText(tr("login.subtitle"))
        self.lbl_user.setText(tr("login.username"))
        self.lbl_pass.setText(tr("login.password"))
        self.remember.setText(tr("login.remember"))
        self.btn_signin.setText(tr("login.signin"))
        self.btn_to_signup.setText(tr("login.create"))
        self.su_title.setText(tr("login.create_title"))
        self.su_warning.setText(tr("login.warning"))
        self.su_lbl_user.setText(tr("login.username"))
        self.su_lbl_pass.setText(tr("login.password"))
        self.su_lbl_pass2.setText(tr("login.password2"))
        self.su_btn_create.setText(tr("login.create"))
        self.su_btn_back.setText(tr("common.cancel"))

    def _show_error(self, text: str) -> None:
        self.error.setText(text)
        self.error.setVisible(bool(text))

    def _show_signup_error(self, text: str) -> None:
        self.su_error.setText(text)
        self.su_error.setVisible(bool(text))

    def _do_signin(self) -> None:
        username = self.profile_box.currentText().strip()
        password = self.password.text()
        if not username or not password:
            self._show_error(tr("login.bad_credentials"))
            return
        self.btn_signin.setEnabled(False)
        try:
            session: Session | None = self.users.authenticate(username, password)
        finally:
            self.btn_signin.setEnabled(True)
        if session is None:
            self._show_error(tr("login.bad_credentials"))
            return

        self.settings.last_username = username
        self.settings.remember_master_password = self.remember.isChecked()
        self.settings.save()
        if self.remember.isChecked():
            keyring_store_password(username, password)
        else:
            keyring_delete_password(username)

        self._show_error("")
        self.logged_in.emit(session)

    def _do_signup(self) -> None:
        username = self.su_username.text().strip()
        p1, p2 = self.su_password.text(), self.su_password2.text()
        if not username:
            self._show_signup_error(tr("login.username"))
            return
        if self.users.exists(username):
            self._show_signup_error(tr("login.user_exists"))
            return
        if len(p1) < MIN_PASSWORD_LEN:
            self._show_signup_error(tr("login.password_short"))
            return
        if p1 != p2:
            self._show_signup_error(tr("login.password_mismatch"))
            return

        session = self.users.create(username, p1)
        self.settings.last_username = username
        self.settings.save()
        self._show_signup_error("")
        self.logged_in.emit(session)

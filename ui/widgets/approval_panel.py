"""Панель решений human-in-the-loop (этап 7).

Когда ядро останавливается и ждёт человека, здесь появляется карточка с
вопросом, выжимкой по делу и кнопками. Панель намеренно встроена в страницу
«Выполнение», а не сделана модальным окном: вопросов может быть несколько
одновременно, и модалка заслоняла бы прогресс, по которому как раз и
принимается решение.
"""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.hitl import DECISION_TITLES, REASON_TITLES, ApprovalRequest, Decision
from ui.theme import current_palette

#: у деструктивных решений своя окраска, чтобы их не нажимали на автомате
DECISION_STYLES = {
    Decision.APPROVE: "Primary",
    Decision.REWORK: "",
    Decision.SKIP: "",
    Decision.ABORT: "Danger",
}

DECISION_HINTS = {
    Decision.APPROVE: "Принять результат как есть и продолжить",
    Decision.REWORK: "Вернуть исполнителю; комментарий уйдёт ему первым",
    Decision.SKIP: "Пометить подзадачу неудачной и идти дальше",
    Decision.ABORT: "Остановить весь прогон",
}


class ApprovalCard(QFrame):
    """Один вопрос к пользователю."""

    def __init__(self, request: ApprovalRequest,
                 on_decide: Callable[[int, Decision, str], None],
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.request = request
        self.on_decide = on_decide

        colours = current_palette()
        self.setObjectName("Card")
        self.setStyleSheet(
            f"QFrame#Card {{ border: 1px solid {colours['warn']}; "
            f"border-radius: 12px; background: {colours['surface']}; }}"
        )

        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(8)

        head = QHBoxLayout()
        badge = QLabel(REASON_TITLES.get(request.reason, request.reason.value))
        badge.setStyleSheet(
            f"color: {colours['warn']}; border: 1px solid {colours['warn']};"
            f"border-radius: 9px; padding: 2px 10px; font-size: 12px; font-weight: 600;"
        )
        head.addWidget(badge)
        if request.agent_name:
            who = QLabel(request.agent_name)
            who.setObjectName("Dim")
            head.addWidget(who)
        head.addStretch(1)
        lay.addLayout(head)

        question = QLabel(request.question)
        question.setObjectName("H2")
        question.setWordWrap(True)
        lay.addWidget(question)

        if request.details:
            self.details = QLabel(_clip(request.details, 700))
            self.details.setObjectName("Dim")
            self.details.setWordWrap(True)
            self.details.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            lay.addWidget(self.details)

            if len(request.details) > 700:
                self._expanded = False
                self.btn_more = QPushButton("Показать полностью")
                self.btn_more.clicked.connect(self._toggle_details)
                lay.addWidget(self.btn_more, 0, Qt.AlignmentFlag.AlignLeft)

        self.comment = QLineEdit()
        self.comment.setPlaceholderText(
            "Комментарий (уйдёт исполнителю при отправке на доработку)"
        )
        lay.addWidget(self.comment)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        for decision in request.options:
            button = QPushButton(DECISION_TITLES.get(decision, decision.value))
            style = DECISION_STYLES.get(decision, "")
            if style:
                button.setObjectName(style)
            button.setToolTip(DECISION_HINTS.get(decision, ""))
            button.clicked.connect(
                lambda _=False, d=decision: self._decide(d)
            )
            buttons.addWidget(button)
        buttons.addStretch(1)
        lay.addLayout(buttons)

    def _toggle_details(self) -> None:
        self._expanded = not self._expanded
        self.details.setText(self.request.details if self._expanded
                             else _clip(self.request.details, 700))
        self.btn_more.setText("Свернуть" if self._expanded else "Показать полностью")

    def _decide(self, decision: Decision) -> None:
        self.setEnabled(False)
        self.on_decide(self.request.id, decision, self.comment.text())


class ApprovalPanel(QWidget):
    """Стопка открытых вопросов; скрывается, когда их нет."""

    def __init__(self, on_decide: Callable[[int, Decision, str], None],
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.on_decide = on_decide
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(10)
        self.setVisible(False)

    def set_requests(self, requests: list[ApprovalRequest]) -> None:
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for request in requests:
            self._layout.addWidget(ApprovalCard(request, self.on_decide, self))
        self.setVisible(bool(requests))


def _clip(text: str, limit: int) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[:limit] + " …"

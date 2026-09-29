"""Мелкие переиспользуемые виджеты."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from ui.theme import STATUS_COLORS


class Card(QFrame):
    """Карточка-контейнер со скруглением и рамкой."""

    def __init__(self, parent: QWidget | None = None, spacing: int = 12) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(16, 16, 16, 16)
        self.body.setSpacing(spacing)


class StatusBadge(QLabel):
    """Цветной бейдж статуса агента/подзадачи."""

    def __init__(self, status: str = "idle", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Иначе в строке с крупным заголовком бейдж растягивается по высоте.
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.set_status(status)

    def set_status(self, status: str) -> None:
        color = STATUS_COLORS.get(status, STATUS_COLORS["idle"])
        self.setText(tr(f"status.{status}") if f"status.{status}" else status)
        self.setStyleSheet(
            f"color: {color}; border: 1px solid {color}; border-radius: 9px;"
            f"padding: 2px 10px; font-size: 12px; font-weight: 600; background: transparent;"
        )


class Header(QWidget):
    """Заголовок страницы: title + subtitle + слот для кнопок справа."""

    def __init__(self, title: str, subtitle: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)

        texts = QVBoxLayout()
        texts.setSpacing(2)
        self.title_label = QLabel(title)
        self.title_label.setObjectName("H1")
        texts.addWidget(self.title_label)
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("Dim")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setVisible(bool(subtitle))
        texts.addWidget(self.subtitle_label)
        row.addLayout(texts, 1)

        self.actions = QHBoxLayout()
        self.actions.setSpacing(8)
        row.addLayout(self.actions)

    def add_action(self, button: QPushButton) -> None:
        self.actions.addWidget(button)

    def set_texts(self, title: str, subtitle: str = "") -> None:
        self.title_label.setText(title)
        self.subtitle_label.setText(subtitle)
        self.subtitle_label.setVisible(bool(subtitle))


class PageSwitcher(QWidget):
    """Замена QStackedWidget для форм с переносом строк.

    QStackedWidget не передаёт height-for-width своих страниц, из-за чего
    длинные надписи с переносом обрезаются. Здесь страницы просто лежат
    в одном layout, а видна только текущая.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._pages: list[QWidget] = []
        self._current = -1

    def addWidget(self, page: QWidget) -> int:  # noqa: N802 — как у QStackedWidget
        self._pages.append(page)
        self._layout.addWidget(page)
        if self._current < 0:
            self._current = 0
        page.setVisible(len(self._pages) - 1 == self._current)
        return len(self._pages) - 1

    def setCurrentIndex(self, index: int) -> None:  # noqa: N802
        self._current = index
        for i, page in enumerate(self._pages):
            page.setVisible(i == index)

    def currentIndex(self) -> int:  # noqa: N802
        return self._current


class EmptyState(QLabel):
    """Заглушка для пустых списков."""

    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("Dim")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWordWrap(True)
        self.setMinimumHeight(120)


def confirm(parent: QWidget, text: str) -> bool:
    """Диалог подтверждения с локализованными кнопками."""
    box = QMessageBox(parent)
    box.setWindowTitle(tr("common.confirm"))
    box.setText(text)
    box.setIcon(QMessageBox.Icon.Question)
    yes = box.addButton(tr("common.yes"), QMessageBox.ButtonRole.YesRole)
    box.addButton(tr("common.no"), QMessageBox.ButtonRole.NoRole)
    box.exec()
    return box.clickedButton() is yes


def warn(parent: QWidget, text: str, title: str = "") -> None:
    QMessageBox.warning(parent, title or tr("common.error"), text)


def info(parent: QWidget, text: str, title: str = "") -> None:
    QMessageBox.information(parent, title or tr("common.success"), text)

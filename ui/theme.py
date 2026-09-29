"""Оформление приложения: палитра и QSS.

Тема тёмная по умолчанию, светлая — переключается в настройках. Цвета
статусов вынесены отдельно: ими красятся бейджи агентов на дашборде.
"""

from __future__ import annotations

from app.config import PATHS

DARK = {
    "bg": "#12141a",
    "surface": "#191c24",
    "surface2": "#20242e",
    "border": "#2c313d",
    "text": "#e6e9f0",
    "text_dim": "#99a1b3",
    "accent": "#6c8cff",
    "accent_hover": "#8099ff",
    "danger": "#ef5f6b",
    "ok": "#3ecf8e",
    "warn": "#f0b429",
}

LIGHT = {
    "bg": "#f4f5f8",
    "surface": "#ffffff",
    "surface2": "#eef0f5",
    "border": "#d7dae2",
    "text": "#1a1d24",
    "text_dim": "#6a7080",
    "accent": "#3a5bd9",
    "accent_hover": "#2c49ba",
    "danger": "#d63a48",
    "ok": "#1f9d63",
    "warn": "#c98a06",
}

STATUS_COLORS = {
    "idle": "#99a1b3",
    "running": "#6c8cff",
    "paused": "#f0b429",
    "error": "#ef5f6b",
    "done": "#3ecf8e",
    "review": "#b07cff",
    "rework": "#f0b429",
}


#: текущая активная тема; графики берут цвета отсюда, чтобы не тянуть
#: настройки через полдюжины конструкторов
_ACTIVE_THEME = "dark"


def palette(theme: str) -> dict[str, str]:
    return LIGHT if theme == "light" else DARK


def set_active_theme(theme: str) -> None:
    """Запоминает тему, применённую к приложению."""
    global _ACTIVE_THEME
    _ACTIVE_THEME = theme if theme in ("dark", "light") else "dark"


def active_theme() -> str:
    return _ACTIVE_THEME


def current_palette() -> dict[str, str]:
    """Палитра активной темы — для виджетов, рисующих себя вручную."""
    return palette(_ACTIVE_THEME)


_ARROW_POINTS = {"down": ((1, 3), (5, 7), (9, 3)), "up": ((1, 7), (5, 3), (9, 7))}


def _arrow_icon(direction: str, colour: str) -> str:
    """Рисует стрелку в PNG-файл кэша и возвращает путь для QSS.

    Стрелки у QComboBox и QSpinBox пропадают, как только их кнопки
    стилизованы через QSS, а треугольник из рамок Qt не рисует — нужна
    картинка. SVG не годится: плагина qsvg в сборке PySide6 может не быть.
    Рядом кладётся вариант @2x — Qt сам берёт его на HiDPI-экранах.
    Вызывать можно только после создания QApplication.
    """
    from PySide6.QtCore import QPointF, Qt
    from PySide6.QtGui import QColor, QImage, QPainter, QPen

    folder = PATHS.home / "cache" / "theme"
    base = f"arrow_{direction}_{colour.lstrip('#')}"
    path = folder / f"{base}.png"
    if not path.exists():
        folder.mkdir(parents=True, exist_ok=True)
        for scale, target in ((1, path), (2, folder / f"{base}@2x.png")):
            image = QImage(10 * scale, 10 * scale, QImage.Format.Format_ARGB32)
            image.fill(Qt.GlobalColor.transparent)
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            pen = QPen(QColor(colour), 1.6 * scale)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.drawPolyline([QPointF(x * scale, y * scale)
                                  for x, y in _ARROW_POINTS[direction]])
            painter.end()
            image.save(str(target))
    return path.as_posix()


def stylesheet(theme: str = "dark") -> str:
    """Собирает QSS под выбранную палитру."""
    set_active_theme(theme)
    c = palette(theme)
    down, up = _arrow_icon("down", c["text_dim"]), _arrow_icon("up", c["text_dim"])
    down_off, up_off = _arrow_icon("down", c["border"]), _arrow_icon("up", c["border"])
    return f"""
    QWidget {{
        background: {c['bg']};
        color: {c['text']};
        font-family: "Inter", "Segoe UI", "SF Pro Text", "Noto Sans", sans-serif;
        font-size: 14px;
    }}
    /* Правило выше красит фон всем виджетам. Внутри карточек это давало
       тёмные «заплатки» под надписями и под контейнерами-раскладками, поэтому
       у них фон прозрачный. «.QWidget» — только сам QWidget, без подклассов:
       окна и страницы свой фон сохраняют. */
    QLabel, QCheckBox, QRadioButton {{ background: transparent; }}
    .QWidget {{ background: transparent; }}
    QLabel#H1 {{ font-size: 24px; font-weight: 600; }}
    QLabel#H2 {{ font-size: 18px; font-weight: 600; }}
    QLabel#Dim {{ color: {c['text_dim']}; }}
    QLabel#Error {{ color: {c['danger']}; }}
    QLabel#Ok {{ color: {c['ok']}; }}

    QFrame#Card, QWidget#Card {{
        background: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 12px;
    }}
    QFrame#Sidebar {{
        background: {c['surface']};
        border-right: 1px solid {c['border']};
    }}

    QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
        background: {c['surface2']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 7px 10px;
        selection-background-color: {c['accent']};
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {{
        border: 1px solid {c['accent']};
    }}
    QComboBox::drop-down {{ border: none; width: 22px; }}
    QComboBox::down-arrow {{ image: url("{down}"); width: 10px; height: 10px; }}
    QComboBox::down-arrow:on {{ image: url("{up}"); }}
    QAbstractSpinBox {{ padding-right: 24px; }}
    QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {{
        subcontrol-origin: border; width: 22px;
        border: none; background: transparent;
    }}
    QAbstractSpinBox::up-button {{ subcontrol-position: top right; }}
    QAbstractSpinBox::down-button {{ subcontrol-position: bottom right; }}
    QAbstractSpinBox::up-arrow {{ image: url("{up}"); width: 8px; height: 8px; }}
    QAbstractSpinBox::down-arrow {{ image: url("{down}"); width: 8px; height: 8px; }}
    QAbstractSpinBox::up-arrow:disabled, QAbstractSpinBox::up-arrow:off {{ image: url("{up_off}"); }}
    QAbstractSpinBox::down-arrow:disabled, QAbstractSpinBox::down-arrow:off {{ image: url("{down_off}"); }}
    QComboBox QAbstractItemView {{
        background: {c['surface2']};
        border: 1px solid {c['border']};
        selection-background-color: {c['accent']};
        outline: none;
    }}

    QPushButton {{
        background: {c['surface2']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 8px 16px;
    }}
    QPushButton:hover {{ border-color: {c['accent']}; }}
    QPushButton:disabled {{ color: {c['text_dim']}; border-color: {c['border']}; }}
    QPushButton#Primary {{
        background: {c['accent']};
        border: 1px solid {c['accent']};
        color: #ffffff;
        font-weight: 600;
    }}
    QPushButton#Primary:hover {{ background: {c['accent_hover']}; }}
    QPushButton#Primary:disabled {{
        background: {c['surface2']}; border-color: {c['border']};
        color: {c['text_dim']}; font-weight: 600;
    }}
    QPushButton#Icon {{ padding: 6px 0; }}
    QPushButton#Danger {{ color: {c['danger']}; }}
    QPushButton#Danger:hover {{ border-color: {c['danger']}; }}
    QPushButton#Nav {{
        background: transparent;
        border: none;
        border-radius: 8px;
        padding: 10px 14px;
        text-align: left;
    }}
    QPushButton#Nav:hover {{ background: {c['surface2']}; }}
    QPushButton#Nav:checked {{ background: {c['accent']}; color: #ffffff; font-weight: 600; }}

    QListWidget, QTableWidget, QTreeWidget {{
        background: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 10px;
        outline: none;
    }}
    QListWidget::item {{ padding: 8px; border-radius: 6px; }}
    QListWidget::item:selected {{ background: {c['accent']}; color: #ffffff; }}
    QHeaderView::section {{
        background: {c['surface2']};
        border: none;
        border-bottom: 1px solid {c['border']};
        padding: 8px;
        font-weight: 600;
    }}
    QTableWidget {{ gridline-color: {c['border']}; }}

    QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
    QScrollBar::handle:vertical {{
        background: {c['border']}; border-radius: 5px; min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {c['text_dim']}; }}
    QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
    QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px; }}
    QScrollBar::handle:horizontal {{
        background: {c['border']}; border-radius: 5px; min-width: 30px;
    }}

    QProgressBar {{
        background: {c['surface2']};
        border: none; border-radius: 6px; height: 10px; text-align: center;
    }}
    QProgressBar::chunk {{ background: {c['accent']}; border-radius: 6px; }}

    QCheckBox::indicator, QRadioButton::indicator {{
        width: 16px; height: 16px; border-radius: 4px;
        border: 1px solid {c['border']}; background: {c['surface2']};
    }}
    QCheckBox::indicator:checked {{ background: {c['accent']}; border-color: {c['accent']}; }}

    QTabWidget::pane {{ border: 1px solid {c['border']}; border-radius: 10px; top: -1px; }}
    QTabBar::tab {{
        background: transparent; padding: 8px 16px; border: none;
        color: {c['text_dim']};
    }}
    QTabBar::tab:selected {{ color: {c['text']}; border-bottom: 2px solid {c['accent']}; }}

    QToolTip {{
        background: {c['surface2']}; color: {c['text']};
        border: 1px solid {c['border']}; padding: 6px; border-radius: 6px;
    }}
    QMenu {{
        background: {c['surface2']}; border: 1px solid {c['border']}; border-radius: 8px;
    }}
    QMenu::item:selected {{ background: {c['accent']}; }}
    QSplitter::handle {{ background: {c['border']}; }}
    """

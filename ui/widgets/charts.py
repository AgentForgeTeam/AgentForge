"""Лёгкие графики на QPainter.

Намеренно без QtCharts и pyqtgraph: дашборду нужны две простые диаграммы,
а собственная отрисовка не тянет зависимостей, мгновенно подхватывает тему
приложения и не ломается при разных сборках PySide6.

Все виджеты безопасны к пустым данным: при отсутствии точек рисуется
аккуратная надпись, а не пустой прямоугольник.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from ui.theme import current_palette

PADDING_LEFT = 58
PADDING_RIGHT = 14
PADDING_TOP = 26
PADDING_BOTTOM = 30
GRID_LINES = 4


def _color(key: str, alpha: int = 255) -> QColor:
    colour = QColor(current_palette().get(key, "#888888"))
    colour.setAlpha(alpha)
    return colour


def _nice_max(value: float) -> float:
    """Округляет верх шкалы вверх до «красивого» числа (1, 2, 5 × 10^n)."""
    if value <= 0:
        return 1.0
    import math

    exponent = math.floor(math.log10(value))
    base = 10 ** exponent
    for step in (1, 2, 2.5, 5, 10):
        if value <= step * base:
            return step * base
    return 10 * base


def _fmt(value: float, unit: str) -> str:
    """Короткая подпись оси: 12.3k, $0.0412, 1.2M."""
    if unit == "usd":
        if value >= 1:
            return f"${value:,.2f}".replace(",", " ")
        return f"${value:.4f}"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}k"
    return f"{value:.0f}"


class ChartBase(QWidget):
    """Общая рамка: заголовок, сетка, подписи оси Y."""

    def __init__(self, title: str = "", unit: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.title = title
        self.unit = unit
        self.empty_text = "нет данных"
        self.setMinimumHeight(190)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def set_title(self, title: str) -> None:
        self.title = title
        self.update()

    def _plot_rect(self) -> QRectF:
        return QRectF(
            PADDING_LEFT, PADDING_TOP,
            max(10.0, self.width() - PADDING_LEFT - PADDING_RIGHT),
            max(10.0, self.height() - PADDING_TOP - PADDING_BOTTOM),
        )

    def _draw_frame(self, painter: QPainter, top_value: float) -> QRectF:
        """Рисует заголовок, горизонтальную сетку и подписи, возвращает поле графика."""
        rect = self._plot_rect()

        if self.title:
            font = QFont(painter.font())
            font.setPointSizeF(max(8.0, font.pointSizeF()))
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QPen(_color("text")))
            painter.drawText(QRectF(PADDING_LEFT, 2, rect.width(), 20),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             self.title)
            font.setBold(False)
            painter.setFont(font)

        grid_pen = QPen(_color("border"))
        grid_pen.setWidthF(1.0)
        painter.setPen(grid_pen)
        for i in range(GRID_LINES + 1):
            y = rect.bottom() - rect.height() * i / GRID_LINES
            painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))
            painter.setPen(QPen(_color("text_dim")))
            painter.drawText(
                QRectF(0, y - 9, PADDING_LEFT - 8, 18),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                _fmt(top_value * i / GRID_LINES, self.unit),
            )
            painter.setPen(grid_pen)
        return rect

    def _draw_empty(self, painter: QPainter) -> None:
        painter.setPen(QPen(_color("text_dim")))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.empty_text)


@dataclass
class SeriesPoint:
    """Точка временного ряда: подпись по оси X и значение."""

    label: str
    value: float


class LineChart(ChartBase):
    """Кумулятивная кривая с заливкой под ней."""

    def __init__(self, title: str = "", unit: str = "",
                 parent: QWidget | None = None) -> None:
        super().__init__(title, unit, parent)
        self._points: list[SeriesPoint] = []

    def set_points(self, points: list[SeriesPoint]) -> None:
        self._points = points
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802 — сигнатура Qt
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if len(self._points) < 2:
            if self.title:
                self._draw_frame(painter, 1.0)
            self._draw_empty(painter)
            return

        top = _nice_max(max(p.value for p in self._points))
        rect = self._draw_frame(painter, top)

        step = rect.width() / (len(self._points) - 1)
        coords = [
            QPointF(rect.left() + i * step,
                    rect.bottom() - (p.value / top) * rect.height())
            for i, p in enumerate(self._points)
        ]

        # Заливка под кривой
        area = QPainterPath()
        area.moveTo(QPointF(coords[0].x(), rect.bottom()))
        for point in coords:
            area.lineTo(point)
        area.lineTo(QPointF(coords[-1].x(), rect.bottom()))
        area.closeSubpath()
        painter.fillPath(area, _color("accent", 46))

        line_pen = QPen(_color("accent"))
        line_pen.setWidthF(2.0)
        painter.setPen(line_pen)
        path = QPainterPath(coords[0])
        for point in coords[1:]:
            path.lineTo(point)
        painter.drawPath(path)

        # Точка последнего значения и её подпись
        painter.setBrush(_color("accent"))
        painter.drawEllipse(coords[-1], 3.5, 3.5)
        painter.setPen(QPen(_color("text")))
        painter.drawText(
            QRectF(coords[-1].x() - 90, coords[-1].y() - 24, 86, 18),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
            _fmt(self._points[-1].value, self.unit),
        )

        # Подписи по краям оси X
        painter.setPen(QPen(_color("text_dim")))
        painter.drawText(QRectF(rect.left(), rect.bottom() + 6, 120, 18),
                         Qt.AlignmentFlag.AlignLeft, self._points[0].label)
        painter.drawText(QRectF(rect.right() - 120, rect.bottom() + 6, 120, 18),
                         Qt.AlignmentFlag.AlignRight, self._points[-1].label)


@dataclass
class Bar:
    """Столбец: подпись, значение и необязательный цвет."""

    label: str
    value: float
    color: str = ""


class BarChart(ChartBase):
    """Горизонтальные столбцы — удобны, когда подписи длинные (имена агентов)."""

    ROW_HEIGHT = 30

    def __init__(self, title: str = "", unit: str = "",
                 parent: QWidget | None = None) -> None:
        super().__init__(title, unit, parent)
        self._bars: list[Bar] = []

    def set_bars(self, bars: list[Bar]) -> None:
        self._bars = bars
        self.setMinimumHeight(max(140, PADDING_TOP + 14 + self.ROW_HEIGHT * max(1, len(bars))))
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.title:
            font = QFont(painter.font())
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QPen(_color("text")))
            painter.drawText(QRectF(10, 2, self.width() - 20, 20),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             self.title)
            font.setBold(False)
            painter.setFont(font)

        if not self._bars:
            self._draw_empty(painter)
            return

        top = max((b.value for b in self._bars), default=0.0) or 1.0
        label_width = 150.0
        metrics = painter.fontMetrics()
        bar_left = 12 + label_width
        bar_width = max(30.0, self.width() - bar_left - 90)

        for i, bar in enumerate(self._bars):
            y = PADDING_TOP + 6 + i * self.ROW_HEIGHT
            painter.setPen(QPen(_color("text_dim")))
            painter.drawText(
                QRectF(12, y, label_width - 10, self.ROW_HEIGHT - 8),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                metrics.elidedText(bar.label, Qt.TextElideMode.ElideRight,
                                   int(label_width - 10)),
            )

            track = QRectF(bar_left, y + 6, bar_width, self.ROW_HEIGHT - 18)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(_color("surface2"))
            painter.drawRoundedRect(track, 5, 5)

            filled = QRectF(track)
            filled.setWidth(max(3.0, bar_width * (bar.value / top)))
            painter.setBrush(QColor(bar.color) if bar.color else _color("accent"))
            painter.drawRoundedRect(filled, 5, 5)

            painter.setPen(QPen(_color("text")))
            painter.drawText(
                QRectF(bar_left + bar_width + 8, y, 80, self.ROW_HEIGHT - 8),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                _fmt(bar.value, self.unit),
            )


class SegmentBar(QWidget):
    """Одна полоска, разбитая на цветные сегменты — статусы подзадач."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._segments: list[tuple[str, int, str]] = []   # (подпись, количество, цвет)
        self.setFixedHeight(14)

    def set_segments(self, segments: list[tuple[str, int, str]]) -> None:
        self._segments = [s for s in segments if s[1] > 0]
        self.update()
        self.setToolTip(", ".join(f"{label}: {count}" for label, count, _ in self._segments))

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        total = sum(count for _, count, _ in self._segments)
        track = QRectF(0, 0, self.width(), self.height())
        painter.setBrush(_color("surface2"))
        painter.drawRoundedRect(track, 7, 7)
        if not total:
            return

        painter.setClipping(True)
        path = QPainterPath()
        path.addRoundedRect(track, 7, 7)
        painter.setClipPath(path)

        x = 0.0
        for _, count, colour in self._segments:
            width = self.width() * count / total
            painter.setBrush(QColor(colour))
            painter.drawRect(QRectF(x, 0, width + 0.5, self.height()))
            x += width

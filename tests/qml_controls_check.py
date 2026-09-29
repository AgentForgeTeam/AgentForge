"""Переключатели Ao (Toggle, Chip) держатся за данные и после щелчка.

Отдельный процесс, как и тур: Qt нужен собственный цикл событий. Код
возврата 0 — всё в порядке, иначе в stdout описание расхождения.

Ошибка, которую ловит проверка: checkable-кнопка сама переключает
``checked``, и если щелчок не изменил данные (сохранение не прошло, щелчок
по уже выбранной роли агента), она показывала состояние, которого нет.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

QML = b"""
import QtQuick
import Ao

Item {
    id: root
    property bool store: false
    property bool saves: false
    Toggle {
        objectName: "toggle"
        isOn: root.store
        onToggled: if (root.saves) root.store = checked
    }
    Chip {
        objectName: "chip"
        isOn: root.store
        onClicked: if (root.saves) root.store = checked
    }
}
"""


def main() -> int:
    from PySide6.QtCore import QUrl
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlComponent, QQmlEngine
    from PySide6.QtQuickControls2 import QQuickStyle

    from ui.app import QML_DIR, ensure_qt_dll_path

    ensure_qt_dll_path()
    QQuickStyle.setStyle("Basic")
    app = QGuiApplication(sys.argv)
    engine = QQmlEngine()
    engine.addImportPath(str(QML_DIR))
    component = QQmlComponent(engine)
    component.setData(QML, QUrl.fromLocalFile(str(ROOT / "tests" / "controls.qml")))
    root = component.create()
    if root is None:
        print("QML не загрузился:", [e.toString() for e in component.errors()])
        return 1

    def settle() -> None:
        for _ in range(5):
            app.processEvents()

    problems: list[str] = []
    for name in ("toggle", "chip"):
        control = root.findChild(object, name)

        def expect(state: bool, when: str) -> None:
            settle()
            if bool(control.property("checked")) != state:
                problems.append(f"{name}: {when}: checked={control.property('checked')}, "
                                f"ожидалось {state}")

        root.setProperty("saves", False)
        root.setProperty("store", False)
        control.click()
        expect(False, "владелец не сохранил щелчок — показываем сохранённое")
        root.setProperty("store", True)
        expect(True, "данные изменились извне — переключатель следует за ними")

        root.setProperty("saves", True)
        control.click()
        expect(False, "щелчок сохранён владельцем")
        root.setProperty("store", True)
        expect(True, "после щелчка привязка к данным не потеряна")

    if problems:
        print("\n".join(problems))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

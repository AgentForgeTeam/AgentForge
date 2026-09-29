import QtQuick
import QtQuick.Controls.Basic as T

// Тонкая полоса прокрутки, которая проявляется при наведении и движении.
T.ScrollBar {
    id: bar
    implicitWidth: 10
    implicitHeight: 10
    padding: 2
    minimumSize: 0.08
    policy: T.ScrollBar.AsNeeded
    contentItem: Rectangle {
        implicitWidth: 6
        implicitHeight: 6
        radius: 3
        color: bar.pressed ? Theme.violetSoft : (bar.hovered ? Theme.borderStrong : Theme.surface3)
        opacity: bar.active || bar.hovered ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: Theme.normal } }
        Behavior on color { ColorAnimation { duration: Theme.fast } }
    }
    background: Item {}
}

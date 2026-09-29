import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Переключатель с «пружинящим» бегунком и подписью слева.
T.AbstractButton {
    id: control
    property string label: ""
    property string hint: ""
    checkable: true
    hoverEnabled: true
    implicitWidth: row.implicitWidth
    implicitHeight: Math.max(28, row.implicitHeight)
    opacity: enabled ? 1 : 0.45

    contentItem: RowLayout {
        id: row
        spacing: 14
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 2
            visible: control.label !== ""
            AText { text: control.label; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone }
            AText {
                visible: control.hint !== ""
                text: control.hint
                mute: true
                size: Theme.fsSmall
                wrapMode: Text.Wrap
                elide: Text.ElideNone
                Layout.fillWidth: true
            }
        }
        Rectangle {
            id: track
            Layout.alignment: Qt.AlignVCenter
            width: 42; height: 24; radius: 12
            color: control.checked ? "transparent" : Theme.surface3
            border.width: control.checked ? 0 : 1
            border.color: control.hovered ? Theme.borderStrong : Theme.border
            gradient: control.checked ? onGradient : null
            Gradient {
                id: onGradient
                orientation: Gradient.Horizontal
                GradientStop { position: 0; color: Theme.violet }
                GradientStop { position: 1; color: Theme.teal }
            }
            Rectangle {
                id: knob
                width: 18; height: 18; radius: 9
                y: 3
                x: control.checked ? track.width - width - 3 : 3
                color: "white"
                scale: control.pressed ? 0.85 : 1
                Behavior on x { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutBack; easing.overshoot: 1.6 } }
                Behavior on scale { NumberAnimation { duration: Theme.fast } }
            }
        }
    }
}

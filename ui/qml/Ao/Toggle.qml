import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Переключатель с «пружинящим» бегунком и подписью слева.
//
// Состояние из данных задаётся через isOn, а не через checked. Щелчок
// переключает checked (обработчики onToggled видят новое значение), а затем
// переключатель снова показывает isOn — то, что реально сохранено. Кнопка,
// которой задали checked напрямую, после щелчка, не изменившего данные
// (сохранение не прошло, щелчок по уже выбранному пункту), показывала бы
// состояние, которого на самом деле нет.
T.AbstractButton {
    id: control
    property string label: ""
    property string hint: ""
    property var isOn: undefined
    checkable: true
    checked: isOn === undefined ? false : !!isOn
    hoverEnabled: true

    function resync() {
        control.checked = Qt.binding(function() { return !!control.isOn })
    }
    Connections {
        target: control
        function onToggled() { if (control.isOn !== undefined) Qt.callLater(control.resync) }
    }
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

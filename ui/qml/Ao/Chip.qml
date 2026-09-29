import QtQuick
import QtQuick.Controls.Basic as T

// Переключаемая «таблетка»: для инструментов, опций, фильтров.
// Состояние из данных - через isOn (подробности в Toggle.qml).
T.AbstractButton {
    id: control
    property string iconName: ""
    property color accent: Theme.violet
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
    implicitHeight: 32
    implicitWidth: row.implicitWidth + 26
    scale: pressed ? 0.95 : 1
    Behavior on scale { NumberAnimation { duration: Theme.fast; easing.type: Easing.OutBack } }

    background: Rectangle {
        radius: height / 2
        color: control.checked ? Theme.alpha(control.accent, 0.18)
             : (control.hovered ? Theme.surface3 : Theme.surface2)
        border.width: 1
        border.color: control.checked ? Theme.alpha(control.accent, 0.65) : Theme.border
        Behavior on color { ColorAnimation { duration: Theme.fast } }
        Behavior on border.color { ColorAnimation { duration: Theme.fast } }
    }
    contentItem: Item {
        Row {
            id: row
            anchors.centerIn: parent
            spacing: 6
            Icon {
                name: control.checked ? "check" : control.iconName
                visible: control.checked || control.iconName !== ""
                size: 14
                color: control.checked ? Theme.violetSoft : Theme.textMute
                anchors.verticalCenter: parent.verticalCenter
            }
            AText {
                text: control.text
                size: Theme.fsSmall
                weight: Font.Medium
                color: control.checked ? Theme.text : Theme.textDim
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
}

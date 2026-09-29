import QtQuick
import QtQuick.Controls.Basic as T

// Кнопка-иконка с подсказкой: IconButton { icon: "pencil"; tip: "Изменить" }
T.AbstractButton {
    id: control
    property string iconName: "circle-dot"
    property string tip: ""
    property color tint: Theme.textDim
    property color hoverTint: Theme.text
    property bool danger: false
    property int size: 32
    implicitWidth: size
    implicitHeight: size
    hoverEnabled: true
    opacity: enabled ? 1 : 0.4
    scale: pressed ? 0.9 : 1
    Behavior on scale { NumberAnimation { duration: Theme.fast; easing.type: Easing.OutBack } }

    background: Rectangle {
        radius: Theme.radiusS
        color: control.hovered ? (control.danger ? Theme.alpha(Theme.danger, 0.16)
                                                 : Theme.alpha(Theme.text, 0.07)) : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.fast } }
    }
    contentItem: Icon {
        name: control.iconName
        size: Math.round(control.size * 0.5)
        color: control.hovered ? (control.danger ? Theme.danger : control.hoverTint) : control.tint
    }

    Tip {
        text: control.tip
        shown: control.hovered && control.tip !== ""
    }
}

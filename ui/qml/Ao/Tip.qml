import QtQuick
import QtQuick.Controls.Basic as T

// Подсказка в стиле темы; появляется с небольшой задержкой и «всплывает».
T.ToolTip {
    id: tip
    property bool shown: false
    visible: shown && text !== ""
    delay: 450
    timeout: 6000
    y: -implicitHeight - 8
    x: (parent ? parent.width - implicitWidth : 0) / 2
    padding: 8
    leftPadding: 10
    rightPadding: 10

    contentItem: AText {
        text: tip.text
        size: Theme.fsSmall
        color: Theme.text
        wrapMode: Text.Wrap
        elide: Text.ElideNone
        width: Math.min(implicitWidth, 320)
    }
    background: Rectangle {
        radius: Theme.radiusS
        color: Theme.surface3
        border.color: Theme.borderStrong
    }
    enter: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.fast }
            NumberAnimation { property: "scale"; from: 0.92; to: 1; duration: Theme.fast; easing.type: Easing.OutBack }
        }
    }
    exit: Transition { NumberAnimation { property: "opacity"; to: 0; duration: Theme.fast } }
}

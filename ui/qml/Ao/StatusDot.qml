import QtQuick

// Точка статуса; для «работает» - расходящиеся круги пульса.
Item {
    id: root
    property string status: "idle"
    property int size: 8
    readonly property color tint: Theme.statusColor(status)
    readonly property bool live: status === "running"
    implicitWidth: size
    implicitHeight: size

    Rectangle {
        id: pulse
        anchors.centerIn: parent
        width: root.size; height: root.size; radius: width / 2
        color: "transparent"
        border.width: 2
        border.color: root.tint
        opacity: 0
        visible: root.live && Theme.motion > 0
        SequentialAnimation on scale {
            running: pulse.visible
            loops: Animation.Infinite
            NumberAnimation { from: 1; to: 2.8; duration: 1300; easing.type: Easing.OutCubic }
        }
        SequentialAnimation on opacity {
            running: pulse.visible
            loops: Animation.Infinite
            NumberAnimation { from: 0.8; to: 0; duration: 1300; easing.type: Easing.OutCubic }
        }
    }
    Rectangle {
        anchors.centerIn: parent
        width: root.size; height: root.size; radius: width / 2
        color: root.tint
        Behavior on color { ColorAnimation { duration: Theme.normal } }
    }
}

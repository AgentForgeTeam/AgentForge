import QtQuick
import QtQuick.Layouts

// Сегментированный переключатель: подсветка «переезжает» к выбранному пункту.
// options: [{value, title, icon?}]
Rectangle {
    id: root
    property var options: []
    property var value
    property bool stretch: false
    signal picked(var value)

    readonly property int current: {
        for (var i = 0; i < options.length; ++i)
            if (options[i].value === value) return i
        return -1
    }

    implicitHeight: 36
    implicitWidth: stretch ? 200 : row.implicitWidth + 8
    radius: Theme.radius
    color: Theme.input
    border.color: Theme.border

    Rectangle {
        id: pill
        visible: root.current >= 0 && repeater.count > root.current
        property Item target: repeater.count > root.current && root.current >= 0 ? repeater.itemAt(root.current) : null
        x: target ? row.x + target.x : 4
        y: 4
        width: target ? target.width : 0
        height: root.height - 8
        radius: Theme.radiusS
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0; color: Theme.alpha(Theme.violet, 0.9) }
            GradientStop { position: 1; color: Theme.alpha(Theme.indigo, 0.9) }
        }
        Behavior on x { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
        Behavior on width { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
    }

    RowLayout {
        id: row
        x: 4
        y: 4
        height: root.height - 8
        width: root.stretch ? root.width - 8 : implicitWidth
        spacing: 2
        Repeater {
            id: repeater
            model: root.options
            delegate: Item {
                id: seg
                required property var modelData
                required property int index
                readonly property bool active: index === root.current
                Layout.fillWidth: root.stretch
                Layout.fillHeight: true
                implicitWidth: segRow.implicitWidth + 24
                Row {
                    id: segRow
                    anchors.centerIn: parent
                    spacing: 6
                    Icon {
                        visible: !!seg.modelData.icon
                        name: seg.modelData.icon || "circle-dot"
                        size: 14
                        color: seg.active ? "white" : Theme.textMute
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    AText {
                        text: seg.modelData.title
                        size: Theme.fsSmall
                        weight: seg.active ? Font.DemiBold : Font.Medium
                        color: seg.active ? "white" : (mouse.containsMouse ? Theme.text : Theme.textDim)
                        anchors.verticalCenter: parent.verticalCenter
                        Behavior on color { ColorAnimation { duration: Theme.fast } }
                    }
                }
                MouseArea {
                    id: mouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.picked(seg.modelData.value)
                }
            }
        }
    }
}

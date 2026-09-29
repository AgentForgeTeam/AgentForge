import QtQuick
import QtQuick.Layouts

// Полоса прогресса по статусам: сегменты растут плавно, а под полосой - легенда.
ColumnLayout {
    id: root
    property var segments: []      // [{status, title, count}]
    property bool legend: true
    readonly property int total: {
        var t = 0
        for (var i = 0; i < segments.length; ++i) t += segments[i].count
        return t
    }
    spacing: 10

    Rectangle {
        id: track
        Layout.fillWidth: true
        height: 10
        radius: 5
        color: Theme.surface3
        clip: true
        Row {
            anchors.fill: parent
            spacing: 2
            Repeater {
                model: root.segments
                delegate: Rectangle {
                    required property var modelData
                    height: track.height
                    width: root.total > 0 ? Math.max(0, (track.width - 2 * (root.segments.length - 1)) * modelData.count / root.total) : 0
                    radius: 5
                    color: Theme.statusColor(modelData.status)
                    Behavior on width { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }
                }
            }
        }
    }

    Flow {
        visible: root.legend && root.segments.length > 0
        Layout.fillWidth: true
        spacing: 14
        Repeater {
            model: root.segments
            delegate: Row {
                required property var modelData
                spacing: 6
                Rectangle { width: 8; height: 8; radius: 4; color: Theme.statusColor(modelData.status); anchors.verticalCenter: parent.verticalCenter }
                AText { text: modelData.title + " · " + modelData.count; size: Theme.fsSmall; dim: true }
            }
        }
    }
}

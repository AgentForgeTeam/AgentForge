import QtQuick
import QtQuick.Layouts

// Горизонтальные полосы «кто сколько потратил»; полосы дорастают плавно.
ColumnLayout {
    id: root
    property var bars: []        // [{label, value, text, cost, supervisor}]
    property string emptyText: ""
    readonly property real maxValue: {
        var m = 0
        for (var i = 0; i < bars.length; ++i) m = Math.max(m, bars[i].value)
        return m || 1
    }
    spacing: 12

    Repeater {
        model: root.bars
        delegate: ColumnLayout {
            required property var modelData
            required property int index
            Layout.fillWidth: true
            spacing: 5
            RowLayout {
                Layout.fillWidth: true
                Icon {
                    name: modelData.supervisor ? "shield-check" : "bot"
                    size: 13
                    color: modelData.supervisor ? Theme.violetSoft : Theme.textMute
                }
                AText { text: modelData.label; size: Theme.fsSmall; Layout.fillWidth: true }
                AText { text: modelData.text; size: Theme.fsSmall; mono: true; dim: true }
                AText { text: modelData.cost; size: Theme.fsSmall; mono: true; mute: true }
            }
            Rectangle {
                Layout.fillWidth: true
                height: 8
                radius: 4
                color: Theme.surface3
                Rectangle {
                    id: fill
                    height: parent.height
                    radius: 4
                    width: 0
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0; color: modelData.supervisor ? Theme.magenta : Theme.violet }
                        GradientStop { position: 1; color: modelData.supervisor ? Theme.violetSoft : Theme.cyan }
                    }
                    Behavior on width { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }
                    Component.onCompleted: width = Qt.binding(function() { return parent.width * modelData.value / root.maxValue })
                }
            }
        }
    }

    AText {
        visible: root.bars.length === 0
        text: root.emptyText
        mute: true
        Layout.alignment: Qt.AlignHCenter
    }
}

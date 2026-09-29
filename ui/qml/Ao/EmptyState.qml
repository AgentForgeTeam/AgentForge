import QtQuick
import QtQuick.Layouts

// Пустое состояние: парящая иконка в градиентном круге, текст и действие.
ColumnLayout {
    id: root
    property string icon: "sparkles"
    property string title: ""
    property string text: ""
    property string actionText: ""
    property string actionIcon: "plus"
    signal action()
    spacing: 10

    Item {
        Layout.alignment: Qt.AlignHCenter
        implicitWidth: 76
        implicitHeight: 76
        Rectangle {
            id: orb
            anchors.centerIn: parent
            width: 64; height: 64; radius: 32
            gradient: Gradient {
                GradientStop { position: 0; color: Theme.alpha(Theme.violet, 0.35) }
                GradientStop { position: 1; color: Theme.alpha(Theme.teal, 0.18) }
            }
            border.color: Theme.alpha(Theme.violetSoft, 0.35)
            Icon { anchors.centerIn: parent; name: root.icon; size: 26; color: Theme.violetSoft }
            SequentialAnimation on anchors.verticalCenterOffset {
                running: Theme.rich && root.visible
                loops: Animation.Infinite
                NumberAnimation { from: 0; to: -6; duration: 1800; easing.type: Easing.InOutSine }
                NumberAnimation { from: -6; to: 0; duration: 1800; easing.type: Easing.InOutSine }
            }
        }
    }
    AText {
        visible: root.title !== ""
        Layout.alignment: Qt.AlignHCenter
        text: root.title
        size: Theme.fsH3
        weight: Font.DemiBold
    }
    AText {
        visible: root.text !== ""
        Layout.alignment: Qt.AlignHCenter
        Layout.maximumWidth: 420
        horizontalAlignment: Text.AlignHCenter
        text: root.text
        dim: true
        wrapMode: Text.Wrap
        elide: Text.ElideNone
    }
    Button {
        visible: root.actionText !== ""
        Layout.alignment: Qt.AlignHCenter
        Layout.topMargin: 6
        variant: "primary"
        text: root.actionText
        iconName: root.actionIcon
        onClicked: root.action()
    }
}

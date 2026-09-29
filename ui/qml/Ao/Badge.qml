import QtQuick

// Цветная метка-таблетка: Badge { text: "готово"; tone: "success" }
Rectangle {
    id: badge
    property string text: ""
    property string tone: "muted"
    property string icon: ""
    property color tint: Theme.tone(tone)
    property bool solid: false
    implicitHeight: 22
    implicitWidth: row.implicitWidth + 16
    radius: height / 2
    color: solid ? tint : Theme.alpha(tint, 0.14)
    border.width: solid ? 0 : 1
    border.color: Theme.alpha(tint, 0.35)
    Behavior on color { ColorAnimation { duration: Theme.normal } }

    Row {
        id: row
        anchors.centerIn: parent
        spacing: 5
        Icon {
            visible: badge.icon !== ""
            name: badge.icon
            size: 12
            color: badge.solid ? Theme.bg : badge.tint
            anchors.verticalCenter: parent.verticalCenter
        }
        AText {
            text: badge.text
            size: Theme.fsMicro
            weight: Font.DemiBold
            color: badge.solid ? Theme.bg : badge.tint
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}

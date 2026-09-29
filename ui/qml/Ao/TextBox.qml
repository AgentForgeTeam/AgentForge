import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Многострочное поле с прокруткой и тем же фокусом, что у Field.
ColumnLayout {
    id: root
    property alias text: area.text
    property alias placeholder: area.placeholderText
    property alias area: area
    property string label: ""
    property string hint: ""
    property bool mono: false
    property bool readOnly: false
    property int minHeight: 120
    spacing: 6

    AText {
        visible: root.label !== ""
        text: root.label
        size: Theme.fsSmall
        weight: Font.Medium
        dim: true
    }

    Rectangle {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.minimumHeight: root.minHeight
        radius: Theme.radius
        color: area.activeFocus ? Theme.surface2 : Theme.input
        border.width: 1
        border.color: area.activeFocus ? Theme.violet : Theme.border
        Behavior on border.color { ColorAnimation { duration: Theme.fast } }

        Rectangle {
            anchors.fill: parent
            anchors.margins: -3
            radius: parent.radius + 3
            color: "transparent"
            border.width: 3
            border.color: Theme.alpha(Theme.violet, 0.18)
            opacity: area.activeFocus ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: Theme.normal } }
        }

        T.ScrollView {
            id: scroll
            anchors.fill: parent
            anchors.margins: 2
            clip: true
            T.ScrollBar.vertical: ScrollBar {}

            T.TextArea {
                id: area
                padding: 10
                wrapMode: TextEdit.Wrap
                readOnly: root.readOnly
                font.family: root.mono ? Theme.monoFamily : Theme.fontFamily
                font.pixelSize: root.mono ? Theme.fsSmall : Theme.fsBody
                color: Theme.text
                placeholderTextColor: Theme.textFaint
                selectionColor: Theme.alpha(Theme.violet, 0.45)
                selectedTextColor: Theme.text
                background: null
                selectByMouse: true
            }
        }
    }

    AText {
        visible: root.hint !== ""
        text: root.hint
        mute: true
        size: Theme.fsSmall
        wrapMode: Text.Wrap
        elide: Text.ElideNone
        Layout.fillWidth: true
    }
}

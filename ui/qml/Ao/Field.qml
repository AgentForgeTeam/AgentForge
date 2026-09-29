import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Поле ввода с подписью, иконкой, ошибкой и светящимся фокусом.
// password: true — скрытый ввод с кнопкой «показать».
ColumnLayout {
    id: root
    property alias text: input.text
    property alias placeholder: input.placeholderText
    property alias input: input
    property string label: ""
    property string hint: ""
    property string error: ""
    property string icon: ""
    property bool password: false
    property bool mono: false
    property bool readOnly: false
    property int inputMethodHints: Qt.ImhNone
    property bool reveal: false
    signal accepted()
    signal editingFinished()
    signal upPressed()
    signal downPressed()
    spacing: 6

    function focusInput() { input.forceActiveFocus() }

    AText {
        visible: root.label !== ""
        text: root.label
        size: Theme.fsSmall
        weight: Font.Medium
        dim: true
    }

    T.TextField {
        id: input
        Layout.fillWidth: true
        implicitHeight: Theme.controlH + 2
        leftPadding: root.icon !== "" ? 38 : 12
        rightPadding: root.password ? 40 : 12
        font.family: root.mono ? Theme.monoFamily : Theme.fontFamily
        font.pixelSize: Theme.fsBody
        color: Theme.text
        placeholderTextColor: Theme.textFaint
        selectionColor: Theme.alpha(Theme.violet, 0.45)
        selectedTextColor: Theme.text
        echoMode: root.password && !root.reveal ? TextInput.Password : TextInput.Normal
        readOnly: root.readOnly
        inputMethodHints: root.inputMethodHints
        verticalAlignment: TextInput.AlignVCenter
        onAccepted: root.accepted()
        onEditingFinished: root.editingFinished()
        Keys.onUpPressed: root.upPressed()
        Keys.onDownPressed: root.downPressed()

        background: Rectangle {
            radius: Theme.radius
            color: input.activeFocus ? Theme.surface2 : Theme.input
            border.width: 1
            border.color: root.error !== "" ? Theme.danger
                        : input.activeFocus ? Theme.violet
                        : (hover.hovered ? Theme.borderStrong : Theme.border)
            Behavior on border.color { ColorAnimation { duration: Theme.fast } }
            Behavior on color { ColorAnimation { duration: Theme.fast } }

            // Внешнее свечение фокуса.
            Rectangle {
                anchors.fill: parent
                anchors.margins: -3
                radius: parent.radius + 3
                color: "transparent"
                border.width: 3
                border.color: Theme.alpha(root.error !== "" ? Theme.danger : Theme.violet, 0.18)
                opacity: input.activeFocus ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: Theme.normal } }
            }
            HoverHandler { id: hover }
        }

        Icon {
            visible: root.icon !== ""
            name: root.icon
            size: 16
            color: input.activeFocus ? Theme.violetSoft : Theme.textMute
            anchors.left: parent.left
            anchors.leftMargin: 12
            anchors.verticalCenter: parent.verticalCenter
        }

        IconButton {
            visible: root.password
            iconName: root.reveal ? "eye-off" : "eye"
            size: 28
            anchors.right: parent.right
            anchors.rightMargin: 6
            anchors.verticalCenter: parent.verticalCenter
            onClicked: root.reveal = !root.reveal
            focusPolicy: Qt.NoFocus
        }
    }

    AText {
        visible: root.error !== "" || root.hint !== ""
        text: root.error !== "" ? root.error : root.hint
        color: root.error !== "" ? Theme.danger : Theme.textMute
        size: Theme.fsSmall
        wrapMode: Text.Wrap
        elide: Text.ElideNone
        Layout.fillWidth: true
    }
}

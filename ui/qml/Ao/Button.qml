import QtQuick
import QtQuick.Controls.Basic as T

// Кнопка с вариантами: primary | secondary | ghost | danger | success.
// Микровзаимодействия: подсветка при наведении, «вдавливание» при нажатии,
// бегущий блик на основной кнопке и индикатор загрузки вместо иконки.
T.AbstractButton {
    id: control
    property string variant: "secondary"
    property string iconName: ""
    property bool loading: false
    property bool compact: false
    property color accent: variant === "danger" ? Theme.danger
                         : variant === "success" ? Theme.success : Theme.violet

    readonly property bool primary: variant === "primary"
    readonly property bool hot: hovered && enabled && !loading

    implicitHeight: compact ? 32 : Theme.controlH
    implicitWidth: Math.max(implicitHeight, row.implicitWidth + (compact ? 22 : 30))
    hoverEnabled: true
    focusPolicy: Qt.StrongFocus
    opacity: enabled ? 1 : 0.45
    scale: pressed ? 0.965 : 1
    Behavior on scale { NumberAnimation { duration: Theme.fast; easing.type: Easing.OutBack } }
    Behavior on opacity { NumberAnimation { duration: Theme.fast } }

    background: Rectangle {
        id: bg
        radius: Theme.radius
        clip: true
        color: control.primary ? "transparent"
             : control.variant === "ghost" ? (control.hot ? Theme.alpha(Theme.text, 0.06) : "transparent")
             : control.variant === "danger" ? (control.hot ? Theme.alpha(Theme.danger, 0.22) : Theme.alpha(Theme.danger, 0.12))
             : control.variant === "success" ? (control.hot ? Theme.alpha(Theme.success, 0.22) : Theme.alpha(Theme.success, 0.12))
             : (control.hot ? Theme.surface3 : Theme.surface2)
        border.width: control.primary || control.variant === "ghost" ? 0 : 1
        border.color: control.variant === "danger" ? Theme.alpha(Theme.danger, 0.35)
                    : control.variant === "success" ? Theme.alpha(Theme.success, 0.35)
                    : (control.hot ? Theme.borderStrong : Theme.border)
        Behavior on color { ColorAnimation { duration: Theme.fast } }

        // Градиент основной кнопки: фиолетовый → индиго, при наведении ярче.
        Rectangle {
            anchors.fill: parent
            radius: parent.radius
            visible: control.primary
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0; color: control.hot ? "#9D72FF" : Theme.violet }
                GradientStop { position: 1; color: control.hot ? "#7C7FFB" : Theme.indigo }
            }
        }
        // Бегущий блик - только на основной кнопке и только при полном движении.
        Rectangle {
            id: shine
            visible: control.primary && Theme.rich
            width: parent.height * 1.6
            height: parent.height * 3
            y: -parent.height
            x: -width * 1.5
            rotation: 20
            opacity: 0.0
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0; color: "transparent" }
                GradientStop { position: 0.5; color: Qt.rgba(1, 1, 1, 0.28) }
                GradientStop { position: 1; color: "transparent" }
            }
        }
        // Светящийся контур фокуса клавиатуры.
        Rectangle {
            anchors.fill: parent
            anchors.margins: -3
            radius: parent.radius + 3
            color: "transparent"
            border.width: 2
            border.color: Theme.alpha(Theme.violetSoft, 0.7)
            visible: control.visualFocus
        }
    }

    SequentialAnimation {
        running: control.hot && control.primary && Theme.rich
        loops: 1
        PropertyAction { target: shine; property: "opacity"; value: 1 }
        NumberAnimation { target: shine; property: "x"; from: -shine.width * 1.5
                          to: control.width + shine.width; duration: 650; easing.type: Easing.OutCubic }
        PropertyAction { target: shine; property: "opacity"; value: 0 }
    }

    contentItem: Item {
        implicitWidth: row.implicitWidth
        implicitHeight: row.implicitHeight
        Row {
            id: row
            anchors.centerIn: parent
            spacing: 8
            Spinner {
                visible: control.loading
                size: 14
                color: control.primary ? "white" : Theme.violetSoft
                anchors.verticalCenter: parent.verticalCenter
            }
            Icon {
                visible: control.iconName !== "" && !control.loading
                name: control.iconName
                size: control.compact ? 14 : 16
                color: control.primary ? "white"
                     : control.variant === "danger" ? Theme.danger
                     : control.variant === "success" ? Theme.success
                     : (control.hot ? Theme.text : Theme.textDim)
                anchors.verticalCenter: parent.verticalCenter
            }
            AText {
                visible: control.text !== ""
                text: control.text
                size: control.compact ? Theme.fsSmall : Theme.fsBody
                weight: Font.DemiBold
                color: control.primary ? "white"
                     : control.variant === "danger" ? Theme.danger
                     : control.variant === "success" ? Theme.success : Theme.text
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
}

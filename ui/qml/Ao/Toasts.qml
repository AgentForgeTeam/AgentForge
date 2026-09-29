import QtQuick
import QtQuick.Layouts
import QtQuick.Effects

// Стопка уведомлений в правом верхнем углу. Каждое въезжает справа,
// показывает полосу оставшегося времени и уходит само (наведение - пауза).
Item {
    id: host
    width: 380
    property int maxVisible: 4

    function show(kind, title, message) {
        if (toastModel.count >= maxVisible) toastModel.remove(0)
        toastModel.append({ kind: kind || "info", title: title || "", message: message || "",
                            life: kind === "error" || kind === "warning" ? 7000 : 4500 })
    }

    ListModel { id: toastModel }

    ListView {
        id: list
        anchors.fill: parent
        spacing: 10
        interactive: false
        model: toastModel
        verticalLayoutDirection: ListView.TopToBottom

        add: Transition {
            ParallelAnimation {
                NumberAnimation { property: "x"; from: 420; to: 0; duration: Theme.slow; easing.type: Easing.OutBack; easing.overshoot: 0.9 }
                NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.normal }
            }
        }
        remove: Transition {
            ParallelAnimation {
                NumberAnimation { property: "x"; to: 420; duration: Theme.normal; easing.type: Easing.InCubic }
                NumberAnimation { property: "opacity"; to: 0; duration: Theme.normal }
            }
        }
        displaced: Transition {
            NumberAnimation { properties: "y"; duration: Theme.normal; easing.type: Easing.OutCubic }
        }

        delegate: Item {
            id: toast
            required property int index
            required property string kind
            required property string title
            required property string message
            required property int life
            width: list.width
            height: card.height
            readonly property color tint: Theme.tone(kind === "info" ? "accent" : kind)
            readonly property string glyph: kind === "success" ? "circle-check"
                                          : kind === "error" ? "octagon-x"
                                          : kind === "warning" ? "triangle-alert" : "info"

            Rectangle {
                id: card
                width: parent.width
                height: col.implicitHeight + 28
                radius: Theme.radiusL
                color: Theme.surfaceSolid
                border.color: Theme.alpha(toast.tint, 0.45)
                layer.enabled: Theme.rich
                layer.effect: MultiEffect {
                    shadowEnabled: true
                    shadowColor: Qt.rgba(0, 0, 0, 0.55)
                    shadowBlur: 0.8
                    shadowVerticalOffset: 8
                }

                RowLayout {
                    id: col
                    anchors { left: parent.left; right: parent.right; top: parent.top; margins: 14 }
                    spacing: 12
                    Rectangle {
                        Layout.alignment: Qt.AlignTop
                        width: 30; height: 30; radius: 10
                        color: Theme.alpha(toast.tint, 0.16)
                        Icon { anchors.centerIn: parent; name: toast.glyph; size: 16; color: toast.tint }
                    }
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 3
                        AText { text: toast.title; weight: Font.DemiBold; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone }
                        AText {
                            visible: toast.message !== ""
                            text: toast.message
                            dim: true
                            size: Theme.fsSmall
                            Layout.fillWidth: true
                            wrapMode: Text.Wrap
                            elide: Text.ElideRight
                            maximumLineCount: 4
                        }
                    }
                    IconButton {
                        Layout.alignment: Qt.AlignTop
                        iconName: "x"
                        size: 26
                        onClicked: toastModel.remove(toast.index)
                    }
                }

                // Полоса оставшегося времени.
                Rectangle {
                    id: bar
                    anchors { left: parent.left; bottom: parent.bottom; leftMargin: 14; bottomMargin: 7 }
                    height: 2
                    radius: 1
                    color: toast.tint
                    opacity: 0.7
                    width: card.width - 28
                }
                NumberAnimation {
                    id: countdown
                    target: bar
                    property: "width"
                    from: card.width - 28
                    to: 0
                    duration: toast.life
                    running: true
                    paused: hover.hovered
                    onFinished: toastModel.remove(toast.index)
                }
                HoverHandler { id: hover }
            }
        }
    }
}

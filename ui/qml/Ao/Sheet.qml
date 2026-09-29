import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Модальное окно внутри приложения: затемнение, «всплытие» с пружиной,
// закрытие по Esc и клику мимо. Содержимое — в default-свойство.
T.Popup {
    id: sheet
    property string title: ""
    property string subtitle: ""
    property string icon: ""
    property int sheetWidth: 560
    default property alias content: body.data
    property alias footer: footerRow.data
    property bool busy: false

    parent: T.Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(sheetWidth, (parent ? parent.width : sheetWidth) - 48)
    height: Math.min(implicitHeight, (parent ? parent.height : 800) - 48)
    modal: true
    focus: true
    padding: 0
    closePolicy: busy ? T.Popup.NoAutoClose : (T.Popup.CloseOnEscape | T.Popup.CloseOnPressOutside)

    T.Overlay.modal: Rectangle {
        color: Theme.overlay
        Behavior on opacity { NumberAnimation { duration: Theme.normal } }
    }

    enter: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.normal }
            NumberAnimation { property: "scale"; from: 0.94; to: 1; duration: Theme.slow
                              easing.type: Easing.OutBack; easing.overshoot: 1.2 }
        }
    }
    exit: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; to: 0; duration: Theme.fast }
            NumberAnimation { property: "scale"; to: 0.97; duration: Theme.fast }
        }
    }

    background: Rectangle {
        radius: Theme.radiusXL
        color: Theme.surfaceSolid
        border.color: Theme.borderStrong
        Rectangle {
            anchors { left: parent.left; right: parent.right; top: parent.top; margins: 1 }
            height: 90
            radius: parent.radius
            gradient: Gradient {
                GradientStop { position: 0; color: Theme.alpha(Theme.violet, 0.10) }
                GradientStop { position: 1; color: "transparent" }
            }
        }
    }

    contentItem: ColumnLayout {
        spacing: 0

        RowLayout {
            Layout.fillWidth: true
            Layout.margins: 24
            Layout.bottomMargin: 8
            spacing: 14
            Rectangle {
                visible: sheet.icon !== ""
                width: 40; height: 40; radius: 12
                color: Theme.alpha(Theme.violet, 0.18)
                border.color: Theme.alpha(Theme.violetSoft, 0.3)
                Icon { anchors.centerIn: parent; name: sheet.icon; size: 18; color: Theme.violetSoft }
            }
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 2
                AText { text: sheet.title; size: Theme.fsH2; weight: Font.Bold; Layout.fillWidth: true }
                AText {
                    visible: sheet.subtitle !== ""
                    text: sheet.subtitle
                    dim: true
                    size: Theme.fsSmall
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                    Layout.fillWidth: true
                }
            }
            IconButton {
                Layout.alignment: Qt.AlignTop
                iconName: "x"
                enabled: !sheet.busy
                onClicked: sheet.close()
            }
        }

        T.ScrollView {
            id: scroll
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: body.implicitHeight + 16
            clip: true
            contentWidth: availableWidth
            T.ScrollBar.vertical: ScrollBar {}
            ColumnLayout {
                id: body
                width: scroll.availableWidth - 48
                x: 24
                y: 8
                spacing: 14
            }
        }

        Rectangle { Layout.fillWidth: true; height: 1; color: Theme.border; visible: footerRow.children.length > 0 }

        RowLayout {
            id: footerRow
            Layout.fillWidth: true
            Layout.margins: 18
            Layout.leftMargin: 24
            Layout.rightMargin: 24
            spacing: 10
            visible: children.length > 0
        }
    }
}

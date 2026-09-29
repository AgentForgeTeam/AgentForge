import QtQuick
import QtQuick.Layouts

// Заголовок страницы: иконка, название, подзаголовок и действия справа.
RowLayout {
    id: root
    property string title: ""
    property string subtitle: ""
    property string icon: ""
    default property alias actions: actionRow.data
    spacing: 16

    Rectangle {
        visible: root.icon !== ""
        Layout.alignment: Qt.AlignTop
        width: 44; height: 44; radius: 14
        gradient: Gradient {
            GradientStop { position: 0; color: Theme.alpha(Theme.violet, 0.30) }
            GradientStop { position: 1; color: Theme.alpha(Theme.cyan, 0.14) }
        }
        border.color: Theme.alpha(Theme.violetSoft, 0.3)
        Icon { anchors.centerIn: parent; name: root.icon; size: 20; color: Theme.violetSoft }
    }

    ColumnLayout {
        Layout.fillWidth: true
        spacing: 3
        AText {
            text: root.title
            size: Theme.fsH1
            weight: Font.Bold
            Layout.fillWidth: true
        }
        AText {
            visible: root.subtitle !== ""
            text: root.subtitle
            dim: true
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            elide: Text.ElideNone
            maximumLineCount: 2
        }
    }

    RowLayout {
        id: actionRow
        Layout.alignment: Qt.AlignTop
        spacing: 10
    }
}

import QtQuick
import QtQuick.Layouts

// Подзаголовок секции внутри страницы или карточки.
RowLayout {
    id: root
    property string text: ""
    property string icon: ""
    property string hint: ""
    default property alias trailing: trail.data
    spacing: 10
    Icon { visible: root.icon !== ""; name: root.icon; size: 16; color: Theme.violetSoft }
    ColumnLayout {
        Layout.fillWidth: true
        spacing: 1
        AText { text: root.text; size: Theme.fsH3; weight: Font.DemiBold; Layout.fillWidth: true }
        AText {
            visible: root.hint !== ""
            text: root.hint
            mute: true
            size: Theme.fsSmall
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            elide: Text.ElideNone
        }
    }
    RowLayout { id: trail; spacing: 8 }
}

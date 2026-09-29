import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Шаблон страницы: заголовок с действиями и прокручиваемое содержимое.
// fill: true — содержимое растягивается на всю высоту без прокрутки
// (страницы с собственными прокручиваемыми панелями, как «Выполнение»).
Item {
    id: page
    property string title: ""
    property string subtitle: ""
    property string icon: ""
    property bool fill: false
    property alias headerActions: header.actions
    default property alias content: col.data
    readonly property int contentWidth: col.width

    PageHeader {
        id: header
        anchors { left: parent.left; right: parent.right; top: parent.top }
        anchors.margins: Theme.pagePad
        anchors.bottomMargin: 0
        title: page.title
        subtitle: page.subtitle
        icon: page.icon
    }

    Flickable {
        id: flick
        anchors { left: parent.left; right: parent.right; top: header.bottom; bottom: parent.bottom }
        anchors.topMargin: 22
        clip: true
        interactive: !page.fill
        contentWidth: width
        contentHeight: page.fill ? height : col.implicitHeight + Theme.pagePad
        boundsBehavior: Flickable.StopAtBounds
        T.ScrollBar.vertical: ScrollBar { visible: !page.fill }

        ColumnLayout {
            id: col
            x: Theme.pagePad
            width: flick.width - Theme.pagePad * 2
            height: page.fill ? flick.height - Theme.pagePad : implicitHeight
            spacing: 18
        }
    }
}

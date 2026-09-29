import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Выпадающий список. options: [{value, title}] или массив строк.
// editable: можно вписать своё значение (например, имя модели).
ColumnLayout {
    id: root
    property var options: []
    property var value: undefined
    property string label: ""
    property string placeholder: ""
    property bool editable: false
    property string icon: ""
    property alias combo: combo
    readonly property string editText: combo.editText
    signal picked(var value)
    signal edited(string text)
    spacing: 6

    readonly property bool plain: options.length > 0 && typeof options[0] !== "object"

    function titleOf(v) {
        for (var i = 0; i < options.length; ++i) {
            var o = options[i]
            if (plain ? o === v : o.value === v) return plain ? o : o.title
        }
        return v === undefined || v === null ? "" : String(v)
    }
    function indexOf(v) {
        for (var i = 0; i < options.length; ++i) {
            var o = options[i]
            if (plain ? o === v : o.value === v) return i
        }
        return -1
    }

    AText {
        visible: root.label !== ""
        text: root.label
        size: Theme.fsSmall
        weight: Font.Medium
        dim: true
    }

    T.ComboBox {
        id: combo
        Layout.fillWidth: true
        implicitHeight: Theme.controlH + 2
        model: root.options
        textRole: root.plain ? "" : "title"
        valueRole: root.plain ? "" : "value"
        editable: root.editable
        currentIndex: root.indexOf(root.value)
        font.family: Theme.fontFamily
        font.pixelSize: Theme.fsBody
        hoverEnabled: true
        onActivated: function(index) {
            var o = root.options[index]
            root.picked(root.plain ? o : o.value)
        }
        onAccepted: root.edited(editText)
        Component.onCompleted: if (root.editable && root.indexOf(root.value) < 0) editText = root.titleOf(root.value)

        leftPadding: root.icon !== "" ? 38 : 12
        rightPadding: 36

        contentItem: T.TextField {
            text: combo.editable ? combo.editText : combo.displayText
            readOnly: !combo.editable
            enabled: combo.editable
            color: text === "" ? Theme.textFaint : Theme.text
            placeholderText: root.placeholder
            placeholderTextColor: Theme.textFaint
            font: combo.font
            verticalAlignment: Text.AlignVCenter
            selectionColor: Theme.alpha(Theme.violet, 0.45)
            background: null
            leftPadding: 0
            onTextEdited: root.edited(text)
        }

        indicator: Icon {
            name: "chevron-down"
            size: 16
            color: combo.hovered ? Theme.text : Theme.textMute
            x: combo.width - width - 12
            y: (combo.height - height) / 2
            rotation: combo.popup.visible ? 180 : 0
            Behavior on rotation { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
        }

        background: Rectangle {
            radius: Theme.radius
            color: combo.activeFocus || combo.popup.visible ? Theme.surface2 : Theme.input
            border.width: 1
            border.color: combo.popup.visible || combo.activeFocus ? Theme.violet
                        : (combo.hovered ? Theme.borderStrong : Theme.border)
            Behavior on border.color { ColorAnimation { duration: Theme.fast } }
            Icon {
                visible: root.icon !== ""
                name: root.icon
                size: 16
                color: Theme.textMute
                anchors.left: parent.left
                anchors.leftMargin: 12
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        delegate: T.ItemDelegate {
            id: item
            required property var modelData
            required property int index
            width: ListView.view ? ListView.view.width : combo.width
            height: 36
            hoverEnabled: true
            highlighted: combo.highlightedIndex === index
            contentItem: RowLayout {
                spacing: 8
                AText {
                    Layout.fillWidth: true
                    text: root.plain ? item.modelData : item.modelData.title
                    color: item.index === combo.currentIndex ? Theme.violetSoft : Theme.text
                    weight: item.index === combo.currentIndex ? Font.DemiBold : Font.Normal
                }
                Icon {
                    visible: item.index === combo.currentIndex
                    name: "check"
                    size: 14
                    color: Theme.violetSoft
                }
            }
            background: Rectangle {
                radius: Theme.radiusS
                color: item.highlighted ? Theme.alpha(Theme.violet, 0.16) : "transparent"
                Behavior on color { ColorAnimation { duration: Theme.fast } }
            }
        }

        popup: T.Popup {
            y: combo.height + 6
            width: combo.width
            implicitHeight: Math.min(contentItem.implicitHeight + 12, 320)
            padding: 6
            contentItem: ListView {
                clip: true
                implicitHeight: contentHeight
                model: combo.popup.visible ? combo.delegateModel : null
                currentIndex: combo.highlightedIndex
                boundsBehavior: Flickable.StopAtBounds
                T.ScrollBar.vertical: ScrollBar {}
            }
            background: Rectangle {
                radius: Theme.radius
                color: Theme.surfaceSolid
                border.color: Theme.borderStrong
            }
            enter: Transition {
                ParallelAnimation {
                    NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.fast }
                    NumberAnimation { property: "y"; from: combo.height; to: combo.height + 6
                                      duration: Theme.normal; easing.type: Easing.OutCubic }
                }
            }
            exit: Transition { NumberAnimation { property: "opacity"; to: 0; duration: Theme.fast } }
        }
    }
}

import QtQuick
import QtQuick.Layouts

// Подтверждение действия. open(title, text, callback[, danger])
Sheet {
    id: dlg
    property var onYes: null
    property bool danger: true
    property string confirmText: ""
    property string cancelText: ""
    property string actionText: ""
    sheetWidth: 440
    icon: danger ? "triangle-alert" : "circle-alert"

    function ask(title, text, callback, isDanger, yesText) {
        dlg.title = title
        dlg.subtitle = text
        dlg.onYes = callback
        dlg.danger = isDanger === undefined ? true : isDanger
        dlg.actionText = yesText ? yesText : dlg.confirmText
        open()
    }

    footer: [
        Item { Layout.fillWidth: true },
        Button {
            text: dlg.cancelText
            variant: "ghost"
            onClicked: dlg.close()
        },
        Button {
            text: dlg.actionText !== "" ? dlg.actionText : dlg.confirmText
            variant: dlg.danger ? "danger" : "primary"
            iconName: dlg.danger ? "trash-2" : "check"
            onClicked: {
                var cb = dlg.onYes
                dlg.close()
                if (cb) cb()
            }
        }
    ]
}

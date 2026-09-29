import QtQuick
import QtQuick.Layouts
import Ao

// API-ключи: карточки подключений с живой проверкой и мастер добавления,
// где провайдер выбирается плиткой, а адрес подставляется сам.
Page {
    id: page
    title: i18n.t["keys.title"]
    subtitle: i18n.t["keys.subtitle"]
    icon: "key-round"
    readonly property var ctl: backend.keys

    headerActions: [
        Button {
            variant: "primary"
            iconName: "plus"
            text: i18n.t["keys.new"]
            onClicked: editor.openNew()
        }
    ]

    EmptyState {
        visible: page.ctl.model.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "key-round"
        title: i18n.t["keys.empty_title"]
        text: i18n.t["keys.empty"]
        actionText: i18n.t["keys.new"]
        onAction: editor.openNew()
    }

    Repeater {
        model: page.ctl.model
        delegate: Card {
            Layout.fillWidth: true
            hoverable: true
            stagger: index
            padding: 18

            RowLayout {
                width: parent.width
                spacing: 16

                Rectangle {
                    width: 46; height: 46; radius: 14
                    color: model.local ? Theme.alpha(Theme.teal, 0.14) : Theme.alpha(Theme.violet, 0.14)
                    border.color: model.local ? Theme.alpha(Theme.teal, 0.35) : Theme.alpha(Theme.violetSoft, 0.3)
                    Icon {
                        anchors.centerIn: parent
                        name: model.local ? "hard-drive" : "key-round"
                        size: 20
                        color: model.local ? Theme.teal : Theme.violetSoft
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 4
                    RowLayout {
                        spacing: 8
                        AText { text: model.label; weight: Font.DemiBold; size: Theme.fsH3 }
                        Badge { text: model.providerTitle; tone: "violet" }
                        Badge { visible: model.free; text: i18n.t["keys.free"]; tone: "success" }
                        Badge { visible: model.local; text: i18n.t["keys.local"]; tone: "accent"; icon: "hard-drive" }
                    }
                    AText { text: model.baseUrl; mute: true; mono: true; size: Theme.fsSmall; Layout.fillWidth: true }
                    RowLayout {
                        spacing: 8
                        Icon {
                            name: model.hasSecret ? "lock" : "circle-dot"
                            size: 12
                            color: model.hasSecret ? Theme.success : Theme.textMute
                        }
                        AText {
                            text: model.hasSecret ? i18n.t["keys.stored"] : i18n.t["keys.no_secret"]
                            size: Theme.fsSmall
                            dim: true
                        }
                        AText {
                            visible: model.models > 0
                            text: "· " + i18n.fmt(i18n.t["keys.models_cached"], { n: model.models })
                            size: Theme.fsSmall
                            mute: true
                        }
                    }
                    // Результат проверки соединения.
                    RowLayout {
                        visible: model.testState !== ""
                        spacing: 8
                        Spinner { visible: model.testState === "testing"; size: 14 }
                        Icon {
                            visible: model.testState !== "testing"
                            name: model.testState === "ok" ? "circle-check" : "circle-x"
                            size: 14
                            color: model.testState === "ok" ? Theme.success : Theme.danger
                        }
                        AText {
                            text: model.testState === "testing" ? i18n.t["keys.testing"] : model.testMessage
                            size: Theme.fsSmall
                            color: model.testState === "fail" ? Theme.danger
                                 : model.testState === "ok" ? Theme.success : Theme.textDim
                            Layout.maximumWidth: 560
                            wrapMode: Text.Wrap
                            elide: Text.ElideNone
                        }
                    }
                }

                Button {
                    Layout.alignment: Qt.AlignTop
                    compact: true
                    iconName: "activity"
                    text: i18n.t["common.test"]
                    loading: model.testState === "testing"
                    enabled: model.testState !== "testing"
                    onClicked: page.ctl.test(model.id)
                }
                IconButton {
                    Layout.alignment: Qt.AlignTop
                    iconName: "pencil"
                    tip: i18n.t["common.edit"]
                    onClicked: editor.openEdit(model.id, model.provider, model.label, model.baseUrl)
                }
                IconButton {
                    Layout.alignment: Qt.AlignTop
                    iconName: "trash-2"
                    danger: true
                    tip: i18n.t["common.delete"]
                    onClicked: confirm.ask(i18n.t["keys.delete_title"], i18n.t["keys.delete_confirm"],
                                           function() { page.ctl.remove(model.id) })
                }
            }
        }
    }

    Confirm {
        id: confirm
        confirmText: i18n.t["common.delete"]
        cancelText: i18n.t["common.cancel"]
    }

    Sheet {
        id: editor
        property int keyId: -1
        property string provider: "openai"
        property string error: ""
        readonly property var preset: {
            var list = page.ctl.presets
            for (var i = 0; i < list.length; ++i) if (list[i].key === provider) return list[i]
            return list.length ? list[0] : ({})
        }
        title: keyId >= 0 ? i18n.t["keys.edit"] : i18n.t["keys.new"]
        subtitle: i18n.t["keys.subtitle"]
        icon: "key-round"
        sheetWidth: 680

        function openNew() {
            keyId = -1; error = ""; provider = "openai"
            labelField.text = ""; urlField.text = preset.baseUrl; secretField.text = ""
            open()
        }
        function openEdit(id, prov, label, url) {
            keyId = id; error = ""; provider = prov
            labelField.text = label; urlField.text = url; secretField.text = ""
            open()
        }
        function pick(key) {
            provider = key
            urlField.text = preset.baseUrl
            if (labelField.text === "") labelField.text = ""
        }
        function save() {
            var err = keyId >= 0 ? page.ctl.update(keyId, labelField.text, urlField.text, secretField.text)
                                 : page.ctl.create(provider, labelField.text, urlField.text, secretField.text)
            if (err === "") close(); else error = err
        }

        // Провайдеры плитками (только при создании: провайдер ключа не меняется).
        AText { visible: editor.keyId < 0; text: i18n.t["keys.provider"]; size: Theme.fsSmall; weight: Font.Medium; dim: true }
        GridLayout {
            visible: editor.keyId < 0
            Layout.fillWidth: true
            columns: 4
            columnSpacing: 10
            rowSpacing: 10
            Repeater {
                model: page.ctl.presets
                delegate: Rectangle {
                    id: tile
                    required property var modelData
                    readonly property bool chosen: editor.provider === modelData.key
                    Layout.fillWidth: true
                    implicitHeight: 64
                    radius: Theme.radius
                    color: chosen ? Theme.alpha(Theme.violet, 0.16) : (tileMouse.containsMouse ? Theme.surface3 : Theme.surface2)
                    border.color: chosen ? Theme.violet : Theme.border
                    Behavior on color { ColorAnimation { duration: Theme.fast } }
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 4
                        AText { text: tile.modelData.title; weight: Font.DemiBold; size: Theme.fsSmall; Layout.fillWidth: true }
                        RowLayout {
                            spacing: 4
                            Badge { visible: tile.modelData.free; text: i18n.t["keys.free"]; tone: "success" }
                            Badge { visible: tile.modelData.local; text: i18n.t["keys.local"]; tone: "accent" }
                        }
                    }
                    MouseArea {
                        id: tileMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: editor.pick(tile.modelData.key)
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            visible: (editor.preset.notes || "") !== "" || (editor.preset.docsUrl || "") !== ""
            radius: Theme.radius
            color: Theme.alpha(Theme.cyan, 0.06)
            border.color: Theme.alpha(Theme.cyan, 0.2)
            implicitHeight: notesCol.implicitHeight + 20
            ColumnLayout {
                id: notesCol
                anchors.fill: parent
                anchors.margins: 10
                spacing: 4
                AText {
                    visible: (editor.preset.notes || "") !== ""
                    text: editor.preset.notes || ""
                    size: Theme.fsSmall
                    dim: true
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                    Layout.fillWidth: true
                }
                AText {
                    visible: (editor.preset.docsUrl || "") !== ""
                    text: "<a href=\"" + editor.preset.docsUrl + "\">" + i18n.t["keys.get_key"] + " ↗</a>"
                    textFormat: Text.RichText
                    size: Theme.fsSmall
                    onLinkActivated: function(link) { Qt.openUrlExternally(link) }
                    HoverHandler { cursorShape: Qt.PointingHandCursor }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            Field {
                id: labelField
                Layout.fillWidth: true
                label: i18n.t["keys.label"]
                placeholder: editor.preset.title || ""
                icon: "star"
            }
            Field {
                id: urlField
                Layout.fillWidth: true
                Layout.preferredWidth: 2
                label: i18n.t["keys.base_url"]
                mono: true
                icon: "globe"
            }
        }
        Field {
            id: secretField
            Layout.fillWidth: true
            label: i18n.t["keys.key"]
            password: true
            mono: true
            icon: "lock"
            placeholder: editor.keyId >= 0 ? i18n.t["keys.keep_secret"] : "sk-…"
            hint: editor.preset.requiresKey === false ? i18n.t["keys.no_key_needed"] : ""
            error: editor.error
            onAccepted: editor.save()
        }

        footer: [
            Icon { name: "shield-check"; size: 14; color: Theme.success },
            AText { text: i18n.t["keys.encrypted_note"]; mute: true; size: Theme.fsSmall; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: editor.close() },
            Button { text: i18n.t["common.save"]; variant: "primary"; iconName: "check"; onClicked: editor.save() }
        ]
    }
}

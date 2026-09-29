import QtQuick
import QtQuick.Layouts
import Ao

// Воркспейсы: параллельные проекты. Активный подсвечен, клик — сделать активным.
Page {
    id: page
    title: i18n.t["ws.title"]
    subtitle: i18n.t["ws.subtitle"]
    icon: "layers"
    readonly property var ctl: backend.workspaces

    headerActions: [
        Button {
            variant: "primary"
            iconName: "plus"
            text: i18n.t["ws.new"]
            onClicked: editor.edit(-1, "", "")
        }
    ]

    EmptyState {
        visible: page.ctl.model.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "layers"
        title: i18n.t["ws.empty_title"]
        text: i18n.t["ws.empty"]
        actionText: i18n.t["ws.new"]
        onAction: editor.edit(-1, "", "")
    }

    GridLayout {
        id: grid
        Layout.fillWidth: true
        visible: page.ctl.model.count > 0
        columns: Math.max(1, Math.floor((page.contentWidth + 16) / 340))
        columnSpacing: 16
        rowSpacing: 16

        Repeater {
            model: page.ctl.model
            delegate: Card {
                id: wsCard
                Layout.fillWidth: true
                Layout.preferredHeight: 214
                hoverable: true
                glow: model.active
                stagger: index

                MouseArea {
                    anchors.fill: parent
                    cursorShape: model.active ? Qt.ArrowCursor : Qt.PointingHandCursor
                    onClicked: if (!model.active) page.ctl.select(model.id)
                }

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 10

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        Rectangle {
                            width: 40; height: 40; radius: 12
                            gradient: Gradient {
                                GradientStop { position: 0; color: model.active ? Theme.violet : Theme.surface3 }
                                GradientStop { position: 1; color: model.active ? Theme.teal : Theme.surface2 }
                            }
                            AText {
                                anchors.centerIn: parent
                                text: model.name.length ? model.name[0].toUpperCase() : "?"
                                weight: Font.Bold
                                size: Theme.fsH2
                                color: model.active ? "white" : Theme.textDim
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 2
                            AText { text: model.name; weight: Font.DemiBold; size: Theme.fsH3; Layout.fillWidth: true }
                            AText { text: i18n.fmt(i18n.t["ws.updated"], { when: model.updated }); mute: true; size: Theme.fsSmall }
                        }
                        Badge {
                            visible: model.active
                            text: i18n.t["ws.active"]
                            tone: "violet"
                            icon: "check"
                        }
                    }

                    AText {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: model.description !== "" ? model.description : i18n.t["ws.no_description"]
                        dim: model.description !== ""
                        mute: model.description === ""
                        wrapMode: Text.Wrap
                        elide: Text.ElideRight
                        maximumLineCount: 2
                        verticalAlignment: Text.AlignTop
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 14
                        Stat { glyph: "bot"; value: model.agents }
                        Stat { glyph: "coins"; value: model.tokens }
                        Stat { glyph: "dollar-sign"; value: model.cost; tint: Theme.teal }
                        Item { Layout.fillWidth: true }
                        IconButton {
                            iconName: "pencil"
                            tip: i18n.t["common.edit"]
                            onClicked: editor.edit(model.id, model.name, model.description)
                        }
                        IconButton {
                            iconName: "trash-2"
                            danger: true
                            tip: i18n.t["common.delete"]
                            onClicked: confirm.ask(i18n.t["ws.delete_title"], i18n.t["ws.delete_confirm"],
                                                   function() { page.ctl.remove(model.id) })
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        visible: model.taskTitle !== ""
                        height: 30
                        radius: Theme.radiusS
                        color: Theme.alpha(Theme.surface3, 0.6)
                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 10
                            anchors.rightMargin: 10
                            spacing: 8
                            Icon { name: "list-checks"; size: 13; color: Theme.textMute }
                            AText { text: model.taskTitle; size: Theme.fsSmall; dim: true; Layout.fillWidth: true }
                        }
                    }
                }
            }
        }
    }

    component Stat: Row {
        property string glyph: ""
        property var value
        property color tint: Theme.textDim
        spacing: 5
        Icon { name: glyph; size: 13; color: Theme.textMute; anchors.verticalCenter: parent.verticalCenter }
        AText { text: value; size: Theme.fsSmall; mono: true; color: tint; anchors.verticalCenter: parent.verticalCenter }
    }

    Confirm {
        id: confirm
        confirmText: i18n.t["common.delete"]
        cancelText: i18n.t["common.cancel"]
    }

    Sheet {
        id: editor
        property int wsId: -1
        property string error: ""
        title: wsId >= 0 ? i18n.t["ws.edit"] : i18n.t["ws.new"]
        icon: "layers"
        sheetWidth: 480

        function edit(id, name, description) {
            wsId = id
            error = ""
            nameField.text = name
            descField.text = description
            open()
            nameField.focusInput()
        }
        function save() {
            var err = wsId >= 0 ? page.ctl.update(wsId, nameField.text, descField.text)
                                : page.ctl.create(nameField.text, descField.text)
            if (err === "") close(); else error = err
        }

        Field {
            id: nameField
            Layout.fillWidth: true
            label: i18n.t["ws.name"]
            icon: "layers"
            error: editor.error
            onAccepted: editor.save()
        }
        TextBox {
            id: descField
            Layout.fillWidth: true
            label: i18n.t["common.description"]
            placeholder: i18n.t["ws.desc_placeholder"]
            minHeight: 100
        }

        footer: [
            Item { Layout.fillWidth: true },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: editor.close() },
            Button { text: i18n.t["common.save"]; variant: "primary"; iconName: "check"; onClicked: editor.save() }
        ]
    }
}

import QtQuick
import QtQuick.Layouts
import Ao

// Агенты воркспейса: сетка карточек и редактор с шаблонами ролей,
// загрузкой моделей, инструментами и системным промптом.
Page {
    id: page
    title: i18n.t["agents.title"]
    subtitle: i18n.t["agents.isolated_note"]
    icon: "bot"
    readonly property var ctl: backend.agents

    headerActions: [
        Button {
            variant: "primary"
            iconName: "plus"
            text: i18n.t["agents.new"]
            enabled: backend.workspaceId >= 0 && page.ctl.hasKeys
            onClicked: editor.openNew()
        }
    ]

    EmptyState {
        visible: backend.workspaceId < 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "layers"
        title: i18n.t["ws.empty_title"]
        text: i18n.t["ws.empty"]
        actionText: i18n.t["nav.workspaces"]
        actionIcon: "arrow-right"
        onAction: backend.navigate("workspaces")
    }
    EmptyState {
        visible: backend.workspaceId >= 0 && !page.ctl.hasKeys
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "key-round"
        title: i18n.t["agents.no_keys_title"]
        text: i18n.t["agents.no_keys"]
        actionText: i18n.t["keys.new"]
        onAction: backend.navigate("keys")
    }
    EmptyState {
        visible: backend.workspaceId >= 0 && page.ctl.hasKeys && page.ctl.model.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "bot"
        title: i18n.t["agents.empty_title"]
        text: i18n.t["agents.empty"]
        actionText: i18n.t["agents.new"]
        onAction: editor.openNew()
    }

    GridLayout {
        Layout.fillWidth: true
        visible: page.ctl.model.count > 0
        columns: Math.max(1, Math.floor((page.contentWidth + 16) / 360))
        columnSpacing: 16
        rowSpacing: 16

        Repeater {
            model: page.ctl.model
            delegate: Card {
                id: agentCard
                Layout.fillWidth: true
                Layout.preferredHeight: 232
                hoverable: true
                stagger: index
                glow: model.status === "running"
                glowColor: Theme.cyan
                opacity: model.enabled ? enter : enter * 0.55
                readonly property var toolList: model.toolTitles

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 10

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        Item {
                            width: 46; height: 46
                            Rectangle {
                                anchors.fill: parent
                                radius: 23
                                gradient: Gradient {
                                    GradientStop { position: 0; color: model.isSupervisor ? Theme.magenta : Theme.violet }
                                    GradientStop { position: 1; color: model.isSupervisor ? Theme.violetSoft : Theme.cyan }
                                }
                                opacity: 0.9
                                Icon { anchors.centerIn: parent; name: model.icon; size: 20; color: "white" }
                            }
                            StatusDot {
                                anchors.right: parent.right
                                anchors.bottom: parent.bottom
                                size: 11
                                status: model.status
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 2
                            RowLayout {
                                spacing: 6
                                AText { text: model.name; weight: Font.DemiBold; size: Theme.fsH3; Layout.maximumWidth: 180 }
                                Icon { visible: model.isSupervisor; name: "star"; size: 14; color: Theme.warning }
                            }
                            AText { text: model.roleTitle + " · " + model.statusTitle; mute: true; size: Theme.fsSmall }
                        }
                        Toggle {
                            isOn: model.enabled
                            onToggled: page.ctl.setEnabled(model.id, checked)
                        }
                    }

                    RowLayout {
                        spacing: 6
                        Badge { text: model.modelName !== "" ? model.modelName : "—"; tone: "accent"; icon: "cpu" }
                        Badge { visible: model.price !== ""; text: model.price; tone: "muted"; icon: "coins" }
                    }

                    AText {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: model.promptPreview !== "" ? model.promptPreview : i18n.t["agents.no_prompt"]
                        dim: true
                        size: Theme.fsSmall
                        wrapMode: Text.Wrap
                        elide: Text.ElideRight
                        maximumLineCount: 3
                        verticalAlignment: Text.AlignTop
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 6
                        // Инструменты: сколько помещается; край плавно гаснет.
                        Item {
                            Layout.fillWidth: true
                            height: 22
                            clip: true
                            Row {
                                id: toolRow
                                spacing: 6
                                Repeater {
                                    model: agentCard.toolList
                                    delegate: Rectangle {
                                        required property string modelData
                                        required property int index
                                        radius: 8
                                        height: 22
                                        width: toolText.implicitWidth + 14
                                        color: Theme.surface3
                                        AText { id: toolText; anchors.centerIn: parent; text: modelData; size: Theme.fsMicro; dim: true }
                                    }
                                }
                            }
                            Rectangle {
                                visible: toolRow.width > parent.width
                                anchors.right: parent.right
                                width: 28
                                height: parent.height
                                gradient: Gradient {
                                    orientation: Gradient.Horizontal
                                    GradientStop { position: 0; color: "transparent" }
                                    GradientStop { position: 1; color: agentCard.color }
                                }
                            }
                        }
                        IconButton { iconName: "copy"; tip: i18n.t["agents.duplicate"]; onClicked: page.ctl.duplicate(model.id) }
                        IconButton {
                            iconName: "pencil"
                            tip: i18n.t["common.edit"]
                            onClicked: editor.openEdit(page.ctl.model.get(index))
                        }
                        IconButton {
                            iconName: "trash-2"
                            danger: true
                            tip: i18n.t["common.delete"]
                            onClicked: confirm.ask(i18n.t["agents.delete_title"], i18n.t["agents.delete_confirm"],
                                                   function() { page.ctl.remove(model.id) })
                        }
                    }
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
        property int agentId: -1
        property string role: "analyst"
        property string autoName: ""
        property string autoPrompt: ""
        property var tools: []
        property var models: []
        property string error: ""
        property bool loadingModels: false
        title: agentId >= 0 ? i18n.t["agents.edit"] : i18n.t["agents.new"]
        subtitle: i18n.t["agents.isolated_note"]
        icon: "bot"
        sheetWidth: 760

        function openNew() {
            agentId = -1; error = ""
            nameField.text = ""; promptBox.text = ""
            autoName = ""; autoPrompt = ""
            temp.value = 0.7; maxTok.value = 2048
            supervisorToggle.checked = false
            keySelect.value = page.ctl.keyOptions.length ? page.ctl.keyOptions[0].id : -1
            applyTemplate("analyst")
            refreshModels()
            modelSelect.combo.editText = models.length ? models[0] : ""
            open()
        }
        function openEdit(data) {
            agentId = data.id; error = ""
            role = data.role
            nameField.text = data.name; autoName = ""
            promptBox.text = data.prompt; autoPrompt = ""
            tools = data.tools
            temp.value = data.temperature; maxTok.value = data.maxTokens
            supervisorToggle.checked = data.isSupervisor
            keySelect.value = data.keyId
            refreshModels()
            modelSelect.combo.editText = data.modelName
            open()
        }
        // Шаблон роли подставляет имя, промпт и инструменты, но не затирает
        // то, что пользователь уже успел поправить руками.
        function applyTemplate(key) {
            role = key
            var info = page.ctl.templateInfo(key)
            if (nameField.text === "" || nameField.text === autoName) { nameField.text = info.name; autoName = info.name }
            if (info.prompt !== "" && (promptBox.text === "" || promptBox.text === autoPrompt)) { promptBox.text = info.prompt; autoPrompt = info.prompt }
            tools = info.tools
        }
        function refreshModels() { models = page.ctl.modelsForKey(keySelect.value === undefined ? -1 : keySelect.value) }
        function toggleTool(name, on) {
            var list = tools.slice()
            var i = list.indexOf(name)
            if (on && i < 0) list.push(name)
            if (!on && i >= 0) list.splice(i, 1)
            tools = list
        }
        function save() {
            var err = page.ctl.save({
                id: agentId, name: nameField.text, role: role, prompt: promptBox.text,
                keyId: keySelect.value === undefined ? -1 : keySelect.value,
                model: modelSelect.combo.editText, temperature: temp.value, maxTokens: maxTok.value,
                tools: tools, isSupervisor: supervisorToggle.checked
            })
            if (err === "") close(); else error = err
        }

        Connections {
            target: page.ctl
            function onModelsLoaded(keyId, list, err) {
                // Пока шёл запрос, могли выбрать другой ключ: чужой список не нужен.
                if (keyId !== keySelect.value) return
                editor.loadingModels = false
                if (err !== "") { editor.error = err; return }
                var current = modelSelect.combo.editText
                editor.models = list
                modelSelect.combo.editText = current
            }
        }

        AText { text: i18n.t["agents.template"]; size: Theme.fsSmall; weight: Font.Medium; dim: true }
        Flow {
            Layout.fillWidth: true
            spacing: 8
            Repeater {
                model: page.ctl.templates
                delegate: Chip {
                    required property var modelData
                    text: modelData.title
                    iconName: modelData.icon
                    isOn: editor.role === modelData.key
                    onClicked: editor.applyTemplate(modelData.key)
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            Field { id: nameField; Layout.fillWidth: true; label: i18n.t["agents.name"]; icon: "user" }
            Select {
                id: keySelect
                Layout.fillWidth: true
                label: i18n.t["agents.provider_key"]
                icon: "key-round"
                options: page.ctl.keyOptions.map(function(k) { return { value: k.id, title: k.title } })
                onPicked: function(v) { keySelect.value = v; editor.loadingModels = false; editor.refreshModels() }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            Select {
                id: modelSelect
                Layout.fillWidth: true
                label: i18n.t["agents.model"]
                icon: "cpu"
                editable: true
                options: editor.models
                placeholder: "gpt-4o-mini"
            }
            Button {
                Layout.alignment: Qt.AlignBottom
                iconName: "refresh-cw"
                text: i18n.t["agents.load_models"]
                loading: editor.loadingModels
                onClicked: { editor.loadingModels = true; editor.error = ""; page.ctl.loadModels(keySelect.value) }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 24
            RangeSlider {
                id: temp
                Layout.fillWidth: true
                label: i18n.t["agents.temperature"]
                from: 0; to: 2; stepSize: 0.1; decimals: 1
                onCommitted: function(v) { temp.value = v }
            }
            RangeSlider {
                id: maxTok
                Layout.fillWidth: true
                label: i18n.t["agents.max_tokens"]
                from: 256; to: 32768; stepSize: 256; decimals: 0
                onCommitted: function(v) { maxTok.value = v }
            }
        }

        AText { text: i18n.t["agents.tools"]; size: Theme.fsSmall; weight: Font.Medium; dim: true }
        Flow {
            Layout.fillWidth: true
            spacing: 8
            Repeater {
                model: page.ctl.tools
                delegate: Chip {
                    required property var modelData
                    text: modelData.title
                    isOn: editor.tools.indexOf(modelData.name) >= 0
                    onClicked: editor.toggleTool(modelData.name, checked)
                }
            }
        }

        TextBox {
            id: promptBox
            Layout.fillWidth: true
            label: i18n.t["agents.prompt"]
            mono: true
            minHeight: 190
        }

        Toggle {
            id: supervisorToggle
            Layout.fillWidth: true
            label: i18n.t["agents.is_supervisor"]
            hint: i18n.t["agents.is_supervisor_hint"]
        }

        AText {
            visible: editor.error !== ""
            text: editor.error
            color: Theme.danger
            wrapMode: Text.Wrap
            elide: Text.ElideNone
            Layout.fillWidth: true
        }

        footer: [
            Item { Layout.fillWidth: true },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: editor.close() },
            Button { text: i18n.t["common.save"]; variant: "primary"; iconName: "check"; onClicked: editor.save() }
        ]
    }
}

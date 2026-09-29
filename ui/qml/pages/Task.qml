import QtQuick
import QtQuick.Layouts
import Ao

// Постановка задачи слева, подзадачи справа: ручные или от ИИ-планировщика,
// с исполнителями и зависимостями.
Page {
    id: page
    title: i18n.t["task.title"]
    subtitle: i18n.t["task.subtitle"]
    icon: "list-checks"
    readonly property var ctl: backend.task
    property string error: ""
    property string fmt: ctl.format

    Connections {
        target: page.ctl
        function onChanged() {
            if (!titleField.input.activeFocus) titleField.text = page.ctl.title
            if (!bodyBox.area.activeFocus) bodyBox.text = page.ctl.description
            if (!limitField.input.activeFocus) limitField.text = page.ctl.tokenLimit
            page.fmt = page.ctl.format
        }
    }
    Component.onCompleted: {
        titleField.text = ctl.title
        bodyBox.text = ctl.description
        limitField.text = ctl.tokenLimit
    }

    function save() {
        error = ctl.saveTask(titleField.text, bodyBox.text, fmt, limitField.text)
        if (error === "") backend.toast("success", i18n.t["toast.task_saved"], "")
        return error === ""
    }

    headerActions: [
        Button {
            iconName: "square-pen"
            text: i18n.t["task.new_task"]
            visible: page.ctl.hasTask
            enabled: !backend.running
            onClicked: confirm.ask(i18n.t["task.new_task"], i18n.t["task.new_task_confirm"],
                                   function() { var e = page.ctl.newTask(); if (e !== "") backend.toast("warning", e, "") }, false,
                                   i18n.t["task.new_task"])
        },
        Button {
            variant: "primary"
            iconName: "play"
            text: i18n.t["run.start"]
            enabled: !backend.running && backend.workspaceId >= 0
            onClicked: if (page.save()) { backend.navigate("run"); backend.run.start() }
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

    RowLayout {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        spacing: 18

        // --- задача -----------------------------------------------------------
        Card {
            Layout.preferredWidth: Math.max(380, page.contentWidth * 0.42)
            Layout.alignment: Qt.AlignTop
            stagger: 0

            ColumnLayout {
                width: parent.width
                spacing: 16

                SectionTitle {
                    Layout.fillWidth: true
                    text: i18n.t["task.statement"]
                    icon: "square-pen"
                    Badge {
                        visible: page.ctl.status !== ""
                        text: page.ctl.statusTitle
                        tone: page.ctl.status === "done" ? "success" : page.ctl.status === "running" ? "accent"
                            : page.ctl.status === "failed" ? "error" : "muted"
                    }
                }
                Field {
                    id: titleField
                    Layout.fillWidth: true
                    label: i18n.t["task.name"]
                    placeholder: i18n.t["task.untitled"]
                    icon: "sparkles"
                }
                TextBox {
                    id: bodyBox
                    Layout.fillWidth: true
                    label: i18n.t["task.body"]
                    placeholder: i18n.t["task.placeholder"]
                    minHeight: 240
                }

                AText { text: i18n.t["task.result_format"]; size: Theme.fsSmall; weight: Font.Medium; dim: true }
                Segmented {
                    Layout.fillWidth: true
                    stretch: true
                    options: page.ctl.formats.map(function(f) { return { value: f.key, title: f.title, icon: f.icon } })
                    value: page.fmt
                    onPicked: function(v) { page.fmt = v }
                }

                Field {
                    id: limitField
                    Layout.fillWidth: true
                    label: i18n.t["task.token_limit"]
                    placeholder: i18n.t["task.token_limit_hint"]
                    hint: i18n.t["task.token_limit_note"]
                    icon: "gauge"
                    mono: true
                }

                AText {
                    visible: page.error !== ""
                    text: page.error
                    color: Theme.danger
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                    Layout.fillWidth: true
                }

                Button {
                    Layout.fillWidth: true
                    variant: "primary"
                    iconName: "check"
                    text: i18n.t["task.save"]
                    onClicked: page.save()
                }
            }
        }

        // --- подзадачи ----------------------------------------------------------
        ColumnLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop
            spacing: 12

            SectionTitle {
                Layout.fillWidth: true
                text: i18n.t["task.subtasks"] + (page.ctl.subtasks.count ? "  ·  " + page.ctl.subtasks.count : "")
                hint: i18n.t["task.subtasks_hint"]
                icon: "workflow"
                Button {
                    compact: true
                    iconName: "plus"
                    text: i18n.t["task.add_subtask"]
                    onClicked: { if (!page.ctl.hasTask && !page.save()) return; subEditor.openNew() }
                }
                Button {
                    compact: true
                    variant: "primary"
                    iconName: "wand-sparkles"
                    text: i18n.t["task.autosplit"]
                    loading: page.ctl.planning
                    enabled: !page.ctl.planning
                    onClicked: if (page.save()) page.ctl.autosplit()
                }
            }

            // Пока ИИ планирует - «скелет» будущих карточек.
            Repeater {
                model: page.ctl.planning ? 3 : 0
                delegate: Card {
                    Layout.fillWidth: true
                    padding: 16
                    ColumnLayout {
                        width: parent.width
                        spacing: 10
                        Skeleton { Layout.preferredWidth: parent.width * 0.55; height: 14 }
                        Skeleton { Layout.fillWidth: true; height: 10 }
                        Skeleton { Layout.preferredWidth: parent.width * 0.35; height: 10 }
                    }
                }
            }

            Card {
                visible: page.ctl.subtasks.count === 0 && !page.ctl.planning
                Layout.fillWidth: true
                EmptyState {
                    width: parent.width
                    icon: "workflow"
                    title: i18n.t["task.no_subtasks_title"]
                    text: i18n.t["task.no_subtasks"]
                }
            }

            ListView {
                id: subList
                Layout.fillWidth: true
                Layout.preferredHeight: contentHeight
                interactive: false
                spacing: 10
                model: page.ctl.subtasks
                move: Transition { NumberAnimation { properties: "y"; duration: Theme.normal; easing.type: Easing.OutCubic } }
                displaced: Transition { NumberAnimation { properties: "y"; duration: Theme.normal; easing.type: Easing.OutCubic } }
                add: Transition {
                    ParallelAnimation {
                        NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.slow }
                        NumberAnimation { property: "scale"; from: 0.96; to: 1; duration: Theme.slow; easing.type: Easing.OutBack }
                    }
                }
                remove: Transition { NumberAnimation { property: "opacity"; to: 0; duration: Theme.normal } }

                delegate: Card {
                    width: subList.width
                    padding: 16
                    hoverable: true
                    glow: model.status === "running"
                    glowColor: Theme.cyan

                    RowLayout {
                        width: parent.width
                        spacing: 14

                        Rectangle {
                            Layout.alignment: Qt.AlignTop
                            width: 30; height: 30; radius: 15
                            color: Theme.alpha(Theme.statusColor(model.status), 0.16)
                            border.color: Theme.alpha(Theme.statusColor(model.status), 0.5)
                            AText { anchors.centerIn: parent; text: model.index; weight: Font.Bold; size: Theme.fsSmall; color: Theme.statusColor(model.status) }
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 6
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 8
                                AText { text: model.title; weight: Font.DemiBold; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone }
                                Badge {
                                    text: model.statusTitle
                                    tint: Theme.statusColor(model.status)
                                }
                            }
                            Flow {
                                Layout.fillWidth: true
                                spacing: 6
                                Badge {
                                    text: model.agentName
                                    icon: model.agentId >= 0 ? "bot" : "circle-alert"
                                    tone: model.agentId >= 0 ? "violet" : "warning"
                                }
                                Repeater {
                                    model: depsHolder.titles
                                    delegate: Badge {
                                        required property string modelData
                                        text: modelData
                                        icon: "git-branch"
                                        tone: "muted"
                                    }
                                }
                                Badge { visible: model.reworks > 0; text: i18n.fmt(i18n.t["task.reworks"], { n: model.reworks }); tone: "warning"; icon: "rotate-ccw" }
                                Badge { visible: model.tokens !== "0"; text: model.tokens + " · " + model.cost; tone: "muted"; icon: "coins" }
                            }
                            Item { id: depsHolder; property var titles: model.depTitles; visible: false }
                            AText {
                                visible: model.description !== ""
                                text: model.description
                                dim: true
                                size: Theme.fsSmall
                                wrapMode: Text.Wrap
                                maximumLineCount: 3
                                Layout.fillWidth: true
                            }
                            Rectangle {
                                visible: model.result !== ""
                                Layout.fillWidth: true
                                radius: Theme.radiusS
                                color: Theme.alpha(Theme.success, 0.06)
                                border.color: Theme.alpha(Theme.success, 0.2)
                                implicitHeight: resultText.implicitHeight + 16
                                AText {
                                    id: resultText
                                    anchors.fill: parent
                                    anchors.margins: 8
                                    text: model.resultPreview
                                    size: Theme.fsSmall
                                    dim: true
                                    wrapMode: Text.Wrap
                                    maximumLineCount: 3
                                }
                            }
                        }

                        ColumnLayout {
                            Layout.alignment: Qt.AlignTop
                            spacing: 2
                            RowLayout {
                                spacing: 2
                                IconButton { iconName: "chevron-up"; size: 28; enabled: index > 0; tip: i18n.t["task.move_up"]; onClicked: page.ctl.move(model.id, -1) }
                                IconButton { iconName: "chevron-down"; size: 28; enabled: index < subList.count - 1; tip: i18n.t["task.move_down"]; onClicked: page.ctl.move(model.id, 1) }
                            }
                            RowLayout {
                                spacing: 2
                                IconButton { iconName: "pencil"; size: 28; tip: i18n.t["common.edit"]; onClicked: subEditor.openEdit(page.ctl.subtasks.get(index)) }
                                IconButton {
                                    iconName: "trash-2"; size: 28; danger: true; tip: i18n.t["common.delete"]
                                    onClicked: confirm.ask(i18n.t["task.delete_subtask"], model.title, function() { page.ctl.removeSubtask(model.id) })
                                }
                            }
                            IconButton {
                                visible: model.status === "done" || model.status === "error" || model.status === "review"
                                iconName: "rotate-ccw"; size: 28; tip: i18n.t["task.rerun"]
                                onClicked: page.ctl.resetSubtask(model.id)
                            }
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
        id: subEditor
        property int subId: -1
        property var deps: []
        property int agentId: -1
        property string error: ""
        title: subId >= 0 ? i18n.t["task.edit_subtask"] : i18n.t["task.add_subtask"]
        icon: "workflow"
        sheetWidth: 620

        function openNew() {
            subId = -1; deps = []; error = ""
            agentId = page.ctl.agentOptions.length ? page.ctl.agentOptions[0].id : -1
            subTitle.text = ""; subDesc.text = ""
            open(); subTitle.focusInput()
        }
        function openEdit(d) {
            subId = d.id; deps = d.deps; error = ""
            agentId = d.agentId
            subTitle.text = d.title; subDesc.text = d.description
            open()
        }
        function toggleDep(id, on) {
            var list = deps.slice()
            var i = list.indexOf(id)
            if (on && i < 0) list.push(id)
            if (!on && i >= 0) list.splice(i, 1)
            deps = list
        }
        function save() {
            var err = page.ctl.saveSubtask({ id: subId, title: subTitle.text, description: subDesc.text,
                                             agentId: agentId, deps: deps })
            if (err === "") close(); else error = err
        }

        Field { id: subTitle; Layout.fillWidth: true; label: i18n.t["task.subtask_title"]; icon: "square-pen"; error: subEditor.error }
        TextBox { id: subDesc; Layout.fillWidth: true; label: i18n.t["common.description"]; minHeight: 120 }
        Select {
            Layout.fillWidth: true
            label: i18n.t["task.assignee"]
            icon: "bot"
            options: [{ value: -1, title: i18n.t["task.unassigned"] }].concat(
                         page.ctl.agentOptions.map(function(a) { return { value: a.id, title: a.name + " · " + a.model } }))
            value: subEditor.agentId
            onPicked: function(v) { subEditor.agentId = v }
        }
        SectionTitle { Layout.fillWidth: true; text: i18n.t["task.depends_on"]; hint: i18n.t["task.depends_hint"]; icon: "git-branch" }
        Flow {
            Layout.fillWidth: true
            spacing: 8
            Repeater {
                model: page.ctl.subtasks
                delegate: Chip {
                    visible: model.id !== subEditor.subId
                    text: model.index + ". " + model.title
                    isOn: subEditor.deps.indexOf(model.id) >= 0
                    onClicked: subEditor.toggleDep(model.id, checked)
                }
            }
        }
        AText {
            visible: page.ctl.subtasks.count <= (subEditor.subId >= 0 ? 1 : 0)
            text: i18n.t["task.no_deps_possible"]
            mute: true
            size: Theme.fsSmall
        }

        footer: [
            Item { Layout.fillWidth: true },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: subEditor.close() },
            Button { text: i18n.t["common.save"]; variant: "primary"; iconName: "check"; onClicked: subEditor.save() }
        ]
    }
}

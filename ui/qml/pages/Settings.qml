import QtQuick
import QtQuick.Layouts
import Ao

// Настройки: интерфейс, human-in-the-loop, супервайзер, выполнение,
// инструменты, песочница, доступные каталоги и безопасность профиля.
Page {
    id: page
    title: i18n.t["settings.title"]
    subtitle: i18n.t["settings.subtitle"]
    icon: "settings"
    readonly property var ctl: backend.prefs
    readonly property var ws: ctl.ws
    readonly property bool hasWs: backend.workspaceId >= 0

    function set(key, value) { ctl.setValue(key, value) }

    Component.onCompleted: ctl.refresh()

    GridLayout {
        Layout.fillWidth: true
        columns: page.contentWidth > 1050 ? 2 : 1
        columnSpacing: 18
        rowSpacing: 18

        // --- интерфейс -----------------------------------------------------------
        Section {
            glyph: "monitor"
            heading: i18n.t["settings.interface"]
            idx: 0
            RowLayout {
                Layout.fillWidth: true
                AText { text: i18n.t["settings.language"]; Layout.fillWidth: true }
                Segmented {
                    options: i18n.languages.map(function(l) { return { value: l.code, title: l.title } })
                    value: i18n.lang
                    onPicked: function(v) { backend.setLanguage(v) }
                }
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 14
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 2
                    AText { text: i18n.t["settings.motion"] }
                    AText { text: i18n.t["settings.motion_hint"]; mute: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
                }
                OrbitLogo { size: 34 }
            }
            Segmented {
                Layout.fillWidth: true
                stretch: true
                options: [
                    { value: "full", title: i18n.t["settings.motion_full"], icon: "sparkles" },
                    { value: "reduced", title: i18n.t["settings.motion_reduced"], icon: "gauge" },
                    { value: "off", title: i18n.t["settings.motion_off"], icon: "pause" }
                ]
                value: backend.motion
                onPicked: function(v) { backend.setMotion(v) }
            }
        }

        // --- human-in-the-loop -----------------------------------------------------
        Section {
            glyph: "hand"
            heading: i18n.t["settings.hitl_title"]
            idx: 1
            enabled: page.hasWs
            Toggle {
                Layout.fillWidth: true
                label: i18n.t["settings.hitl"]
                hint: i18n.t["settings.hitl_hint"]
                isOn: !!page.ws.human_in_the_loop
                onToggled: page.set("human_in_the_loop", checked)
            }
            RangeSlider {
                Layout.fillWidth: true
                enabled: !!page.ws.human_in_the_loop
                opacity: enabled ? 1 : 0.45
                label: i18n.t["settings.hitl_threshold"]
                from: 0; to: 1; stepSize: 0.05
                value: page.ws.hitl_confidence_threshold || 0
                format: function(v) { return v <= 0 ? i18n.t["settings.never"] : v.toFixed(2) }
                onCommitted: function(v) { page.set("hitl_confidence_threshold", v) }
            }
            AText { text: i18n.t["settings.hitl_threshold_hint"]; mute: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
            Toggle {
                Layout.fillWidth: true
                enabled: !!page.ws.human_in_the_loop
                label: i18n.t["settings.hitl_milestone"]
                hint: i18n.t["settings.hitl_milestone_hint"]
                isOn: !!page.ws.hitl_pause_on_milestone
                onToggled: page.set("hitl_pause_on_milestone", checked)
            }
        }

        // --- супервайзер -------------------------------------------------------------
        Section {
            glyph: "shield-check"
            heading: i18n.t["settings.supervisor"]
            idx: 2
            enabled: page.hasWs
            Segmented {
                Layout.fillWidth: true
                stretch: true
                options: [
                    { value: "api", title: i18n.t["settings.sup_api_short"], icon: "key-round" },
                    { value: "local", title: i18n.t["settings.sup_local_short"], icon: "hard-drive" }
                ]
                value: page.ws.supervisor_mode || "api"
                onPicked: function(v) { page.set("supervisor_mode", v) }
            }
            Select {
                visible: (page.ws.supervisor_mode || "api") === "api"
                Layout.fillWidth: true
                label: i18n.t["settings.supervisor_agent"]
                icon: "bot"
                options: page.ctl.supervisorOptions.map(function(o) { return { value: o.id, title: o.title } })
                value: page.ws.supervisor_agent_id === undefined ? -1 : page.ws.supervisor_agent_id
                onPicked: function(v) { page.set("supervisor_agent_id", v) }
            }
            RowLayout {
                visible: page.ws.supervisor_mode === "local"
                Layout.fillWidth: true
                spacing: 12
                Field {
                    Layout.fillWidth: true
                    label: i18n.t["settings.local_model"]
                    text: page.ws.supervisor_local_model || ""
                    mono: true
                    icon: "cpu"
                    onEditingFinished: page.set("supervisor_local_model", text)
                }
                Field {
                    Layout.fillWidth: true
                    label: i18n.t["keys.base_url"]
                    text: page.ws.supervisor_local_base_url || ""
                    mono: true
                    icon: "globe"
                    onEditingFinished: page.set("supervisor_local_base_url", text)
                }
            }
            RangeSlider {
                Layout.fillWidth: true
                label: i18n.t["settings.summary_interval"]
                from: 0; to: 120; stepSize: 5
                value: page.ws.summary_interval_minutes || 0
                format: function(v) { return v <= 0 ? i18n.t["settings.off"] : Math.round(v) + " " + i18n.t["settings.min"] }
                onCommitted: function(v) { page.set("summary_interval_minutes", v) }
            }
            Toggle {
                Layout.fillWidth: true
                label: i18n.t["settings.summary_on_event"]
                hint: i18n.t["settings.summary_cost_hint"]
                isOn: !!page.ws.summary_on_event
                onToggled: page.set("summary_on_event", checked)
            }
            Toggle {
                Layout.fillWidth: true
                label: i18n.t["settings.anonymize"]
                hint: i18n.t["settings.anonymize_hint"]
                isOn: page.ws.anonymize_summaries !== false
                onToggled: page.set("anonymize_summaries", checked)
            }
        }

        // --- выполнение ---------------------------------------------------------------
        Section {
            glyph: "workflow"
            heading: i18n.t["settings.execution"]
            idx: 3
            enabled: page.hasWs
            RangeSlider {
                Layout.fillWidth: true
                label: i18n.t["settings.max_steps"]
                from: 1; to: 50; stepSize: 1; decimals: 0
                value: page.ws.agent_max_steps || 10
                onCommitted: function(v) { page.set("agent_max_steps", v) }
            }
            RangeSlider {
                Layout.fillWidth: true
                label: i18n.t["settings.rework_rounds"]
                from: 0; to: 10; stepSize: 1; decimals: 0
                value: page.ws.max_rework_rounds === undefined ? 2 : page.ws.max_rework_rounds
                onCommitted: function(v) { page.set("max_rework_rounds", v) }
            }
            RangeSlider {
                Layout.fillWidth: true
                label: i18n.t["settings.parallel"]
                from: 1; to: 16; stepSize: 1; decimals: 0
                value: page.ws.max_parallel_agents || 6
                onCommitted: function(v) { page.set("max_parallel_agents", v) }
            }
        }

        // --- инструменты -----------------------------------------------------------------
        Section {
            glyph: "zap"
            heading: i18n.t["settings.tools"]
            idx: 4
            enabled: page.hasWs
            AText { text: i18n.t["settings.tools_hint"]; mute: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
            Flow {
                Layout.fillWidth: true
                spacing: 8
                Repeater {
                    model: page.ctl.toolSwitches
                    delegate: Chip {
                        required property var modelData
                        text: modelData.title
                        isOn: (page.ws.tools_enabled || []).indexOf(modelData.key) >= 0
                        onClicked: page.ctl.setTool(modelData.key, checked)
                    }
                }
            }
            AText { text: i18n.t["settings.search_backend"]; size: Theme.fsSmall; weight: Font.Medium; dim: true }
            Segmented {
                options: [{ value: "duckduckgo", title: "DuckDuckGo" }, { value: "tavily", title: "Tavily" }, { value: "brave", title: "Brave" }]
                value: page.ws.search_backend || "duckduckgo"
                onPicked: function(v) { page.set("search_backend", v) }
            }
            RowLayout {
                visible: (page.ws.search_backend || "duckduckgo") !== "duckduckgo"
                Layout.fillWidth: true
                spacing: 10
                Field {
                    id: searchKey
                    Layout.fillWidth: true
                    label: i18n.t["settings.search_key"]
                    placeholder: page.ctl.hasSearchKey ? i18n.t["settings.search_key_set"] : "tvly-…"
                    password: true
                    mono: true
                    icon: "lock"
                    onAccepted: { page.ctl.setSearchKey(text); text = "" }
                }
                Button {
                    Layout.alignment: Qt.AlignBottom
                    iconName: "check"
                    text: i18n.t["common.save"]
                    onClicked: { page.ctl.setSearchKey(searchKey.text); searchKey.text = "" }
                }
            }
            Toggle {
                Layout.fillWidth: true
                label: i18n.t["settings.fetch_pages"]
                isOn: page.ws.fetch_pages !== false
                onToggled: page.set("fetch_pages", checked)
            }
        }

        // --- песочница ---------------------------------------------------------------------
        Section {
            glyph: "box"
            heading: i18n.t["settings.sandbox"]
            idx: 5
            enabled: page.hasWs
            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                Segmented {
                    options: [{ value: "auto", title: i18n.t["settings.sb_auto"] },
                              { value: "subprocess", title: i18n.t["settings.sb_process"] },
                              { value: "docker", title: "Docker" }]
                    value: page.ws.sandbox_backend || "auto"
                    onPicked: function(v) { page.set("sandbox_backend", v) }
                }
                Item { Layout.fillWidth: true }
                Spinner { visible: page.ctl.docker === "checking"; size: 14 }
                Badge {
                    visible: page.ctl.docker !== "checking"
                    text: page.ctl.docker === "yes" ? i18n.t["settings.docker_yes"] : i18n.t["settings.docker_no"]
                    tone: page.ctl.docker === "yes" ? "success" : "warning"
                    icon: page.ctl.docker === "yes" ? "circle-check" : "triangle-alert"
                }
                IconButton { iconName: "refresh-cw"; tip: i18n.t["settings.docker_recheck"]; onClicked: page.ctl.checkDocker() }
            }
            AText {
                text: page.ctl.docker === "yes" ? i18n.t["settings.docker_note_yes"] : i18n.t["settings.docker_note_no"]
                mute: true
                size: Theme.fsSmall
                wrapMode: Text.Wrap
                elide: Text.ElideNone
                Layout.fillWidth: true
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 20
                RangeSlider {
                    Layout.fillWidth: true
                    label: i18n.t["settings.sb_timeout"]
                    from: 5; to: 300; stepSize: 5; decimals: 0; suffix: " s"
                    value: page.ws.sandbox_timeout_sec || 30
                    onCommitted: function(v) { page.set("sandbox_timeout_sec", v) }
                }
                RangeSlider {
                    Layout.fillWidth: true
                    label: i18n.t["settings.sb_memory"]
                    from: 64; to: 4096; stepSize: 64; decimals: 0; suffix: " MB"
                    value: page.ws.sandbox_memory_mb || 512
                    onCommitted: function(v) { page.set("sandbox_memory_mb", v) }
                }
            }
        }

        // --- каталоги --------------------------------------------------------------------------
        Section {
            glyph: "folder-open"
            heading: i18n.t["settings.allowed_paths"]
            idx: 6
            enabled: page.hasWs
            AText { text: i18n.t["settings.paths_warning"]; color: Theme.warning; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
            Repeater {
                model: page.ws.extra_allowed_paths || []
                delegate: Rectangle {
                    required property string modelData
                    Layout.fillWidth: true
                    height: 38
                    radius: Theme.radiusS
                    color: Theme.surface2
                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 12
                        anchors.rightMargin: 4
                        Icon { name: "folder"; size: 14; color: Theme.textMute }
                        AText { text: modelData; mono: true; size: Theme.fsSmall; Layout.fillWidth: true; elide: Text.ElideMiddle }
                        IconButton { iconName: "x"; size: 28; danger: true; onClicked: page.ctl.removePath(modelData) }
                    }
                }
            }
            AText { visible: (page.ws.extra_allowed_paths || []).length === 0; text: i18n.t["settings.paths_empty"]; mute: true; size: Theme.fsSmall }
            Button { iconName: "plus"; text: i18n.t["settings.add_path"]; onClicked: page.ctl.addPath() }
        }

        // --- безопасность и данные ----------------------------------------------------------
        Section {
            glyph: "lock"
            heading: i18n.t["settings.security"]
            idx: 7
            AText { text: i18n.t["settings.security_text"]; dim: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
            RowLayout {
                spacing: 10
                Button { iconName: "key-round"; text: i18n.t["settings.change_password"]; onClicked: pwd.openFresh() }
                Button { iconName: "folder-open"; text: i18n.t["settings.open_data"]; onClicked: backend.openPath(backend.dataRoot) }
            }
            AText { text: backend.dataRoot; mono: true; mute: true; size: Theme.fsMicro; Layout.fillWidth: true; elide: Text.ElideMiddle }
        }
    }

    component Section: Card {
        id: sec
        property string glyph: ""
        property string heading: ""
        property int idx: 0
        default property alias items: sectionBody.data
        Layout.fillWidth: true
        Layout.alignment: Qt.AlignTop
        stagger: idx
        opacity: enabled ? enter : enter * 0.5
        ColumnLayout {
            id: sectionBody
            width: parent.width
            spacing: 14
            SectionTitle { Layout.fillWidth: true; text: sec.heading; icon: sec.glyph }
        }
    }

    Sheet {
        id: pwd
        title: i18n.t["settings.change_password"]
        subtitle: i18n.t["settings.password_note"]
        icon: "key-round"
        sheetWidth: 460
        property string error: ""
        function openFresh() { error = ""; oldPwd.text = ""; newPwd.text = ""; newPwd2.text = ""; open(); oldPwd.focusInput() }
        function submit() {
            error = page.ctl.changePassword(oldPwd.text, newPwd.text, newPwd2.text)
            if (error === "") close()
        }
        Field { id: oldPwd; Layout.fillWidth: true; label: i18n.t["settings.old_password"]; password: true; icon: "lock" }
        Field { id: newPwd; Layout.fillWidth: true; label: i18n.t["login.password"]; password: true; icon: "lock" }
        Field { id: newPwd2; Layout.fillWidth: true; label: i18n.t["login.password2"]; password: true; icon: "lock"; error: pwd.error; onAccepted: pwd.submit() }
        footer: [
            Item { Layout.fillWidth: true },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: pwd.close() },
            Button { text: i18n.t["common.save"]; variant: "primary"; iconName: "check"; onClicked: pwd.submit() }
        ]
    }
}

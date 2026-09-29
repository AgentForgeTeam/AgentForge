import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts
import Ao

// Оболочка после входа: боковая навигация, верхняя панель со статусом
// прогона и страницы, которые загружаются при первом открытии и дальше
// переключаются с анимацией.
Item {
    id: shell
    // Стартовая страница выбирается один раз; дальше страницу меняет только
    // пользователь. Связывание со статусом воркспейса сбрасывало бы выбор при
    // каждом изменении состояния приложения.
    property string page: ""
    Component.onCompleted: page = backend.workspaceId >= 0 ? "dashboard" : "workspaces"

    readonly property var sections: [
        { title: i18n.t["nav.g_project"], items: [
            { key: "workspaces", icon: "layers", title: i18n.t["nav.workspaces"] },
            { key: "agents", icon: "bot", title: i18n.t["nav.agents"] },
            { key: "task", icon: "list-checks", title: i18n.t["nav.task"] } ] },
        { title: i18n.t["nav.g_work"], items: [
            { key: "run", icon: "play", title: i18n.t["nav.run"] },
            { key: "supervisor", icon: "shield-check", title: i18n.t["nav.supervisor"] },
            { key: "dashboard", icon: "layout-dashboard", title: i18n.t["nav.dashboard"] } ] },
        { title: i18n.t["nav.g_resources"], items: [
            { key: "keys", icon: "key-round", title: i18n.t["nav.keys"] },
            { key: "budget", icon: "wallet", title: i18n.t["nav.budget"] },
            { key: "export", icon: "package", title: i18n.t["nav.export"] } ] }
    ]
    readonly property var pageFiles: ({
        workspaces: "pages/Workspaces.qml", agents: "pages/Agents.qml", task: "pages/Task.qml",
        run: "pages/Run.qml", supervisor: "pages/Supervisor.qml", dashboard: "pages/Dashboard.qml",
        keys: "pages/Keys.qml", budget: "pages/Budget.qml", export: "pages/Export.qml",
        settings: "pages/Settings.qml"
    })
    readonly property var order: ["workspaces", "agents", "task", "run", "supervisor",
                                  "dashboard", "keys", "budget", "export", "settings"]

    function go(key) { if (pageFiles[key]) page = key }

    Connections {
        target: backend
        function onNavigateRequested(key) { shell.go(key) }
    }

    // Горячие клавиши: Ctrl+1…0 — страницы, Ctrl+K — палитра команд.
    Repeater {
        model: shell.order
        delegate: Item {
            required property string modelData
            required property int index
            Shortcut {
                sequence: "Ctrl+" + ((index + 1) % 10)
                onActivated: shell.go(modelData)
            }
        }
    }
    Shortcut { sequence: "Ctrl+K"; onActivated: palette.open() }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // --- боковая панель -----------------------------------------------------
        Rectangle {
            id: sidebar
            Layout.preferredWidth: 248
            Layout.fillHeight: true
            color: Theme.alpha(Theme.sidebar, 0.86)
            Rectangle { anchors.right: parent.right; width: 1; height: parent.height; color: Theme.border }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                anchors.topMargin: 20
                spacing: 4

                RowLayout {
                    Layout.fillWidth: true
                    Layout.leftMargin: 6
                    Layout.bottomMargin: 18
                    spacing: 12
                    OrbitLogo { size: 36 }
                    ColumnLayout {
                        spacing: 0
                        AText { text: backend.appName; weight: Font.Bold; size: Theme.fsH3 }
                        AText { text: "v" + backend.appVersion; mute: true; size: Theme.fsMicro; mono: true }
                    }
                }

                // Быстрый поиск / палитра команд.
                Rectangle {
                    Layout.fillWidth: true
                    Layout.bottomMargin: 10
                    height: 36
                    radius: Theme.radius
                    color: searchHover.hovered ? Theme.surface2 : Theme.input
                    border.color: Theme.border
                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 12
                        anchors.rightMargin: 8
                        spacing: 8
                        Icon { name: "search"; size: 15; color: Theme.textMute }
                        AText { text: i18n.t["nav.search"]; mute: true; size: Theme.fsSmall; Layout.fillWidth: true }
                        Rectangle {
                            radius: 5; color: Theme.surface3
                            implicitWidth: kbd.implicitWidth + 10; implicitHeight: 20
                            AText { id: kbd; anchors.centerIn: parent; text: "Ctrl K"; size: Theme.fsMicro; mono: true; dim: true }
                        }
                    }
                    HoverHandler { id: searchHover; cursorShape: Qt.PointingHandCursor }
                    TapHandler { onTapped: palette.open() }
                }

                // Навигация с «переезжающей» подсветкой.
                Item {
                    id: navArea
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Rectangle {
                        id: highlight
                        property Item target: null
                        x: 0
                        width: navArea.width
                        height: 38
                        // Зависимость от высот нужна, чтобы позиция пересчиталась после раскладки.
                        y: target ? (navColumn.height, sidebar.height, target.mapToItem(navArea, 0, 0).y) : -100
                        radius: Theme.radius
                        visible: target !== null
                        gradient: Gradient {
                            orientation: Gradient.Horizontal
                            GradientStop { position: 0; color: Theme.alpha(Theme.violet, 0.28) }
                            GradientStop { position: 1; color: Theme.alpha(Theme.cyan, 0.06) }
                        }
                        border.color: Theme.alpha(Theme.violetSoft, 0.25)
                        Behavior on y { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
                        Rectangle {
                            width: 3; height: 18; radius: 2
                            anchors.verticalCenter: parent.verticalCenter
                            x: 4
                            gradient: Gradient {
                                GradientStop { position: 0; color: Theme.violetSoft }
                                GradientStop { position: 1; color: Theme.cyan }
                            }
                        }
                    }

                    Column {
                        id: navColumn
                        width: parent.width
                        spacing: 2
                        Repeater {
                            model: shell.sections
                            delegate: Column {
                                id: section
                                required property var modelData
                                width: navColumn.width
                                spacing: 2
                                AText {
                                    text: section.modelData.title.toUpperCase()
                                    size: Theme.fsMicro
                                    weight: Font.DemiBold
                                    color: Theme.textFaint
                                    leftPadding: 12
                                    topPadding: 12
                                    bottomPadding: 6
                                    font.letterSpacing: 1.2
                                }
                                Repeater {
                                    model: section.modelData.items
                                    delegate: NavItem {
                                        width: navColumn.width
                                    }
                                }
                            }
                        }
                    }
                }

                NavItem {
                    Layout.fillWidth: true
                    modelData: ({ key: "settings", icon: "settings", title: i18n.t["nav.settings"] })
                }

                // Профиль и выход.
                Rectangle {
                    Layout.fillWidth: true
                    Layout.topMargin: 8
                    height: 56
                    radius: Theme.radius
                    color: Theme.alpha(Theme.surface2, 0.7)
                    border.color: Theme.border
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 10
                        Rectangle {
                            width: 34; height: 34; radius: 17
                            gradient: Gradient {
                                GradientStop { position: 0; color: Theme.violet }
                                GradientStop { position: 1; color: Theme.teal }
                            }
                            AText {
                                anchors.centerIn: parent
                                text: backend.username.length ? backend.username[0].toUpperCase() : "?"
                                weight: Font.Bold
                                color: "white"
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 0
                            AText { text: backend.username; weight: Font.DemiBold; Layout.fillWidth: true }
                            AText { text: i18n.t["nav.local_profile"]; mute: true; size: Theme.fsMicro; Layout.fillWidth: true }
                        }
                        IconButton {
                            iconName: "log-out"
                            tip: i18n.t["nav.logout"]
                            onClicked: backend.logout()
                        }
                    }
                }
            }
        }

        // --- правая часть ------------------------------------------------------
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            TopBar {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
            }

            Item {
                id: stage
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                Repeater {
                    model: shell.order
                    delegate: Loader {
                        id: pageLoader
                        required property string modelData
                        readonly property bool current: shell.page === modelData
                        property bool visited: false
                        anchors.fill: parent
                        active: visited || current
                        visible: opacity > 0.01
                        opacity: current ? 1 : 0
                        source: shell.pageFiles[modelData]
                        onCurrentChanged: if (current) { visited = true; slide.y = Theme.rich ? 16 : 0; slideIn.restart() }
                        Behavior on opacity { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
                        transform: Translate { id: slide }
                        NumberAnimation { id: slideIn; target: slide; property: "y"; to: 0; duration: Theme.slow; easing.type: Easing.OutCubic }
                    }
                }
            }
        }
    }

    // Строка навигации (используется и для «Настроек» внизу панели).
    component NavItem: Item {
        id: nav
        required property var modelData
        readonly property bool active: shell.page === modelData.key
        height: 38
        onActiveChanged: if (active) highlight.target = nav
        Component.onCompleted: if (active) highlight.target = nav

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 14
            anchors.rightMargin: 10
            spacing: 12
            Icon {
                name: nav.modelData.icon
                size: 17
                color: nav.active ? Theme.violetSoft : (navMouse.containsMouse ? Theme.text : Theme.textMute)
            }
            AText {
                text: nav.modelData.title
                Layout.fillWidth: true
                weight: nav.active ? Font.DemiBold : Font.Medium
                color: nav.active ? Theme.text : (navMouse.containsMouse ? Theme.text : Theme.textDim)
                Behavior on color { ColorAnimation { duration: Theme.fast } }
            }
            // Живые индикаторы: идёт прогон, ждут решения.
            StatusDot {
                visible: nav.modelData.key === "run" && backend.running
                status: "running"
            }
            Badge {
                visible: nav.modelData.key === "run" && backend.pendingApprovals > 0
                text: backend.pendingApprovals
                tone: "warning"
                solid: true
            }
            Badge {
                visible: nav.modelData.key === "supervisor" && backend.supervisor.openIncidents > 0
                text: backend.supervisor.openIncidents
                tone: "error"
            }
        }
        MouseArea {
            id: navMouse
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: shell.go(nav.modelData.key)
        }
    }

    // Верхняя панель: активный воркспейс и живой статус прогона.
    component TopBar: Rectangle {
        color: "transparent"
        Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: Theme.alpha(Theme.border, 0.7) }
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: Theme.pagePad
            anchors.rightMargin: Theme.pagePad
            spacing: 14

            Icon { name: "layers"; size: 15; color: Theme.textMute }
            T.AbstractButton {
                id: wsButton
                hoverEnabled: true
                implicitHeight: 34
                implicitWidth: wsRow.implicitWidth + 20
                onClicked: shell.go("workspaces")
                background: Rectangle {
                    radius: Theme.radiusS
                    color: wsButton.hovered ? Theme.surface2 : "transparent"
                    Behavior on color { ColorAnimation { duration: Theme.fast } }
                }
                contentItem: Item {
                    RowLayout {
                        id: wsRow
                        anchors.centerIn: parent
                        spacing: 8
                        AText {
                            text: backend.workspaceName !== "" ? backend.workspaceName : i18n.t["top.no_ws"]
                            weight: Font.DemiBold
                            color: backend.workspaceName !== "" ? Theme.text : Theme.textMute
                        }
                        Icon { name: "chevron-down"; size: 14; color: Theme.textMute }
                    }
                }
            }

            Item { Layout.fillWidth: true }

            // Статус прогона: пульсирующая точка, время, токены, стоимость.
            Rectangle {
                visible: backend.running
                implicitHeight: 34
                implicitWidth: runRow.implicitWidth + 24
                radius: 17
                color: Theme.alpha(Theme.cyan, 0.08)
                border.color: Theme.alpha(Theme.cyan, 0.35)
                RowLayout {
                    id: runRow
                    anchors.centerIn: parent
                    spacing: 10
                    StatusDot { status: backend.paused ? "paused" : "running" }
                    AText { text: backend.paused ? i18n.t["top.paused"] : i18n.t["top.running"]; weight: Font.DemiBold; size: Theme.fsSmall }
                    AText { text: backend.runElapsed; mono: true; size: Theme.fsSmall; dim: true }
                    Rectangle { width: 1; height: 14; color: Theme.border }
                    Icon { name: "coins"; size: 13; color: Theme.textMute }
                    AText { text: backend.runTokens; mono: true; size: Theme.fsSmall; dim: true }
                    AText { text: backend.runCost; mono: true; size: Theme.fsSmall; color: Theme.teal }
                }
                MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: shell.go("run") }
            }

            // Колокольчик: ждут решения человека.
            T.AbstractButton {
                id: bell
                visible: backend.pendingApprovals > 0
                implicitWidth: 38; implicitHeight: 34
                hoverEnabled: true
                onClicked: shell.go("run")
                background: Rectangle {
                    radius: Theme.radiusS
                    color: Theme.alpha(Theme.warning, bell.hovered ? 0.22 : 0.12)
                    border.color: Theme.alpha(Theme.warning, 0.4)
                }
                contentItem: Icon {
                    name: "bell"; size: 16; color: Theme.warning
                    SequentialAnimation on rotation {
                        running: Theme.rich && bell.visible
                        loops: Animation.Infinite
                        NumberAnimation { to: 14; duration: 90 }
                        NumberAnimation { to: -12; duration: 110 }
                        NumberAnimation { to: 8; duration: 90 }
                        NumberAnimation { to: 0; duration: 90 }
                        PauseAnimation { duration: 2200 }
                    }
                }
                Tip { text: i18n.fmt(i18n.t["top.pending"], { n: backend.pendingApprovals }); shown: bell.hovered }
            }

            Button {
                visible: !backend.running && shell.page !== "run"
                compact: true
                variant: "secondary"
                iconName: "play"
                text: i18n.t["run.start"]
                enabled: backend.run.canStart
                onClicked: { shell.go("run"); backend.run.start() }
            }
        }
    }

    CommandPalette { id: palette }

    // Палитра команд: переход на страницы и частые действия с клавиатуры.
    component CommandPalette: Sheet {
        id: pal
        sheetWidth: 560
        title: i18n.t["palette.title"]
        icon: "command"
        property string query: ""
        readonly property var entries: {
            var list = []
            for (var s = 0; s < shell.sections.length; ++s)
                for (var i = 0; i < shell.sections[s].items.length; ++i) {
                    var it = shell.sections[s].items[i]
                    list.push({ kind: "page", key: it.key, icon: it.icon, title: it.title })
                }
            list.push({ kind: "page", key: "settings", icon: "settings", title: i18n.t["nav.settings"] })
            list.push({ kind: "action", key: "start", icon: "play", title: i18n.t["palette.start"] })
            list.push({ kind: "action", key: "summary", icon: "scroll-text", title: i18n.t["sup.make_summary"] })
            list.push({ kind: "action", key: "motion", icon: "sparkles", title: i18n.t["palette.motion"] })
            var q = pal.query.toLowerCase()
            return q === "" ? list : list.filter(function(e) { return e.title.toLowerCase().indexOf(q) >= 0 })
        }
        property int selected: 0
        onOpened: { query = ""; selected = 0; searchField.text = ""; searchField.focusInput() }

        function run(entry) {
            close()
            if (!entry) return
            if (entry.kind === "page") shell.go(entry.key)
            else if (entry.key === "start") { shell.go("run"); backend.run.start() }
            else if (entry.key === "summary") backend.supervisor.makeSummary()
            else if (entry.key === "motion") backend.setMotion(backend.motion === "full" ? "reduced" : backend.motion === "reduced" ? "off" : "full")
        }

        Field {
            id: searchField
            Layout.fillWidth: true
            icon: "search"
            placeholder: i18n.t["palette.placeholder"]
            onTextChanged: { pal.query = text; pal.selected = 0 }
            onAccepted: pal.run(pal.entries[pal.selected])
            onDownPressed: pal.selected = Math.min(pal.selected + 1, pal.entries.length - 1)
            onUpPressed: pal.selected = Math.max(pal.selected - 1, 0)
        }
        Repeater {
            model: pal.entries
            delegate: Rectangle {
                required property var modelData
                required property int index
                Layout.fillWidth: true
                height: 40
                radius: Theme.radius
                color: index === pal.selected ? Theme.alpha(Theme.violet, 0.18)
                     : (entryMouse.containsMouse ? Theme.surface2 : "transparent")
                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 12
                    anchors.rightMargin: 12
                    spacing: 12
                    Icon { name: modelData.icon; size: 16; color: index === pal.selected ? Theme.violetSoft : Theme.textMute }
                    AText { text: modelData.title; Layout.fillWidth: true }
                    AText { text: modelData.kind === "page" ? i18n.t["palette.page"] : i18n.t["palette.action"]; mute: true; size: Theme.fsMicro }
                }
                MouseArea {
                    id: entryMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: pal.selected = index
                    onClicked: pal.run(modelData)
                }
            }
        }
    }
}

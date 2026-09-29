import QtQuick
import QtQuick.Layouts
import Ao

// Дашборд: метрики, прогресс, кривые расхода, агенты, лента и инциденты.
Page {
    id: page
    title: i18n.t["dash.title"]
    subtitle: i18n.t["dash.subtitle"]
    icon: "layout-dashboard"
    readonly property var ctl: backend.dashboard
    property string series: "cost"

    Component.onCompleted: ctl.refresh()

    headerActions: [
        IconButton { iconName: "refresh-cw"; tip: i18n.t["common.refresh"]; onClicked: page.ctl.refresh() }
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

    // --- метрики ---------------------------------------------------------------
    GridLayout {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        columns: page.contentWidth > 1100 ? 6 : 3
        columnSpacing: 14
        rowSpacing: 14
        Metric { idx: 0; glyph: "bot"; caption: i18n.t["dash.m_agents"]; value: page.ctl.agentsCount }
        Metric {
            idx: 1; glyph: "list-checks"; caption: i18n.t["dash.m_subtasks"]
            value: page.ctl.done; total: page.ctl.total > 0 ? String(page.ctl.total) : ""
            tint: Theme.success
        }
        Metric {
            idx: 2; glyph: "coins"; unit: "tokens"; value: page.ctl.tokens
            caption: page.ctl.limitPct >= 0 ? i18n.fmt(i18n.t["dash.m_tokens_pct"], { pct: Math.round(page.ctl.limitPct * 100) })
                                            : i18n.t["dash.m_tokens"]
            tint: page.ctl.limitPct >= 1 ? Theme.danger : page.ctl.limitPct >= 0.8 ? Theme.warning : Theme.text
        }
        Metric { idx: 3; glyph: "dollar-sign"; unit: "usd"; caption: i18n.t["dash.m_cost"]; value: page.ctl.cost; tint: Theme.teal }
        Metric { idx: 4; glyph: "rotate-ccw"; caption: i18n.t["dash.m_reworks"]; value: page.ctl.reworks; tint: page.ctl.reworks ? Theme.warning : Theme.text }
        Metric {
            idx: 5; glyph: "triangle-alert"; caption: i18n.t["dash.m_open_incidents"]; value: page.ctl.openIncidents
            tint: page.ctl.openIncidents ? Theme.danger : Theme.text
            clickable: true
            onActivated: backend.navigate("supervisor")
        }
    }

    // --- прогресс --------------------------------------------------------------
    Card {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        stagger: 2
        ColumnLayout {
            width: parent.width
            spacing: 12
            RowLayout {
                Layout.fillWidth: true
                Icon { name: "list-checks"; color: Theme.violetSoft }
                AText {
                    text: page.ctl.taskTitle !== "" ? page.ctl.taskTitle : i18n.t["task.no_task"]
                    weight: Font.DemiBold
                    size: Theme.fsH3
                    Layout.fillWidth: true
                }
                AText {
                    visible: page.ctl.total > 0
                    text: page.ctl.done + " / " + page.ctl.total + "  ·  " + Math.round(page.ctl.total ? page.ctl.done / page.ctl.total * 100 : 0) + "%"
                    mono: true
                    dim: true
                }
            }
            SegmentBar { Layout.fillWidth: true; segments: page.ctl.segments }
        }
    }

    // --- графики ------------------------------------------------------------------
    RowLayout {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        spacing: 16
        Card {
            Layout.fillWidth: true
            Layout.preferredWidth: 3
            Layout.preferredHeight: 300
            stagger: 3
            ColumnLayout {
                anchors.fill: parent
                spacing: 12
                RowLayout {
                    Layout.fillWidth: true
                    SectionTitle { Layout.fillWidth: true; text: i18n.t["dash.spend"]; icon: "chart-line" }
                    Segmented {
                        options: [{ value: "cost", title: i18n.t["dash.money"] }, { value: "tokens", title: i18n.t["dash.tokens"] }]
                        value: page.series
                        onPicked: function(v) { page.series = v }
                    }
                }
                LineChart {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    points: page.series === "cost" ? page.ctl.costSeries : page.ctl.tokenSeries
                    unit: page.series === "cost" ? "usd" : "tokens"
                    lineColor: page.series === "cost" ? Theme.teal : Theme.violetSoft
                    fillColor: page.series === "cost" ? Theme.teal : Theme.violet
                    emptyText: i18n.t["dash.no_usage"]
                }
            }
        }
        Card {
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Layout.preferredHeight: 300
            stagger: 4
            ColumnLayout {
                anchors.fill: parent
                spacing: 12
                SectionTitle {
                    Layout.fillWidth: true
                    text: i18n.t["dash.by_agent"]
                    icon: "chart-bar"
                    Badge {
                        visible: page.ctl.supervisorShare > 0
                        text: i18n.fmt(i18n.t["dash.sup_share"], { pct: Math.round(page.ctl.supervisorShare * 100) })
                        tone: page.ctl.supervisorShare > 0.5 ? "warning" : "violet"
                        icon: "shield-check"
                    }
                }
                Flickable {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    contentHeight: bars.implicitHeight
                    BarList { id: bars; width: parent.width; bars: page.ctl.bars; emptyText: i18n.t["dash.no_usage"] }
                }
            }
        }
    }

    // --- агенты ------------------------------------------------------------------
    Card {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        stagger: 5
        ColumnLayout {
            width: parent.width
            spacing: 8
            SectionTitle { Layout.fillWidth: true; text: i18n.t["dash.agents"]; icon: "users" }
            AText { visible: page.ctl.agentsModel.count === 0; text: i18n.t["agents.empty"]; mute: true }
            Repeater {
                model: page.ctl.agentsModel
                delegate: Rectangle {
                    Layout.fillWidth: true
                    height: 46
                    radius: Theme.radius
                    color: rowHover.hovered ? Theme.alpha(Theme.surface3, 0.6) : "transparent"
                    HoverHandler { id: rowHover }
                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 10
                        anchors.rightMargin: 10
                        spacing: 12
                        StatusDot { status: model.status }
                        Icon { name: model.icon; size: 15; color: model.isSupervisor ? Theme.magenta : Theme.violetSoft }
                        AText { text: model.name; weight: Font.Medium; Layout.preferredWidth: 180 }
                        AText {
                            text: model.doing !== "" ? "→ " + model.doing : model.statusTitle
                            dim: model.doing !== ""
                            mute: model.doing === ""
                            size: Theme.fsSmall
                            Layout.fillWidth: true
                        }
                        Rectangle {
                            Layout.preferredWidth: 120
                            height: 5
                            radius: 3
                            color: Theme.surface3
                            Rectangle {
                                height: parent.height
                                radius: 3
                                width: parent.width * Math.min(1, model.share)
                                color: Theme.violet
                                Behavior on width { NumberAnimation { duration: Theme.slow } }
                            }
                        }
                        AText { text: model.tokens; mono: true; size: Theme.fsSmall; dim: true; Layout.preferredWidth: 70; horizontalAlignment: Text.AlignRight }
                        AText { text: model.cost; mono: true; size: Theme.fsSmall; color: Theme.teal; Layout.preferredWidth: 70; horizontalAlignment: Text.AlignRight }
                    }
                }
            }
        }
    }

    // --- лента и инциденты -------------------------------------------------------------
    RowLayout {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        spacing: 16
        Card {
            Layout.fillWidth: true
            Layout.preferredWidth: 3
            Layout.alignment: Qt.AlignTop
            stagger: 6
            ColumnLayout {
                width: parent.width
                spacing: 10
                SectionTitle { Layout.fillWidth: true; text: i18n.t["dash.feed"]; icon: "message-square-text" }
                AText { visible: page.ctl.feed.count === 0; text: i18n.t["dash.no_feed"]; mute: true; wrapMode: Text.Wrap; Layout.fillWidth: true }
                Repeater {
                    model: page.ctl.feed
                    delegate: ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 3
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 8
                            Rectangle { width: 6; height: 6; radius: 3; color: Theme.tone(model.tone) }
                            AText { text: model.who; weight: Font.DemiBold; size: Theme.fsSmall; color: Theme.tone(model.tone) }
                            Badge { visible: model.badge !== ""; text: model.badge; tone: model.tone }
                            AText { visible: model.confidence !== ""; text: i18n.t["dash.confidence"] + " " + model.confidence; mute: true; size: Theme.fsMicro }
                            Item { Layout.fillWidth: true }
                            AText { text: model.when; mute: true; mono: true; size: Theme.fsMicro }
                        }
                        AText { text: model.text; dim: true; size: Theme.fsSmall; Layout.fillWidth: true; wrapMode: Text.Wrap; maximumLineCount: 2; leftPadding: 14 }
                    }
                }
            }
        }
        Card {
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Layout.alignment: Qt.AlignTop
            stagger: 7
            ColumnLayout {
                width: parent.width
                spacing: 10
                SectionTitle { Layout.fillWidth: true; text: i18n.t["dash.incidents"]; icon: "triangle-alert" }
                AText { visible: page.ctl.incidents.count === 0; text: i18n.t["sup.no_incidents"]; mute: true; wrapMode: Text.Wrap; Layout.fillWidth: true }
                Repeater {
                    model: page.ctl.incidents
                    delegate: ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 3
                        RowLayout {
                            Layout.fillWidth: true
                            AText { text: model.kindTitle; weight: Font.DemiBold; size: Theme.fsSmall; color: Theme.tone(model.tone) }
                            Item { Layout.fillWidth: true }
                            AText { text: model.statusTitle; mute: true; size: Theme.fsMicro }
                        }
                        AText { text: model.description; dim: true; size: Theme.fsSmall; Layout.fillWidth: true; wrapMode: Text.Wrap; maximumLineCount: 2 }
                    }
                }
            }
        }
    }

    // Крупная метрика с «досчитывающим» числом.
    component Metric: Card {
        id: metric
        property int idx: 0
        property string glyph: ""
        property string caption: ""
        property real value: 0
        property string total: ""
        property string unit: "int"
        property color tint: Theme.text
        property bool clickable: false
        signal activated()
        Layout.fillWidth: true
        stagger: idx
        hoverable: true
        padding: 16
        ColumnLayout {
            width: parent.width
            spacing: 6
            RowLayout {
                Layout.fillWidth: true
                Rectangle {
                    width: 30; height: 30; radius: 9
                    color: Theme.alpha(metric.tint === Theme.text ? Theme.violet : metric.tint, 0.14)
                    Icon { anchors.centerIn: parent; name: metric.glyph; size: 15; color: metric.tint === Theme.text ? Theme.violetSoft : metric.tint }
                }
                Item { Layout.fillWidth: true }
                Icon { visible: metric.clickable; name: "arrow-up-right"; size: 14; color: Theme.textMute }
            }
            Ticker {
                value: metric.value
                unit: metric.unit
                total: metric.total
                size: 26
                weight: Font.Bold
                color: metric.tint
            }
            AText { text: metric.caption; mute: true; size: Theme.fsSmall; Layout.fillWidth: true }
        }
        MouseArea {
            anchors.fill: parent
            enabled: metric.clickable
            cursorShape: Qt.PointingHandCursor
            onClicked: metric.activated()
        }
    }
}

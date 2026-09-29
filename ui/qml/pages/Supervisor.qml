import QtQuick
import QtQuick.Layouts
import Ao

// Супервайзер: кто проверяет, анонимные сводки, инциденты и решения человека.
Page {
    id: page
    title: i18n.t["sup.title"]
    subtitle: i18n.t["sup.subtitle"]
    icon: "shield-check"
    readonly property var ctl: backend.supervisor
    property string tab: "summaries"

    headerActions: [
        Button {
            variant: "primary"
            iconName: "scroll-text"
            text: i18n.t["sup.make_summary"]
            loading: page.ctl.summarizing
            enabled: backend.workspaceId >= 0 && !backend.running && !page.ctl.summarizing
            onClicked: page.ctl.makeSummary()
        }
    ]

    // Кто сейчас супервайзер.
    Card {
        Layout.fillWidth: true
        padding: 16
        glow: page.ctl.configured
        glowColor: Theme.magenta
        RowLayout {
            width: parent.width
            spacing: 14
            Rectangle {
                width: 42; height: 42; radius: 21
                gradient: Gradient {
                    GradientStop { position: 0; color: page.ctl.configured ? Theme.magenta : Theme.surface3 }
                    GradientStop { position: 1; color: page.ctl.configured ? Theme.violetSoft : Theme.surface2 }
                }
                Icon { anchors.centerIn: parent; name: page.ctl.mode === "local" ? "hard-drive" : "shield-check"; size: 18; color: "white" }
            }
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 2
                AText { text: page.ctl.modelTitle; weight: Font.DemiBold; Layout.fillWidth: true }
                AText {
                    text: page.ctl.configured ? i18n.t["sup.checklist"] : i18n.t["sup.configure_hint"]
                    dim: true
                    size: Theme.fsSmall
                    Layout.fillWidth: true
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                }
            }
            Badge {
                text: page.ctl.mode === "local" ? i18n.t["sup.mode_local"] : i18n.t["sup.mode_api"]
                tone: page.ctl.mode === "local" ? "accent" : "violet"
            }
            Button {
                compact: true
                iconName: "settings"
                text: i18n.t["nav.settings"]
                onClicked: backend.navigate("settings")
            }
        }
    }

    Segmented {
        options: [
            { value: "summaries", title: i18n.t["sup.summaries"] + " · " + page.ctl.summaries.count, icon: "scroll-text" },
            { value: "incidents", title: i18n.t["sup.incidents"] + " · " + page.ctl.incidents.count, icon: "triangle-alert" },
            { value: "decisions", title: i18n.t["sup.approvals"] + " · " + page.ctl.decisions.count, icon: "hand" }
        ]
        value: page.tab
        onPicked: function(v) { page.tab = v }
    }

    // --- сводки ---
    EmptyState {
        visible: page.tab === "summaries" && page.ctl.summaries.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 30
        icon: "scroll-text"
        title: i18n.t["sup.no_summaries_title"]
        text: i18n.t["sup.no_summaries"]
    }
    Repeater {
        model: page.tab === "summaries" ? page.ctl.summaries : null
        delegate: Card {
            Layout.fillWidth: true
            stagger: index
            ColumnLayout {
                width: parent.width
                spacing: 10
                RowLayout {
                    spacing: 10
                    Icon { name: "scroll-text"; size: 15; color: Theme.violetSoft }
                    AText { text: model.when; weight: Font.DemiBold }
                    Badge { text: model.triggerTitle; tone: model.trigger === "final" ? "success" : "violet" }
                    Item { Layout.fillWidth: true }
                    AText { text: i18n.fmt(i18n.t["sup.delivered"], { n: model.recipients }); mute: true; size: Theme.fsSmall }
                    IconButton { iconName: "copy"; size: 28; tip: i18n.t["common.copy"]; onClicked: backend.copyText(model.content) }
                }
                AText {
                    Layout.fillWidth: true
                    text: model.content
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                    dim: true
                    lineHeight: 1.2
                }
            }
        }
    }

    // --- инциденты ---
    EmptyState {
        visible: page.tab === "incidents" && page.ctl.incidents.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 30
        icon: "badge-check"
        title: i18n.t["sup.no_incidents_title"]
        text: i18n.t["sup.no_incidents"]
    }
    Repeater {
        model: page.tab === "incidents" ? page.ctl.incidents : null
        delegate: Card {
            Layout.fillWidth: true
            stagger: index
            padding: 16
            glow: model.status === "escalated"
            glowColor: Theme.warning
            RowLayout {
                width: parent.width
                spacing: 14
                Rectangle {
                    Layout.alignment: Qt.AlignTop
                    width: 34; height: 34; radius: 10
                    color: Theme.alpha(Theme.tone(model.tone), 0.15)
                    Icon { anchors.centerIn: parent; name: model.open ? "triangle-alert" : "circle-check"; size: 16; color: model.open ? Theme.tone(model.tone) : Theme.success }
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 5
                    RowLayout {
                        spacing: 8
                        AText { text: model.kindTitle; weight: Font.DemiBold }
                        Badge { text: model.severityTitle; tone: model.tone }
                        Badge { text: model.statusTitle; tone: model.open ? "warning" : "success" }
                        Item { Layout.fillWidth: true }
                        AText { text: model.when; mute: true; size: Theme.fsSmall }
                    }
                    AText { text: model.description; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone; dim: true }
                    AText {
                        visible: model.resolution !== ""
                        text: "→ " + model.resolution
                        Layout.fillWidth: true
                        wrapMode: Text.Wrap
                        elide: Text.ElideNone
                        mute: true
                        size: Theme.fsSmall
                    }
                }
                Button {
                    Layout.alignment: Qt.AlignTop
                    visible: model.open
                    compact: true
                    iconName: "check"
                    text: i18n.t["sup.resolve"]
                    onClicked: resolver.openFor(model.id, model.description)
                }
            }
        }
    }

    // --- решения ---
    EmptyState {
        visible: page.tab === "decisions" && page.ctl.decisions.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 30
        icon: "hand"
        title: i18n.t["sup.no_approvals_title"]
        text: i18n.t["sup.no_approvals"]
    }
    Repeater {
        model: page.tab === "decisions" ? page.ctl.decisions : null
        delegate: Card {
            Layout.fillWidth: true
            stagger: index
            padding: 16
            RowLayout {
                width: parent.width
                spacing: 14
                Rectangle {
                    Layout.alignment: Qt.AlignTop
                    width: 10; height: 10; radius: 5
                    Layout.topMargin: 5
                    color: Theme.tone(model.tone)
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 4
                    RowLayout {
                        spacing: 8
                        AText { text: model.reasonTitle; weight: Font.DemiBold }
                        Badge { text: model.decisionTitle; tone: model.tone }
                        Item { Layout.fillWidth: true }
                        AText { text: model.when; mute: true; size: Theme.fsSmall }
                    }
                    AText { text: model.question; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone; dim: true }
                    AText {
                        visible: model.comment !== "" || model.agent !== ""
                        text: [model.agent, model.comment].filter(function(x) { return x !== "" }).join(" · ")
                        mute: true
                        size: Theme.fsSmall
                        Layout.fillWidth: true
                        wrapMode: Text.Wrap
                        elide: Text.ElideNone
                    }
                }
            }
        }
    }

    Sheet {
        id: resolver
        property int incidentId: -1
        property string problem: ""
        title: i18n.t["sup.resolve"]
        subtitle: problem
        icon: "badge-check"
        sheetWidth: 520
        function openFor(id, text) { incidentId = id; problem = text; resolution.text = ""; open() }
        TextBox { id: resolution; Layout.fillWidth: true; label: i18n.t["sup.resolution"]; minHeight: 110 }
        footer: [
            Item { Layout.fillWidth: true },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: resolver.close() },
            Button {
                text: i18n.t["sup.resolve"]
                variant: "primary"
                iconName: "check"
                onClicked: { page.ctl.resolveIncident(resolver.incidentId, resolution.text); resolver.close() }
            }
        ]
    }
}

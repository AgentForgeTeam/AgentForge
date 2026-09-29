import QtQuick
import QtQuick.Layouts
import Ao

// Бюджеты: по одной карточке на уровень (проект, задача, агент) с живой
// шкалой расхода и полями лимитов, которые сохраняются по Enter.
Page {
    id: page
    title: i18n.t["bud.title"]
    subtitle: i18n.t["bud.subtitle"]
    icon: "wallet"
    readonly property var ctl: backend.budget

    Component.onCompleted: ctl.refresh()

    headerActions: [
        IconButton { iconName: "refresh-cw"; tip: i18n.t["common.refresh"]; onClicked: page.ctl.refresh() }
    ]

    // Последний алерт бюджета.
    Rectangle {
        visible: page.ctl.alert !== ""
        Layout.fillWidth: true
        radius: Theme.radius
        color: Theme.alpha(Theme.tone(page.ctl.alertTone), 0.1)
        border.color: Theme.alpha(Theme.tone(page.ctl.alertTone), 0.4)
        implicitHeight: alertRow.implicitHeight + 22
        RowLayout {
            id: alertRow
            anchors.fill: parent
            anchors.margins: 11
            spacing: 10
            Icon { name: page.ctl.alertTone === "error" ? "octagon-x" : "triangle-alert"; color: Theme.tone(page.ctl.alertTone) }
            AText { text: page.ctl.alert; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone; color: Theme.tone(page.ctl.alertTone) }
            IconButton { iconName: "x"; size: 26; onClicked: page.ctl.dismissAlert() }
        }
    }

    // Как работает бюджет - коротко, один раз.
    Card {
        Layout.fillWidth: true
        padding: 16
        RowLayout {
            width: parent.width
            spacing: 18
            Hint { glyph: "shield-check"; text: i18n.t["bud.h_before"] }
            Hint { glyph: "hand"; text: i18n.t["bud.h_ask"] }
            Hint { glyph: "database"; text: i18n.t["bud.h_log"] }
        }
    }

    EmptyState {
        visible: page.ctl.model.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 40
        icon: "wallet"
        title: i18n.t["bud.nothing_title"]
        text: i18n.t["bud.nothing"]
    }

    Repeater {
        model: page.ctl.model
        delegate: Card {
            id: row
            Layout.fillWidth: true
            stagger: index
            hoverable: true
            glow: model.exceeded
            glowColor: Theme.danger
            property string error: ""
            readonly property color barColor: model.ratio >= 1 ? Theme.danger : model.ratio >= model.threshold ? Theme.warning : Theme.violet

            function save(tokens, cost, threshold) {
                row.error = page.ctl.save(model.scope, model.scopeId, tokens, cost, threshold)
            }

            ColumnLayout {
                width: parent.width
                spacing: 14

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12
                    Rectangle {
                        width: 38; height: 38; radius: 12
                        color: Theme.alpha(Theme.violet, 0.14)
                        Icon { anchors.centerIn: parent; name: model.icon; size: 17; color: Theme.violetSoft }
                    }
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 1
                        AText { text: model.name; weight: Font.DemiBold; size: Theme.fsH3; Layout.fillWidth: true }
                        AText { text: model.scopeTitle; mute: true; size: Theme.fsSmall }
                    }
                    ColumnLayout {
                        spacing: 1
                        AText { text: model.tokensText + " " + i18n.t["bud.tokens_short"]; mono: true; Layout.alignment: Qt.AlignRight }
                        AText { text: model.costText; mono: true; color: Theme.teal; Layout.alignment: Qt.AlignRight }
                    }
                }

                // Шкала расхода.
                ColumnLayout {
                    visible: model.isSet
                    Layout.fillWidth: true
                    spacing: 6
                    Rectangle {
                        Layout.fillWidth: true
                        height: 10
                        radius: 5
                        color: Theme.surface3
                        Rectangle {
                            height: parent.height
                            radius: 5
                            width: parent.width * Math.min(1, model.ratio)
                            gradient: Gradient {
                                orientation: Gradient.Horizontal
                                GradientStop { position: 0; color: Theme.alpha(row.barColor, 0.7) }
                                GradientStop { position: 1; color: row.barColor }
                            }
                            Behavior on width { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }
                        }
                        // Отметка порога алерта.
                        Rectangle {
                            x: parent.width * model.threshold - 1
                            width: 2
                            height: parent.height + 6
                            y: -3
                            radius: 1
                            color: Theme.warning
                            opacity: 0.8
                        }
                    }
                    AText {
                        text: model.exceeded ? i18n.t["bud.exceeded"] : i18n.fmt(i18n.t["bud.used_pct"], { pct: Math.round(model.ratio * 100) })
                        color: row.barColor
                        size: Theme.fsSmall
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 14
                    Field {
                        id: tokField
                        Layout.fillWidth: true
                        label: i18n.t["bud.token_limit"]
                        placeholder: i18n.t["bud.no_limit"]
                        text: model.tokenLimit
                        icon: "coins"
                        mono: true
                        onAccepted: row.save(tokField.text, costField.text, thr.value)
                        onEditingFinished: if (tokField.text !== model.tokenLimit) row.save(tokField.text, costField.text, thr.value)
                    }
                    Field {
                        id: costField
                        Layout.fillWidth: true
                        label: i18n.t["bud.cost_limit"]
                        placeholder: i18n.t["bud.no_limit"]
                        text: model.costLimit
                        icon: "dollar-sign"
                        mono: true
                        onAccepted: row.save(tokField.text, costField.text, thr.value)
                        onEditingFinished: if (costField.text !== model.costLimit) row.save(tokField.text, costField.text, thr.value)
                    }
                    RangeSlider {
                        id: thr
                        Layout.preferredWidth: 220
                        label: i18n.t["bud.alert_at"]
                        from: 0.1; to: 1; stepSize: 0.05
                        value: model.threshold
                        format: function(v) { return Math.round(v * 100) + "%" }
                        onCommitted: function(v) { if (model.isSet) row.save(tokField.text, costField.text, v) }
                    }
                }
                AText { visible: row.error !== ""; text: row.error; color: Theme.danger; size: Theme.fsSmall }
            }
        }
    }

    component Hint: RowLayout {
        property string glyph: ""
        property string text: ""
        Layout.fillWidth: true
        spacing: 10
        Icon { name: glyph; size: 16; color: Theme.violetSoft; Layout.alignment: Qt.AlignTop }
        AText { text: parent.text; dim: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
    }
}

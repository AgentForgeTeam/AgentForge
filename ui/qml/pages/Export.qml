import QtQuick
import QtQuick.Layouts
import Ao

// Экспорт: формат выбирается плиткой (рекомендованный отмечен и объяснён),
// состав документа — переключателями, путь — полем с кнопкой «Обзор».
Page {
    id: page
    title: i18n.t["exp.title"]
    subtitle: i18n.t["exp.subtitle"]
    icon: "package"
    readonly property var ctl: backend.exporter

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
    }

    ColumnLayout {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        spacing: 18

        // Статистика и рекомендация.
        Card {
            Layout.fillWidth: true
            padding: 16
            RowLayout {
                width: parent.width
                spacing: 12
                Icon { name: page.ctl.nothing ? "inbox" : "wand-sparkles"; size: 18; color: page.ctl.nothing ? Theme.textMute : Theme.violetSoft }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 2
                    AText {
                        text: page.ctl.nothing ? i18n.t["exp.nothing"] : i18n.fmt(i18n.t["exp.auto_hint"], { reason: page.ctl.reason })
                        Layout.fillWidth: true
                        wrapMode: Text.Wrap
                        elide: Text.ElideNone
                    }
                    AText { text: page.ctl.stats; mute: true; size: Theme.fsSmall }
                }
            }
        }

        SectionTitle { Layout.fillWidth: true; text: i18n.t["exp.format"]; icon: "file-type" }
        GridLayout {
            Layout.fillWidth: true
            columns: 4
            columnSpacing: 14
            Repeater {
                model: page.ctl.formats
                delegate: Card {
                    id: fmtCard
                    required property var modelData
                    required property int index
                    readonly property bool chosen: page.ctl.format === modelData.key
                    readonly property bool recommended: page.ctl.recommended === modelData.key
                    Layout.fillWidth: true
                    Layout.preferredHeight: 150
                    hoverable: true
                    glow: chosen
                    stagger: index
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 8
                        RowLayout {
                            Layout.fillWidth: true
                            Rectangle {
                                width: 40; height: 40; radius: 12
                                color: fmtCard.chosen ? Theme.alpha(Theme.violet, 0.3) : Theme.surface3
                                Icon { anchors.centerIn: parent; name: fmtCard.modelData.icon; size: 18; color: fmtCard.chosen ? "white" : Theme.textDim }
                            }
                            Item { Layout.fillWidth: true }
                            Badge { visible: fmtCard.recommended; text: i18n.t["exp.recommended"]; tone: "success"; icon: "sparkles" }
                        }
                        AText { text: fmtCard.modelData.title; weight: Font.DemiBold; size: Theme.fsH3 }
                        AText { text: fmtCard.modelData.hint; dim: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
                    }
                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: page.ctl.setFormat(fmtCard.modelData.key) }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 18

            Card {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop
                ColumnLayout {
                    width: parent.width
                    spacing: 12
                    SectionTitle { Layout.fillWidth: true; text: i18n.t["exp.content"]; icon: "list-checks" }
                    Repeater {
                        model: page.ctl.optionList
                        delegate: Toggle {
                            required property var modelData
                            Layout.fillWidth: true
                            label: modelData.title
                            hint: modelData.key === "files" && page.ctl.format !== "zip" ? i18n.t["exp.files_zip_only"]
                                : modelData.key === "anon" ? i18n.t["exp.opt_anon_hint"] : ""
                            enabled: modelData.key !== "files" || page.ctl.format === "zip"
                            isOn: !!page.ctl.options[modelData.key]
                            onToggled: page.ctl.setOption(modelData.key, checked)
                        }
                    }
                }
            }

            Card {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop
                ColumnLayout {
                    width: parent.width
                    spacing: 14
                    SectionTitle { Layout.fillWidth: true; text: i18n.t["exp.output"]; icon: "folder-open" }
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 10
                        Field {
                            id: pathField
                            Layout.fillWidth: true
                            text: page.ctl.path
                            mono: true
                            icon: "folder"
                            onEditingFinished: page.ctl.setPath(text)
                        }
                        Button { iconName: "folder-open"; text: i18n.t["exp.browse"]; onClicked: page.ctl.browse() }
                    }
                    Button {
                        Layout.fillWidth: true
                        variant: "primary"
                        iconName: "download"
                        text: i18n.t["exp.export"]
                        enabled: page.ctl.canExport && !page.ctl.exporting
                        loading: page.ctl.exporting
                        onClicked: { page.ctl.setPath(pathField.text); page.ctl.exportNow() }
                    }
                    // Результат последнего экспорта.
                    Rectangle {
                        visible: page.ctl.lastPath !== ""
                        Layout.fillWidth: true
                        radius: Theme.radius
                        color: Theme.alpha(Theme.success, 0.08)
                        border.color: Theme.alpha(Theme.success, 0.35)
                        implicitHeight: doneRow.implicitHeight + 20
                        RowLayout {
                            id: doneRow
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 10
                            Icon { name: "circle-check"; color: Theme.success }
                            AText { text: page.ctl.lastInfo; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone; size: Theme.fsSmall }
                            Button { compact: true; iconName: "external-link"; text: i18n.t["exp.open_folder"]; onClicked: page.ctl.openFolder() }
                        }
                    }
                }
            }
        }
    }
}

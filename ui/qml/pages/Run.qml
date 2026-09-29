import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts
import QtQuick.Shapes
import Ao

// Выполнение: управление прогоном, решения человека, живые рассуждения
// агентов, граф подзадач и лента событий.
Page {
    id: page
    title: i18n.t["run.title"]
    subtitle: backend.run.taskTitle !== "" ? backend.run.taskTitle : i18n.t["run.subtitle"]
    icon: "play"
    fill: true
    readonly property var ctl: backend.run

    headerActions: [
        Button {
            visible: !backend.running
            variant: "primary"
            iconName: "play"
            text: i18n.t["run.start"]
            loading: page.ctl.starting
            enabled: page.ctl.canStart && !page.ctl.starting
            onClicked: page.ctl.start()
        },
        Button {
            visible: backend.running
            iconName: backend.paused ? "circle-play" : "circle-pause"
            text: backend.paused ? i18n.t["run.resume"] : i18n.t["run.pause"]
            onClicked: page.ctl.togglePause()
        },
        Button {
            visible: backend.running
            variant: "danger"
            iconName: "square"
            text: i18n.t["run.stop"]
            onClicked: confirm.ask(i18n.t["run.stop"], i18n.t["run.stop_confirm"],
                                   function() { page.ctl.stop() }, true, i18n.t["run.stop"])
        }
    ]

    // --- сводка прогона ------------------------------------------------------
    Card {
        Layout.fillWidth: true
        padding: 16
        RowLayout {
            width: parent.width
            spacing: 22
            ProgressRing {
                size: 64
                thickness: 6
                value: page.ctl.progress
                label: page.ctl.total > 0 ? Math.round(page.ctl.progress * 100) + "%" : "-"
            }
            Kpi { caption: i18n.t["run.k_done"]; value: page.ctl.done + " / " + page.ctl.total; tint: Theme.success }
            Kpi { caption: i18n.t["run.k_review"]; value: page.ctl.review; tint: page.ctl.review ? Theme.violetSoft : Theme.text }
            Kpi { caption: i18n.t["run.k_errors"]; value: page.ctl.errors; tint: page.ctl.errors ? Theme.danger : Theme.text }
            Kpi { caption: i18n.t["run.k_time"]; value: backend.runElapsed !== "" ? backend.runElapsed : "-" }
            Kpi { caption: i18n.t["run.k_tokens"]; value: backend.running ? backend.runTokens : "-" }
            Kpi { caption: i18n.t["run.k_cost"]; value: backend.running ? backend.runCost : "-"; tint: Theme.teal }
            Item { Layout.fillWidth: true }
            // Почему нельзя запустить - сразу видно, без попытки.
            RowLayout {
                visible: !backend.running && page.ctl.blocker !== ""
                spacing: 8
                Icon { name: "info"; size: 15; color: Theme.warning }
                AText { text: page.ctl.blocker; color: Theme.warning; size: Theme.fsSmall; Layout.maximumWidth: 360; wrapMode: Text.Wrap; elide: Text.ElideNone }
            }
        }
    }

    // --- решения человека ------------------------------------------------------
    Repeater {
        model: page.ctl.approvals
        delegate: Card {
            id: ask
            Layout.fillWidth: true
            glow: true
            glowColor: Theme.warning
            padding: 18
            stagger: 0
            property bool expanded: false
            readonly property var opts: model.options
            readonly property int approvalId: model.id

            ColumnLayout {
                width: parent.width
                spacing: 12
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12
                    Rectangle {
                        width: 38; height: 38; radius: 12
                        color: Theme.alpha(Theme.warning, 0.16)
                        Icon { anchors.centerIn: parent; name: model.icon; size: 18; color: Theme.warning }
                    }
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 2
                        RowLayout {
                            spacing: 8
                            AText { text: model.reasonTitle; weight: Font.Bold; color: Theme.warning }
                            AText { visible: model.agent !== ""; text: "· " + model.agent; dim: true }
                        }
                        AText { text: model.question; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone }
                    }
                    Button {
                        visible: model.details !== ""
                        compact: true
                        variant: "ghost"
                        iconName: ask.expanded ? "chevron-up" : "chevron-down"
                        text: ask.expanded ? i18n.t["run.hide_details"] : i18n.t["run.show_details"]
                        onClicked: ask.expanded = !ask.expanded
                    }
                }
                Rectangle {
                    visible: ask.expanded
                    Layout.fillWidth: true
                    radius: Theme.radius
                    color: Theme.input
                    border.color: Theme.border
                    implicitHeight: Math.min(detailsText.implicitHeight + 20, 260)
                    clip: true
                    Flickable {
                        anchors.fill: parent
                        anchors.margins: 10
                        contentHeight: detailsText.implicitHeight
                        T.ScrollBar.vertical: ScrollBar {}
                        AText {
                            id: detailsText
                            width: parent.width
                            text: model.details
                            dim: true
                            size: Theme.fsSmall
                            wrapMode: Text.Wrap
                            elide: Text.ElideNone
                        }
                    }
                }
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10
                    Field {
                        id: comment
                        Layout.fillWidth: true
                        placeholder: i18n.t["run.comment_placeholder"]
                        icon: "message-square-text"
                    }
                    Repeater {
                        model: ask.opts
                        delegate: Button {
                            required property var modelData
                            text: modelData.title
                            variant: modelData.value === "approve" || modelData.value === "extend" ? "primary"
                                   : modelData.value === "abort" ? "danger" : "secondary"
                            iconName: modelData.value === "approve" ? "check"
                                    : modelData.value === "rework" ? "rotate-ccw"
                                    : modelData.value === "skip" ? "skip-forward"
                                    : modelData.value === "extend" ? "trending-up" : "octagon-x"
                            onClicked: page.ctl.decide(ask.approvalId, modelData.value, comment.text)
                        }
                    }
                }
            }
        }
    }

    // --- основная область --------------------------------------------------------
    RowLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        spacing: 18

        // Живые рассуждения агентов.
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 12
            SectionTitle {
                Layout.fillWidth: true
                text: i18n.t["run.live"]
                hint: i18n.t["run.live_hint"]
                icon: "brain"
            }
            GridView {
                id: streams
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                model: page.ctl.streams
                readonly property int cols: Math.max(1, Math.floor(width / 420))
                cellWidth: Math.floor(width / cols)
                cellHeight: Math.max(300, Math.floor(height / Math.ceil(Math.max(1, count) / cols)))
                boundsBehavior: Flickable.StopAtBounds
                T.ScrollBar.vertical: ScrollBar {}
                delegate: Item {
                    width: streams.cellWidth
                    height: streams.cellHeight
                    StreamCard {
                        anchors.fill: parent
                        anchors.rightMargin: 12
                        anchors.bottomMargin: 12
                    }
                }
            }
        }

        // Граф и лента.
        ColumnLayout {
            Layout.preferredWidth: Math.min(460, page.contentWidth * 0.38)
            Layout.fillHeight: true
            spacing: 12

            SectionTitle { Layout.fillWidth: true; text: i18n.t["run.graph"]; icon: "workflow" }
            Card {
                Layout.fillWidth: true
                Layout.preferredHeight: 260
                padding: 0
                Graph { anchors.fill: parent; anchors.margins: 12 }
            }

            SectionTitle {
                Layout.fillWidth: true
                text: i18n.t["run.feed"]
                icon: "activity"
                Segmented {
                    id: feedFilter
                    property string mode: "all"
                    options: [{ value: "all", title: i18n.t["run.f_all"] }, { value: "key", title: i18n.t["run.f_key"] },
                              { value: "error", title: i18n.t["run.f_errors"] }]
                    value: mode
                    onPicked: function(v) { mode = v }
                }
                IconButton { iconName: "eraser"; tip: i18n.t["run.clear_feed"]; onClicked: page.ctl.clearFeed() }
            }
            Card {
                Layout.fillWidth: true
                Layout.fillHeight: true
                padding: 6
                ListView {
                    id: feed
                    anchors.fill: parent
                    clip: true
                    model: page.ctl.feed
                    spacing: 0
                    boundsBehavior: Flickable.StopAtBounds
                    T.ScrollBar.vertical: ScrollBar {}
                    property bool follow: true
                    onCountChanged: if (follow) Qt.callLater(positionViewAtEnd)
                    onMovementEnded: follow = atYEnd
                    add: Transition { NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.normal } }
                    delegate: Item {
                        readonly property bool shown: feedFilter.mode === "all"
                                                   || (feedFilter.mode === "error" && model.tone === "error")
                                                   || (feedFilter.mode === "key" && model.tone !== "muted")
                        width: feed.width
                        height: shown ? row.implicitHeight + 10 : 0
                        visible: shown
                        RowLayout {
                            id: row
                            anchors { left: parent.left; right: parent.right; verticalCenter: parent.verticalCenter; leftMargin: 8; rightMargin: 8 }
                            spacing: 8
                            AText { text: model.time; mono: true; size: Theme.fsMicro; mute: true; Layout.alignment: Qt.AlignTop; topPadding: 2 }
                            Rectangle { width: 6; height: 6; radius: 3; color: Theme.tone(model.tone); Layout.alignment: Qt.AlignTop; Layout.topMargin: 6 }
                            AText {
                                Layout.fillWidth: true
                                text: "<b>" + model.agent.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</b>  "
                                      + model.message.replace(/&/g, "&amp;").replace(/</g, "&lt;")
                                textFormat: Text.StyledText
                                size: Theme.fsSmall
                                color: model.tone === "muted" ? Theme.textMute : Theme.textDim
                                wrapMode: Text.Wrap
                                elide: Text.ElideNone
                            }
                        }
                    }
                    AText {
                        anchors.centerIn: parent
                        visible: feed.count === 0
                        text: i18n.t["run.feed_empty"]
                        mute: true
                    }
                }
            }
        }
    }

    Confirm {
        id: confirm
        confirmText: i18n.t["run.stop"]
        cancelText: i18n.t["common.cancel"]
    }

    // --- компоненты страницы -------------------------------------------------------
    component Kpi: ColumnLayout {
        property string caption: ""
        property var value: ""
        property color tint: Theme.text
        spacing: 2
        AText { text: value; size: Theme.fsH2; weight: Font.Bold; color: tint; mono: true }
        AText { text: caption; size: Theme.fsMicro; mute: true }
    }

    // Карточка агента с живым потоком рассуждения.
    component StreamCard: Card {
        id: sc
        padding: 0
        glow: model.live
        glowColor: model.isSupervisor ? Theme.magenta : Theme.cyan
        readonly property string phaseTitle: model.phase === "tool" ? i18n.t["run.ph_tool"]
                                            : model.phase === "thinking" ? i18n.t["run.ph_thinking"]
                                            : model.phase === "review" ? i18n.t["run.ph_review"]
                                            : model.phase === "done" ? i18n.t["run.ph_done"]
                                            : model.phase === "error" ? i18n.t["run.ph_error"] : i18n.t["run.ph_idle"]

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 14
            spacing: 10

            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                Item {
                    width: 36; height: 36
                    Rectangle {
                        anchors.fill: parent
                        radius: 18
                        gradient: Gradient {
                            GradientStop { position: 0; color: model.isSupervisor ? Theme.magenta : Theme.violet }
                            GradientStop { position: 1; color: model.isSupervisor ? Theme.violetSoft : Theme.cyan }
                        }
                        Icon { anchors.centerIn: parent; name: model.icon; size: 16; color: "white" }
                    }
                    // Вращающееся кольцо вокруг аватара, пока агент работает.
                    Rectangle {
                        anchors.centerIn: parent
                        width: 44; height: 44; radius: 22
                        color: "transparent"
                        border.width: 2
                        border.color: Theme.alpha(sc.glowColor, 0.5)
                        visible: model.live
                        opacity: 0.8
                        SequentialAnimation on scale {
                            running: model.live && Theme.rich
                            loops: Animation.Infinite
                            NumberAnimation { from: 0.92; to: 1.08; duration: 900; easing.type: Easing.InOutSine }
                            NumberAnimation { from: 1.08; to: 0.92; duration: 900; easing.type: Easing.InOutSine }
                        }
                    }
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 1
                    RowLayout {
                        spacing: 6
                        AText { text: model.name; weight: Font.DemiBold; Layout.maximumWidth: 170 }
                        AText { text: model.modelName; mono: true; size: Theme.fsMicro; mute: true; Layout.maximumWidth: 150 }
                    }
                    AText {
                        text: model.subtask !== "" ? model.subtask : i18n.t["run.waiting"]
                        dim: model.subtask !== ""
                        mute: model.subtask === ""
                        size: Theme.fsSmall
                        Layout.fillWidth: true
                    }
                }
                Badge {
                    text: sc.phaseTitle
                    tone: model.phase === "tool" ? "accent" : model.phase === "done" ? "success"
                        : model.phase === "error" ? "error" : model.phase === "idle" ? "muted" : "violet"
                    icon: model.phase === "tool" ? "zap" : model.phase === "done" ? "check" : ""
                }
                IconButton {
                    iconName: "copy"
                    size: 28
                    tip: i18n.t["run.copy_stream"]
                    onClicked: backend.copyText(page.ctl.fullText(model.id))
                }
            }

            // Шаги: точки заполняются по мере продвижения по ReAct-циклу.
            RowLayout {
                visible: model.maxSteps > 0
                spacing: 4
                Repeater {
                    model: sc.stepsCount
                    delegate: Rectangle {
                        required property int index
                        width: 16; height: 4; radius: 2
                        color: index < sc.currentStep ? (index === sc.currentStep - 1 && sc.isLive ? Theme.cyan : Theme.violet) : Theme.surface3
                        Behavior on color { ColorAnimation { duration: Theme.normal } }
                    }
                }
                AText {
                    visible: sc.currentStep > 0
                    text: i18n.fmt(i18n.t["run.step_of"], { n: sc.currentStep, m: sc.stepsCount })
                    size: Theme.fsMicro
                    mute: true
                    leftPadding: 6
                }
                Item { Layout.fillWidth: true }
                TypingDots { visible: sc.isLive && model.phase === "thinking" }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: Theme.radius
                color: Theme.alpha(Theme.bg, 0.55)
                border.color: Theme.border
                clip: true

                Flickable {
                    id: flow
                    anchors.fill: parent
                    anchors.margins: 12
                    contentHeight: streamText.implicitHeight
                    boundsBehavior: Flickable.StopAtBounds
                    T.ScrollBar.vertical: ScrollBar {}
                    property bool follow: true
                    onContentHeightChanged: if (follow && contentHeight > height) contentY = contentHeight - height
                    onMovementEnded: follow = contentY >= contentHeight - height - 8
                    Text {
                        id: streamText
                        width: flow.width - 8
                        text: model.html
                        textFormat: Text.StyledText
                        wrapMode: Text.Wrap
                        color: Theme.text
                        font.family: Theme.monoFamily
                        font.pixelSize: 13
                        lineHeight: 1.15
                        renderType: Text.QtRendering
                    }
                }
                AText {
                    anchors.centerIn: parent
                    visible: model.html === ""
                    text: model.isSupervisor ? i18n.t["run.sup_empty"] : i18n.t["run.stream_empty"]
                    mute: true
                    size: Theme.fsSmall
                }
                Button {
                    visible: !flow.follow
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.margins: 10
                    compact: true
                    iconName: "arrow-down"
                    text: i18n.t["run.to_latest"]
                    onClicked: { flow.follow = true; flow.contentY = Math.max(0, flow.contentHeight - flow.height) }
                }
            }
        }
        readonly property int stepsCount: Math.min(model.maxSteps, 20)
        readonly property int currentStep: Math.min(model.step, stepsCount)
        readonly property bool isLive: model.live
    }

    // «Печатает…» - три прыгающие точки.
    component TypingDots: Row {
        spacing: 4
        Repeater {
            model: 3
            delegate: Rectangle {
                required property int index
                width: 5; height: 5; radius: 2.5
                color: Theme.cyan
                SequentialAnimation on opacity {
                    running: Theme.motion > 0
                    loops: Animation.Infinite
                    PauseAnimation { duration: index * 160 }
                    NumberAnimation { from: 0.25; to: 1; duration: 320 }
                    NumberAnimation { from: 1; to: 0.25; duration: 320 }
                    PauseAnimation { duration: (2 - index) * 160 }
                }
            }
        }
    }

    // Граф подзадач: слои по зависимостям, рёбра «текут», пока идёт работа.
    component Graph: Flickable {
        id: graph
        // Узлы сужаются, чтобы все слои графа помещались в колонку без прокрутки.
        readonly property int nodeW: page.ctl.levels > 0
            ? Math.max(118, Math.min(170, Math.floor((width - gapX * (page.ctl.levels - 1)) / page.ctl.levels)))
            : 170
        readonly property int nodeH: 54
        readonly property int gapX: 34
        readonly property int gapY: 12
        clip: true
        contentWidth: Math.max(width, page.ctl.levels * (nodeW + gapX) - gapX)
        contentHeight: Math.max(height, page.ctl.maxRows * (nodeH + gapY) - gapY)
        boundsBehavior: Flickable.StopAtBounds
        T.ScrollBar.vertical: ScrollBar {}
        T.ScrollBar.horizontal: ScrollBar {}

        Repeater {
            model: page.ctl.edges
            delegate: Shape {
                id: edge
                readonly property real x1: model.fromLevel * (graph.nodeW + graph.gapX) + graph.nodeW
                readonly property real y1: model.fromRow * (graph.nodeH + graph.gapY) + graph.nodeH / 2
                readonly property real x2: model.toLevel * (graph.nodeW + graph.gapX)
                readonly property real y2: model.toRow * (graph.nodeH + graph.gapY) + graph.nodeH / 2
                anchors.fill: parent
                preferredRendererType: Shape.CurveRenderer
                ShapePath {
                    id: path
                    strokeWidth: model.state === "active" ? 2 : 1.5
                    strokeColor: model.state === "active" ? Theme.cyan
                               : model.state === "done" ? Theme.alpha(Theme.success, 0.6) : Theme.borderStrong
                    fillColor: "transparent"
                    strokeStyle: model.state === "active" ? ShapePath.DashLine : ShapePath.SolidLine
                    dashPattern: [4, 3]
                    startX: edge.x1; startY: edge.y1
                    PathCubic {
                        x: edge.x2; y: edge.y2
                        control1X: edge.x1 + graph.gapX * 0.6; control1Y: edge.y1
                        control2X: edge.x2 - graph.gapX * 0.6; control2Y: edge.y2
                    }
                    NumberAnimation on dashOffset {
                        running: model.state === "active" && Theme.motion > 0
                        from: 7; to: 0; duration: 500; loops: Animation.Infinite
                    }
                }
            }
        }

        Repeater {
            model: page.ctl.nodes
            delegate: Rectangle {
                id: node
                x: model.level * (graph.nodeW + graph.gapX)
                y: model.row * (graph.nodeH + graph.gapY)
                width: graph.nodeW
                height: graph.nodeH
                radius: Theme.radius
                color: Theme.alpha(Theme.statusColor(model.status), 0.10)
                border.width: model.status === "running" ? 2 : 1
                border.color: Theme.alpha(Theme.statusColor(model.status), model.status === "idle" ? 0.35 : 0.8)
                Behavior on color { ColorAnimation { duration: Theme.normal } }
                Behavior on x { NumberAnimation { duration: Theme.slow; easing.type: Easing.OutCubic } }
                Behavior on y { NumberAnimation { duration: Theme.slow; easing.type: Easing.OutCubic } }
                scale: model.status === "done" ? 1 : 1
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 2
                    RowLayout {
                        spacing: 6
                        StatusDot { status: model.status; size: 7 }
                        AText { text: model.title; size: Theme.fsSmall; weight: Font.DemiBold; Layout.fillWidth: true }
                        Icon { visible: model.status === "done"; name: "check"; size: 13; color: Theme.success }
                    }
                    AText { text: model.agentName; size: Theme.fsMicro; mute: true; Layout.fillWidth: true }
                }
                Tip { text: model.title + " · " + model.statusTitle; shown: nodeHover.hovered }
                HoverHandler { id: nodeHover }
                // «Щелчок» при завершении подзадачи.
                SequentialAnimation {
                    id: pop
                    NumberAnimation { target: node; property: "scale"; to: 1.08; duration: 120; easing.type: Easing.OutQuad }
                    NumberAnimation { target: node; property: "scale"; to: 1.0; duration: 220; easing.type: Easing.OutBack }
                }
                property string lastStatus: model.status
                onLastStatusChanged: if (lastStatus === "done" && Theme.rich) pop.restart()
            }
        }

        AText {
            anchors.centerIn: parent
            visible: page.ctl.nodes.count === 0
            text: i18n.t["run.graph_empty"]
            mute: true
            size: Theme.fsSmall
        }
    }
}

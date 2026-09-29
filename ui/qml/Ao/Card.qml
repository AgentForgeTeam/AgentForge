import QtQuick

// «Стеклянная» карточка. hoverable: при наведении приподнимается и
// подсвечивает контур; glow: постоянное свечение (активный элемент).
Rectangle {
    id: card
    default property alias content: body.data
    property int padding: Theme.pad
    property bool hoverable: false
    property bool glow: false
    property color glowColor: Theme.violet
    property alias hovered: hover.hovered
    readonly property bool lifted: hoverable && hover.hovered
    // порядковый номер для каскадного появления списка; -1 — без анимации
    property int stagger: -1
    property real enter: stagger >= 0 && Theme.motion > 0 ? 0 : 1

    radius: Theme.radiusL
    color: lifted ? Theme.surfaceHover : Theme.surface
    border.width: 1
    border.color: glow ? Theme.alpha(glowColor, 0.55) : (lifted ? Theme.borderStrong : Theme.border)
    implicitHeight: body.childrenRect.height + padding * 2
    opacity: enter
    transform: Translate {
        y: (card.lifted && Theme.rich ? -2 : 0) + (1 - card.enter) * 16
        Behavior on y { enabled: card.enter >= 1; NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
    }
    SequentialAnimation {
        running: card.stagger >= 0 && card.enter < 1
        PauseAnimation { duration: Theme.rich ? Math.max(0, Math.min(card.stagger, 12)) * 45 : 0 }
        NumberAnimation { target: card; property: "enter"; to: 1; duration: Theme.slow; easing.type: Easing.OutCubic }
    }
    Behavior on color { ColorAnimation { duration: Theme.normal } }
    Behavior on border.color { ColorAnimation { duration: Theme.normal } }

    // Мягкий блик по верхней кромке — ощущение объёма стекла.
    Rectangle {
        anchors { left: parent.left; right: parent.right; top: parent.top; margins: 1 }
        height: parent.radius * 2
        radius: parent.radius
        opacity: 0.55
        gradient: Gradient {
            GradientStop { position: 0; color: Qt.rgba(1, 1, 1, 0.045) }
            GradientStop { position: 1; color: "transparent" }
        }
    }
    // Свечение вокруг активной карточки.
    Rectangle {
        anchors.fill: parent
        anchors.margins: -4
        radius: parent.radius + 4
        color: "transparent"
        border.width: 4
        border.color: Theme.alpha(card.glowColor, 0.12)
        visible: card.glow
    }

    HoverHandler { id: hover; enabled: card.hoverable }

    Item {
        id: body
        anchors.fill: parent
        anchors.margins: card.padding
    }
}

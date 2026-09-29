import QtQuick

// Кривая нарастающего итога: градиентная заливка, «прорисовка» слева
// направо при обновлении и перекрестие с подсказкой при наведении.
Item {
    id: root
    property var points: []          // [{label, value}]
    property string unit: "tokens"   // tokens | usd
    property color lineColor: Theme.violetSoft
    property color fillColor: Theme.violet
    property string emptyText: ""
    property real reveal: 1
    property int hoverIndex: -1

    readonly property real maxValue: {
        var m = 0
        for (var i = 0; i < points.length; ++i) m = Math.max(m, points[i].value)
        return m > 0 ? m * 1.12 : 1
    }
    readonly property int padL: 8
    readonly property int padB: 18

    function fmt(v) {
        if (unit === "usd") return v >= 1 ? "$" + v.toFixed(2) : "$" + v.toFixed(v >= 0.01 ? 3 : 4)
        if (v >= 1e6) return (v / 1e6).toFixed(2) + "M"
        if (v >= 1e4) return (v / 1e3).toFixed(1) + "k"
        return Math.round(v).toString()
    }
    function px(i) { return padL + (points.length > 1 ? i / (points.length - 1) : 0.5) * (width - padL * 2) }
    function py(v) { return (height - padB) - (v / maxValue) * (height - padB - 10) }

    onPointsChanged: {
        canvas.requestPaint()
        if (Theme.rich && points.length > 1) { reveal = 0; revealAnim.restart() }
    }
    onRevealChanged: canvas.requestPaint()
    onWidthChanged: canvas.requestPaint()
    onHeightChanged: canvas.requestPaint()
    NumberAnimation { id: revealAnim; target: root; property: "reveal"; from: 0; to: 1; duration: 900; easing.type: Easing.OutCubic }

    Canvas {
        id: canvas
        anchors.fill: parent
        renderTarget: Canvas.FramebufferObject
        onPaint: {
            var ctx = getContext("2d")
            ctx.reset()
            var n = root.points.length
            // Сетка
            ctx.strokeStyle = Qt.rgba(1, 1, 1, 0.05)
            ctx.lineWidth = 1
            for (var g = 0; g <= 3; ++g) {
                var gy = root.py(root.maxValue / 1.12 * g / 3)
                ctx.beginPath(); ctx.moveTo(root.padL, gy); ctx.lineTo(width - root.padL, gy); ctx.stroke()
            }
            if (n < 2) return
            var limitX = root.padL + (width - root.padL * 2) * root.reveal
            ctx.save()
            ctx.beginPath()
            ctx.rect(0, 0, limitX + 1, height)
            ctx.clip()
            // Заливка
            var grad = ctx.createLinearGradient(0, 0, 0, height - root.padB)
            grad.addColorStop(0, Qt.rgba(root.fillColor.r, root.fillColor.g, root.fillColor.b, 0.35))
            grad.addColorStop(1, Qt.rgba(root.fillColor.r, root.fillColor.g, root.fillColor.b, 0.0))
            ctx.beginPath()
            ctx.moveTo(root.px(0), height - root.padB)
            for (var i = 0; i < n; ++i) ctx.lineTo(root.px(i), root.py(root.points[i].value))
            ctx.lineTo(root.px(n - 1), height - root.padB)
            ctx.closePath()
            ctx.fillStyle = grad
            ctx.fill()
            // Линия
            ctx.beginPath()
            for (var j = 0; j < n; ++j) {
                var x = root.px(j), y = root.py(root.points[j].value)
                if (j === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y)
            }
            ctx.strokeStyle = root.lineColor
            ctx.lineWidth = 2.2
            ctx.lineJoin = "round"
            ctx.stroke()
            ctx.restore()
        }
    }

    // Подписи оси: первая и последняя метка времени, максимум слева сверху.
    AText {
        visible: root.points.length > 1
        text: root.fmt(root.maxValue / 1.12)
        mute: true; size: Theme.fsMicro; mono: true
        x: root.padL + 2; y: 0
    }
    AText {
        visible: root.points.length > 1
        text: root.points.length ? root.points[0].label : ""
        mute: true; size: Theme.fsMicro
        x: root.padL; anchors.bottom: parent.bottom
    }
    AText {
        visible: root.points.length > 1
        text: root.points.length ? root.points[root.points.length - 1].label : ""
        mute: true; size: Theme.fsMicro
        anchors.right: parent.right; anchors.rightMargin: root.padL; anchors.bottom: parent.bottom
    }

    // Перекрестие и подсказка.
    Rectangle {
        visible: root.hoverIndex >= 0
        x: root.hoverIndex >= 0 ? root.px(root.hoverIndex) : 0
        y: 0; width: 1; height: root.height - root.padB
        color: Theme.alpha(Theme.text, 0.18)
    }
    Rectangle {
        visible: root.hoverIndex >= 0
        width: 10; height: 10; radius: 5
        color: root.lineColor
        border.color: Theme.bg; border.width: 2
        x: root.hoverIndex >= 0 ? root.px(root.hoverIndex) - 5 : 0
        y: root.hoverIndex >= 0 ? root.py(root.points[root.hoverIndex].value) - 5 : 0
    }
    Rectangle {
        visible: root.hoverIndex >= 0
        radius: Theme.radiusS
        color: Theme.surface3
        border.color: Theme.borderStrong
        width: tipText.implicitWidth + 16
        height: tipText.implicitHeight + 10
        x: root.hoverIndex >= 0 ? Math.min(Math.max(0, root.px(root.hoverIndex) - width / 2), root.width - width) : 0
        y: 4
        AText {
            id: tipText
            anchors.centerIn: parent
            size: Theme.fsSmall
            text: root.hoverIndex >= 0 ? root.points[root.hoverIndex].label + "  ·  " + root.fmt(root.points[root.hoverIndex].value) : ""
        }
    }
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onPositionChanged: function(mouse) {
            var n = root.points.length
            if (n < 2) { root.hoverIndex = -1; return }
            var t = (mouse.x - root.padL) / (root.width - root.padL * 2)
            root.hoverIndex = Math.max(0, Math.min(n - 1, Math.round(t * (n - 1))))
        }
        onExited: root.hoverIndex = -1
    }

    AText {
        anchors.centerIn: parent
        visible: root.points.length < 2
        text: root.emptyText
        mute: true
    }
}

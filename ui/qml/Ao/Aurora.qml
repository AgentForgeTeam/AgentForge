import QtQuick
import QtQuick.Shapes

// Живой фон: крупные размытые «сияния» фиолетового, бирюзового и голубого
// медленно дрейфуют под интерфейсом. На сдержанном уровне движения замирают,
// оставаясь мягким градиентом; при выключенных анимациях — неподвижны.
Item {
    id: root
    property real intensity: 1.0
    clip: true

    Rectangle { anchors.fill: parent; color: Theme.bg }

    component Glow: Shape {
        id: glow
        property color tint: Theme.violet
        property real strength: 0.5
        property int radius: 420
        property real driftX: 120
        property real driftY: 80
        property int period: 22000
        property real baseX: 0
        property real baseY: 0
        width: radius * 2
        height: radius * 2
        x: baseX - radius
        y: baseY - radius
        preferredRendererType: Shape.GeometryRenderer
        opacity: root.intensity
        ShapePath {
            strokeColor: "transparent"
            fillGradient: RadialGradient {
                centerX: glow.radius; centerY: glow.radius; centerRadius: glow.radius
                focalX: glow.radius; focalY: glow.radius
                GradientStop { position: 0.0; color: Qt.rgba(glow.tint.r, glow.tint.g, glow.tint.b, glow.strength) }
                GradientStop { position: 0.45; color: Qt.rgba(glow.tint.r, glow.tint.g, glow.tint.b, glow.strength * 0.35) }
                GradientStop { position: 1.0; color: "transparent" }
            }
            PathAngleArc {
                centerX: glow.radius; centerY: glow.radius
                radiusX: glow.radius; radiusY: glow.radius
                startAngle: 0; sweepAngle: 360
            }
        }
        transform: Translate { id: shift }
        SequentialAnimation {
            running: Theme.rich && root.visible
            loops: Animation.Infinite
            ParallelAnimation {
                NumberAnimation { target: shift; property: "x"; to: glow.driftX; duration: glow.period; easing.type: Easing.InOutSine }
                NumberAnimation { target: shift; property: "y"; to: glow.driftY; duration: glow.period; easing.type: Easing.InOutSine }
            }
            ParallelAnimation {
                NumberAnimation { target: shift; property: "x"; to: -glow.driftX * 0.6; duration: glow.period * 1.1; easing.type: Easing.InOutSine }
                NumberAnimation { target: shift; property: "y"; to: glow.driftY * 0.4; duration: glow.period * 1.1; easing.type: Easing.InOutSine }
            }
            ParallelAnimation {
                NumberAnimation { target: shift; property: "x"; to: 0; duration: glow.period; easing.type: Easing.InOutSine }
                NumberAnimation { target: shift; property: "y"; to: 0; duration: glow.period; easing.type: Easing.InOutSine }
            }
        }
    }

    Glow { tint: Theme.violet; strength: 0.34; radius: 520; baseX: root.width * 0.18; baseY: root.height * 0.10; driftX: 160; driftY: 120; period: 26000 }
    Glow { tint: Theme.teal; strength: 0.20; radius: 460; baseX: root.width * 0.92; baseY: root.height * 0.22; driftX: -140; driftY: 150; period: 30000 }
    Glow { tint: Theme.cyan; strength: 0.14; radius: 420; baseX: root.width * 0.70; baseY: root.height * 0.98; driftX: -170; driftY: -90; period: 34000 }
    Glow { tint: Theme.magenta; strength: 0.12; radius: 380; baseX: root.width * 0.05; baseY: root.height * 0.95; driftX: 120; driftY: -110; period: 38000 }

    // Лёгкая виньетка, чтобы края не спорили с контентом.
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: Theme.alpha(Theme.bg, 0.0) }
            GradientStop { position: 0.75; color: Theme.alpha(Theme.bg, 0.25) }
            GradientStop { position: 1.0; color: Theme.alpha(Theme.bg, 0.7) }
        }
    }
}

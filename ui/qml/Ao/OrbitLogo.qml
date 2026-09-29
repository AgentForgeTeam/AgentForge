import QtQuick
import QtQuick.Shapes

// Знак приложения: центральный узел-«оркестратор» и спутники-агенты на
// орбитах, связанные с центром. Вращение — только при полном движении.
Item {
    id: root
    property int size: 40
    property bool animated: true
    property real speed: 1.0
    implicitWidth: size
    implicitHeight: size

    readonly property real r1: size * 0.30
    readonly property real r2: size * 0.44

    Shape {
        anchors.fill: parent
        preferredRendererType: Shape.CurveRenderer
        ShapePath {
            strokeColor: Theme.alpha(Theme.violetSoft, 0.28)
            strokeWidth: Math.max(1, root.size / 48)
            fillColor: "transparent"
            strokeStyle: ShapePath.DashLine
            dashPattern: [2, 3]
            PathAngleArc { centerX: root.size / 2; centerY: root.size / 2; radiusX: root.r1; radiusY: root.r1; startAngle: 0; sweepAngle: 360 }
        }
        ShapePath {
            strokeColor: Theme.alpha(Theme.cyan, 0.22)
            strokeWidth: Math.max(1, root.size / 48)
            fillColor: "transparent"
            PathAngleArc { centerX: root.size / 2; centerY: root.size / 2; radiusX: root.r2; radiusY: root.r2; startAngle: 0; sweepAngle: 360 }
        }
    }

    // Центральный узел с градиентом.
    Rectangle {
        anchors.centerIn: parent
        width: root.size * 0.30; height: width; radius: width / 2
        gradient: Gradient {
            GradientStop { position: 0; color: Theme.violetSoft }
            GradientStop { position: 1; color: Theme.indigo }
        }
        Rectangle {
            anchors.centerIn: parent
            width: parent.width * 1.9; height: width; radius: width / 2
            color: "transparent"
            border.width: Math.max(1, root.size / 40)
            border.color: Theme.alpha(Theme.violet, 0.25)
        }
    }

    component Satellite: Item {
        id: sat
        property real orbit: root.r1
        property real phase: 0
        property color tint: Theme.teal
        property real dot: root.size * 0.12
        property int period: 9000
        anchors.fill: parent
        rotation: phase
        Rectangle {
            width: sat.dot; height: sat.dot; radius: sat.dot / 2
            color: sat.tint
            x: root.size / 2 + sat.orbit - sat.dot / 2
            y: root.size / 2 - sat.dot / 2
        }
        NumberAnimation on rotation {
            from: sat.phase; to: sat.phase + 360
            duration: sat.period / root.speed
            loops: Animation.Infinite
            running: root.animated && Theme.rich && root.visible
        }
    }

    Satellite { orbit: root.r1; phase: 20; tint: Theme.teal; period: 7000 }
    Satellite { orbit: root.r2; phase: 150; tint: Theme.cyan; period: 11000; dot: root.size * 0.10 }
    Satellite { orbit: root.r2; phase: 270; tint: Theme.magenta; period: 13000; dot: root.size * 0.09 }
}

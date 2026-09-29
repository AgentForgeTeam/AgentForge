import QtQuick
import QtQuick.Shapes

// Индикатор ожидания: вращающаяся дуга с градиентным хвостом.
Item {
    id: root
    property int size: 18
    property color color: Theme.violetSoft
    property real stroke: Math.max(2, size / 8)
    implicitWidth: size
    implicitHeight: size

    Shape {
        id: arc
        anchors.fill: parent
        preferredRendererType: Shape.CurveRenderer
        ShapePath {
            strokeWidth: root.stroke
            strokeColor: root.color
            fillColor: "transparent"
            capStyle: ShapePath.RoundCap
            PathAngleArc {
                centerX: root.size / 2; centerY: root.size / 2
                radiusX: root.size / 2 - root.stroke; radiusY: root.size / 2 - root.stroke
                startAngle: 0; sweepAngle: 270
            }
        }
        RotationAnimator on rotation {
            from: 0; to: 360
            duration: 900
            loops: Animation.Infinite
            running: root.visible
        }
    }
}

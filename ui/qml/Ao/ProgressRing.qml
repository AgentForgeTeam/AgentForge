import QtQuick
import QtQuick.Shapes

// Кольцевой индикатор прогресса: дуга плавно дорастает до значения,
// а её цвет по пути переходит от фиолетового к сине-зелёному.
Item {
    id: root
    property real value: 0          // 0..1
    property int size: 72
    property real thickness: 7
    property string label: ""
    property string caption: ""
    property color from: Theme.violet
    property color to: Theme.teal
    property real shown: value
    implicitWidth: size
    implicitHeight: size
    Behavior on shown { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }

    function mix(a, b, t) {
        t = Math.max(0, Math.min(1, t))
        return Qt.rgba(a.r + (b.r - a.r) * t, a.g + (b.g - a.g) * t, a.b + (b.b - a.b) * t, 1)
    }

    Shape {
        anchors.fill: parent
        preferredRendererType: Shape.CurveRenderer
        ShapePath {
            strokeWidth: root.thickness
            strokeColor: Theme.surface3
            fillColor: "transparent"
            PathAngleArc {
                centerX: root.size / 2; centerY: root.size / 2
                radiusX: (root.size - root.thickness) / 2; radiusY: (root.size - root.thickness) / 2
                startAngle: 0; sweepAngle: 360
            }
        }
        ShapePath {
            strokeWidth: root.thickness
            fillColor: "transparent"
            capStyle: ShapePath.RoundCap
            strokeColor: root.shown > 0.002 ? root.mix(root.from, root.to, root.shown) : "transparent"
            PathAngleArc {
                centerX: root.size / 2; centerY: root.size / 2
                radiusX: (root.size - root.thickness) / 2; radiusY: (root.size - root.thickness) / 2
                startAngle: -90; sweepAngle: Math.max(0.01, Math.min(root.shown, 1)) * 360
            }
        }
    }

    Column {
        anchors.centerIn: parent
        spacing: 0
        AText {
            anchors.horizontalCenter: parent.horizontalCenter
            text: root.label
            size: root.size > 80 ? Theme.fsH2 : Theme.fsBody
            weight: Font.Bold
        }
        AText {
            visible: root.caption !== ""
            anchors.horizontalCenter: parent.horizontalCenter
            text: root.caption
            size: Theme.fsMicro
            mute: true
        }
    }
}

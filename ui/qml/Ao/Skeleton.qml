import QtQuick

// Заглушка загрузки с бегущим отблеском.
Rectangle {
    id: root
    radius: Theme.radiusS
    color: Theme.surface2
    clip: true
    Rectangle {
        id: sweep
        width: root.width * 0.5
        height: root.height
        x: -width
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0; color: "transparent" }
            GradientStop { position: 0.5; color: Qt.rgba(1, 1, 1, 0.06) }
            GradientStop { position: 1; color: "transparent" }
        }
        NumberAnimation on x {
            from: -sweep.width; to: root.width
            duration: 1300
            loops: Animation.Infinite
            running: root.visible && Theme.motion > 0
        }
    }
}

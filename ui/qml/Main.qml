import QtQuick
import QtQuick.Controls.Basic as T
import Ao

// Главное окно: живой фон, экран входа или оболочка приложения, уведомления.
T.ApplicationWindow {
    id: window
    width: 1440
    height: 900
    minimumWidth: 1180
    minimumHeight: 720
    visible: true
    color: Theme.bg
    title: backend.loggedIn ? backend.appName + " · " + backend.username : backend.appName
    font.family: Theme.fontFamily

    Component.onCompleted: {
        Theme.fontFamily = fonts.sans
        Theme.monoFamily = fonts.mono
        Theme.iconFamily = fonts.icons
        Theme.motion = Qt.binding(function() { return backend.motionLevel })
    }

    Aurora {
        anchors.fill: parent
        intensity: backend.loggedIn ? 0.75 : 1.0
        Behavior on intensity { NumberAnimation { duration: Theme.slow } }
    }

    // Экран входа и оболочка сменяют друг друга плавным «растворением».
    Loader {
        id: loginLoader
        anchors.fill: parent
        active: opacity > 0
        opacity: backend.loggedIn ? 0 : 1
        visible: opacity > 0
        source: "Login.qml"
        Behavior on opacity { NumberAnimation { duration: Theme.slow; easing.type: Easing.InOutQuad } }
    }
    Loader {
        id: shellLoader
        anchors.fill: parent
        active: backend.loggedIn
        opacity: backend.loggedIn ? 1 : 0
        visible: opacity > 0
        source: "Shell.qml"
        Behavior on opacity { NumberAnimation { duration: Theme.slow; easing.type: Easing.InOutQuad } }
        transform: Scale {
            origin.x: shellLoader.width / 2; origin.y: shellLoader.height / 2
            xScale: backend.loggedIn ? 1 : 0.985; yScale: xScale
            Behavior on xScale { NumberAnimation { duration: Theme.slow; easing.type: Easing.OutCubic } }
        }
    }

    Toasts {
        id: toasts
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: 18
        anchors.rightMargin: 18
        height: parent.height - 36
        z: 1000
    }

    Connections {
        target: backend
        function onToast(kind, title, message) { toasts.show(kind, title, message) }
    }
}

import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts
import Ao

// Экран входа: слева - знак и суть продукта, справа - карточка входа или
// создания профиля с индикатором надёжности пароля.
Item {
    id: root
    property bool signUp: backend.profiles.length === 0
    property string error: ""
    property real appear: 0
    Component.onCompleted: appear = 1
    Behavior on appear { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }

    Connections {
        target: backend
        function onAuthFinished(ok, message) {
            root.error = ok ? "" : message
            if (!ok) shake.restart()
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // --- бренд --------------------------------------------------------------
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            ColumnLayout {
                anchors.centerIn: parent
                width: Math.min(parent.width - 120, 520)
                spacing: 22
                opacity: root.appear
                transform: Translate { y: (1 - root.appear) * 24 }

                OrbitLogo { size: 132; Layout.alignment: Qt.AlignLeft; speed: 0.8 }
                AText {
                    text: backend.appName
                    size: 44
                    weight: Font.Bold
                    Layout.fillWidth: true
                }
                AText {
                    text: i18n.t["login.tagline"]
                    size: Theme.fsH3
                    dim: true
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                    Layout.fillWidth: true
                    lineHeight: 1.25
                }
                ColumnLayout {
                    Layout.topMargin: 6
                    spacing: 14
                    Repeater {
                        model: [
                            { icon: "users", text: i18n.t["login.f1"] },
                            { icon: "shield-check", text: i18n.t["login.f2"] },
                            { icon: "lock", text: i18n.t["login.f3"] }
                        ]
                        delegate: RowLayout {
                            required property var modelData
                            required property int index
                            spacing: 12
                            opacity: root.appear
                            Rectangle {
                                width: 34; height: 34; radius: 11
                                color: Theme.alpha(Theme.violet, 0.14)
                                border.color: Theme.alpha(Theme.violetSoft, 0.25)
                                Icon { anchors.centerIn: parent; name: modelData.icon; size: 16; color: Theme.violetSoft }
                            }
                            AText { text: modelData.text; dim: true; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone }
                        }
                    }
                }
            }
        }

        // --- форма ---------------------------------------------------------------
        Item {
            Layout.preferredWidth: 560
            Layout.fillHeight: true

            Card {
                id: card
                anchors.centerIn: parent
                width: 420
                padding: 30
                radius: Theme.radiusXL
                opacity: root.appear
                transform: [
                    Translate { id: shakeShift; x: 0 },
                    Translate { y: (1 - root.appear) * 36 }
                ]

                SequentialAnimation {
                    id: shake
                    NumberAnimation { target: shakeShift; property: "x"; to: -10; duration: 50 }
                    NumberAnimation { target: shakeShift; property: "x"; to: 10; duration: 70 }
                    NumberAnimation { target: shakeShift; property: "x"; to: -6; duration: 60 }
                    NumberAnimation { target: shakeShift; property: "x"; to: 0; duration: 60 }
                }

                ColumnLayout {
                    width: parent.width
                    spacing: 16

                    RowLayout {
                        Layout.fillWidth: true
                        AText {
                            text: root.signUp ? i18n.t["login.create_title"] : i18n.t["login.title"]
                            size: Theme.fsH1
                            weight: Font.Bold
                            Layout.fillWidth: true
                            wrapMode: Text.Wrap
                            elide: Text.ElideNone
                        }
                        Segmented {
                            options: i18n.languages.map(function(l) { return { value: l.code, title: l.code.toUpperCase() } })
                            value: i18n.lang
                            onPicked: function(v) { backend.setLanguage(v) }
                        }
                    }
                    AText {
                        text: i18n.t["login.subtitle"]
                        dim: true
                        wrapMode: Text.Wrap
                        elide: Text.ElideNone
                        Layout.fillWidth: true
                    }

                    // --- вход ---
                    ColumnLayout {
                        visible: !root.signUp
                        Layout.fillWidth: true
                        spacing: 14
                        Select {
                            id: profile
                            Layout.fillWidth: true
                            label: i18n.t["login.username"]
                            icon: "user"
                            options: backend.profiles
                            value: backend.lastUsername
                            onPicked: function(v) { password.text = backend.savedPassword(v); password.focusInput() }
                        }
                        Field {
                            id: password
                            Layout.fillWidth: true
                            label: i18n.t["login.password"]
                            icon: "lock"
                            password: true
                            onAccepted: signInButton.clicked()
                            Component.onCompleted: {
                                text = backend.savedPassword(backend.lastUsername)
                                focusInput()
                            }
                        }
                        Toggle {
                            id: remember
                            Layout.fillWidth: true
                            label: i18n.t["login.remember"]
                            checked: backend.rememberDefault
                            enabled: backend.keyringAvailable
                        }
                    }

                    // --- создание профиля ---
                    ColumnLayout {
                        visible: root.signUp
                        Layout.fillWidth: true
                        spacing: 14
                        Rectangle {
                            Layout.fillWidth: true
                            radius: Theme.radius
                            color: Theme.alpha(Theme.warning, 0.08)
                            border.color: Theme.alpha(Theme.warning, 0.3)
                            implicitHeight: warn.implicitHeight + 22
                            RowLayout {
                                id: warn
                                anchors.fill: parent
                                anchors.margins: 11
                                spacing: 10
                                Icon { name: "triangle-alert"; color: Theme.warning; Layout.alignment: Qt.AlignTop }
                                AText {
                                    text: i18n.t["login.warning"]
                                    size: Theme.fsSmall
                                    color: Theme.textDim
                                    wrapMode: Text.Wrap
                                    elide: Text.ElideNone
                                    Layout.fillWidth: true
                                }
                            }
                        }
                        Field { id: newName; Layout.fillWidth: true; label: i18n.t["login.username"]; icon: "user" }
                        Field {
                            id: newPass
                            Layout.fillWidth: true
                            label: i18n.t["login.password"]
                            icon: "lock"
                            password: true
                        }
                        // Индикатор надёжности пароля.
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 6
                            property int strength: backend.passwordStrength(newPass.text)
                            Repeater {
                                model: 4
                                delegate: Rectangle {
                                    required property int index
                                    Layout.fillWidth: true
                                    height: 4
                                    radius: 2
                                    color: index < parent.strength
                                           ? (parent.strength <= 1 ? Theme.danger : parent.strength === 2 ? Theme.warning : Theme.success)
                                           : Theme.surface3
                                    Behavior on color { ColorAnimation { duration: Theme.normal } }
                                }
                            }
                            AText {
                                text: [i18n.t["login.s0"], i18n.t["login.s1"], i18n.t["login.s2"], i18n.t["login.s3"], i18n.t["login.s4"]][parent.strength]
                                size: Theme.fsMicro
                                mute: true
                                Layout.preferredWidth: 80
                                horizontalAlignment: Text.AlignRight
                            }
                        }
                        Field {
                            id: newPass2
                            Layout.fillWidth: true
                            label: i18n.t["login.password2"]
                            icon: "lock"
                            password: true
                            error: newPass2.text !== "" && newPass2.text !== newPass.text ? i18n.t["login.password_mismatch"] : ""
                            onAccepted: signUpButton.clicked()
                        }
                    }

                    // Ошибка входа.
                    Rectangle {
                        Layout.fillWidth: true
                        visible: root.error !== ""
                        radius: Theme.radius
                        color: Theme.alpha(Theme.danger, 0.1)
                        border.color: Theme.alpha(Theme.danger, 0.35)
                        implicitHeight: errText.implicitHeight + 18
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 9
                            spacing: 8
                            Icon { name: "circle-alert"; color: Theme.danger }
                            AText { id: errText; text: root.error; color: Theme.danger; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true; size: Theme.fsSmall }
                        }
                    }

                    Button {
                        id: signInButton
                        visible: !root.signUp
                        Layout.fillWidth: true
                        Layout.topMargin: 4
                        variant: "primary"
                        iconName: "arrow-right"
                        text: i18n.t["login.signin"]
                        loading: backend.authBusy
                        enabled: !backend.authBusy
                        onClicked: backend.signIn(profile.combo.currentText, password.text, remember.checked)
                    }
                    Button {
                        id: signUpButton
                        visible: root.signUp
                        Layout.fillWidth: true
                        Layout.topMargin: 4
                        variant: "primary"
                        iconName: "sparkles"
                        text: i18n.t["login.create"]
                        loading: backend.authBusy
                        enabled: !backend.authBusy
                        onClicked: backend.signUp(newName.text, newPass.text, newPass2.text)
                    }
                    Button {
                        visible: backend.profiles.length > 0
                        Layout.fillWidth: true
                        variant: "ghost"
                        text: root.signUp ? i18n.t["login.have_profile"] : i18n.t["login.create"]
                        onClicked: { root.signUp = !root.signUp; root.error = "" }
                    }
                }
            }

            AText {
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 22
                anchors.horizontalCenter: parent.horizontalCenter
                text: backend.appName + " " + backend.appVersion + " · " + i18n.t["login.local"]
                mute: true
                size: Theme.fsSmall
            }
        }
    }
}

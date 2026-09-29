import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Слайдер с подписью и значением справа; значение применяется по отпусканию.
ColumnLayout {
    id: root
    property string label: ""
    property real from: 0
    property real to: 1
    property real stepSize: 0.05
    property real value: 0
    property int decimals: 2
    property string suffix: ""
    property var format: null
    signal committed(real value)
    spacing: 6

    RowLayout {
        Layout.fillWidth: true
        AText { text: root.label; size: Theme.fsSmall; weight: Font.Medium; dim: true; Layout.fillWidth: true }
        AText {
            text: root.format ? root.format(slider.value) : slider.value.toFixed(root.decimals) + root.suffix
            size: Theme.fsSmall
            weight: Font.DemiBold
            color: Theme.violetSoft
            mono: true
        }
    }

    T.Slider {
        id: slider
        Layout.fillWidth: true
        from: root.from
        to: root.to
        stepSize: root.stepSize
        value: root.value
        snapMode: T.Slider.SnapAlways
        hoverEnabled: true
        onPressedChanged: if (!pressed) root.committed(value)
        // Стрелки и колёсико двигают ползунок без нажатия - применяем сразу.
        onMoved: if (!pressed) root.committed(value)

        background: Rectangle {
            x: slider.leftPadding
            y: slider.topPadding + slider.availableHeight / 2 - height / 2
            width: slider.availableWidth
            height: 6
            radius: 3
            color: Theme.surface3
            Rectangle {
                width: slider.visualPosition * parent.width
                height: parent.height
                radius: 3
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0; color: Theme.violet }
                    GradientStop { position: 1; color: Theme.teal }
                }
            }
        }
        handle: Rectangle {
            x: slider.leftPadding + slider.visualPosition * (slider.availableWidth - width)
            y: slider.topPadding + slider.availableHeight / 2 - height / 2
            width: 18; height: 18; radius: 9
            color: "white"
            scale: slider.pressed ? 1.25 : (slider.hovered ? 1.1 : 1)
            Behavior on scale { NumberAnimation { duration: Theme.fast; easing.type: Easing.OutBack } }
            Rectangle {
                anchors.centerIn: parent
                width: 30; height: 30; radius: 15
                color: Theme.alpha(Theme.violet, 0.25)
                visible: slider.pressed
            }
        }
    }
}

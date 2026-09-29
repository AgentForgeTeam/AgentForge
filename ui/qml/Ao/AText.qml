import QtQuick

// Базовый текст интерфейса с шрифтом и цветом темы.
Text {
    property bool dim: false
    property bool mute: false
    property bool mono: false
    property int size: Theme.fsBody
    property int weight: Font.Normal

    color: mute ? Theme.textMute : (dim ? Theme.textDim : Theme.text)
    font.family: mono ? Theme.monoFamily : Theme.fontFamily
    font.pixelSize: size
    font.weight: weight
    wrapMode: Text.NoWrap
    elide: Text.ElideRight
    textFormat: Text.PlainText
    renderType: Text.QtRendering
    linkColor: Theme.cyan
}

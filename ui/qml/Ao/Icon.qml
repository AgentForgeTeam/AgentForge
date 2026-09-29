import QtQuick

// Иконка из шрифта Lucide: Icon { name: "bot"; size: 18; color: Theme.textDim }
Text {
    property string name: "circle-dot"
    property int size: 16
    text: Icons.glyph(name)
    font.family: Theme.iconFamily
    font.pixelSize: size
    color: Theme.textDim
    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignVCenter
    renderType: Text.QtRendering
    Behavior on color { ColorAnimation { duration: Theme.fast } }
}

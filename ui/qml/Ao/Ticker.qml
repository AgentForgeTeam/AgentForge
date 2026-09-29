import QtQuick

// Число, которое «досчитывает» до нового значения.
AText {
    id: root
    property real value: 0
    property string unit: "int"     // int | tokens | usd | percent | fraction
    property real shown: 0
    property string total: ""
    Behavior on shown { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }
    onValueChanged: shown = value
    Component.onCompleted: shown = value

    function fmt(v) {
        if (unit === "usd") return v >= 100 ? "$" + Math.round(v) : v >= 1 ? "$" + v.toFixed(2) : v === 0 ? "$0" : "$" + v.toFixed(v >= 0.01 ? 3 : 4)
        if (unit === "tokens") {
            if (v >= 1e6) return (v / 1e6).toFixed(2) + "M"
            if (v >= 1e4) return (v / 1e3).toFixed(1) + "k"
            return Math.round(v).toLocaleString(Qt.locale("ru_RU"), "f", 0)
        }
        if (unit === "percent") return Math.round(v * 100) + "%"
        return Math.round(v).toString()
    }
    text: fmt(shown) + (total !== "" ? " / " + total : "")
}

pragma Singleton
import QtQuick

// Дизайн-система: палитра, типографика, отступы, радиусы и анимации.
// Основа — глубокий чернильно-фиолетовый фон; акцент — фиолетовый,
// второй акцент — сине-зелёный (teal → cyan). Все длительности анимаций
// проходят через dur(), поэтому уровень «движения» из настроек
// одним переключателем делает интерфейс спокойнее или выключает анимации.
QtObject {
    id: theme

    // --- движение: 2 — полное, 1 — сдержанное, 0 — без анимаций ---------
    property int motion: 2
    readonly property bool rich: motion >= 2
    function dur(ms) { return motion === 0 ? 0 : (motion === 1 ? Math.round(ms * 0.6) : ms) }
    readonly property int fast: dur(140)
    readonly property int normal: dur(220)
    readonly property int slow: dur(420)

    // --- шрифты (семейства задаёт Python после загрузки файлов) --------------
    property string fontFamily: "Inter"
    property string monoFamily: "JetBrains Mono"
    property string iconFamily: "lucide"

    // --- фоны и поверхности ----------------------------------------------------
    readonly property color bg: "#09080F"
    readonly property color bgRaised: "#0E0C18"
    readonly property color sidebar: "#0C0A16"
    readonly property color surface: Qt.rgba(0.10, 0.09, 0.17, 0.78)
    readonly property color surfaceSolid: "#15132A"
    readonly property color surfaceHover: Qt.rgba(0.14, 0.12, 0.24, 0.85)
    readonly property color surface2: "#1A1733"
    readonly property color surface3: "#221E40"
    readonly property color input: "#120F22"
    readonly property color overlay: Qt.rgba(0.02, 0.01, 0.05, 0.62)

    readonly property color border: "#262244"
    readonly property color borderSoft: Qt.rgba(1, 1, 1, 0.06)
    readonly property color borderStrong: "#3B3566"

    // --- текст ---------------------------------------------------------------------
    readonly property color text: "#EEEBFA"
    readonly property color textDim: "#A9A3C8"
    readonly property color textMute: "#6E6891"
    readonly property color textFaint: "#4B4668"

    // --- акценты ---------------------------------------------------------------------
    readonly property color violet: "#8B5CF6"
    readonly property color violetSoft: "#A78BFA"
    readonly property color violetDeep: "#6D28D9"
    readonly property color indigo: "#6366F1"
    readonly property color teal: "#2DD4BF"
    readonly property color cyan: "#22D3EE"
    readonly property color magenta: "#D946EF"

    readonly property color success: "#34D399"
    readonly property color warning: "#FBBF24"
    readonly property color danger: "#FB7185"
    readonly property color info: "#60A5FA"

    function tone(name) {
        switch (name) {
        case "success": return success
        case "warning": return warning
        case "error": return danger
        case "danger": return danger
        case "info": return info
        case "accent": return cyan
        case "tool": return cyan
        case "violet": return violetSoft
        case "muted": return textMute
        default: return textDim
        }
    }

    function statusColor(status) {
        switch (status) {
        case "running": return cyan
        case "done": return success
        case "review": return violetSoft
        case "rework": return warning
        case "paused": return "#F59E0B"
        case "error": return danger
        case "failed": return danger
        case "stopped": return "#F59E0B"
        default: return textMute
        }
    }

    function alpha(c, a) { return Qt.rgba(c.r, c.g, c.b, a) }

    // --- типографика ---------------------------------------------------------------------
    readonly property int fsDisplay: 30
    readonly property int fsH1: 23
    readonly property int fsH2: 17
    readonly property int fsH3: 15
    readonly property int fsBody: 14
    readonly property int fsSmall: 13
    readonly property int fsMicro: 11

    // --- геометрия -------------------------------------------------------------------------
    readonly property int radiusS: 8
    readonly property int radius: 12
    readonly property int radiusL: 16
    readonly property int radiusXL: 22
    readonly property int gap: 12
    readonly property int pad: 20
    readonly property int pagePad: 28
    readonly property int controlH: 38
}

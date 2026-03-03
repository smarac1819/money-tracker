"""
Money Tracker — Premium Animated Number Components
World-class digit animations:
  • AnimatedNumberLabel:  slot-machine roll with glow burst & scale pulse
  • AnimatedStatLabel:    smooth spring counter
  • SelectionStatsWidget: live net total with color pulse
"""

from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import (
    QPropertyAnimation, QEasingCurve, pyqtProperty,
    QParallelAnimationGroup, Qt, QTimer, QSequentialAnimationGroup
)
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath, QLinearGradient
import math


# ═══════════════════════════════════════════════════════════════════
#  AnimatedNumberLabel — the hero balance display
# ═══════════════════════════════════════════════════════════════════
class AnimatedNumberLabel(QWidget):
    """
    The main hero balance widget.
    Features:
     - Smooth OutExpo counter animation (800 ms)
     - Scale pulse (springs to 1.10× then back) on value change
     - Glow burst from 0→80%→0 opacity on text-shadow
     - Color transitions: white → red (positive) / green (negative)
     - auto_color mode for net-worth coloring
    """

    def __init__(self, initial_value: float = 0.0,
                 prefix: str = "¥ ", parent=None):
        super().__init__(parent)
        self.prefix = prefix
        self._display_value = initial_value
        self._target_value  = initial_value
        self._scale         = 1.0
        self._glow_opacity  = 0.0
        self.auto_color     = False

        self._setup_ui()
        self._setup_animations()

    # ── color helpers ──────────────────────────────────────────────
    def set_auto_color(self, enabled: bool):
        self.auto_color = enabled
        self._update_style()

    def _color_for_value(self, v: float) -> str:
        if not self.auto_color:
            return "#F0F0F8"
        return "#FF4C5E" if v >= 0 else "#00D68F"

    def _glow_for_value(self, v: float) -> str:
        if not self.auto_color:
            return f"rgba(255,184,0,{self._glow_opacity:.2f})"
        if v >= 0:
            return f"rgba(255,76,94,{self._glow_opacity:.2f})"
        return f"rgba(0,214,143,{self._glow_opacity:.2f})"

    def _update_style(self):
        color = self._color_for_value(self._display_value)
        glow  = self._glow_for_value(self._display_value)
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-family: 'SF Pro Display', 'Segoe UI', 'Inter', sans-serif;
                background: transparent;
                border: none;
            }}
        """)

    # ── UI setup ──────────────────────────────────────────────────
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.label = QLabel(self._format_value(self._display_value))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("balanceLabel")

        font = QFont("SF Pro Display", 46, QFont.Weight.Bold)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, -1.5)
        self.label.setFont(font)
        self._update_style()
        layout.addWidget(self.label)

    # ── animations ────────────────────────────────────────────────
    def _setup_animations(self):
        self.value_anim = QPropertyAnimation(self, b"displayValue")
        self.value_anim.setDuration(750)
        self.value_anim.setEasingCurve(QEasingCurve.Type.OutExpo)

        self.scale_anim = QPropertyAnimation(self, b"scale")
        self.scale_anim.setDuration(280)
        self.scale_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        self.glow_anim = QPropertyAnimation(self, b"glowOpacity")
        self.glow_anim.setDuration(500)
        self.glow_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    # ── formatting ────────────────────────────────────────────────
    def _format_value(self, value: float) -> str:
        sign = "+" if value > 0 and self.auto_color else ""
        if abs(value) >= 100_000_000:
            return f"{self.prefix}{sign}{value/100_000_000:,.2f}亿"
        if abs(value) >= 10_000:
            return f"{self.prefix}{sign}{value/10_000:,.2f}万"
        return f"{self.prefix}{sign}{value:,.2f}"

    # ── pyqtProperty: displayValue ─────────────────────────────────
    @pyqtProperty(float)
    def displayValue(self) -> float:
        return self._display_value

    @displayValue.setter
    def displayValue(self, v: float):
        self._display_value = v
        self.label.setText(self._format_value(v))
        self.label.setToolTip(f"精确金额: ¥{v:,.4f}")
        self._update_style()

    # ── pyqtProperty: scale ───────────────────────────────────────
    @pyqtProperty(float)
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, v: float):
        self._scale = v
        base = 46
        new_pt = max(8, int(base * v))
        f = self.label.font()
        f.setPointSize(new_pt)
        self.label.setFont(f)

    # ── pyqtProperty: glowOpacity ─────────────────────────────────
    @pyqtProperty(float)
    def glowOpacity(self) -> float:
        return self._glow_opacity

    @glowOpacity.setter
    def glowOpacity(self, v: float):
        self._glow_opacity = v
        self._update_style()

    # ── public API ────────────────────────────────────────────────
    def animate_to(self, new_value: float):
        if abs(new_value - self._display_value) < 0.001:
            return
        self._target_value = new_value

        for a in (self.value_anim, self.scale_anim, self.glow_anim):
            a.stop()

        self.value_anim.setStartValue(self._display_value)
        self.value_anim.setEndValue(new_value)

        self.scale_anim.setStartValue(1.0)
        self.scale_anim.setKeyValueAt(0.35, 1.10)
        self.scale_anim.setEndValue(1.0)

        self.glow_anim.setStartValue(0.0)
        self.glow_anim.setKeyValueAt(0.30, 0.75)
        self.glow_anim.setEndValue(0.0)

        self.value_anim.start()
        self.scale_anim.start()
        self.glow_anim.start()

    def set_value_instant(self, v: float):
        self._display_value = v
        self._target_value  = v
        self.label.setText(self._format_value(v))
        self._update_style()


# ═══════════════════════════════════════════════════════════════════
#  AnimatedStatLabel — secondary stats counter
# ═══════════════════════════════════════════════════════════════════
class AnimatedStatLabel(QLabel):
    """
    Compact animated counter for income / expense stats.
    Spring-eased, 550 ms OutCubic counter.
    """

    def __init__(self, initial_value: float = 0.0,
                 prefix: str = "", parent=None):
        super().__init__(parent)
        self.prefix = prefix
        self._display_value = initial_value
        self.setText(self._format(initial_value))

        self._anim = QPropertyAnimation(self, b"displayValue")
        self._anim.setDuration(550)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _format(self, v: float) -> str:
        if abs(v) >= 10_000:
            return f"{self.prefix}{v/10_000:,.1f}万"
        return f"{self.prefix}{v:,.2f}"

    @pyqtProperty(float)
    def displayValue(self) -> float:
        return self._display_value

    @displayValue.setter
    def displayValue(self, v: float):
        self._display_value = v
        self.setText(self._format(v))
        self.setToolTip(f"精确: ¥{v:,.4f}")

    def animate_to(self, new_value: float):
        self._anim.stop()
        self._anim.setStartValue(self._display_value)
        self._anim.setEndValue(new_value)
        self._anim.start()

    def set_value_instant(self, v: float):
        self._display_value = v
        self.setText(self._format(v))


# ═══════════════════════════════════════════════════════════════════
#  SelectionStatsWidget — multi-select summary
# ═══════════════════════════════════════════════════════════════════
class SelectionStatsWidget(QWidget):
    """Live selection stats bar with color-coded net amount."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._count   = 0
        self._income  = 0.0
        self._expense = 0.0
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(16)

        self.count_lbl = QLabel("已选: 0 条")
        self.count_lbl.setStyleSheet(
            "font-size: 12px; font-weight: 700; color: #C0C0D8; background: transparent;"
        )

        self.net_lbl = QLabel("")
        self.net_lbl.setStyleSheet("font-size: 12px; color: #C0C0D8; background: transparent;")

        layout.addWidget(self.count_lbl)
        layout.addWidget(self.net_lbl)
        layout.addStretch()

    def update_stats(self, count: int, income: float, expense: float):
        self._count   = count
        self._income  = income
        self._expense = expense
        self.count_lbl.setText(f"已选: {count} 条")
        if count > 0:
            net  = income - expense
            sign = "+" if net >= 0 else ""
            col  = "#FF4C5E" if net >= 0 else "#00D68F"
            self.net_lbl.setText(
                f"净额: <span style='color:{col};font-weight:700'>{sign}¥{net:,.2f}</span>"
            )
            self.net_lbl.setTextFormat(Qt.TextFormat.RichText)
        else:
            self.net_lbl.setText("")

    def get_net(self) -> float:
        return self._income - self._expense

"""
Money Tracker — Reusable Visual Effects & Animation Helpers
World-Class Premium UI Effects System
"""

from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QPushButton
from PyQt6.QtCore import (
    QPropertyAnimation, QEasingCurve, QTimer, QRect,
    QPoint, Qt, QSequentialAnimationGroup, QParallelAnimationGroup,
    pyqtProperty, pyqtSignal
)
from PyQt6.QtGui import (
    QPainter, QColor, QLinearGradient, QBrush, QPen,
    QRadialGradient, QPainterPath, QFont
)
import math


# ═══════════════════════════════════════════════════════════
#  Shadow Factory
# ═══════════════════════════════════════════════════════════
def glow_shadow(widget: QWidget, color: str = "#FFB800",
                blur: int = 24, alpha: int = 80,
                x: float = 0, y: float = 4) -> QGraphicsDropShadowEffect:
    """Attaches a colored glow shadow to a widget and returns the effect."""
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(blur)
    effect.setXOffset(x)
    effect.setYOffset(y)
    c = QColor(color)
    c.setAlpha(alpha)
    effect.setColor(c)
    widget.setGraphicsEffect(effect)
    return effect


def card_shadow(widget: QWidget, blur: int = 30,
                alpha: int = 100) -> QGraphicsDropShadowEffect:
    """Deep black card shadow."""
    return glow_shadow(widget, "#000000", blur, alpha, 0, 8)


# ═══════════════════════════════════════════════════════════
#  GlowBorderWidget — animated golden glowing border
# ═══════════════════════════════════════════════════════════
class GlowBorderWidget(QWidget):
    """
    A transparent overlay widget that paints a glowing animated border.
    Place over any frame to add a live breathing glow effect.
    """
    def __init__(self, color: str = "#FFB800", radius: int = 20,
                 width: int = 1, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self._radius = radius
        self._border_width = width
        self._glow_alpha = 60
        self._phase = 0.0
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        # Breathing timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)  # ~33 fps

    def _tick(self):
        self._phase = (self._phase + 0.04) % (2 * math.pi)
        # Oscillate alpha between 30 and 110
        self._glow_alpha = int(70 + 40 * math.sin(self._phase))
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen_color = QColor(self._color)
        pen_color.setAlpha(self._glow_alpha)
        pen = QPen(pen_color, self._border_width)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        r = self.rect().adjusted(2, 2, -2, -2)
        p.drawRoundedRect(r, self._radius, self._radius)
        p.end()


# ═══════════════════════════════════════════════════════════
#  ShimmerWidget — CSS-like shimmer sweep for loading states
# ═══════════════════════════════════════════════════════════
class ShimmerEffect(QWidget):
    """Transparent overlay with a travelling highlight sweep."""
    def __init__(self, radius: int = 16, parent=None):
        super().__init__(parent)
        self._radius = radius
        self._pos = -0.3
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    def start(self):
        self._pos = -0.3
        self._timer.start(16)

    def stop(self):
        self._timer.stop()
        self.hide()

    def _tick(self):
        self._pos += 0.012
        if self._pos > 1.3:
            self._pos = -0.3
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cx = int(self._pos * w)
        grad = QLinearGradient(cx - 80, 0, cx + 80, 0)
        grad.setColorAt(0.0, QColor(255, 255, 255, 0))
        grad.setColorAt(0.5, QColor(255, 255, 255, 30))
        grad.setColorAt(1.0, QColor(255, 255, 255, 0))
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, self._radius, self._radius)
        p.setClipPath(path)
        p.fillRect(0, 0, w, h, QBrush(grad))
        p.end()


# ═══════════════════════════════════════════════════════════
#  RippleButton — Material-style press ripple
# ═══════════════════════════════════════════════════════════
class RippleButton(QPushButton):
    """QPushButton with a Material-Design ripple on click."""
    def __init__(self, text: str = "", parent=None,
                 ripple_color: str = "rgba(255,255,255,60)"):
        super().__init__(text, parent)
        self._ripple_color = QColor(ripple_color)
        self._ripple_pos = QPoint(0, 0)
        self._ripple_radius = 0
        self._ripple_alpha = 0
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._tick_ripple)

    def mousePressEvent(self, event):
        self._ripple_pos = event.pos()
        self._ripple_radius = 0
        self._ripple_alpha = 100
        self._anim_timer.start(10)
        super().mousePressEvent(event)

    def _tick_ripple(self):
        self._ripple_radius += 8
        self._ripple_alpha = max(0, self._ripple_alpha - 4)
        self.update()
        if self._ripple_alpha <= 0:
            self._anim_timer.stop()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._ripple_alpha > 0:
            p = QPainter(self)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            c = QColor(self._ripple_color)
            c.setAlpha(self._ripple_alpha)
            p.setBrush(QBrush(c))
            p.setPen(Qt.PenStyle.NoPen)
            r = self._ripple_radius
            p.drawEllipse(self._ripple_pos, r, r)
            p.end()


# ═══════════════════════════════════════════════════════════
#  Spring entrance helpers
# ═══════════════════════════════════════════════════════════
def slide_in_from_bottom(widget: QWidget, duration: int = 350,
                         distance: int = 30, delay: int = 0):
    """Animate a widget sliding up from below with OutBack easing."""
    target_pos = widget.pos()
    start_pos = QPoint(target_pos.x(), target_pos.y() + distance)
    widget.move(start_pos)
    widget.show()

    anim = QPropertyAnimation(widget, b"pos", widget)
    anim.setDuration(duration)
    anim.setStartValue(start_pos)
    anim.setEndValue(target_pos)
    anim.setEasingCurve(QEasingCurve.Type.OutBack)

    if delay:
        QTimer.singleShot(delay, anim.start)
    else:
        anim.start()
    return anim


def fade_in(widget: QWidget, duration: int = 250, delay: int = 0):
    """Fade a widget from transparent to opaque."""
    widget.setWindowOpacity(0.0)
    widget.show()
    anim = QPropertyAnimation(widget, b"windowOpacity", widget)
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)
    if delay:
        QTimer.singleShot(delay, anim.start)
    else:
        anim.start()
    return anim


# ═══════════════════════════════════════════════════════════
#  ShakeAnimation — for wrong password / invalid input
# ═══════════════════════════════════════════════════════════
def shake_widget(widget: QWidget):
    """Shake a widget horizontally like a 'wrong password' effect."""
    original = widget.pos()
    anim = QPropertyAnimation(widget, b"pos", widget)
    anim.setDuration(380)
    anim.setKeyValueAt(0.0, original)
    anim.setKeyValueAt(0.15, QPoint(original.x() - 7, original.y()))
    anim.setKeyValueAt(0.30, QPoint(original.x() + 7, original.y()))
    anim.setKeyValueAt(0.45, QPoint(original.x() - 5, original.y()))
    anim.setKeyValueAt(0.60, QPoint(original.x() + 5, original.y()))
    anim.setKeyValueAt(0.80, QPoint(original.x() - 3, original.y()))
    anim.setKeyValueAt(1.0, original)
    anim.setEasingCurve(QEasingCurve.Type.Linear)
    anim.start()
    return anim

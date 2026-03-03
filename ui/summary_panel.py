"""
Money Tracker — Premium Summary Panel
World-class animated analytics dashboard.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QScrollArea, QPushButton, QCheckBox,
    QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QCursor, QColor, QPainter, QLinearGradient, QBrush

from .animated_number import AnimatedNumberLabel, AnimatedStatLabel
from .styles import THEME
from .effects import card_shadow, glow_shadow, ShimmerEffect


class ModuleSummaryCard(QFrame):
    """Premium module summary card with color accent, balance, and income/expense detail."""

    toggled = pyqtSignal(int, bool)

    def __init__(self, module_id: int, name: str, icon: str, color: str, parent=None):
        super().__init__(parent)
        self.module_id  = module_id
        self.is_selected = True
        self.selectable_mode = False
        self.income  = 0.0
        self.expense = 0.0
        self.balance = 0.0
        self._accent = color

        self.setObjectName("moduleSummaryCard")
        self.setMinimumHeight(80)
        self._setup_ui(name, icon, color)
        self._apply_style(False)

        # Hover-based glow
        self.setMouseTracking(True)

    def _setup_ui(self, name: str, icon: str, color: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 15, 20, 15)
        layout.setSpacing(14)

        # ── Checkbox (hidden by default) ──────────────────────────
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(True)
        self.checkbox.setVisible(False)
        self.checkbox.stateChanged.connect(self._on_check)
        self.checkbox.setStyleSheet("""
            QCheckBox::indicator { width:18px; height:18px; border-radius:5px; border:2px solid #3A3A50; background:transparent; }
            QCheckBox::indicator:checked { background:#FFB800; border-color:#FFB800; }
            QCheckBox::indicator:hover { border-color:#888; }
        """)
        layout.addWidget(self.checkbox)

        # ── Colored accent bar on the left ───────────────────────
        accent_bar = QFrame()
        accent_bar.setFixedWidth(4)
        accent_bar.setStyleSheet(f"background:{color}; border-radius:2px;")
        layout.addWidget(accent_bar)

        # ── Icon badge ───────────────────────────────────────────
        self._icon_lbl = QLabel(icon)
        self._icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._icon_lbl.setFixedSize(46, 46)
        self._icon_lbl.setStyleSheet(f"""
            QLabel {{
                background: {color}20;
                color: {color};
                border: 1px solid {color}40;
                border-radius: 13px;
                font-size: 22px;
            }}
        """)
        layout.addWidget(self._icon_lbl)

        # ── Name / detail ────────────────────────────────────────
        info = QVBoxLayout()
        info.setSpacing(3)
        self._name_lbl = QLabel(name)
        self._name_lbl.setStyleSheet("font-size:15px; font-weight:700; color:#F0F0F8; background:transparent;")
        info.addWidget(self._name_lbl)
        self._detail_lbl = QLabel("")
        self._detail_lbl.setStyleSheet("font-size:11px; color:#606074; background:transparent;")
        info.addWidget(self._detail_lbl)
        layout.addLayout(info)
        layout.addStretch()

        # ── Balance ──────────────────────────────────────────────
        self._balance_lbl = QLabel("¥0.00")
        self._balance_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._balance_lbl.setStyleSheet("font-size:17px; font-weight:700; background:transparent;")
        layout.addWidget(self._balance_lbl)

    def _apply_style(self, hovered: bool):
        base = "rgba(32,32,44,0.95)" if not hovered else "rgba(42,42,58,0.98)"
        bord = self._accent + "55" if hovered else "rgba(255,255,255,0.06)"
        self.setStyleSheet(f"""
            QFrame#moduleSummaryCard {{
                background: {base};
                border: 1px solid {bord};
                border-radius: 16px;
            }}
        """)

    def enterEvent(self, e):
        self._apply_style(True)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._apply_style(False)
        super().leaveEvent(e)

    def update_stats(self, balance: float, income: float, expense: float):
        self.balance = balance
        self.income  = income
        self.expense = expense

        sign  = "+" if balance >= 0 else "−"
        color = "#FF4C5E" if balance >= 0 else "#00D68F"
        if abs(balance) >= 10_000:
            txt = f"{sign}¥{abs(balance)/10_000:,.1f}万"
        else:
            txt = f"{sign}¥{abs(balance):,.2f}"

        self._balance_lbl.setText(txt)
        self._balance_lbl.setStyleSheet(
            f"font-size:17px; font-weight:700; color:{color}; background:transparent;"
        )
        self.setToolTip(f"精确余额: ¥{balance:,.2f}\n收入: ¥{income:,.2f}\n支出: ¥{expense:,.2f}")

        i_fmt = f"收 ¥{income:,.0f}" if income < 10_000 else f"收 ¥{income/10_000:.1f}万"
        e_fmt = f"支 ¥{expense:,.0f}" if expense < 10_000 else f"支 ¥{expense/10_000:.1f}万"
        self._detail_lbl.setText(f"{i_fmt}  ·  {e_fmt}")

    def set_select_mode(self, active: bool):
        self.selectable_mode = active
        self.checkbox.setVisible(active)
        if not active:
            self.checkbox.setChecked(True)
            self.is_selected = True

    def _on_check(self, state):
        self.is_selected = (state == 2)
        self.toggled.emit(self.module_id, self.is_selected)


class SummaryPanel(QWidget):
    """Analytics dashboard — net worth hero card + per-module breakdown."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.module_cards = {}
        self.raw_data = []
        self.is_select_mode = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(22)

        # ── Top bar ──────────────────────────────────────────────
        top_bar = QHBoxLayout()
        title = QLabel("数据分析")
        title.setStyleSheet("font-size:26px; font-weight:800; color:#F0F0F8; letter-spacing:0.5px;")
        top_bar.addWidget(title)
        top_bar.addStretch()

        self.select_btn = QPushButton("☑  多选统计")
        self.select_btn.setCheckable(True)
        self.select_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.select_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.06);
                color: #A0A0B8;
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 12px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background: rgba(255,255,255,0.12); color:#FFF; }
            QPushButton:checked {
                background: rgba(10,132,255,0.20);
                color: #0A84FF;
                border-color: rgba(10,132,255,0.50);
            }
        """)
        self.select_btn.toggled.connect(self._toggle_select_mode)
        top_bar.addWidget(self.select_btn)
        layout.addLayout(top_bar)

        # ── Hero balance card ─────────────────────────────────────
        self._build_hero_card(layout)

        # ── Module list section ───────────────────────────────────
        section_row = QHBoxLayout()
        sec_lbl = QLabel("账本明细")
        sec_lbl.setStyleSheet("color:#606074; font-size:11px; font-weight:700; letter-spacing:1.5px;")
        section_row.addWidget(sec_lbl)
        section_row.addStretch()
        layout.addLayout(section_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical { background:transparent; width:4px; }
            QScrollBar::handle:vertical { background:rgba(255,255,255,0.12); border-radius:2px; min-height:20px; }
            QScrollBar::handle:vertical:hover { background:rgba(255,255,255,0.30); }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }
        """)

        content = QWidget()
        content.setStyleSheet("background:transparent;")
        self.modules_layout = QVBoxLayout(content)
        self.modules_layout.setContentsMargins(0, 0, 4, 0)
        self.modules_layout.setSpacing(10)
        self.modules_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

    def _build_hero_card(self, parent_layout):
        """Build the gradient net-worth hero card."""
        hero = QFrame()
        hero.setObjectName("heroCard")
        hero.setMinimumHeight(200)
        hero.setStyleSheet("""
            QFrame#heroCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1E1E2C, stop:0.45 #181824, stop:1 #111118);
                border: 1px solid rgba(255,184,0,0.30);
                border-radius: 24px;
            }
        """)
        card_shadow(hero, blur=35, alpha=120)

        card_layout = QVBoxLayout(hero)
        card_layout.setContentsMargins(32, 28, 32, 28)
        card_layout.setSpacing(0)

        # Title row
        title_row = QHBoxLayout()
        net_title = QLabel("NET WORTH  净资产")
        net_title.setStyleSheet(
            "color:#606074; font-size:11px; font-weight:700; letter-spacing:2px; background:transparent;"
        )
        title_row.addWidget(net_title)
        title_row.addStretch()

        live_dot = QLabel("● LIVE")
        live_dot.setStyleSheet(
            "color:#00D68F; font-size:10px; font-weight:700; background:transparent;"
        )
        title_row.addWidget(live_dot)
        card_layout.addLayout(title_row)

        card_layout.addSpacing(10)

        # Main balance label
        self.total_balance = AnimatedNumberLabel(0.0)
        self.total_balance.set_auto_color(True)
        card_layout.addWidget(self.total_balance)

        # Divider
        card_layout.addSpacing(16)
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(255,255,255,0.07); border:none;")
        card_layout.addWidget(divider)
        card_layout.addSpacing(16)

        # Income / Expense row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(0)

        # Income block
        inc_box = self._stat_box("总收入  INCOME", "+¥", "#FF4C5E", is_income=True)
        self.total_income, _inc_widget = inc_box
        stats_row.addLayout(_inc_widget)

        # Vertical separator
        vsep = QFrame()
        vsep.setFixedWidth(1)
        vsep.setFixedHeight(50)
        vsep.setStyleSheet("background:rgba(255,255,255,0.07); border:none;")
        stats_row.addWidget(vsep, 0, Qt.AlignmentFlag.AlignVCenter)

        # Expense block
        exp_box = self._stat_box("总支出  EXPENSE", "−¥", "#00D68F", is_income=False)
        self.total_expense, _exp_widget = exp_box
        stats_row.addLayout(_exp_widget)

        card_layout.addLayout(stats_row)
        parent_layout.addWidget(hero)

    def _stat_box(self, label_txt: str, prefix: str, color: str, is_income: bool):
        """Helper to build income or expense stat column."""
        box = QVBoxLayout()
        box.setSpacing(6)
        box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel(label_txt)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color:#606074; font-size:10px; font-weight:700; letter-spacing:1px; background:transparent;")
        box.addWidget(lbl)

        stat = AnimatedStatLabel(0.0, prefix)
        stat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stat.setStyleSheet(
            f"font-size:20px; font-weight:700; color:{color}; background:transparent;"
        )
        box.addWidget(stat)
        return stat, box

    # ── Select mode ───────────────────────────────────────────────
    def _toggle_select_mode(self, active: bool):
        self.is_select_mode = active
        for card in self.module_cards.values():
            card.set_select_mode(active)
        if not active:
            self._recalculate_totals()

    def _on_module_toggled(self, mid, selected):
        self._recalculate_totals()

    def _recalculate_totals(self):
        t_inc = sum(c.income  for c in self.module_cards.values() if c.is_selected)
        t_exp = sum(c.expense for c in self.module_cards.values() if c.is_selected)
        self.total_balance.animate_to(t_inc - t_exp)
        self.total_income.animate_to(t_inc)
        self.total_expense.animate_to(t_exp)

    # ── Data update ───────────────────────────────────────────────
    def update_data(self, total_balance, total_income, total_expense, modules_data):
        self.raw_data = modules_data
        if not self.is_select_mode:
            self.total_balance.animate_to(total_balance)
            self.total_income.animate_to(total_income)
            self.total_expense.animate_to(total_expense)

        existing_ids = set(self.module_cards.keys())
        new_ids      = {m[0] for m in modules_data}

        for mid in existing_ids - new_ids:
            card = self.module_cards.pop(mid)
            card.deleteLater()

        for i, module in enumerate(modules_data):
            mid, name, icon, color, income, expense = module
            balance = income - expense
            if mid not in self.module_cards:
                card = ModuleSummaryCard(mid, name, icon, color)
                card.toggled.connect(self._on_module_toggled)
                self.modules_layout.insertWidget(i, card)
                self.module_cards[mid] = card
            self.module_cards[mid].update_stats(balance, income, expense)

        if self.is_select_mode:
            self._recalculate_totals()

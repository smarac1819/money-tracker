"""
Money Tracker — Module (Ledger) Dialog
Simple, clean dialog: just name + cancel/save.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class ModuleDialog(QDialog):
    """Create or edit a ledger. Only shows: name, cancel, save."""

    def __init__(self, parent=None, module_data=None, db=None):
        super().__init__(parent)
        self.module_data = module_data  # (mid, name, icon, color) or None
        self.db = db
        self._result_name = ""
        self._result_icon = "💰"
        self._result_color = "#FFB800"
        self._setup_ui()

        # Pre-fill when editing
        if module_data:
            mid, name, icon, color = module_data
            self._result_icon = icon or "💰"
            self._result_color = color or "#FFB800"
            self.name_input.setText(name)

    def _setup_ui(self):
        from .styles import THEME
        self.theme = THEME

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedWidth(420)

        # ── Outer container ──────────────────────────────────────
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("moduleCard")
        card.setStyleSheet(f"""
            QFrame#moduleCard {{
                background: {self.theme['bg_layer1']};
                border: 1px solid {self.theme['border_bright']};
                border-radius: 24px;
            }}
        """)
        outer.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # ── Title ────────────────────────────────────────────────
        title_text = "编辑账本" if self.module_data else "新建账本"
        title = QLabel(title_text)
        title.setStyleSheet(f"""
            font-size: 22px; font-weight: 800;
            color: {self.theme['text_p']};
            background: transparent;
        """)
        layout.addWidget(title)

        # ── Name input ───────────────────────────────────────────
        name_label = QLabel("账本名称")
        name_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {self.theme['text_s']}; background: transparent;")
        layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("为账本起个名字…")
        self.name_input.setFixedHeight(52)
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background: {self.theme['bg_input']};
                border: 1.5px solid {self.theme['border']};
                border-radius: 14px;
                padding: 0 18px;
                font-size: 16px;
                color: {self.theme['text_p']};
            }}
            QLineEdit:focus {{
                border-color: {self.theme['accent']};
                background: {self.theme['bg_layer2']};
            }}
        """)
        # Auto-generate next name when adding
        if not self.module_data:
            self.name_input.setText(self._next_name())
            QTimer.singleShot(50, lambda: self.name_input.selectAll())

        layout.addWidget(self.name_input)

        # ── Divider ──────────────────────────────────────────────
        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet(f"background: {self.theme['border']}; border: none;")
        layout.addWidget(div)

        # ── Buttons ──────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        btn_cancel = QPushButton("取 消")
        btn_cancel.setFixedHeight(48)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background: {self.theme['bg_layer2']};
                color: {self.theme['text_s']};
                border: 1px solid {self.theme['border']};
                border-radius: 14px; font-size: 15px; font-weight: 700;
            }}
            QPushButton:hover {{ background: {self.theme['bg_layer3']}; color: {self.theme['text_p']}; }}
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("保 存  ✓")
        btn_save.setFixedHeight(48)
        btn_save.setDefault(True)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.theme['accent']}, stop:1 {self.theme['accent_deep']});
                color: #000;
                border: none;
                border-radius: 14px; font-size: 15px; font-weight: 800;
            }}
            QPushButton:hover {{ opacity: 0.9; }}
        """)
        btn_save.clicked.connect(self._on_save)
        # Also allow Enter to save
        self.name_input.returnPressed.connect(self._on_save)

        btn_row.addWidget(btn_cancel, 1)
        btn_row.addWidget(btn_save, 1)
        layout.addLayout(btn_row)

        # Delete button only if editing
        if self.module_data:
            btn_delete = QPushButton("删除此账本")
            btn_delete.setFixedHeight(40)
            btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_delete.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; color: #FF453A;
                    border: none; font-size: 13px; font-weight: 600;
                }}
                QPushButton:hover {{ color: #FF6B6B; }}
            """)
            btn_delete.clicked.connect(self._on_delete)
            layout.addWidget(btn_delete, alignment=Qt.AlignmentFlag.AlignCenter)

    def _next_name(self) -> str:
        if not self.db:
            return "账本 1"
        existing = [row[1] for row in self.db.get_modules_sorted_by_balance()]
        i = 1
        while f"账本 {i}" in existing:
            i += 1
        return f"账本 {i}"

    def _on_save(self):
        name = self.name_input.text().strip()
        if not name:
            self.name_input.setPlaceholderText("❗ 账本名称不能为空")
            self.name_input.setFocus()
            return
        self._result_name = name
        self.done(1)

    def _on_delete(self):
        self.done(2)

    def get_result(self):
        return self._result_name, self._result_icon, self._result_color

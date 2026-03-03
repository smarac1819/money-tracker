"""
💰 Money Tracker v2
精美的Windows桌面多模块记账应用

Features:
- 多模块账本管理
- 收入/支出跟踪
- 勾选统计模式
- 全局搜索
- 动画数字显示
- 本地SQLite存储
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.main_window import MainWindow
from common.locale import load_lang


import os
from PyQt6.QtGui import QIcon

def main():
    # 启用高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Money Tracker")
    app.setApplicationVersion("4.0.0")
    
    # 设置应用图标
    icon_path = os.path.join(os.path.dirname(__file__), "ui", "mnlogo.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # 设置全局字体
    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(font)
    
    # 确保关闭窗口时退出应用
    app.setQuitOnLastWindowClosed(True)
    
    # Load language preference before building any UI
    load_lang()

    # Create and show main window
    window = MainWindow()
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

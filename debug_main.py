import sys
import traceback
import logging

logging.basicConfig(filename='ui_crash.log', level=logging.DEBUG)

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logging.error("Uncaught exception:\\n" + tb)
    print("CRASH:", tb)
    QApplication.quit()

sys.excepthook = excepthook

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()

# Simulate entering correct password instantly
if hasattr(window, 'lock_widget'):
    print("Bypassing password internally...")
    window.pwd_input.setText("") # assuming empty is pwd if none set
    window._verify_password()

sys.exit(app.exec())

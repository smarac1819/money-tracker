import traceback
import sys
try:
    import ui.main_window
    print("OK")
except BaseException as e:
    traceback.print_exc(file=sys.stdout)

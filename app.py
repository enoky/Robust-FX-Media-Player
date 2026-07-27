import os
import sys

from PySide6 import QtGui, QtWidgets
from ui import MainWindow

ICON_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "icon.ico")


def main():
    if sys.platform == "win32":
        # Without a distinct AppUserModelID, Windows groups the app under the
        # host interpreter and shows the Python icon in the taskbar.
        import ctypes

        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "enoky.RobustFXMediaPlayer"
            )
        except Exception:
            pass

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(ICON_PATH))
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

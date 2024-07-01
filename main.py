import sys
from PyQt6.QtWidgets import QApplication
from window_manager import WindowManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = WindowManager()
    ex.show()
    sys.exit(app.exec())
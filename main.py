import sys
from PyQt5.QtWidgets import QApplication
from ui import DeadlockToolkit

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeadlockToolkit()
    window.show()
    sys.exit(app.exec_())
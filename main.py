import sys
from PyQt6.QtWidgets import QApplication
from windows.mainWindow import MainWindow


# Точка входа в программу
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

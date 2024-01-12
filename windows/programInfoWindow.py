from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow


class ProgramInfoWindow(QMainWindow):
    """
    Класс, представляющий окно
    с информацией о программе
    """
    def __init__(self):
        super().__init__()
        # Загрузка пользовательского интерфейса из файла aboutProgram.ui
        uic.loadUi('forms/aboutProgram.ui', self)

        # Привязка события нажатия кнопки "Назад" к закрытию окна
        self.back.clicked.connect(self.close)

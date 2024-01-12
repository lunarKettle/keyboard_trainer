from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices


class AuthorWindow(QMainWindow):
    """
    Класс, представляющий окно
    с информацией об авторе программы
    """
    def __init__(self):
        super().__init__()

        # Загрузка пользовательского интерфейса из файла author.ui
        uic.loadUi('forms/author.ui', self)

        self.label.setOpenExternalLinks(True)
        self.label.linkActivated.connect(self.openLink)
        # Привязка события нажатия кнопки "Назад" к закрытию окна
        self.back.clicked.connect(self.close)

    def openLink(self, url):
        QDesktopServices.openUrl(QUrl(url))

import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from random import randint


class App(QMainWindow):
    textIndex = 0

    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)
        self.generateText.clicked.connect(self.generateClick)
        self.startTyping.clicked.connect(self.startClick)

    def generateClick(self):
        texts = self.__readTexts()
        self.textEdit.setText(texts[randint(0, len(texts) - 1)])

    def startClick(self):
        self.__colorLetter()

    def keyPressEvent(self, event):
        text = self.textEdit.toPlainText()
        if event.text() == text[self.textIndex]:
            self.__colorLetter()
        elif event.text() == text[self.textIndex].upper() and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.__colorLetter()


    def __colorLetter(self):
        text = self.textEdit.toPlainText()
        greenColor = QColor(0, 128, 0)
        blackColor = QColor(0, 0, 0)
        self.textEdit.setText(text[:self.textIndex])

        cursor = self.textEdit.textCursor()

        cursor.setPosition(self.textIndex)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.setTextColor(greenColor)
        self.textEdit.insertPlainText(text[self.textIndex])

        cursor.setPosition(self.textIndex + 1)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.setTextColor(blackColor)
        self.textEdit.insertPlainText(text[self.textIndex + 1:])
        self.textIndex += 1

    @staticmethod
    def __readTexts():
        return open('texts.txt', 'r').read().split('%')


def main():
    app = QApplication([])
    ex = App()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QColor, QTextBlockFormat, QTextCursor
from PyQt6.QtCore import Qt, QTimer
from random import randint
from results import Result
from windows.resultsViewWindow import ResultsViewWindow
from windows.authorWindow import AuthorWindow
from windows.programInfoWindow import ProgramInfoWindow


class MainWindow(QMainWindow):
    """
    Класс MainWindow представляет собой основное окно программы,
    где пользователь осуществляет процесс обучения
    и оценивает свои навыки печати. Позволяет выбирать
    тему и сложность текста для тренировки.
    Класс осуществляет запись результатов в файл.
    """
    textIndex = -1
    isType = False
    isLetterRed = False
    mistakesNum = 0
    timer = QTimer()
    time_elapsed = 0

    def __init__(self):
        super().__init__()
        # Загрузка пользовательского интерфейса из файла main.ui
        uic.loadUi('forms/main.ui', self)
        # Настройка подсказки, выводимой при наведении на QLabel
        self.correctnessLabel.setToolTip('Правильность - процент символов '
                                         'введённых с первого раза')
        self.indent()
        # Чтение текстов из файла
        self.texts = self.readTexts()
        self.updateComboBoxes()

        # Привязка событий к кнопкам и действиям в меню
        self.randomText.clicked.connect(self.randomTextClick)
        self.startEndButton.clicked.connect(self.startEndClick)
        self.timer.timeout.connect(self.updateTime)
        self.showAuthor.triggered.connect(self.showAuthorWindow)
        self.showProgramDetails.triggered.connect(self.showProgramInfoWindow)
        self.resultsAction.triggered.connect(self.showResults)
        self.exitAction.triggered.connect(self.close)

    # Метод обновления выпадающих списков
    def updateComboBoxes(self):
        self.textComplexity.addItem('Начинающий')
        self.textComplexity.addItem('Средний')
        self.textComplexity.addItem('Продвинутый')

        for topic in self.texts.keys():
            self.textTopic.addItem(topic)

    # Метод, вызываемый при нажатии кнопки "Случайный текст"
    def randomTextClick(self):
        texts = self.readTexts()
        topic = self.textTopic.currentText()
        complexity = self.textComplexity.currentText()
        text = texts[topic][complexity][randint(0, len(texts[topic][complexity]) - 1)]
        self.textEdit.setText(text)
        self.indent()

    # Метод, вызываемый при нажатии кнопки "Начать/Закончить"
    def startEndClick(self):
        if not self.isType:
            if self.textEdit.toPlainText():
                self.startTyping()
        else:
            self.stopTyping()

    # Метод начала набора текста
    def startTyping(self):
        self.isType = True
        self.textIndex = -1
        self.mistakesNum = 0
        self.textEdit.setReadOnly(True)
        self.randomText.setEnabled(False)
        self.colorLetter()
        self.resetTimer()
        self.toggleTimer()
        self.startEndButton.setText('Закончить')

    # Метод окончания набора текста
    def stopTyping(self):
        if self.textIndex > 0:
            result = Result(round(self.textIndex / self.time_elapsed * 60),
                            round((((self.textIndex - self.mistakesNum)
                                    / self.textIndex) * 100), 2))
            result.write()
        self.textIndex = -1
        self.isType = False
        self.textEdit.setReadOnly(False)
        self.randomText.setEnabled(True)
        self.resetTimer()
        self.colorLetter()
        self.startEndButton.setText('Начать')

    # Метод переключения таймера
    def toggleTimer(self):
        if not self.timer.isActive():
            self.timer.start(1000)
        else:
            self.timer.stop()

    # Метод обновления времени на экране
    def updateTime(self):
        self.time_elapsed += 1
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        self.timeLabel.setText(f'Время: {minutes}:{seconds:02}')
        self.speedLabel.setText(f'Скорость: '
                                f'{round(self.textIndex / self.time_elapsed * 60)} зн/мин')
        self.correctnessLabel.setText(f'Правильность:')
        if self.textIndex > 0:
            correctness = round((((self.textIndex - self.mistakesNum) / self.textIndex) * 100), 2)
            self.correctnessLabel.setText(self.correctnessLabel.text() +
                                          f'{correctness}%')
        else:
            self.correctnessLabel.setText(self.correctnessLabel.text() + '100%')

    # Метод сброса таймера
    def resetTimer(self):
        self.timer.stop()
        self.time_elapsed = 0

    # Метод обработки событий нажатия клавиш
    def keyPressEvent(self, event):
        if self.isType:
            text = self.textEdit.toPlainText()
            current_char = text[self.textIndex]
            if (
                    event.text() == current_char or
                    (event.key() == Qt.Key.Key_Space and
                     current_char == ' ') or
                    (event.key() == Qt.Key.Key_Return and
                     text[self.textIndex] == '\n')
            ):
                self.colorLetter()
                return
            if (event.key() == Qt.Key.Key_Shift or
                    event.key() == Qt.Key.Key_Alt or
                    event.key() == Qt.Key.Key_Control):
                self.setFocus()
                return
            self.colorLetter(isRightLetter=False)
            self.setFocus()

    # Метод подсветки символов вводимого текста
    def colorLetter(self, isRightLetter=True):
        text = self.textEdit.toPlainText()
        whiteColor = QColor(255, 255, 255)

        if len(text) == self.textIndex + 1 and isRightLetter:
            self.stopTyping()

        if self.isType:
            self.textIndex += isRightLetter

            self.textEdit.setText(text[:self.textIndex])

            cursor = self.textEdit.textCursor()
            cursor.setPosition(self.textIndex)
            self.textEdit.setTextCursor(cursor)

            if isRightLetter:
                greenColor = QColor(0, 255, 0)
                self.textEdit.setTextBackgroundColor(greenColor)
                self.isLetterRed = False
            else:
                redColor = QColor(255, 0, 0)
                self.textEdit.setTextBackgroundColor(redColor)
                if not self.isLetterRed:
                    self.mistakesNum += 1
                    self.isLetterRed = True

            self.textEdit.insertPlainText(text[self.textIndex])

            cursor.setPosition(self.textIndex + 1)
            self.textEdit.setTextCursor(cursor)
            self.textEdit.setTextBackgroundColor(whiteColor)
            self.textEdit.insertPlainText(text[self.textIndex + 1:])

            cursor.setPosition(self.textIndex + 5)
            self.textEdit.setTextCursor(cursor)
        else:
            self.textEdit.setTextBackgroundColor(whiteColor)
            self.textEdit.setText(text)
        self.indent()

    # Метод отображения окна результатов
    def showResults(self):
        self.resultsWindow = ResultsViewWindow()
        self.resultsWindow.show()

    # Метод отображения окна автора
    def showAuthorWindow(self):
        self.authorWindow = AuthorWindow()
        self.authorWindow.show()

    # Метод отображения окна с информацией о программе
    def showProgramInfoWindow(self):
        self.programInfoWindow = ProgramInfoWindow()
        self.programInfoWindow.show()

    # Метод для отступа в текстовом поле
    def indent(self):
        cursor = QTextCursor(self.textEdit.document())
        cursor.select(QTextCursor.SelectionType.Document)
        fmt = QTextBlockFormat()
        fmt.setTextIndent(20)
        cursor.mergeBlockFormat(fmt)

    # Метод для чтения текстов из файла
    @staticmethod
    def readTexts():
        substr = open('files/texts.txt', 'r',
                      encoding='utf-8').read().split('|')
        for i in range(len(substr)):
            if substr[i][-1] == '\n':
                substr[i] = substr[i][:-1]

        texts = {}
        topic = ''
        complexity = ''
        for i in range(len(substr)):
            if substr[i][:6] == 'Topic:':
                topic = substr[i][7:]
                texts[topic] = {}
            elif substr[i][:11] == 'Complexity:':
                complexity = substr[i][12:]
                texts[topic][complexity] = []
            else:
                texts[topic][complexity].append(substr[i])
        return texts

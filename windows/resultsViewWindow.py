from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from results import Result


class ResultsViewWindow(QMainWindow):
    """
    Класс ResultsViewWindow представляет
    окно для просмотра и анализа
    результатов печати пользователя.
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 500)
        self.setWindowTitle("Результаты")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.figure = Figure()

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Чтение результатов и выборка последних 5
        resList = Result.read()
        if len(resList) > 5:
            resList = resList[-5:]

        speedList = []
        correctnessList = []
        dateList = []

        # Формирование списков для построения графиков
        for i in range(len(resList)):
            speedList.append(resList[i].speed)
            dateList.append(resList[i].date.strftime("%H:%M:%S\n%d.%m.%y"))
            correctnessList.append(resList[i].correctness)

        # Первый график - Скорость печати
        self.ax1 = self.figure.add_subplot(121)
        self.ax1.set_xlabel('Дата')
        self.ax1.set_ylabel('Скорость, зн/мин')
        self.ax1.plot(dateList, speedList)

        # Второй график - Правильность печати
        self.ax2 = self.figure.add_subplot(122)
        self.ax2.set_xlabel('Дата')
        self.ax2.set_ylabel('Правильность, %')
        self.ax2.plot(dateList, correctnessList)

        # Настройка общего заголовка и расположения графиков
        self.figure.suptitle('Последние 5 результатов')
        self.figure.subplots_adjust(wspace=0.25)
        self.figure.subplots_adjust(left=0.07, right=0.95, bottom=0.15,
                                    top=0.9)
        self.canvas.draw()

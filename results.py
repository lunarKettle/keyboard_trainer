from datetime import datetime
import pickle


class Result:
    """
    Класс Result представляет результаты печати.
    """
    def __init__(self, speed, correctness):
        self.date = datetime.now()
        self.speed = speed
        self.correctness = correctness

    # Метод для записи результатов в файл
    def write(self, path='files/results.bin'):
        results = self.read()
        results.append(self)
        if len(results) > 5:
            results = results[-5:]
        with open(path, 'wb') as file:
            pickle.dump(results, file)

    # Статический метод для чтения результатов из файла
    @staticmethod
    def read(path='files/results.bin'):
        results = []
        with open(path, 'rb') as file:
            try:
                results = pickle.load(file)
            except EOFError:
                pass
            file.close()
        return results

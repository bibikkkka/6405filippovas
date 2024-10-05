import numpy as np
import pandas as pd
from numpy.matlib import empty
from pytrends.request import TrendReq
import matplotlib.pyplot as plt

class DataAnalysis:
    def __init__(self, keywords, timeframe='today 12-m'):
        self.keywords = keywords
        self.timeframe = timeframe
        self.pytrends = TrendReq()
        self.data = None

    def fetch_data(self):
        self.pytrends.build_payload(self.keywords, timeframe=self.timeframe)
        self.data = self.pytrends.interest_over_time()
        return self.data

    @staticmethod
    def _median(values: np.ndarray, window=3) -> np.ndarray:
        buffer = [0.0 for _ in range (window)]
        filtered = np.zeros_like(values)
        for index, value in enumerate(values):
            # if len(buffer) == window:
            buffer.pop(0)
            buffer.append(value)
            filtered[index] = sorted(buffer)[window // 2]
        return filtered

    def median(self, window=3) -> tuple[np.ndarray, ...]:
        if self.data is None:
            return (np.zeros((1, 1), dtype=float),)
        _, cols = self.data.shape
        data = self.data.values
        return tuple(DataAnalysis._median(data[:, col], window) for col in range(cols))

    @staticmethod
    def _moving_average(values: np.ndarray, window=3) -> np.ndarray:
        buffer = []
        filtered = np.zeros_like(values)
        for index, value in enumerate(values):
            if len(buffer) == window:
                buffer.pop(0)
            buffer.append(value)
            filtered[index] = sum(buffer) / window
        return filtered

    def moving_average(self, window=3) -> tuple[np.ndarray, ...]:
        if self.data is None:
            return (np.zeros((1,1), dtype=float), )

        _, cols = self.data.shape
        data = self.data.values
        return tuple(DataAnalysis._moving_average(data[:, col], window) for col in range(cols))

    def plot_data_with_moving_average(self, window=3):
        if self.fetch_data() is None or self.data.empty:
            print("Нет доступных данных для построения графика.")
            return

        moving_avg = self.moving_average(window=window)
        print("Moving averages:", moving_avg)

        plt.figure(figsize=(12, 6))

        # Оригинальные данные
        plt.plot(self.data.index, self.data[self.data.columns[0]], label='Оригинальные данные', color='blue')

        # Скользящее среднее для каждого столбца
        for idx, avg in enumerate(moving_avg):
            if avg.size > 0:  # Проверяем размерность
                plt.plot(self.data.index[:avg.size], avg, label=f'Скользящее среднее (окно={window})', linestyle='--')

        plt.title('Оригинальные данные и скользящее среднее')
        plt.xlabel('Дата')
        plt.ylabel('Значение')
        plt.legend()
        plt.grid()
        plt.show()


    def plot_data_with_median(self, window=3):
        if self.fetch_data() is None or self.data.empty:
            print("Нет доступных данных для построения графика.")
            return

        median = self.median(window=window)

        plt.figure(figsize=(12, 6))

        # Оригинальные данные
        plt.plot(self.data.index, self.data[self.data.columns[0]], label='Оригинальные данные', color='blue')

        # Скользящее среднее для каждого столбца
        for idx, avg in enumerate(median):
            if avg.size > 0:  # Проверяем размерность
                plt.plot(self.data.index[:avg.size], avg, label=f'Медиана (окно={window})', linestyle='--')

        plt.title('Оригинальные данные и медиана')
        plt.xlabel('Дата')
        plt.ylabel('Значение')
        plt.legend()
        plt.grid()
        plt.show()

    # def moving_average(self, window=3) -> np.ndarray:
    #     if self.data is not empty(self.data.shape):
    #         return np.zeros((1,1), dtype=float)
    #     buffer = []
    #     filtered = np.array(self.data.shape, dtype=float)
    #     for index, value in enumerate(self.data.values):
    #         if len(buffer) == window:
    #             buffer.pop(0)
    #         buffer.append(value)
    #         filtered[index] = sum(buffer) / window
    #     return filtered

    # def moving_average(self, window=3):
        # return self.data.rolling(window=window).mean()

    def calculate_difference(self):
        return self.data.diff()

    def autocorrelation(self, lag=1):
        return self.data.autocorr(lag)

    def find_extrema(self):
        maxima = self.data[(self.data.shift(1) < self.data) & (self.data.shift(-1) < self.data)]
        minima = self.data[(self.data.shift(1) > self.data) & (self.data.shift(-1) > self.data)]
        return maxima, minima

    def save_to_excel(self, filename):
        with pd.ExcelWriter(filename) as writer:
            self.data.to_excel(writer, sheet_name='Original Data')
            self.moving_average().to_excel(writer, sheet_name='Moving Average')
            self.calculate_difference().to_excel(writer, sheet_name='Difference')
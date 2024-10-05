import pandas as pd
from pytrends.request import TrendReq

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

    def moving_average(self, window=3):
        return self.data.rolling(window=window).mean()

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
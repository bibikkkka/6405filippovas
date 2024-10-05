import os
import unittest
from data_analysis.analysis import DataAnalysis


class TestDataAnalysis(unittest.TestCase):

    def setUp(self):
        self.analysis = DataAnalysis(keywords=['Python'])

    def test_fetch_data(self):
        data = self.analysis.fetch_data()
        self.assertIsNotNone(data)

    def test_moving_average(self):
        data = self.analysis.fetch_data()
        ma = self.analysis.moving_average(window=3)
        self.assertEqual(len(ma), len(data))

    def test_save_to_excel(self):
        self.analysis.save_to_excel('test_output.xlsx')
        # Проверяем, был ли создан файл
        self.assertTrue(os.path.exists('test_output.xlsx'))


if __name__ == '__main__':
    unittest.main()
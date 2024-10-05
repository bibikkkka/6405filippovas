# Импорт необходимых библиотек
from data_analysis.analysis import DataAnalysis

# Создание экземпляра класса
analysis = DataAnalysis(keywords=['Python'])

# Получение данных
data = analysis.fetch_data()

# Вычисление скользящего среднего и сохранение результатов в Excel
moving_avg = analysis.moving_average(window=5)
analysis.save_to_excel('data_analysis_results.xlsx')
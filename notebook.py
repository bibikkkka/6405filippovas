from data_analysis.analysis import DataAnalysis

analysis = DataAnalysis(keywords=['Python'])

data = analysis.fetch_data()
print(data)
moving_avg = analysis.moving_average(window=5)

analysis.plot_data_with_median()
analysis.plot_data_with_moving_average()

# analysis.save_to_excel('data_analysis_results.xlsx')
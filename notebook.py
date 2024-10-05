from data_analysis.analysis import DataAnalysis

analysis = DataAnalysis(keywords=['Python'])

data = analysis.fetch_data()

moving_avg = analysis.moving_average(window=5)


analysis.plot_data_with_moving_average(window=5)

# analysis.save_to_excel('data_analysis_results.xlsx')
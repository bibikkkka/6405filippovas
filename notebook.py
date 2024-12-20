from data_analysis.analysis import DataAnalysis

analysis = DataAnalysis(keywords=['Python'])

data = analysis.fetch_data()
print(data)

analysis.save_to_excel('data_analysis_results.xlsx')

moving_avg = analysis.moving_average(window=5)
print("Moving average: ", moving_avg)
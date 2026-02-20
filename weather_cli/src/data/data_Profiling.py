from ydata_profiling import ProfileReport
import pandas as pd
train = pd.read_csv('42-station-meteo-toulouse-parc-compans-cafarelli.csv', sep=';')
prof = ProfileReport(train)
prof.to_file(output_file='rapport.html')
import functions
from pathlib import Path
import pandas as pd
import numpy as np


# Create custom reports and analysis

def create_analysis():
    basepath = Path('.')
    folder_type = str(input('Escolha a pasta para analisar: (Research ou Fleets)')).lower()
    report_path = basepath / 'Reports' / folder_type
    folders_list = functions.find_folders(report_path)
    print(folders_list)

    print('Analysis is running... \n\n')
    for group in folders_list:

        print(f'\n\n ---------------------------- Analyzing the group:        ___ {group} ___ '
              f'----------------------------')
        trip_path = report_path / group / 'viagens'

        trips_df = pd.read_csv(trip_path / 'Resultado.csv', sep=';', encoding='cp1252')
        print('\n\ndescribe: \n', trips_df.describe())

        trips_df['VLPesoCargaBruta'] = trips_df['VLPesoCargaBruta_IN'] + trips_df['VLPesoCargaBruta_OUT']
        trips_df['Prancha'] = trips_df['VLPesoCargaBruta'] / trips_df['TOperacao']

        trips_df = trips_df.astype({'Prancha': float})
        #trips_df = trips_df.copy(deep=True)
        trips_df_nok = trips_df[trips_df['Prancha'].isin([np.nan, np.inf, -np.inf])]
        trips_df_ok = trips_df[~trips_df['Prancha'].isin([np.nan, np.inf, -np.inf])]
        print('\n\ndescribe new nok: \n', trips_df_ok.describe())

        prancha_mean = trips_df_ok.describe()['Prancha']['mean']
        okrecords = trips_df_ok.describe()['Prancha']['count']
        emptyrecords = trips_df_nok.describe()['Prancha']['count']
        totalrows = okrecords + emptyrecords

        # print('\n\n >>>>>>>>>>>>>> \n\n'
        #      'Describe prancha mean    =', round(prancha_mean, 2))

        trips_df_nokc = trips_df_nok.copy(deep=True)
        trips_df_nokc['Prancha'] = round(prancha_mean, 2)

        error_perc = round(emptyrecords / (totalrows + emptyrecords), 4)
        print(f'Percentage of blanks flux records = {error_perc*100} %')

        print('next groups...')

        trips_df_merged = pd.concat([trips_df_nokc, trips_df_ok])

        print('\n\ndescribe merged: \n', trips_df_merged.describe())
        trips_df_merged.to_csv(trip_path / 'Resultado-V2all.csv', index=False, sep=';', encoding='cp1252')

    return print('\n\nDone processing data analysis service.')

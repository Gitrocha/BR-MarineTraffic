import functions
from pathlib import Path


def create_analysis():
    teste = Path('.') / 'Reports'
    print(functions.find_folders(teste))
    return print('Analysis is running...')

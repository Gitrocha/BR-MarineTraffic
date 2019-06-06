import pandas as pd
from pathlib import Path


basepath = Path('.') / 'Main' / 'database'
cargageral = basepath / 'raw' / 'Carga_geral'
cargacont = basepath / 'raw' / 'Carga_cont'

#print(tempospath)

full_loads = {}

for y in range(2010, 2020):

    print(y)

    dfaux = pd.read_csv(cargageral / f'{y}Carga.txt',
                        sep=';',
                        encoding='cp1252').fillna(0)

    dfaux = dfaux.astype({'IDCarga': int})
    '''
                          'IDAtracacao': int,
                          'Origem': str,
                          'Destino': str,
                          'CDMercadoria': str,
                          'Tipo Operação da Carga': str,
                          'Carga Geral Acondicionamento': str,
                          'ConteinerEstado': str,
                          'Tipo Navegação': str,
                          'FlagAutorizacao': str,
                          'FlagCabotagem': int,
                          'FlagCabotagemMovimentacao': int,
                          'FlagConteinerTamanho': int,
                          'FlagLongoCurso': int,
                          'FlagMCOperacaoCarga': int,
                          'FlagOffshore': int,
                          'FlagTransporteViaInterioir': int,
                          'Percurso Transporte em vias Interiores': str,
                          'Percurso Transporte Interiores': str,
                          'STNaturezaCarga': str,
                          'STSH2': str,
                          'STSH4': str,
                          'Natureza da Carga': str,
                          'Sentido': str,
                          'TEU': int,
                          'QTCarga': int,
                          'VLPesoCargaBruta': str})
    '''
    full_loads[y] = dfaux

    '''
    dtype={'IDCarga': int,
                                       'IDAtracacao': int,
                                       'Origem': str,
                                       'Destino': str,
                                       'CDMercadoria': str,
                                       'Tipo Operação da Carga': str,
                                       'Carga Geral Acondicionamento': str,
                                       'ConteinerEstado': str,
                                       'Tipo Navegação': str,
                                       'FlagAutorizacao': str,
                                       'FlagCabotagem': int,
                                       'FlagCabotagemMovimentacao': int,
                                       'FlagConteinerTamanho': int,
                                       'FlagLongoCurso': int,
                                       'FlagMCOperacaoCarga': int,
                                       'FlagOffshore': int,
                                       'FlagTransporteViaInterioir': int,
                                       'Percurso Transporte em vias Interiores': str,
                                       'Percurso Transporte Interiores': str,
                                       'STNaturezaCarga': str,
                                       'STSH2': str,
                                       'STSH4': str,
                                       'Natureza da Carga': str,
                                       'Sentido': str,
                                       'TEU': int,
                                       'QTCarga': int,
                                       'VLPesoCargaBruta': str}
    '''


print('df_cargas all read')
#print(atr_tempos[2010][0:5])

carga_cont = {}

for y in range(2010, 2020):

    print(y)

    dfaux = pd.read_csv(cargacont / f'{y}Carga_Conteinerizada.txt',
                                  sep=';',
                                  encoding='cp1252').fillna(0)

    dfaux = dfaux.astype({'IDCarga': int})

    '''
                          'CDMercadoriaConteinerizada': str,
                          'VLPesoCargaConteinerizada': float})
    '''
    carga_cont[y] = dfaux


    '''
                                  dtype={'IDCarga': int,
                                         'CDMercadoriaConteinerizada': str,
                                         'VLPesoCargaConteinerizada': float}
    '''



print('df_conts read')
#print(atr_info[2010][0:5])

all_loads = {}
for y in range(2010, 2020):

    all_loads[y] = pd.merge(full_loads[y],
                            carga_cont[y],
                            on='IDCarga',
                            how='left')

    print(f'merged year {y}')


df_full = pd.DataFrame()

for y in range(2010, 2020):

    df_full = df_full.append(all_loads[y])

    print(f'appended year {y}')

print('saving dataframe full')
df_full.to_csv(basepath / 'raw' / 'all_loads2.csv', sep=',', encoding='utf-8', index=False)

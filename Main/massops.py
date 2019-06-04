from database import connectors
import sqlite3
import time as t
import random
import pandas as pd
from pathlib import Path


def imo_query():

    conn = sqlite3.connect('./Main/database/data/atr_info.db')

    x = t.time()

    nimo = int(input('\n Insira o Número IMO para gerar relatório: '))

    result = connectors.find_imo_exact(imo=nimo, connection=conn)

    if isinstance(result['Message'], str):
        print(result['Message'])
        rerun = input('Deseja consultar novamente? (S ou N)').lower()
        return rerun

    else:
        df_teste = pd.DataFrame(result['Message'], columns=["IDAtracacao",
                                                            "TEsperaAtracacao",
                                                            "TEsperaInicioOp",
                                                            "TOperacao",
                                                            "TEsperaDesatracacao",
                                                            "TAtracado",
                                                            "TEstadia",
                                                            "CDTUP",
                                                            "IDBerco",
                                                            "Berço",
                                                            "Porto Atracação",
                                                            "Apelido Instalação Portuária",
                                                            "Complexo Portuário",
                                                            "Tipo da Autoridade Portuária",
                                                            "Data Atracação",
                                                            "Data Chegada",
                                                            "Data Desatracação",
                                                            "Data Início Operação",
                                                            "Data Término Operação",
                                                            "Ano",
                                                            "Mes",
                                                            "Tipo de Operação",
                                                            "Tipo de Navegação da Atracação",
                                                            "Nacionalidade do Armador",
                                                            "FlagMCOperacaoAtracacao",
                                                            "Terminal",
                                                            "Município",
                                                            "UF",
                                                            "SGUF",
                                                            "Região Geográfica",
                                                            "Nº da Capitania",
                                                            "Nº do IMO"])

        # print(df_test[0:5])

        basepath = Path('.') / 'relatórios' / 'viagens'

        df_teste.to_csv(basepath / f'viagens_{nimo}.csv', sep=';', encoding='cp1252', index=False)

        conn.close()

        y = t.time()

        print('\n Finalizado. Tempo total de consulta = ', round((y-x), 3), 'segundos')

        rerun = input('Deseja consultar novamente? (S ou N):').lower()
        return rerun


retorno = imo_query()
while retorno == 's':
    retorno = imo_query()
    print('Executando consultas novamente. (Aperte CTRL+C para sair.) \n')

print('Consultas Finalizadas.')
t.sleep(5)

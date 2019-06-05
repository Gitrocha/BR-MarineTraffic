from database import connectors
import sqlite3
import time as t
import pandas as pd
from pathlib import Path
import sys


def print_exception():
    import linecache
    import sys
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    message = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    return message


def imo_query():

    conn = sqlite3.connect('./Main/database/data/atr_info.db')

    try:
        nimo = int(input('\n Insira o Número IMO para gerar relatório (Ou zero para outras consultas): '))
    except:
        print('\n Entrada inválida, digite o número IMO apenas.')
        return 's'

    x = t.time()
    if nimo == 0:
        result = connectors.find_imo_blank(connection=conn)
    else:
        result = connectors.find_imo_exact(imo=nimo, connection=conn)
    y = t.time()
    conn.close()

    if isinstance(result['Message'], str):
        print(result['Message'])
        rerun = input('Deseja consultar novamente? (S ou N): ').lower()
        return rerun

    else:
        print('\n Consulta concluída...')
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

        basepath = Path('.') / 'Reports' / 'viagens'

        print('\n Salvando dados...')
        df_teste.to_csv(basepath / f'viagens_IMO-{nimo}.csv', sep=';', encoding='cp1252', index=False)

        print('\n Finalizado. Tempo total de consulta = ', round((y-x), 2), 'segundos')

        rerun = input('\n Deseja consultar novamente? (S ou N):  ').lower()
        return rerun


def cap_query():

    conn = sqlite3.connect('./Main/database/data/atr_info.db')

    try:
        nimo = int(input('\n Insira o Número da Capitania para gerar relatório (Ou zero para outras consultas): '))
    except:
        print('\n Entrada inválida, digite o número da Capitania apenas.')
        return 's'

    x = t.time()
    if nimo == 0:
        result = connectors.find_imo_blank(connection=conn)
    else:
        result = connectors.find_imo_exact(imo=nimo, connection=conn)
    y = t.time()
    conn.close()

    if isinstance(result['Message'], str):
        print(result['Message'])
        rerun = input('Deseja consultar novamente? (S ou N): ').lower()
        return rerun

    else:
        print('\n Consulta concluída...')
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

        basepath = Path('.') / 'Reports' / 'viagens'

        print('\n Salvando dados...')
        df_teste.to_csv(basepath / f'viagens_CAPT-{nimo}.csv', sep=';', encoding='cp1252', index=False)

        print('\n Finalizado. Tempo total de consulta = ', round((y-x), 2), 'segundos')

        rerun = input('\n Deseja consultar novamente? (S ou N):  ').lower()
        return rerun


def imo_loop():

    retorno = 's'
    while retorno == 's':
        try:
            retorno = imo_query()
        except:
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            print(errormsg)
            print(print_exception())
            retorno = 'n'

        if retorno == 's':
            print('\n Executando consultas novamente. (Aperte CTRL+C para sair.) \n')
        else:
            print('\n Consultas Finalizadas.')

    t.sleep(3)


def cap_loop():
    retorno = 's'
    while retorno == 's':
        try:
            retorno = cap_query()
        except:
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            print(errormsg)
            print(print_exception())
            retorno = 'n'

        if retorno == 's':
            print('\n Executando consultas novamente. (Aperte CTRL+C para sair.) \n')
        else:
            print('\n Consultas Finalizadas.')

    t.sleep(3)


switch = 0

while switch == 0:

    switch = str(input('\n Insira o tipo de busca (IMO ou CAPITANIA): ')).lower()

    if switch == 'imo':
        imo_loop()
    elif switch == 'capitania':
        cap_loop()
    elif switch == 'sair':
        break
    else:
        print("\n Entrada inválida. Digite 'IMO' ou 'CAPITANIA' para iniciar ou 'SAIR' para fechar a tela.")
        switch = 0

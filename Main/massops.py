from database import connectors
import sqlite3
import time as t
import pandas as pd
from pathlib import Path
import sys
from os import mkdir

# Consultas de info na DB
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


def loads_query(list):
    conn = sqlite3.connect('./Main/database/data/atr_info.db')
    result = connectors.find_load_exact(loadid=list, connection=conn)


    df_trips = pd.DataFrame(result['Message'], columns=["IDCarga",
                                                        "IDAtracacao",
                                                        "Origem",
                                                        "Destino",
                                                        "CDMercadoria",
                                                        "Tipo Operação da Carga",
                                                        "Carga Geral Acondicionamento",
                                                        "ConteinerEstado",
                                                        "Tipo Navegação",
                                                        "FlagAutorizacao",
                                                        "FlagCabotagem",
                                                        "FlagCabotagemMovimentacao",
                                                        "FlagConteinerTamanho",
                                                        "FlagLongoCurso",
                                                        "FlagMCOperacaoCarga",
                                                        "FlagOffshore",
                                                        "FlagTransporteViaInterioir",
                                                        "Percurso Transporte em vias Interiores",
                                                        "Percurso Transporte Interiores",
                                                        "STNaturezaCarga",
                                                        "STSH2",
                                                        "STSH4",
                                                        "Natureza da Carga",
                                                        "Sentido",
                                                        "TEU",
                                                        "QTCarga",
                                                        "VLPesoCargaBruta",
                                                        "CDMercadoriaConteinerizada",
                                                        "VLPesoCargaCont"])

    #print('Result', result['Message'])
    #df_trips=pd.DataFrame()
    return df_trips


def imo_query():

    try:
        nimo = int(input('\n Insira o Número IMO para gerar relatório (Ou zero para outras consultas): '))
    except:
        print('\n Entrada inválida, digite o número IMO apenas.')
        return 's'

    conn = sqlite3.connect('./Main/database/data/atr_info.db')
    basepath = Path('.') / 'Reports' / f'IMO-{nimo}'

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
        print('\n Consulta de navio concluída. Iniciando consulta por cargas...')
        df_trips = pd.DataFrame(result['Message'], columns=["IDAtracacao",
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

        print('head', df_trips.head())
        print('col', df_trips['IDAtracacao'].head())

        df_aux = df_trips['IDAtracacao'].copy(deep=True)
        print('aux1', df_aux.head())

        df = df_aux.drop_duplicates(keep='first')
        print('aux2', df.head())

        idatr_list = df.values.tolist()
        #print('list', idatr_list)
        #idatr_list = [8049372, 23338048]

        u = t.time()
        df_loads = loads_query(list=idatr_list)
        v = t.time()
        print(df_loads.head())

        try:
            mkdir(basepath)
            mkdir(basepath / 'viagens')
            mkdir(basepath / 'cargas')
        except:
            print('Pasta Já existe')
            return 's'

        print('\n Salvando dados...')

        df_trips.to_csv(basepath / 'viagens' / f'Viagens-{nimo}.csv', sep=';', encoding='cp1252', index=False)
        df_loads.to_csv(basepath / 'cargas' / f'Cargas-{nimo}.csv', sep=';', encoding='cp1252', index=False)
        print('\n Finalizado. Tempo total de consulta IMO = ', round((y-x), 2), 'segundos')
        print('\n Tempo total de consulta de viagens = ', round((v - u), 2), 'segundos')
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


def ploads_query():

    try:
        codport = str(input('\n Insira o código do porto para gerar relatório): '))
    except:
        print('\n Entrada inválida, digite o código do porto apenas.')
        return 's'

    conn = sqlite3.connect('./Main/database/data/atr_info.db')
    basepath = Path('.') / 'Reports' / f'Porto-{codport}'

    x = t.time()
    if codport == 0:
        return 'n'
    else:
        result = connectors.find_port_loads(portid=codport, connection=conn)
    y = t.time()
    conn.close()

    if isinstance(result['Message'], str):
        print(result['Message'])
        rerun = input('Deseja consultar novamente? (S ou N): ').lower()
        return rerun

    else:
        print('\n Consulta de navio concluída. Iniciando consulta por cargas...')
        df_trips = pd.DataFrame(result['Message'], columns=["IDCarga",
                                                            "IDAtracacao",
                                                            "Origem",
                                                            "Destino",
                                                            "CDMercadoria",
                                                            "Tipo Operação da Carga",
                                                            "Carga Geral Acondicionamento",
                                                            "ConteinerEstado",
                                                            "Tipo Navegação",
                                                            "FlagAutorizacao",
                                                            "FlagCabotagem",
                                                            "FlagCabotagemMovimentacao",
                                                            "FlagConteinerTamanho",
                                                            "FlagLongoCurso",
                                                            "FlagMCOperacaoCarga",
                                                            "FlagOffshore",
                                                            "FlagTransporteViaInterioir",
                                                            "Percurso Transporte em vias Interiores",
                                                            "Percurso Transporte Interiores",
                                                            "STNaturezaCarga",
                                                            "STSH2",
                                                            "STSH4",
                                                            "Natureza da Carga",
                                                            "Sentido",
                                                            "TEU",
                                                            "QTCarga",
                                                            "VLPesoCargaBruta",
                                                            "CDMercadoriaConteinerizada",
                                                            "VLPesoCargaCont"])


        try:
            mkdir(basepath)

        except:
            print('Pasta Já existe')
            return 's'

        print('\n Salvando dados...')

        df_trips.to_csv(basepath / f'Movimentos-{codport}.csv', sep=';', encoding='cp1252', index=False)
        print('\n Finalizado. Tempo total de consulta de movimentos de cargas = ', round((y-x), 2), 'segundos')
        rerun = input('\n Deseja consultar novamente? (S ou N):  ').lower()
        return rerun


# Front Loops
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


def portload_loop():

    retorno = 's'
    while retorno == 's':
        try:
            retorno = ploads_query()
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


def portships_loop():

    retorno = 's'
    while retorno == 's':
        try:
            retorno = pship_query()
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


switch_ship = 0
switch_mode = 0
switch_port = 0

switch_mode = str(input("\n Deseja buscar portos ou navios? (digite 'portos' ou 'navios' para continuar): ")).lower()

if switch_mode == 'navios':

    while switch_ship == 0:

        switch_ship = str(input('\n Insira o tipo de busca (IMO ou CAPITANIA): ')).lower()

        if switch_ship == 'imo':
            imo_loop()
        elif switch_ship == 'capitania':
            cap_loop()
        elif switch_ship == 'sair':
            break
        else:
            print("\n Entrada inválida. Digite 'IMO' ou 'CAPITANIA' para iniciar ou 'SAIR' para fechar a tela.")
            switch_ship = 0

elif switch_mode == 'portos':

    while switch_port == 0:

        switch_port = str(input("\n Insira o tipo de busca (Digite 'cargas' ou 'navios'): ")).lower()

        if switch_port == 'cargas':
            portload_loop()
        elif switch_port == 'navios':
            portships_loop()
        elif switch_port == 'sair':
            break
        else:
            print("\n Entrada inválida. Digite 'Cargas' ou 'Navios' para iniciar ou 'SAIR' para fechar a tela.")
            switch_port = 0

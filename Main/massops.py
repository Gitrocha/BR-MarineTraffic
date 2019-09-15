from database import connectors
import sqlite3
import time as t
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from os import mkdir
from analysis import metrics


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

    return df_trips


def imo_query():

    try:
        nimo = int(input('\n Insira o Número IMO para gerar relatório (Ou zero para outras consultas): '))
    except:
        print('\n Entrada inválida, digite o número IMO apenas.')
        return 's'

    print('\n Salvando dados...')

    x = t.time()
    conn = sqlite3.connect('./Main/database/data/atr_info.db')
    if nimo == 0:
        result = connectors.find_imo_blank(connection=conn)
    else:
        result = connectors.find_imo_exact(imo=nimo, connection=conn)
    conn.close()
    y = t.time()

    if isinstance(result['Message'], str):
        print('Result Message: \n', result['Message'])
        rerun = input('Deseja consultar novamente? (S ou N): ').lower()
        return rerun

    else:

        try:
            basepath = Path('.') / 'Reports' / f'IMO-{nimo}'
            print('Organizando diretórios.')
            mkdir(basepath)
            mkdir(basepath / 'viagens')
            mkdir(basepath / 'cargas')
        except:
            print('Pasta Já existe')
            return 's'

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

        # ----------- Create report metrics ---------------------------------
        df_trips = df_trips[["IDAtracacao",
                             "TEsperaAtracacao",
                             "TEsperaInicioOp",
                             "TOperacao",
                             "TEsperaDesatracacao",
                             "TAtracado",
                             "TEstadia",
                             "Porto Atracação",
                             "Data Atracação",
                             "Data Chegada",
                             "Data Desatracação",
                             "Data Início Operação",
                             "Data Término Operação",
                             "Tipo de Operação",
                             "Tipo de Navegação da Atracação",
                             "SGUF",
                             "Nº da Capitania",
                             "Nº do IMO"]]

        df_trips = df_trips.rename(columns={
            'Porto Atracação': "Porto",
            'Data Atracação': 'Atracado',
            'Data Chegada': 'Chegada',
            'Data Desatracação': 'Desatracado',
            'Data Início Operação': 'InicioOp',
            'Data Término Operação': 'FimOp',
            'Tipo de Navegação da Atracação': 'TipoNav',
            'SGUF': 'UF',
            'Nº da Capitania': 'Capitania',
            'Nº do IMO': 'IMO'})

        df_trips = df_trips.astype({'IDAtracacao': str,
                                    'TEsperaAtracacao': float,
                                    'TEsperaInicioOp': float,
                                    'TOperacao': float,
                                    'TEsperaDesatracacao': float,
                                    'TAtracado': float,
                                    'TEstadia': float,
                                    'Porto': str,
                                    'Atracado': str,
                                    'Chegada': str,
                                    'Desatracado': str,
                                    'InicioOp': str,
                                    'FimOp': str,
                                    'TipoNav': str,
                                    'UF': str,
                                    'Capitania': str,
                                    'IMO': int})

        prancha = 0
        tope = 1
        tatr = 2
        tesp = 3
        vmed = 4
        load = 5

        filename = basepath / 'resumo.txt'
        with open(filename, 'w+') as reports:
            reports.write(f'Prancha média: {prancha}\n')
            reports.write(f'Tempo médio de operação: {tope}\n')
            reports.write(f'Tempo médio de atracação: {tatr}\n')
            reports.write(f'Tempo médio de espera: {tesp}\n')
            reports.write(f'Velocidade média: {vmed}\n')
            reports.write(f'Carga média transportada: {load}\n')

        # ----------- Loads report generation -------------------------------

        print('\n Consulta de navio concluída. Iniciando consulta por cargas...')

        df_aux = df_trips['IDAtracacao'].copy(deep=True)
        print('aux1', df_aux.head())

        df = df_aux.drop_duplicates(keep='first')
        print('aux2', df.head())

        idatr_list = df.values.tolist()

        u = t.time()
        df_loads = loads_query(list=idatr_list)
        v = t.time()
        print(df_loads.head())

        # -------------- Saving DFs to disk ------------------------

        df_trips.to_csv(basepath / 'viagens' / f'Viagens-{nimo}.csv', sep=';', encoding='cp1252', index=False)
        df_loads.to_csv(basepath / 'cargas' / f'Cargas-{nimo}.csv', sep=';', encoding='cp1252', index=False)
        print('\n Finalizado. Tempo total de consulta IMO = ', round((y-x), 2), 'segundos')
        print('\n Tempo total de consulta de viagens = ', round((v - u), 2), 'segundos')
        rerun = input('\n Deseja consultar novamente? (S ou N):  ').lower()
        return rerun


def imolist_query(nimo, name):


    # System Inputs

    #try:
    #    nimo = input('\n Insira os Números IMO, separados por vírgula, para gerar relatório (Ou zero para outras consultas): ')
    #except:
    #    print('\n Entrada inválida, digite o número IMO apenas.')
    #    return 's'

    print('\n Salvando dados...')

    # System Query

    x = t.time()
    conn = sqlite3.connect('./Main/database/data/atr_info.db')

    if nimo == 0:
        result = connectors.find_imo_blank(connection=conn)
    else:
        print(nimo)
        result = connectors.find_imolist_exact(imolist=nimo, connection=conn)
        #{'Status': 'ok', 'Message': result}

    conn.close()
    y = t.time()

    # System Reports

    if isinstance(result['Message'], str):
        # {'Status': 'ok', 'Message': 'Ship not found'}
        print('Result Message: \n', result['Message'])
        rerun = input('Deseja consultar novamente? (S ou N): ').lower()
        return rerun

    else:
        # {'Status': 'ok', 'Message': [List of ships]}
        # Load json in Pandas DF
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

        # ----------- Create report metrics ---------------------------------
        # Slice dataframe columns
        df_trips = df_trips[["IDAtracacao",
                             "TEsperaAtracacao",
                             "TEsperaInicioOp",
                             "TOperacao",
                             "TEsperaDesatracacao",
                             "TAtracado",
                             "TEstadia",
                             "Porto Atracação",
                             "Data Atracação",
                             "Data Chegada",
                             "Data Desatracação",
                             "Data Início Operação",
                             "Data Término Operação",
                             "Tipo de Operação",
                             "Tipo de Navegação da Atracação",
                             "SGUF",
                             "Nº da Capitania",
                             "Nº do IMO"]]
        df_trips = df_trips.rename(columns={
            'Porto Atracação': "Porto",
            'Data Atracação': 'Atracado',
            'Data Chegada': 'Chegada',
            'Data Desatracação': 'Desatracado',
            'Data Início Operação': 'InicioOp',
            'Data Término Operação': 'FimOp',
            'Tipo de Navegação da Atracação': 'TipoNav',
            'SGUF': 'UF',
            'Nº da Capitania': 'Capitania',
            'Nº do IMO': 'IMO'})
        # Set datatypes of df columns
        df_trips = df_trips.astype({'IDAtracacao': int,
                                    'TEsperaAtracacao': float,
                                    'TEsperaInicioOp': float,
                                    'TOperacao': float,
                                    'TEsperaDesatracacao': float,
                                    'TAtracado': float,
                                    'TEstadia': float,
                                    'Porto': str,
                                    'Atracado': str,
                                    'Chegada': str,
                                    'Desatracado': str,
                                    'InicioOp': str,
                                    'FimOp': str,
                                    'TipoNav': str,
                                    'UF': str,
                                    'Capitania': str,
                                    'IMO': int})
        # Collect report metrics
        # tespatr = round(df_trips['TEsperaAtracacao'].mean(), 2)
        # tespop = round(df_trips['TEsperaInicioOp'].mean(), 2)
        # tope = round(df_trips['TOperacao'].mean(), 2)
        # tatr = round(df_trips['TAtracado'].mean(), 2)
        # tespdatr = round(df_trips['TEsperaDesatracacao'].mean(), 2)
        # testad = round(df_trips['TEstadia'].mean(), 2)

        # ----------- Loads report generation -------------------------------
        print('\n Consulta de navio concluída. Iniciando consulta por cargas...')
        # Add later - generate loads tables
        df_aux = df_trips['IDAtracacao'].copy(deep=True)
        df = df_aux.drop_duplicates(keep='first')
        idatr_list = df.values.tolist()
        # Run query of loads from shiplist history
        print(' List of trips generated. Searching trips in database.')
        u = t.time()
        df_loads = loads_query(list=idatr_list)
        v = t.time()
        print(' Query finished.')
        # Slice loads dataframe columns
        df_loads = df_loads[['IDCarga',
                             'IDAtracacao',
                             'Origem',
                             'Destino',
                             'Tipo Operação da Carga',
                             'Natureza da Carga',
                             'Sentido',
                             'TEU',
                             'QTCarga',
                             'VLPesoCargaBruta',
                             'CDMercadoriaConteinerizada',
                             'VLPesoCargaCont']]
        # Set loads df datatypes
        df_loads = df_loads.astype({'IDCarga': str,
                                    'IDAtracacao': int,
                                    'Origem': str,
                                    'Destino': str,
                                    'Tipo Operação da Carga': str,
                                    'Natureza da Carga': str,
                                    'Sentido': str,
                                    'TEU': int,
                                    'QTCarga': int,
                                    'VLPesoCargaBruta': float,
                                    'CDMercadoriaConteinerizada': str,
                                    'VLPesoCargaCont': str})

        # -------------- Create merged DF -----------
        df_loadsinfo = df_loads.pivot_table(['VLPesoCargaBruta'], ['IDAtracacao'], aggfunc='sum')
        print(' Pivot Table - Sum of loads by trips: \n')
        #print(df_loadsinfo)

        #df_loadsinfo.astype()
        print(' Creating final report.')
        result_merge = pd.merge(df_trips,
                                df_loadsinfo,
                                on='IDAtracacao',
                                how='outer')

        # result_merge['Prancha'] = result_merge['VLPesoCargaBruta'] / result_merge['TOperacao']

        # print(result_merge[result_merge['Prancha'] == 'inf'])

        #result_merge = pd.read_csv(Path('.') / f'Teste.csv', sep=';', encoding='cp1252')

        #result_filtered = result_merge[~result_merge.isin([np.nan, np.inf, -np.inf]).any(1)]
        # print('Result merge before \n', result_filtered[:5])

        # df_trips['MovCargaTot'] =

        # -------------- Saving tables queries ------------------------

        # Print graphics

        # result_filtered = result_filtered.astype({'Prancha': float})

        #max = result_filtered['Prancha'].max()
        #maxrange = int(result_filtered.Prancha.std(axis=0, skipna=True))
        #auxmean = int(result_filtered.Prancha.mean()/25)
        #print(maxrange)

        #result_filtered['Prancha'].hist(bins=[x for x in range(0, maxrange, auxmean)], alpha=0.5, color='green')
        #plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        #plt.show()
        basepath = Path('.') / 'Reports' / f'IMO-Fleet-{name}'

        print(' Organizando diretório de viagens.')
        try:
            mkdir(basepath)
            mkdir(basepath / 'viagens')
            #plt.savefig(basepath / f'Prancha-Hist-{name}.png')
            #df_trips.to_csv(basepath / 'viagens' / f'Viagens-{nimo}.csv', sep=';', encoding='cp1252', index=False)
            result_merge.to_csv(basepath / 'viagens' / f'Resultado.csv', sep=';', encoding='cp1252', index=False)
        except:
            print('Pasta Já existe')
            return 'n'
        print(' Organizando diretório de cargas.')
        try:
            mkdir(basepath / 'cargas')
            df_loads.to_csv(basepath / 'cargas' / f'Cargas.csv', sep=';', encoding='cp1252', index=False)
        except:
            print('Pasta Já existe')
            return 's'

        # -------------- Saving reports to disk -----------

        '''
        print(' Creating report of traffic KPIs.')
        filename = basepath / 'resumo de viagens.txt'
        with open(filename, 'w+') as reports:

            #tespatr = 0
            #tespop = 0
            #tope = 0
            #tatr = 0
            #tespdatr = 0
            #testad = 0

            reports.write('----------- RESUMO DAS VIAGENS DA FROTA ------- \n')
            reports.write('\n')
            reports.write('----------- TEMPOS MÉDIOS --------------------- \n')
            reports.write(f'Tempo médio de espera de atracação: {tespatr} horas\n')
            reports.write(f'Tempo médio de operação: {tope} horas\n')
            reports.write(f'Tempo médio de atracação: {tatr} horas\n')
            reports.write(f'Tempo médio de espera de inicio de operação: {tespop} horas\n')
            reports.write(f'Tempo médio de espera de desatracaçao: {tespdatr} horas\n')
            reports.write(f'Tempo médio de estadia: {testad} horas\n')
            reports.write(f'\n')
            reports.write('----------- MAIS ESTATÍSTICAS DA AMOSTRA ----------- \n')
            reports.write(f'Tempo máximo de espera de atracação: {tespatr} horas\n')
            reports.write(f'Tempo mínimo de operação: {tope} horas\n')
            reports.write(f'Desvio padrão de atracação: {tatr} horas\n')
            reports.write(f'Tempo médio de espera de inicio de operação: {tespop} horas\n')
            reports.write(f'Tempo médio de espera de desatracaçao: {tespdatr} horas\n')
            reports.write(f'Tempo médio de estadia: {testad} horas\n')
        '''

        #y = 3
        #x = 2
        #v = 6
        #u = 4
        print('\n Finalizado. Tempo total de consulta IMO = ', round((y-x), 2), 'segundos')
        print('\n Tempo total de consulta de viagens = ', round((v - u), 2), 'segundos')
        # rerun = input('\n Deseja consultar novamente? (S ou N):  ').lower()
        #return rerun


def imo_multilist_query():

    with open(Path('Inputs') / 'fleets.txt', 'r') as inputfile:
        list_of_groups = []
        group_names = []
        for line in inputfile:
            #print('line:', line)
            split = line.split(';', 1)
            #print('split:', split)

            header = split[0]
            #print('header:', header)
            group_names.append(header)
            tail = split[1]
            #print('tail:', tail)
            list_of_groups.append(tail)

    print('tails', list_of_groups)
    print('headers', group_names)

    list_of_groups = [list.replace('\n', '') for list in list_of_groups]

    print('tails clean', list_of_groups)

    xid = 0
    iters = len(group_names)
    for group in range(iters):

        imo = list_of_groups[xid]
        print(imo)
        name = group_names[xid]
        print(name)
        imolist_query(nimo=imo, name=name)
        xid += 1

    return True


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
        #try:
        retorno = imo_query()
        #except:
        #    errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
        #               str(sys.exc_info()[2])
        #    print(errormsg)
        #    print(print_exception())
        #    retorno = 'n'

        if retorno == 's':
            print('\n Executando consultas novamente. (Aperte CTRL+C para sair.) \n')
        else:
            print('\n Consultas Finalizadas. Encerrando aplicação. \n')
            print(' ...')

    t.sleep(3)


def imolist_loop():

    retorno = 's'
    while retorno == 's':
        #try:
        retorno = imolist_query()
        #except:
        #    errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
        #               str(sys.exc_info()[2])
        #    print(errormsg)
        #    print(print_exception())
        #    retorno = 'n'

        if retorno == 's':
            print('\n Executando consultas novamente. (Aperte CTRL+C para sair.) \n')
        else:
            print('\n Consultas Finalizadas. Encerrando aplicação. \n')
            print(' ...')

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
            print('\n Consultas Finalizadas. Encerrando aplicação. \n')
            print(' ...')
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
            print('\n Consultas Finalizadas. Encerrando aplicação. \n')
            print(' ...')
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
            print('\n Consultas Finalizadas. Encerrando aplicação. \n')
            print(' ...')
    t.sleep(3)


# Web components
def start_local(switch_mode):

    #switch_mode = str(input("\n Deseja buscar portos ou navios? (digite 'portos' ou 'navios' para continuar): ")).lower()

    # shortcut test code
    #switch_mode = 'navios'

    if switch_mode == 'navios':

        switch_ship = 0
        while switch_ship == 0:

            switch_ship = str(input('\n Insira o tipo de execução IMO, ARQUIVO ou ANALISE: ')).lower()
            # shortcut test mode
            #switch_ship = 'analise'

            if switch_ship == 'imo':
                imo_loop()
            elif switch_ship == 'capitania':
                cap_loop()

            elif switch_ship == 'lista':
                imolist_loop()

            elif switch_ship == 'sair':
                break

            elif switch_ship == 'arquivo':
                imo_multilist_query()
                switch_ship = 0

            elif switch_ship == 'analise':
                metrics.create_analysis()
                switch_ship = True

            else:
                print("\n Entrada inválida. Digite 'IMO' ou 'CAPITANIA' para iniciar ou 'SAIR' para fechar a tela.")
                switch_ship = 0

    elif switch_mode == 'portos':

        switch_port = 0
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


start_local(switch_mode='navios')

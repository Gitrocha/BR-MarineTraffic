import pandas as pd
from pathlib import Path


basepath = Path('.') / 'Main' / 'database' / 'raw' / 'all_loads.csv'
df = pd.read_csv(basepath, sep=',')
nocont = df[df['Natureza da Carga'] != 'Carga Conteinerizada'][0:10]
cont = df[df['Natureza da Carga'] == 'Carga Conteinerizada'][0:10]

nocont.to_csv(Path('.') / 'Main' / 'database' / 'raw' / 'nocont.csv', sep=';', index=False)
cont.to_csv(Path('.') / 'Main' / 'database' / 'raw' / 'cont.csv', sep=';', index=False)


(20988397,
 900859,
 'BRSSO',
 'BRSUA',
 2710,
 'Movimentação de Carga',
 0,
 0,
 'Cabotagem',
 'S',
 1,
 1,
 0,
 0,
 1,
 0,
 0,
 0,
 0,
 'Exclusivo',
 'Exclusivo',
 'Exclusivo',
 'Granel Líquido e Gasoso',
 'Desembarcados',
 0, 0,
 118
75,
'',
''),

(20988398,
 900859,
 'BRSSZ',
 'BRSUA',
 2710,
 'Transbordo',
 0,
 0,
 'Cabotagem',
 'S',
 1,
 1,
 0,
 0,
 1,
 0,
 0,
 0,
 0,

 'Exclusivo',
 'Exclusivo',
 'Exclusivo',
 'Granel Líquido e Gasoso',
 'Desembarcados',
 0,
 0,
 11418,
 '',
 ''),

(22537317,
 941
672,
'BRSUA',
'BRMAO',
2710,
'Cabotagem',
0,
0,
'Cabotagem',
'S',
0,
1,
0,
0,
1,
0,
0,
0,
0,
'Exclusivo',
'Exclusivo',
'
Exclusivo','
' 'Granel Líquido e Gasoso','
' 'Embarcados','
' 0,'
' 0,'
' '13144,
899','
' '','
' '')]





























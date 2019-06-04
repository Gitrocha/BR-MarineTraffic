from database import connectors
import sqlite3
import time as t
import random


atra = {}
atra['idatr'] = 977343
atra['tespatr'] = 1.0999999999185
atra['tespin'] = 5.0000000000582
atra['top'] = 37.250000000058
atra['tespout'] = 8.8333333333139
atra['ttot'] = 51.08333333343
atra['testad'] = 52.183333333349


conn = sqlite3.connect('./Main/database/data/tempos_atr.db')

x = t.time()

'''
for i in range(100):

    atra['idatr'] = i
    result = connectors.add_data(atr=atra, connection=conn)
    print(i)
'''

counter = 0

for i in range(10):

    id = random.randint(880000,920000)
    result = connectors.find_atr_exact(atrid=id, connection=conn)
    print(result)
    counter+=1
    #t.sleep(0.5)

conn.close()

y = t.time()


print('\n Estimated time per query = ', round((y-x)/10, 3), ' seconds')

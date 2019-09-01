import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path


fname = Path('.') / 'Inputs' / 'Brasil' / 'BRUFE250GC_SIR.shp'
world = gpd.read_file(fname)
world.plot()
plt.show()

'''
Path('.') / 'Inputs' / 'BRUFE250GC_SIR'
'''
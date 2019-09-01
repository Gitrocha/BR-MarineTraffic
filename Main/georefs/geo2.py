import geopandas as gpd
import matplotlib.pyplot as plt


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.plot()
plt.show()

'''
Path('.') / 'Inputs' / 'BRUFE250GC_SIR'
'''
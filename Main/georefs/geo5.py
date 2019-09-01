import geopandas as gpd
import matplotlib.pyplot as plt


# Create basemap
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create second layer of city points
cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
cities = cities.to_crs(world.crs)

# Create world plot and add second layer
base = world.plot(color='white', edgecolor='black')
cities.plot(ax=base, marker='o', color='green', markersize=5)


# Show plot of the world
plt.show()

'''
Path('.') / 'Inputs' / 'BRUFE250GC_SIR'
'''
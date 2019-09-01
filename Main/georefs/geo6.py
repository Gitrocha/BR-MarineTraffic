import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
from pathlib import Path


# Create basemap
fname = Path('.') / 'Inputs' / 'Brasil' / 'BRUFE250GC_SIR.shp'
pointfolder = Path('.') / 'Inputs'

#world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = gpd.read_file(fname)

# Create second layer of city points
cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
cities = cities.to_crs(world.crs)

# Create world plot and add second layer
base = world.plot(color='white', edgecolor='black')
#cities.plot(ax=base, marker='o', color='green', markersize=5)

# Create a geodataframe using pandas and shapely objects
'''df = pd.DataFrame(
    {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
     'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
     'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
     'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})
'''

df = pd.read_csv(pointfolder / 'Municipios.csv', sep=';', encoding='cp1252')
print(df.head())
print(df.Latitude.head())
points = [Point(x, y) for x, y in zip(df.Longitude, df.Latitude)]
print(points)

gdf = gpd.GeoDataFrame(df, geometry=points)

# We restrict to South America.
#ax2 = world[world.continent == 'South America'].plot(
#    color='white', edgecolor='black')

# We can now plot our GeoDataFrame.
gdf.plot(ax=base, color='red')

# Show plot of the world and America
plt.show()

'''
Path('.') / 'Inputs' / 'BRUFE250GC_SIR'
'''
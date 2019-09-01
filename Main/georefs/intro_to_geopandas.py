import geopandas as gpd 
import matplotlib.pyplot as plt

# Importing and plotting the cities shapefile 
cities = gpd.read_file('C:/Geopandas Tutorials/Belgium/belgian_cities.shp')
cities.plot(cmap = 'jet', column = 'NAME_4', figsize = (15,15))

# Importing and plotting AOI shapefile
AOI = gpd.read_file('C:/Geopandas Tutorials/Belgium/area_of_interest_.shp')
AOI.plot()

# Display both shapefiles together
fig, ax = plt.subplots(1)
cities.plot(ax=ax, cmap = 'rainbow', column = 'NAME_4')
AOI.plot(ax=ax, facecolor = 'yellow')

# Intersecting 
cities_in_AOI = gpd.overlay(cities, AOI, how = 'intersection')
cities_in_AOI.plot(figsize = (10,10), cmap = 'winter',column = 'NAME_4')

#Assigning a new column - Area
cities_in_AOI['Area(km2)'] = cities_in_AOI.area/1000000

# Save the geodataframe to a .shp (Shapefile)
cities_in_AOI.to_file('C:/Geopandas Tutorials/Belgium/intersected_cities.shp')

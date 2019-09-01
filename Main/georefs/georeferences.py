import cartopy.crs as ccrs
import matplotlib.pyplot as plt


ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()

ny_lon, ny_lat = -75, 43
delhi_lon, delhi_lat = 77.23, 28.61

plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
         color='blue', linewidth=2, marker='o',
         transform=ccrs.Geodetic(),
         )

plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
         color='gray', linestyle='--',
         transform=ccrs.PlateCarree(),
         )

plt.text(ny_lon - 3, ny_lat - 12, 'New York',
         horizontalalignment='right',
         transform=ccrs.Geodetic())

plt.text(delhi_lon + 3, delhi_lat - 12, 'Delhi',
         horizontalalignment='left',
         transform=ccrs.Geodetic())

plt.show()


'''
#!/usr/bin/env python

import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from pylab import imread

im = imread('Robinson-projection.jpg')
ax = plt.axes(projection=ccrs.Robinson())
plt.imshow(im, origin='upper', extent=[-17005833.330525, 17005833.330525, -8622512.772008, 8622512.772008], interpolation='nearest')
ax.coastlines(resolution='110m', color='yellow', linewidth=1, alpha=0.7)
plt.plot(-122.4194155, 37.7749295, marker='o', color='red', transform=ccrs.Geodetic())
plt.show()
'''
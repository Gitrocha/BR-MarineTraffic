import matplotlib.pyplot as plt
import cartopy.crs as ccrs


fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
ax.set_global()
ax.stock_img()
ax.coastlines()
ax.plot(-0.08, 51.53, 'o', transform=ccrs.PlateCarree())
ax.plot([-0.08, 132], [51.53, 43.17], transform=ccrs.PlateCarree())
#ax.plot([-0.08, 132], [51.53, 43.17], transform=ccrs.Geodetic())
plt.show()
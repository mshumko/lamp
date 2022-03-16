import numpy as np
import progressbar
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import asilib

import IRBEM

locations = {
    'Poker Flat':(-147.48, 65.12),
    'Venetie':(-146.36, 67.00),
    'Fort Yukon':(-145.25, 66.56)
}

alt_index = 0

# Run IRBEM 
model = IRBEM.MagFields()
resolution=200
_lon = np.linspace(-180, 180, num=resolution)
_lat = np.linspace(50, 80, num=resolution)

lons, lats = np.meshgrid(_lon, _lat)
L = np.nan*np.zeros_like(lons)

for lon_i in progressbar.progressbar(range(_lon.shape[0])):
    for lat_i in range(_lat.shape[0]):
        x = {'time':'2022-03-01T12:00', 'x1':1000, 
            'x2':lats[lon_i, lat_i],'x3':lons[lon_i, lat_i]}
        output = model.make_lstar(x, {})
        if output['Lm'][0] > 1:
            # Skip -1E31 error values
            L[lon_i, lat_i] = output['Lm'][0]

# Get an ASI field of view
skymap = asilib.load_skymap('THEMIS', 'GILL', '2022-03-01T12:00')
min_elevation = 10
invalid_elevation_idx = np.where(skymap['FULL_ELEVATION'] < min_elevation)
valid_elevation_idx = np.where(skymap['FULL_ELEVATION'] >= min_elevation)
el = skymap['FULL_ELEVATION'].copy()
el[invalid_elevation_idx] = np.nan

# Plot
projection=ccrs.Orthographic(central_longitude=-147.48, central_latitude=65.12)
plt.figure(figsize=(8,8))
ax = plt.subplot(1, 1, 1, projection=projection)
ax.coastlines(resolution='10m')

for name, coords in locations.items():
    if name != 'Poker Flat':
        lon_map = skymap['FULL_MAP_LONGITUDE'] - (np.nanmean(skymap['FULL_MAP_LONGITUDE'])-coords[0])
        lat_map = skymap['FULL_MAP_LATITUDE'] - (np.nanmean(skymap['FULL_MAP_LATITUDE'])-coords[1])
        c = ax.contour(lons, lats, L, levels=[4, 6, 8, 10, 12], transform=ccrs.PlateCarree(), colors='g')
        ax.clabel(c, c.levels, inline=False, fontsize=10, fmt=lambda x: f'L={x}')
        min_el = 20
        c2 = ax.contour(lon_map[alt_index, 1:, 1:], lat_map[alt_index, 1:, 1:], el, levels=[min_el], colors='k',
                    transform=ccrs.PlateCarree())

    #Add labels
    ax.scatter(*coords, transform=ccrs.PlateCarree(), c='k', s=50)
    ax.text(coords[0]+1, coords[1], name, transform=ccrs.PlateCarree(), va='center')

ax.set_extent((-170, -130, 55, 75), crs=ccrs.PlateCarree())
ax.set_title(f'OPQ77 L-Shells\nASI FOV at Venetie, elevation contour ${min_el}^{{\circ}}$ '
             f'at {int(skymap["FULL_MAP_ALTITUDE"][alt_index]/1E3)} km altitude'
             f'\nPFISR beam pattern: TBD', fontsize=15)
plt.tight_layout()
plt.show()
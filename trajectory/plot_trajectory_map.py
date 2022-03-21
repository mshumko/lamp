import pathlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.dates
# import matplotlib.ticker
import cartopy.crs as ccrs


locations = {
    'Poker Flat':(-147.48, 65.12),
    'Venetie':(-146.36, 67.00),
    'Fort Yukon':(-145.25, 66.56)
}


def load_trajectory(path):
    """
    Loads the mapped csv trajectory file.
    """
    trajectory = pd.read_csv(path, index_col=0, parse_dates=True)
    return trajectory


def plot_map(trajectory, alt=None, apogee=True):
    """
    as is a dict with the "ax" and "fig" keys.
    """
    projection=ccrs.Orthographic(central_longitude=-147.48, central_latitude=65.12)
    plt.figure(figsize=(8, 7))
    ax = plt.subplot(1, 1, 1, projection=projection)
    ax.coastlines(resolution='10m')

    for name, coords in locations.items():
        ax.scatter(*coords, transform=ccrs.PlateCarree(), c='k', s=50)
        ax.text(coords[0]+1, coords[1], name, transform=ccrs.PlateCarree(), va='center')

    if alt is None:
        ax.plot(trajectory['Lon'], trajectory['Lat'], 'r', transform=ccrs.PlateCarree())
    else:
        ax.plot(trajectory[f'Lon_{alt}km'], trajectory[f'Lat_{alt}km'], 'r', transform=ccrs.PlateCarree())

    ax.set_extent((-170, -130, 55, 75), crs=ccrs.PlateCarree())

    title = (f'LAMP flight trajectory | {trajectory.index[0].date()}\n'
            f'{trajectory.index[0].strftime("%H:%M:%S")} - {trajectory.index[-1].strftime("%H:%M:%S")}')
    if alt is None:
        ax.set_title(title)
    else:
        ax.set_title(title + f'\nmap_alt = {alt} km')
    return ax

if __name__ == '__main__':
    data_dir = pathlib.Path(__file__).parents[0]
    path = data_dir / 'lamp_actual_trajectory_mapped_IGRF.csv'

    trajectory = load_trajectory(path)

    for alt in [None, 90, 100, 110, 120, 130, 140, 150]:
        plot_map(trajectory, alt=alt)
        plt.tight_layout()
        if alt is None:
            plt.savefig('lamp_trajectory.png')
        else:
            plt.savefig(f'lamp_{alt}_km_footprint_trajectory.png')
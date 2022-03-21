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

    if apogee:
        idt = np.argmax(trajectory['Alt'])

    ax.set_extent((-170, -130, 55, 75), crs=ccrs.PlateCarree())
    ax.set_title(f'LAMP flight trajectory | {trajectory.index[0].date()}\n'
        f'{trajectory.index[0].strftime("%H:%M:%S")} - {trajectory.index[-1].strftime("%H:%M:%S")}'
        )
    return ax

# def plot_trajectory(trajectory, alt=None, ax=None, color='k'):
#     """
#     Makes a figure with 2 subplots: the lat/lon trajectory and altitude vs time.
#     """
#     # if ax is None:
#     #     _, ax = plt.subplots(1, 2)
#     if alt is None:
#         alt_key = f'Alt'
#         lat_key = f'Lat'
#         lon_key = f'Lon'
#         plt.suptitle(f'LAMP | {trajectory.index[0].date()} | rocket trajectory')
#     else:
#         alt_key = f'Alt_{alt}km'
#         lat_key = f'Lat_{alt}km'
#         lon_key = f'Lon_{alt}km'
#         plt.suptitle(f'LAMP | {trajectory.index[0].date()} | {alt} km footprint trajectory | IGRF')
    
#     ax = plot_alaska(ax=ax)
#     ax[0].plot(trajectory[lon_key], trajectory[lat_key], color=color)
#     ax[1].plot(trajectory.index, trajectory[alt_key], color=color)
#     ax[0].set(xlabel='Longitude [deg]', ylabel='Latitude [deg]')
#     ax[1].set(xlabel='Time [HH:MM:SS]', ylabel='Altitude [km]')
#     tfmt = matplotlib.dates.DateFormatter('%H:%M:%S')
#     ax[1].xaxis.set_major_formatter(tfmt)
#     ax[1].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(6))
#     return

if __name__ == '__main__':
    data_dir = pathlib.Path(__file__).parents[0]
    path = data_dir / 'lamp_actual_trajectory_mapped_IGRF.csv'

    trajectory = load_trajectory(path)

    plot_map(trajectory)
    plt.tight_layout()
    plt.show()

    # _, ax = plt.subplots(1, 2, figsize=(10, 5))
    # plot_trajectory(trajectory, alt=90, ax=ax)
    # ax[1].set_ylim(0, None)
    # plt.tight_layout()
    # plt.show()
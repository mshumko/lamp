import pathlib

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates
import matplotlib.ticker


def load_trajectory(path):
    """
    Loads the mapped csv trajectory file.
    """
    trajectory = pd.read_csv(path, index_col=0, parse_dates=True)
    return trajectory

def plot_trajectory(trajectory, alt=None, ax=None, color='k'):
    """
    Makes a figure with 2 subplots: the lat/lon trajectory and altitude vs time.
    """
    if ax is None:
        _, ax = plt.subplots(1, 2)
    if alt is None:
        alt_key = f'Alt'
        lat_key = f'Lat'
        lon_key = f'Lon'
        plt.suptitle(f'LAMP | {trajectory.index[0].date()} | rocket trajectory')
    else:
        alt_key = f'Alt_{alt}km'
        lat_key = f'Lat_{alt}km'
        lon_key = f'Lon_{alt}km'
        plt.suptitle(f'LAMP | {trajectory.index[0].date()} | {alt} km footprint trajectory | IGRF')
    
    ax[0].plot(trajectory[lon_key], trajectory[lat_key], color=color)
    ax[1].plot(trajectory.index, trajectory[alt_key], color=color)
    ax[0].set(xlabel='Longitude [deg]', ylabel='Latitude [deg]')
    ax[1].set(xlabel='Time [HH:MM:SS]', ylabel='Altitude [km]')
    tfmt = matplotlib.dates.DateFormatter('%H:%M:%S')
    ax[1].xaxis.set_major_formatter(tfmt)
    ax[1].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(6))
    return

if __name__ == '__main__':
    data_dir = pathlib.Path(__file__).parents[0]
    path = data_dir / 'lamp_actual_trajectory_mapped_IGRF.csv'

    trajectory = load_trajectory(path)
    _, ax = plt.subplots(1, 2, figsize=(10, 5))
    plot_trajectory(trajectory, alt=90, ax=ax)
    ax[1].set_ylim(0, None)
    plt.tight_layout()
    plt.show()
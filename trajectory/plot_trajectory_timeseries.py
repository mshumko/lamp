import pathlib
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates
import matplotlib.ticker

plt.rcParams['font.size'] = 12

def load_trajectory(path):
    """
    Loads the mapped csv trajectory file.
    """
    trajectory = pd.read_csv(path, index_col=0, parse_dates=True)
    return trajectory

def plot_timeseries(trajectory, color='k'):
    """
    Makes a figure with 2 subplots: the lat/lon trajectory and altitude vs time.
    """
    _, ax = plt.subplots(2, 1, sharex=True, figsize=(10, 7))

    plt.suptitle(f'LAMP | {trajectory.index[0].date()} | rocket trajectory')
    
    ax[0].plot(trajectory.index, trajectory['Alt'], color=color)
    ax[1].plot(trajectory.index, trajectory["L"], color=color)
    ax[1].text(0.01, 0.9, f'Mean MLT={round(trajectory["MLT"].mean(), 2)}', transform=ax[1].transAxes, 
        ha='left')
    ax[0].set(ylabel='Altitude [km]')
    ax[1].set(ylabel='L-Shell [IGRF]')
    ax[-1].set(xlabel='Time [HH:MM:SS]')
    tfmt = matplotlib.dates.DateFormatter('%H:%M:%S')
    ax[-1].xaxis.set_major_formatter(tfmt)
    ax[-1].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(6))

    # Plot stars at the start/end of data gathering and apogee
    time_range = (
        datetime(2022, 3, 5, 11, 29, 15),
        datetime(2022, 3, 5, 11, 36, 56)
        )
    for t in time_range:
        for ax_i in ax:
            ax_i.axvline(t, c='k', ls='--')   
    idt = np.argmax(trajectory['Alt'])
    ax[0].scatter(trajectory.index[idt], trajectory['Alt'][idt], c='r', s=100, marker='*')
    ax[1].scatter(trajectory.index[idt], trajectory["L"][idt], c='r', s=100, marker='*')

    ax[0].text(0.5, 0.7, f'max_alt={round(trajectory["Alt"].max())} km\n'
        f'at {trajectory.index[idt].strftime("%H:%M:%S")} UT', 
        transform=ax[0].transAxes, ha='center')
    return

if __name__ == '__main__':
    data_dir = pathlib.Path(__file__).parents[0]
    path = data_dir / 'lamp_actual_trajectory_mapped_IGRF.csv'

    trajectory = load_trajectory(path)
    plot_timeseries(trajectory)
    plt.tight_layout()
    plt.show()
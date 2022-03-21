# Map LAMP's trajectory along magnetic field lines to a specified auroral emission altitude.
import pathlib
import dateutil.parser

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
import matplotlib.ticker

import IRBEM


def load_trajectory(path, t0=None):
    """
    Loads the csv trajectory file containing at least Time, Lat, Lon, and Alt columns.
    """
    trajectory = pd.read_csv(path, index_col=0)
    
    if t0 is not None:
        if isinstance(t0, str):
            t0 = dateutil.parser.parse(t0)
        trajectory.index = pd.to_timedelta(trajectory.index, unit='second') + t0
    return trajectory

def map_trajectory(trajectory, alt, suffix='nominal'):
    """
    Maps the trajectory DataFrame to an altitude.

    Parameters
    ----------
    trajectory: pd.DataFrame
        A DataFrame containing Time, Lat_(suffix), Lon_(suffix), and Alt_(suffix).
    alt: float
        The mapping altitude in kilometers
    suffix: str
        The column suffixes to use to index.
    """
    keys_IRBEM_order = [f'Alt_{alt}km', f'Lat_{alt}km', f'Lon_{alt}km']
    trajectory[keys_IRBEM_order] = np.nan
    m = IRBEM.MagFields(kext='None')  # IGRF with no extrnal model.
    maginput = None

    for i, row in trajectory.iterrows():
        if suffix == 'nominal':
            LLA = {
                'Time':'2022-03-05T11:30:00', 
                'x1':row[f'Alt_{suffix}'], 
                'x2':row[f'Lat_{suffix}'], 
                'x3':row[f'Lon_{suffix}']
                }
        else:
            raise NotImplementedError
        footprint_output = m.find_foot_point(LLA, maginput, alt, 0)
        trajectory.loc[i, keys_IRBEM_order] = footprint_output['XFOOT']
    
    # Replace -1E31 IRBEM errors with np.nan
    trajectory.loc[trajectory[f'Alt_{alt}km'] < 0, keys_IRBEM_order] = np.nan
    return trajectory

def plot_trajectory(trajectory, alt=None, ax=None, color='k'):
    """
    Makes a figure with 2 subplots: the lat/lon trajectory and altitude vs time.
    """
    if ax is None:
        _, ax = plt.subplots(1, 2)
    if alt is None:
        alt_key = f'Alt_nominal'
        lat_key = f'Lat_nominal'
        lon_key = f'Lon_nominal'
        
        plt.suptitle('LAMP nominal trajectory')
    else:
        alt_key = f'Alt_{alt}km'
        lat_key = f'Lat_{alt}km'
        lon_key = f'Lon_{alt}km'
        plt.suptitle(f'LAMP trajectory\nmapped with IGRF to {alt} km')
    
    ax[0].plot(trajectory[lon_key], trajectory[lat_key], color=color)
    ax[1].plot(trajectory.index, trajectory[alt_key], color=color)
    ax[0].set(xlabel='Longitude [deg]', ylabel='Latitude [deg]')
    ax[1].set(xlabel='Time [HH:MM:SS]', ylabel='Altitude [km]')
    tfmt = matplotlib.dates.DateFormatter('%H:%M:%S')
    ax[1].xaxis.set_major_formatter(tfmt)
    ax[1].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    return

if __name__ == '__main__':
    t0 = '2022-03-05T11:27:30'
    data_dir = pathlib.Path(__file__).parents[0]
    path = data_dir / 'lamp_nominal_trajectory.csv'
    trajectory = load_trajectory(path, t0=t0)

    alts = np.arange(90, 160, 10)
    for alt in alts:
        save_path = data_dir / f'lamp_nominal_trajectory_mapped_{alt}_km.csv'
        mapped_trajectory = map_trajectory(trajectory, alt)
        mapped_trajectory.to_csv(save_path, index_label='Time')

        _, ax = plt.subplots(1, 2, figsize=(10, 5))
        plot_trajectory(mapped_trajectory, alt=alt, ax=ax)
        ax[1].set_ylim(0, None)
        plt.tight_layout()
        plt.show()

    # _, ax = plt.subplots(1, 2, figsize=(10, 5))
    # plot_trajectory(trajectory, alt=alt_km, ax=ax)
    # ax[1].set_ylim(0, None)
    # plt.tight_layout()
    # plt.show()
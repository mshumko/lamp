# Map LAMP's trajectory along magnetic field lines to a specified auroral emission altitude.
import pathlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import IRBEM


def load_trajectory(path):
    """
    Loads the csv trajectory file containing at least Time, Lat, Lon, and Alt columns.
    """
    trajectory = pd.read_csv(path)
    # This is short for now, but the actual trajectory will have times to convert.
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

def plot_trajectory(trajectory, alt='nominal', ax=None, color='k'):
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
    ax[1].plot(trajectory['Time'], trajectory[alt_key], color=color)
    ax[0].set(xlabel='Longitude [deg]', ylabel='Latitude [deg]')
    ax[1].set(xlabel='Time since launch [seconds]', ylabel='Altitude [deg]')
    return

if __name__ == '__main__':
    name = 'lamp_nominal_trajectory.csv'
    path = pathlib.Path(__file__).parents[0] / name

    alt_km = 90
    trajectory = load_trajectory(path)

    if alt_km is not None:
        trajectory = map_trajectory(trajectory, alt_km)

    _, ax = plt.subplots(1, 2, figsize=(10, 5))
    plot_trajectory(trajectory, alt=alt_km, ax=ax)
    ax[1].set_ylim(0, None)
    plt.tight_layout()
    plt.show()
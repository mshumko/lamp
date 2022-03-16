# Map LAMP's trajectory along magnetic field lines to a specified auroral emission altitude.
import pathlib

import pandas as pd
import numpy as np

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
    trajectory[[f'Lat_{alt}km', f'Lon_{alt}km', f'Alt_{alt}km']] = np.nan
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
        trajectory.loc[i, [f'Alt_{alt}km', f'Lat_{alt}km', f'Lon_{alt}km']] = footprint_output['XFOOT']
    return trajectory

if __name__ == '__main__':
    name = 'lamp_nominal_trajectory.csv'
    path = pathlib.Path(__file__).parents[0] / name
    
    trajectory = load_trajectory(path)
    trajectory = map_trajectory(trajectory, 90)
    pass
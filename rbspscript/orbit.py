import numpy as np
import pandas as pd
import h5py
import os
import re

def generate_orbit_df(parent_path='/data/ECT/rbsp-ect.lanl.gov/data_pub/rbspa/MagEphem/definitive/'):
    orbit_list = []
    orbit_num = -1
    years = os.listdir(parent_path)
    for year in years:
        path = os.path.join(parent_path, year)
        file_name_list = os.listdir(path)
        for file_name in file_name_list:
            if re.match('rbspa_def_MagEphem_OP77Q'+'.', file_name):
                data = htpy.File(os.path.join(path, file_name))
                for index, value in enumerate(data['OrbitNumber']):
                    if value > orbit_num:
                        orbit_num = value
                        time = pd.to_datetime(bytes.decode(data['IsoTime'][index]))
                        orbit_list.append([orbit_num, time])
    return pd.DataFrame(orbit_list, columns=['orbit_num', 'time'])
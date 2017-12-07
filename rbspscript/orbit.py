import numpy as np
import pandas as pd
import h5py
import os
import re

def generate_rbsp_orbit_info(parrent_path='/data/ECT/rbsp-ect.lanl.gov/data_pub/',
                             output_path='/data/rbspinfo',
                             twin='a'):
    assert twin in ('a', 'b')
    parrent_path = os.path.join(parrent_path, 'rbsp{}/MagEphem/definitive'.format(twin))
    output_file_name = os.path.join(output_path, 'rbsp{}_orbit.csv'.format(twin))
    orbit_list = []
    orbit_num = -1
    years = os.listdir(parrent_path)
    for year in years:
        path = os.path.join(parrent_path, year)
        file_name_list = os.listdir(path)
        for file_name in file_name_list:
            if re.match('rbsp{}_def_MagEphem_OP77Q'.format(twin)+'.', file_name):
                data = h5py.File(os.path.join(path, file_name))
                for index, value in enumerate(data['OrbitNumber']):
                    if value > orbit_num:
                        orbit_num = value
                        time = pd.to_datetime(bytes.decode(data['IsoTime'][index]))
                        orbit_list.append([orbit_num, time])
    pd.DataFrame(orbit_list, columns=['orbit_num', 'time']).to_csv(output_file_name, index=False)
    

def orbit2time(orbitnum, twin='a', orbit_file_path='/data/rbspinfo'):
    assert twin in ('a', 'b')
    orbit_file_name = os.path.join(orbit_file_path, 'rbsp{}_orbit.csv'.format(twin))
    df = pd.read_csv(orbit_file_name)
    if not orbitnum in df['orbit_num']:
        return None
    else :
        df = df[df['orbit_num']>orbitnum]
        return pd.to_datetime(df['time'].values[0:min(2,len(df))])
    
def time2orbit(time, twin='a', orbit_file_path='/data/rbspinfo'):
    assert twin in ('a', 'b')
    orbit_file_name = os.path.join(orbit_file_path, 'rbsp{}_orbit.csv'.format(twin))
    df = pd.read_csv(orbit_file_name)
    df = df[df['time']>time]
    if len(df) == 0:
        return None
    else:
        return df['orbit_num'].values[0]
    
    
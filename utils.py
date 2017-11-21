# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from spacepy.pycdf import CDF
import re
import os
import pickle
from .config import *

# read data
# default load pickle
def load(file_name):
    return load_pickle(file_name)

# read txt file
# \n for newlines and data splited by spaces
def load_txt(file_name, col_names=None):
    f = open(file_name)
    return pd.DataFrame([i.split() for i in f.readlines()], columns=col_names)

# read csv
def load_csv(file_name):
    return pd.read_csv(file_name)

# read pickle
def load_pickle(file_name):
    return pickle.load(open(file_name, 'rb'))

# read cdf
def load_cdf(file_name):
    return CDF(file_name)

# read dict from string
def load_dict(file_name):
    with open(file_name, 'r') as f:
        data = f.read()
        return eval(data)
    
# save data
# default save pickle
def save(data, file_name):
    return save_pickle(data, file_name)

# save pickle
def save_pickle(data, file_name):
    pickle.dump(data, open(file_name, 'wb'))
    
# save dict as string
def save_dict(data, file_name):  
    with open(file_name,'w') as f:
        f.write(str(data))

# convert raw datetime in txt file to datetime format
# the raw datetime in txt should have column name ['Y','M','D','h','m','s']
def convert_raw_datetime(df, raw_keylist=['Y','M','D','h','m','s'], reindex=True):
    for key in raw_keylist:
        if key not in df:
            raise IndexError('Index {} not found'.format(key))
    df['time'] = pd.to_datetime(df['Y']+'-'+df['M']+'-'+df['D']+'T'+df['h']+':'+df['m']+':'+df['s'])
    for key in raw_keylist:
        del df[key]
    if reindex:
        df.set_index(df['time'], inplace=True)
    return df

# parse dir
# 遍历某数据所有版本号，输出匹配的第一个
def parse_mageis_dir(date, parrent_dir=RBSP_PATH):
    mageis_dir_suffix = 'mageis/level3/pitchangle'
    mageis_prefix = 'rbspa_rel03_ect-mageis-L3_'
    date = pd.to_datetime(date)
    time_dir = date.strftime('%Y')
    time_file_name = date.strftime('%Y%m%d')
    file_dir = os.path.join(parrent_dir, mageis_dir_suffix, time_dir)
    file_name = mageis_prefix + time_file_name
    if os.path.exists(file_dir):
        all_file_list = os.listdir(file_dir)
    else:
        return None
    valid_file_name = None
    for temp_file_name in all_file_list:
        if re.match('^'+file_name+'.', temp_file_name):
            valid_file_name = temp_file_name
            break
    if valid_file_name:
        return os.path.join(file_dir, valid_file_name)
    else:
        return None

def parse_rept_dir(date, parrent_dir=RBSP_PATH):
    rept_dir_suffix = 'rept/level3/pitchangle'
    rept_prefix = 'rbspa_rel03_ect-rept-sci-L3_'
    date = pd.to_datetime(date)
    time_dir = date.strftime('%Y')
    time_file_name = date.strftime('%Y%m%d')
    file_dir = os.path.join(parrent_dir, rept_dir_suffix, time_dir)
    file_name = rept_prefix + time_file_name
    if os.path.exists(file_dir):
        all_file_list = os.listdir(file_dir)
    else:
        return None
    valid_file_name = None
    for temp_file_name in all_file_list:
        if re.match('^'+file_name+'.', temp_file_name):
            valid_file_name = temp_file_name
            break
    if valid_file_name:
        return os.path.join(file_dir, valid_file_name)
    else:
        return None
    
def parse_rbsp_B_component_dir(date, parrent_dir=RBSP_B_COMPONENT_PATH):
    B_component_prefix = 'rbsp-a_magnetometer_4sec-sm_emfisis-L3_'
    date = pd.to_datetime(date)
    time_dir = date.strftime('%Y/%m/%d')
    file_dir = os.path.join(parrent_dir, time_dir)
    time_file_name = date.strftime('%Y%m%d')
    file_name = B_component_prefix + time_file_name
    if os.path.exists(file_dir):
        all_file_list = os.listdir(file_dir)
    else:
        return None
    valid_file_name = None
    for temp_file_name in all_file_list:
        if re.match('^'+file_name+'.', temp_file_name):
            valid_file_name = temp_file_name
            break
    if valid_file_name:
        return os.path.join(file_dir, valid_file_name)
    else:
        return None
    
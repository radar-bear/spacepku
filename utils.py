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
    return pickle.load(open(file_name, 'rb'))

# read txt file
# \n for newlines and data splited by spaces
def read_txt(file_name, col_names=None):
    f = open(file_name)
    return pd.DataFrame([i.split() for i in f.readlines()], columns=col_names)

# read csv
def read_csv(file_name):
    return pd.read_csv(file_name)

# read pickle
def read_pickle(file_name):
    return pickle.load(open(file_name, 'rb'))

# read cdf
def read_cdf(file_name):
    return CDF(file_name)

# save data
# default save pickle
def save(data, file_name):
    pickle.dump(data, open(file_name, 'wb'))

# # Time format 2012-04-22
# def mageis_file_name(begin, end):
#     mageis_path =

# # query data
# # 1. query data by project-satellite-data_name-date
# # 2. query a series of data
# # 3. the data should be time series
# # 4. join data by date
# # 5. return a dataframe
# def query_single_data(satellite, instrument, data_name, date):
#     satellite_path = SATELLITE_PATH
# # time format 2012-04-05
# def query_mageis(begin, end):
#     root_path = MAGEIS_PATH
#     begin = pd.to_datetime(begin)
#     end = pd.to_datetime(end)
#     resolution = pd.Timedelta(days=1)
#     while begin<=end:

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
    date = '2016-09-09'
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
        if re.match(file_name+'*', temp_file_name):
            valid_file_name = temp_file_name
            break
    if valid_file_name:
        return os.path.join(file_dir, valid_file_name)
    else:
        return None

def parse_rept_dir(date, parrent_dir=RBSP_PATH):
    rept_dir_suffix = 'rept/level3/pitchangle'
    rept_prefix = 'rbspa_rel03_ect-rept-sci-L3_'
    date = '2016-09-09'
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
        if re.match(file_name+'*', temp_file_name):
            valid_file_name = temp_file_name
            break
    if valid_file_name:
        return os.path.join(file_dir, valid_file_name)
    else:
        return None

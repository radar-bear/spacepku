# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from spacepy.pycdf import CDF
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
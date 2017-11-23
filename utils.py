# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
import os
import pickle
import json

from spacepy.pycdf import CDF
from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objs as go
import plotly.plotly as py
from .config import *
from .tools import *

# load data
# default load pickle
def load(file_name):
    return load_pickle(file_name)

# load txt file
# \n for newlines and data splited by spaces
def load_txt(file_name, col_names=None):
    f = open(file_name)
    return pd.DataFrame([i.split() for i in f.readlines()], columns=col_names)

# load csv
def load_csv(file_name):
    return pd.read_csv(file_name)

# load pickle
def load_pickle(file_name):
    return pickle.load(open(file_name, 'rb'))

# load cdf
def load_cdf(file_name):
    return CDF(file_name)

# load dict from string
def load_dict(file_name):
    with open(file_name, 'r') as f:
        data = f.read()
        return eval(data)

# load plotly fig
def load_fig(file_name):
    """Render a plotly figure from a json file"""
    with open(file_name, 'r') as f:
        v = json.loads(f.read())
    return go.Figure(data=v['data'], layout=v['layout'])

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

# save figs
def save_fig(data, file_name):
    """
    copied from https://github.com/plotly/plotly.py/issues/579

    Serialize a plotly figure object to JSON so it can be persisted to disk.
    Figure's persisted as JSON can be rebuilt using the plotly JSON chart API:

    http://help.plot.ly/json-chart-schema/

    If `file_name` is provided, JSON is written to file.

    Modified from https://github.com/nteract/nteract/issues/1229
    """

    redata = json.loads(json.dumps(data.data, cls=PlotlyJSONEncoder))
    relayout = json.loads(json.dumps(data.layout, cls=PlotlyJSONEncoder))

    fig_json=json.dumps({'data': redata,'layout': relayout})
    with open(file_name, 'w') as f:
        f.write(fig_json)

def save_png(data, file_name, scale=1):

    if file_name.split('.')[-1] != 'png':
        file_name += '.png'
    py.sign_in('radar-bear', 'cKhUAYqJ2KANvRrLrXAW')
    py.image.save_as(data, format='png', scale=scale, filename=file_name)

# set figure params
def set_params(fig, params, trace_name=None):
    params = parse_params_to_plotly(params)
    fig.layout.update(params['layout_params'])
    # 如果trace name是int则修改指定index的trace
    if isinstance(trace_name, int):
        if trace_name < len(fig.data):
            fig.data[trace_name].update(params['trace_params'])
            if fig.data[trace_name].colorbar:
                fig.data[trace_name].colorbar.update(params['colorbar_params'])
    else:
        # 否则进行trace name匹配
        for data in fig.data:
            # 找到匹配的trace name或trace name为空就更新该trace
            if (data.name == trace_name) or not trace_name:
                data.update(params['trace_params'])
                if data.colorbar:
                    data.colorbar.update(params['colorbar_params'])


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

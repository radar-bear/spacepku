# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
import os
import pickle
import json

from spacepy.pycdf import CDF
from plotly.utils import PlotlyJSONEncoder
from plotly import offline
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

# load plotly animation fig
def load_animation(file_name):
    """Render a plotly figure from a json file"""
    with open(file_name, 'r') as f:
        v = json.loads(f.read())
    return go.Figure(data=v['data'], layout=v['layout'], frames=v['frames'])

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

# save csv
def save_csv(data, file_name):
    data = pd.DataFrame(data)
    data.to_csv(file_name, index=False)

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

# save figs
def save_animation(data, file_name):
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
    reframes = json.loads(json.dumps(data.frames, cls=PlotlyJSONEncoder))

    fig_json=json.dumps({'data': redata,'layout': relayout,'frames':reframes})
    with open(file_name, 'w') as f:
        f.write(fig_json)

def save_png(data, file_name, scale=1):

    if file_name.split('.')[-1] != 'png':
        file_name += '.png'
    py.sign_in('radar-bear', 'cKhUAYqJ2KANvRrLrXAW')
    py.image.save_as(data, format='png', scale=scale, filename=file_name)

def save_html(data, file_name):

    if file_name.split('.')[-1] != 'html':
        file_name += '.html'
    offline.plot(data, filename=file_name)

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

import pandas as pd
from pandas.core.tools.datetimes import parse_time_string

layout_keys = ['title', 'showlegend', 'width', 'height']
yaxis_keys = ['ytitle', 'yrange', 'ytype', 'yticktext', 'ytickvals']
xaxis_keys = ['xtitle', 'xrange', 'xtype', 'xticktext', 'xtickvals']
trace_keys = ['name', 'text']
line_keys = ['line_color', 'line_width', 'line_dash']
colorbar_keys = ['ctitle', 'cticktext', 'ctickvals']
colorbar_range = 'crange'

def parse_params_to_plotly(params):

    layout_params = {}
    for key in layout_keys:
        if key in params:
            layout_params[key] = params[key]
            
    yaxis_params = {}
    for key in yaxis_keys:
        if key in params:
            yaxis_params[key[1:]] = params[key]
    if 'range' in yaxis_params:
        yaxis_params['autorange'] = False
    if len(yaxis_params) > 0:
        layout_params['yaxis'] = yaxis_params
            
    xaxis_params = {}
    for key in xaxis_keys:
        if key in params:
            xaxis_params[key[1:]] = params[key]
    if 'range' in xaxis_params:
        xaxis_params['autorange'] = False
    if len(xaxis_params) > 0:
        layout_params['xaxis'] = xaxis_params

    trace_params = {}
    for key in trace_keys:
        if key in params:
            trace_params[key] = params[key]
    if colorbar_range in params:
        trace_params['zmin'] = params[colorbar_range][0]
        trace_params['zmax'] = params[colorbar_range][1]

    line_params = {}
    for key in line_keys:
        if key in params:
            line_params[key[5:]] = params[key]
    if line_params:
        trace_params['line'] = line_params

    colorbar_params = {}
    for key in colorbar_keys:
        if key in params:
            colorbar_params[key[1:]] = params[key]

    return {'layout_params':layout_params, 'trace_params':trace_params, 'colorbar_params':colorbar_params}

def parse_date_str(date_str, tag='begin'):
    assert tag in ('begin', 'end')
    date, _, granularity = parse_time_string(str(date_str))
    if tag == 'begin':
        return date
    else:
        offset = pd.DateOffset(**{granularity+'s': 1})
        return date + offset - pd.to_timedelta('1s')

def is_in(value, value_range):
    assert value_range == 2
    return (value>=value_range[0]) & (value<=value_range[1])
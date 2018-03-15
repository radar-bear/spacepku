# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot
from .config import *
from .tools import parse_params_to_plotly
from .filter import resample2d


###########################
# plot tools
def parse_default_plot_type(value_dim):
    """
    Usage
    ----------
    Given the dimension number of value, decide which
    plot type should be applied

    Parameters
    ----------
    value_dim : int
        the dimension num of value

    Output
    ----------
    type : string
        the plot type that matches best

    Notes
    ----------
    TODO
    This function is private
    """

    if value_dim == 2:
        type = 'heatmap'  # 二维数据默认画heatmap
    elif value_dim == 1:
        type = 'line'  # 一维数据默认画line
    else:
        raise ValueError('wrong dimension {}'.format(value_dim))
    return type


def stdtime(data):
    """
    Usage
    ----------
    convert a normal data to pandas timestamp
    """

    return pd.to_datetime(pd.Series(data))


###########################
# basic plot function
def plot_lines(x, value_list,
               value_name_list=[],
               timeseries=False,
               params={}, mode='lines',
               showfig=True):
    """
    Usage
    ----------
    Plot Lines, also can plot scatter if mode='markers'

    Parameters
    ----------
    x : list-like
        x axis of lines
    value_list : 2d-array
        each element in value_list will be plotted as a single
        line. It MUST be a list of list, even if you just want
        to plot single line.
    value_name_list : list-like
        the name of each line, will be displayed in legend
    params : dict or list
        if dict, parse as plot params.
        if list, parse EACH ELEMENT as plot params corresponding
        to EACH LINE
    mode : string
        'markers', 'lines' or 'lines+markers'
    timeseries : boolean
        wether x axis should be regard as timestamp of normal
        data
    showfig : boolean
        show figure or not

    Output
    ----------
    fig : plotly-graph
        a plotly graph object

    Notes
    ----------
    TO BE FINISHED
    """

    value_list = np.array(value_list)
    assert len(value_list.shape) == 2

    if timeseries:
        x = stdtime(x)

    trace_list = []
    for value in value_list:
        trace_list.append(go.Scatter(x=x,
                                     y=value,
                                     mode=mode,
                                     line=dict(width=1),
                                     showlegend=True))
    # set trace name for each trace
    # this step is not included in trace param setting
    # for the purpose of easy-use
    if value_name_list:
        for value_name, trace in zip(value_name_list, trace_list):
            trace['name'] = value_name

    # set params
    layout_params = {}
    if params:
        if isinstance(params, dict):
            params = parse_params_to_plotly(params)
            layout_params = params['layout_params']
            for trace in trace_list:
                trace.update(params['trace_params'])
        elif isinstance(params, list):
            layout_params = parse_params_to_plotly(params[0])['layout_params']
            for param, trace in zip(params, trace_list):
                trace.update(parse_params_to_plotly(param)['trace_params'])
        else:
            raise ValueError('plot params neither list nor dict')

    # set layout params
    layout = get_default_layout()
    layout.update(layout_params)
    fig = go.Figure(data=trace_list, layout=layout)
    if showfig:
        iplot(fig)
    return fig


def plot_heatmap(x, y, value,
                 params={},
                 log=False,
                 timeseries=False,
                 dist_normalize=False,
                 data_length=-1,
                 showfig=True,):
    """
    Usage
    ----------
    Plot Heatmap

    Parameters
    ----------
    x : list-like
        x axis of heatmap
    y : list-line
        y axis of heatmap
    value : 2d-array
        the value of each point in the heatmap. The 1st axis
        of value should have the same length as x. The 2nd
        axis has length same with y
    params : dict
        plot params
    log : boolean
        log value or not
    dist_normalize : boolean
        if True, the value will be normalized to 0~1 at each
        x point
    timeseries : boolean
        wether x axis should be regard as timestamp of normal
        data
    showfig : boolean
        show figure or not

    Output
    ----------
    fig : plotly-graph
        a plotly graph object

    Notes
    ----------
    this function will always return a plotly-graph, remeber
    using a variable contain the return value if you don't
    want the plotly-graph var crashes your terminal
    """

    params = parse_params_to_plotly(params)

    # downsample if data_length exceed x
    if data_length > 0:
        ratio = data_length / len(x)
        x, y, value = resample2d(x, y, value, xscale=ratio)

        # the 1st axis of value is x
        # the 2nd axis of value is y

    value = np.array(value).T

    if log:
        value = np.log10(value)
    if dist_normalize:
        value = pd.DataFrame(value)
        value = value.apply(lambda x: (x - np.nanmin(x)) /
                            (np.nanmax(x) - np.nanmin(x)))

    color_min = np.nanpercentile(value, 5)
    color_max = np.nanpercentile(value, 95)

    if timeseries:
        x = stdtime(x)

    trace = go.Heatmap(x=x, y=y, z=value, colorscale='Jet',
                       zauto=False, zmin=color_min, zmax=color_max,
                       showscale=True)
    # set colorbar
    colorbar = get_default_colorbar()
    colorbar.update(params['colorbar_params'])
    trace.update(colorbar=colorbar)
    # set trace params
    trace.update(params['trace_params'])
    # set layout
    layout = get_default_layout()
    layout.update(params['layout_params'])
    fig = go.Figure(data=[trace], layout=layout)
    if showfig:
        iplot(fig)
    return fig


###########################
# advanced plot function
def stack_traces(fig_list, params={}, showfig=False):
    """
    Usage
    ----------
    stack the all traces in the same axis

    Parameters
    ----------
    fig_list : list of plotly-graph like variable
        all traces included in the fig_list will be stacked
    params : dict
        plot params. if empty, inherit from fig_list[0]
    showfig : boolean
        show figure or not

    Notes
    ----------
    Only layout params is supported
    """

    # use the layout params of 1st fig defaultly
    # avoid to overwrite origin figs
    if len(fig_list) == 0:
        raise ValueError('fig list is empty')
    from copy import deepcopy
    fig_list = deepcopy(fig_list)
    new_data = []
    for fig in fig_list:
        new_data.extend(fig['data'])
    fig = go.Figure(data=new_data, layout=fig_list[0]['layout'])
    fig['layout'].update(parse_params_to_plotly(params)['layout_params'])
    if showfig:
        iplot(fig)
    return fig


def stack_figs(fig_list, params={}, showfig=False):
    """
    TODO:
    Write doc
    """
    # avoid to overwrite origin figs
    from copy import deepcopy
    fig_list = deepcopy(fig_list)
    # Share xaxis of figs in fig_list
    # return a single fig with multi-yaxis
    # get the pixel height of each panel
    height_list = np.array([fig.layout.height for fig in fig_list])

    def get_stack_layout(height_list, fig_gap, marginb=DEFAULT_MARGIN, margint=DEFAULT_MARGIN):
        # Because the height of a single fig inculde the margin
        # This function stripe the margin and keep the true height of the figure in a stack fig
        # get the real height of each fig
        real_height_list = height_list - (marginb + margint)
        # the total height of the whole stack fig
        total_height = np.sum(real_height_list) + \
            (len(height_list) - 1) * fig_gap + (marginb + margint)
        # calculate the fraction position of each panel
        height_fractions = real_height_list / total_height
        gap_fraction = fig_gap / total_height
        domain_list = []
        pos_begin = marginb / total_height
        for fig_height in height_fractions:
            domain_list.append([pos_begin, pos_begin + fig_height])
            pos_begin += fig_height + gap_fraction
        # total_height is the absolute pixels of stack fig
        # domain_list is the fraction position of each panel
        return total_height, domain_list
    total_height, domain_list = get_stack_layout(height_list, 20)
    data_list = []
    layout = go.Layout()
    # aggregrate the traces
    for i, fig in enumerate(fig_list):
        domain = domain_list[i]
        # set position of each trace
        for trace in fig.data:
            trace.update(yaxis='y' + str(i + 1))
            # set colorbar position
            if 'colorbar' in trace:
                trace.colorbar.update(dict(lenmode='fraction', len=np.abs(domain[1] - domain[0]),
                                           y=np.mean(domain)))
            data_list.append(trace)
        # keep the yaxis parameters of each panel and set the yaxis position
        fig.layout.yaxis.update(domain=domain)
        layout.update({'yaxis' + str(i + 1): fig.layout.yaxis.copy()})
    layout.update(xaxis=fig_list[-1].layout.xaxis)
    layout.xaxis.update({'rangeslider': {'visible': False}})
    layout.update({'height': total_height, 'width': DEFAULT_WIDTH})
    layout.update(parse_params_to_plotly(params)['layout_params'])
    fig = go.Figure(data=data_list, layout=layout)
    if showfig:
        iplot(fig)
    return fig

# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot
from .config import *

def tplot_default_type_parse(value_dim):

    if value_dim >= 3:
        raise IndexError('{} has shape {}, beyond tplot ability'.format(key, target_shape))
    elif value_dim == 2:
        type = 'heatmap' # 二维数据默认画heatmap
    elif value_dim == 1:
        type = 'line' # 一维数据默认画line
    elif value_dim <= 0:
        raise ValueError('wrong dimension {}'.format(value_dim))
    return type

def tplot_line(time,
               value_list,
               value_name_list=[],
               trace_params=[],
               layout_params={},
               showfig=True):
    trace_list = []
    time = pd.Series(time) # 为了正确地显示时间需要用pd.Series
    for value in value_list:
        trace_list.append(go.Scatter(x=time,
                                     y=value,
                                     line=dict(width=0.5),
                                     showlegend=True))
    # set trace name for each trace
    # this step is not included in trace param setting
    # for the purpose of easy-use
    if value_name_list:
        for value_name, trace in zip(value_name_list, trace_list):
            trace['name']=value_name
    # set trace params
    if trace_params:
        if type(trace_params)==dict:
            for trace in trace_list:
                trace.update(trace_params)
        else:
            for param, trace in zip(trace_params, trace_list):
                trace.update(param)
    # set layout params
    layout = get_default_layout()
    layout.update(layout_params)
    fig = go.Figure(data=trace_list, layout=layout)
    if showfig:
        iplot(fig)
    return fig

def tplot_particle(time,
                   y,
                   value,
                   colorbar_params={},
                   trace_params={},
                   layout_params={},
                   log=True,
                   dist_normalize=False,
                   showfig=True):
    # dist_normalize=True会在每个时间点上，把log(PSD)normalize到[0,1]
    # TODO; warning
    value = np.where(value<=0, np.nan, value)
    # normalize 注意最后把log_value改回numpy，不然不能保存json到网页
    if log:
        value = np.log10(value)
    if dist_normalize:
        value = pd.DataFrame(value)
        value = value.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
        value = np.array(value)
    color_min = np.nanpercentile(value, 5)
    color_max = np.nanpercentile(value, 95)
    time = pd.Series(time) # 为了正确地显示时间需要用pd.Series
    trace = go.Heatmap(x=time,y=y,z=value,colorscale='Jet',zauto=False,
                        zmin=color_min, zmax=color_max, showscale=True)
    # set colorbar
    colorbar = get_default_colorbar()
    colorbar.update(colorbar_params)
    trace.update(colorbar=colorbar)
    # set trace params
    trace.update(trace_params)
    # set layout
    layout = get_default_layout()
    layout.update(layout_params)
    fig = go.Figure(data=[trace],layout=layout)
    if showfig:
        iplot(fig)
    return fig

def stack_traces(fig_list, layout_params={}, showfig=True):
    # use the layout params of 1st fig defaultly
    # avoid to overwrite origin figs
    if len(fig_list)==0:
        raise ValueError('fig list is empty')
    from copy import deepcopy
    fig_list = deepcopy(fig_list)
    new_data = []
    for fig in fig_list:
        new_data.extend(fig['data'])
    fig = go.Figure(data=new_data, layout=fig_list[0]['layout'])
    fig['layout'].update(layout_params)
    if showfig:
        iplot(fig)
    return fig

def stack_figs(fig_list, layout_params={}, showfig=True):
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
        real_height_list = height_list-(marginb+margint)
        # the total height of the whole stack fig
        total_height = np.sum(real_height_list)+(len(height_list)-1)*fig_gap+(marginb+margint)
        # calculate the fraction position of each panel
        height_fractions = real_height_list/total_height
        gap_fraction = fig_gap/total_height
        domain_list = []
        pos_begin = marginb/total_height
        for fig_height in height_fractions:
            domain_list.append([pos_begin, pos_begin+fig_height])
            pos_begin += fig_height+gap_fraction
        # total_height is the absolute pixels of stack fig
        # domain_list is the fraction position of each panel
        return total_height, domain_list
    total_height, domain_list = get_stack_layout(height_list, 20)
    data_list = []
    layout = go.Layout()
    # aggregrate the traces
    for i,fig in enumerate(fig_list):
        domain = domain_list[i]
        # set position of each trace
        for trace in fig.data:
            trace.update(yaxis='y'+str(i+1))
            # set colorbar position
            if 'colorbar' in trace:
                trace.colorbar.update(dict(lenmode='fraction',len=np.abs(domain[1]-domain[0]),
                                           y=np.mean(domain)))
            data_list.append(trace)
        # keep the yaxis parameters of each panel and set the yaxis position
        fig.layout.yaxis.update(domain=domain)
        layout.update({'yaxis'+str(i+1):fig.layout.yaxis.copy()})
    layout.update(xaxis=fig_list[-1].layout.xaxis)
    layout.xaxis.update({'rangeslider':{'visible':False}})
    layout.update({'height':total_height, 'width':DEFAULT_WIDTH})
    layout.update(layout_params)
    fig = go.Figure(data=data_list,layout=layout)
    if showfig:
        iplot(fig)
    return fig
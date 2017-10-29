# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot
from .config import *

def tplot_line(time,
               value_list,
               value_name_list=[],
               trace_params=[],
               layout_params={},
               showfig=True):
    trace_list = []
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
    layout = DFAULT_TPLOT_LAYOUT
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
                   showfig=True):
    # TODO; warning
    valid_value = value[np.where(value>0)]
    # set 5% and 95% percentile of the value as colorbar min and max
    color_min=np.log10(np.nanpercentile(valid_value, 5))
    color_max=np.log10(np.nanpercentile(valid_value, 95))
    trace = go.Heatmap(x=time,y=y,z=np.log10(value),colorscale='Jet',zauto=False,
                        zmin=color_min, zmax=color_max, showscale=True)
    # set colorbar
    colorbar = DEFAULT_COLORBAR
    colorbar.update(colorbar_params)
    trace.update(colorbar=colorbar)
    # set trace params
    trace.update(trace_params)
    # set layout
    layout = DFAULT_TPLOT_LAYOUT
    layout.update(layout_params)
    fig = go.Figure(data=[trace],layout=layout)
    if showfig:
        iplot(fig)
    return fig

def stack_layout(height_list, fig_gap, marginb=DEFAULT_MARGIN, margint=DEFAULT_MARGIN):
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

def stack_figs(fig_list, showfig=True):
    # Share xaxis of figs in fig_list
    # return a single fig with multi-yaxis
    # get the pixel height of each panel
    height_list = np.array([fig.layout.height for fig in fig_list])
    total_height, domain_list = stack_layout(height_list, 20)
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
        layout.update({'yaxis'+str(i+1):fig.layout.yaxis})
    layout.update(xaxis=fig_list[-1].layout.xaxis)
    layout.xaxis.update({'rangeslider':{'visible':False}})
    layout.update({'height':total_height, 'width':DEFAULT_WIDTH})
    fig = go.Figure(data=data_list,layout=layout)
    if showfig:
        iplot(fig)
    return fig
import pandas as pd
import numpy as np
import os
import copy
import spacepku as sp
import spacepku.rbsptool as rbsp
from plotly import offline

def rbsp_overview(timerange,
                  save_path,
                  file_name=None,
                  twin='a',
                  log=False,
                  dist_normalize=False,
                  save_source=True,
                  expand_orbit=False):
    '''
    dist_normalize=True会在每个时间点上，把PSDnormalize到[0,1]
    '''
    # check input
    assert twin in ('a', 'b')
    
    # set time
    begin = timerange[0]
    end = timerange[1]
    if expand_orbit:
        begin = rbsp.orbit2time(rbsp.time2orbit(begin, tag='begin'))[0]
        end = rbsp.orbit2time(rbsp.time2orbit(end, tag='end'))[1]
    print('Generate rbsp {} pitchangle overview {} {}'.format(twin, timerange[0], timerange[1]))
    
    # load data
    rept_file_dir = rbsp.parse_rept_dir([begin, end], twin=twin)
    if not rept_file_dir:
        print('Fail! rept data missed between {} and {}'.format(begin, end))
        return None
    mageis_file_dir = rbsp.parse_mageis_dir([begin, end], twin=twin)
    if not mageis_file_dir:
        print('Fail! mageis data missed between {} and {}'.format(begin, end))
        return None
    B_component_file_dir = rbsp.parse_rbsp_B_component_dir([begin, end], twin=twin)
    if not B_component_file_dir:
        print('Fail! B component data missed between {} and {}'.format(begin, end))
        return None

    rept = sp.data_obj(rept_file_dir, 
                       data_keys=['Epoch', 'FEDU'], 
                       label_keys=['FEDU_PA_LABL', 'FEDU_ENERGY_LABL'])
    mageis = sp.data_obj(mageis_file_dir, 
                         data_keys=['Epoch', 'FEDU'], 
                         label_keys=['FEDU_PA_LABL', 'FEDU_ENERGY_LABL'])
    B = sp.data_obj(B_component_file_dir, 
                    data_keys=['Epoch', 'Mag', 'coordinates'])
    position = sp.data_obj(mageis_file_dir, 
                           data_keys=['Epoch', 'L', 'MLT', 'MLAT'])

    # init fig list
    fig_list = []

    # handle L&MLT&MLAT
    MLT = position['MLT']
    MLAT = position['MLAT']
    fig_position_info = ['MLT:{:.3f}<br>MLAT:{:.3f}'.format(i,j) for i,j in zip(MLT, MLAT)]
    params = {'ytitle':'L', 'name':'L', 'text':fig_position_info} 
    fig_position = sp.tplot_line_obj(position['Epoch'], position['L'], params).tplot(showfig=False)
    fig_list.append(fig_position)

    # handle B component
    mag = sp.field_aligned_coordinate(B['Mag'], B['coordinates'])
    delta_mag = mag - sp.smooth(mag, scale=50)
    # plot B
    params = {'ytitle':'B (nT)', 'yrange':[-300, 300]}
    fig_B = sp.stack_traces([sp.tplot_line_obj(B['Epoch'], mag[:, i], params).tplot(showfig=False) for i in range(3)], showfig=False)
    sp.set_params(fig_B, {'name':'Bx'}, trace_name=0)
    sp.set_params(fig_B, {'name':'By'}, trace_name=1)
    sp.set_params(fig_B, {'name':'Bz'}, trace_name=2)
    fig_list.append(fig_B)
    # plot delta B
    params = {'ytitle':'Delta B (nT)', 'yrange':[-5, 5]}
    fig_delta_B = sp.stack_traces([sp.tplot_line_obj(B['Epoch'], delta_mag[:, i], params).tplot(showfig=False) for i in range(3)], showfig=False)
    sp.set_params(fig_delta_B, {'name':'Delta Bx'}, trace_name=0)
    sp.set_params(fig_delta_B, {'name':'Delta By'}, trace_name=1)
    sp.set_params(fig_delta_B, {'name':'Delta Bz'}, trace_name=2)
    fig_list.append(fig_delta_B)

    # handle mageis figs
    pa = [float(i.split(' ')[0]) for i in mageis['FEDU_PA_LABL'][0]]
    energy_list = [''.join(i.split(' ')[:2]) for i in mageis['FEDU_ENERGY_LABL'][0]]
    for energy_index in [6, 9, 11, 14, 15]:
        fedu = mageis['FEDU'][:,:,energy_index] # index0->time, index1->pa
        params = {'ytitle':'{}'.format(energy_list[energy_index]),
                  'yrange':[0, 180],
                  'yticktext':['0', '45', '90', '135', '180'],
                  'ytickvals':[0, 45, 90, 135, 180],
                  'ctitle':'<br>PSD'}
        fig_temp = sp.tplot_heatmap_obj(mageis['Epoch'], pa, fedu, params).tplot(log=log, dist_normalize=dist_normalize, showfig=False)
        fig_list.append(fig_temp)

    # handle rept figs
    pa = [float(i.split(' ')[0]) for i in rept['FEDU_PA_LABL'][0]]
    energy_list = [''.join(i.split(' ')[:2]) for i in rept['FEDU_ENERGY_LABL'][0]]
    for energy_index in [0, 1, 2]:
        fedu = rept['FEDU'][:,:,energy_index] # index0->time, index1->pa
        params = {'ytitle':'{}'.format(energy_list[energy_index]),
                  'yrange':[0, 180],
                  'yticktext':['0', '45', '90', '135', '180'],
                  'ytickvals':[0, 45, 90, 135, 180],
                  'ctitle':'<br>PSD'}
        fig_temp = sp.tplot_heatmap_obj(rept['Epoch'], pa, fedu, params).tplot(log=log, dist_normalize=dist_normalize, showfig=False)
        fig_list.append(fig_temp)

    # stack all
    stack_fig_title = 'RBAP-{} overview {} to {}'.format(twin.upper(), timerange[0], timerange[1])
    if dist_normalize:
      stack_fig_title += ' normalized'
    stack_fig = sp.stack_figs(fig_list, {'title':stack_fig_title, 'showlegend':True}, showfig=False)
    sp.set_params(stack_fig, {'xrange':timerange})
    stack_fig['layout']['legend'].update({'y':0.148, 'yanchor':'middle'})
    stack_fig['layout']['height'] = stack_fig['layout']['height']*0.5

    # save fig
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    if not file_name:
        file_name = '_'.join(stack_fig_title.split(' '))
    sp.save_html(stack_fig, os.path.join(save_path, file_name))
    
    # save source
    if save_source:
        save_source_path = os.path.join(save_path, 'source')
        if not os.path.exists(save_source_path):
            os.mkdir(save_source_path)
        sp.save_fig(stack_fig, os.path.join(save_source_path, file_name))

    return stack_fig
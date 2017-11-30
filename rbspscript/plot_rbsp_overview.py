import pandas as pd
import numpy as np
import os
import copy
from spacepku import *
from plotly import offline

def rbsp_overview(date,
                  save_path,
                  log=False,
                  dist_normalize=False,
                  save_source=True):
    '''
    dist_normalize=True会在每个时间点上，把PSDnormalize到[0,1]
    '''
    # load data
    rept = cdf_obj(parse_rept_dir(date))
    mageis = cdf_obj(parse_mageis_dir(date))
    rbsp_b_component = cdf_obj(parse_rbsp_B_component_dir(date))

    # init fig list
    fig_list = []

    # handle L&MLT&MLAT
    fig_L = tplot_line_obj(mageis['Epoch'], mageis['L'], {'ytitle':'L', 'name':'L'}).tplot(showfig=False)
    MLT = mageis['MLT']
    MLAT = mageis['MLAT']
    position_info = ['MLT:{:.3f}<br>MLAT:{:.3f}'.format(i,j) for i,j in zip(MLT, MLAT)]
    fig_L['data'][0].update({'text':position_info})
    fig_list.append(fig_L)

    # handle B component
    fig_B = rbsp_b_component.tplot('Mag', type='line', showfig=False)
    set_params(fig_B, {'ytitle':'B (nT)', 'yrange':[-500, 500]})
    set_params(fig_B, {'name':'Bx'}, trace_name=0)
    set_params(fig_B, {'name':'By'}, trace_name=1)
    set_params(fig_B, {'name':'Bz'}, trace_name=2)
    fig_list.append(fig_B)

    # handle mageis figs
    time = mageis['Epoch']
    mageis_FEDU = mageis['FEDU']
    pa = [float(i.split(' ')[0]) for i in np.array(mageis['FEDU_PA_LABL'][0])]
    energy_list = [''.join(i.split(' ')[:2]) for i in mageis['FEDU_ENERGY_LABL'][0]]
    for energy_index in [6, 9, 11, 14, 15]:
        value_selected = mageis_FEDU[:,:,energy_index] # index0->time, index1->pa
        params = {'ytitle':'{}'.format(energy_list[energy_index]),
                  'yrange':[0, 180],
                  'yticktext':['0', '45', '90', '135', '180'],
                  'ytickvals':[0, 45, 90, 135, 180],
                  'ctitle':'<br>PSD'}
        fig_temp = tplot_heatmap_obj(time, pa, value_selected, params).tplot(log=log, dist_normalize=dist_normalize, showfig=False)
        fig_list.append(fig_temp)

    # handle rept figs
    time = rept['Epoch']
    rept_FEDU = rept['FEDU']
    pa = [float(i.split(' ')[0]) for i in np.array(rept['FEDU_PA_LABL'][0])]
    energy_list = [''.join(i.split(' ')[:2]) for i in rept['FEDU_ENERGY_LABL'][0]]
    for energy_index in [0, 1, 2]:
        value_selected = rept_FEDU[:,:,energy_index] # index0->time, index1->pa
        params = {'ytitle':'{}'.format(energy_list[energy_index]),
                  'yrange':[0, 180],
                  'yticktext':['0', '45', '90', '135', '180'],
                  'ytickvals':[0, 45, 90, 135, 180],
                  'ctitle':'<br>PSD'}
        fig_temp = tplot_heatmap_obj(time, pa, value_selected, params).tplot(log=log, dist_normalize=dist_normalize, showfig=False)
        fig_list.append(fig_temp)

    # stack all
    stack_fig_title = 'RBAP-A overview {}'.format(date)
    if dist_normalize:
      stack_fig_title += ' normalized'
    stack_fig = stack_figs(fig_list, {'title':stack_fig_title, 'showlegend':False}, showfig=False)
    stack_fig['layout']['height'] = stack_fig['layout']['height']*0.5

    # save fig
    if not os.path.exists(save_path):
        os.mkdir(save_path)
        
    if dist_normalize:
        file_name = 'rbspa_overview_{}_normalized'.format(date)
    else:
        file_name = 'rbspa_overview_{}'.format(date)
    
    save_file_path = os.path.join(save_path, file_name+'.html')
    offline.plot(stack_fig, filename=save_file_path)
    
    # save source
    if save_source:
        save_source_path = os.path.join(save_path, 'source')
        if not os.path.exists(save_source_path):
            os.mkdir(save_source_path)
    save_fig(stack_fig, os.path.join(save_source_path, file_name+'.source'))

    return stack_fig

# for test
if __name__ == '__main__':
    rbsp_demo_file_path = '/Users/leimingda/Documents/code/spacepku/rbsp_demo/'
    rept_file_name = 'rbspa_rel03_ect-rept-sci-L3_20131229_v5.0.0.cdf'
    mageis_file_name = 'rbspa_rel03_ect-mageis-L3_20131229_v7.3.0.cdf'
    rept_file_path = os.path.join(demo_file_path, rept_file_name)
    mageis_file_path = os.path.join(demo_file_path, mageis_file_name)
    date = '20131229'

    rbsp_overview(mageis_file_path=mageis_file_path,
        rept_file_path=rept_file_path, date=date)
    offline.plot(stack, filename='rbspa_overview_{}.html'.format(date))

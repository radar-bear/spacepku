import pandas as pd
import numpy as np
import os
import copy
from spacepy.pycdf import CDF
import plotly.offline as offline
from .plot import *
from .config import *
def rbsp_overview(rept_file_path, 
                  mageis_file_path, 
                  rbsp_b_component_file_path, 
                  date, 
                  save_path, 
                  dist_normalize=False):
    '''
    dist_normalize=True会在每个时间点上，把PSDnormalize到[0,1]
    '''
    # load data
    rept_data = CDF(rept_file_path)
    mageis_data = CDF(mageis_file_path)
    rbsp_b_component_data = CDF(rbsp_b_component_file_path)
    
    # init fig list
    fig_list = []
    
    # handle L&MLT&MLAT
    time = np.array(mageis_data['Epoch'])
    df = pd.DataFrame({'L':np.array(mageis_data['L']), 
                       'MLT':np.array(mageis_data['MLT']),
                       'MLAT':np.array(mageis_data['MLAT']),
                       'time':time})
    df.where(df>-1e30, np.nan, inplace=True)
    position_info = ['MLT:{:.3f}<br>MLAT:{:.3f}'.format(i,j) for i,j in zip(df['MLT'],df['MLAT'])]
    layout_params = {'yaxis':{'title':'L'}}
    trace_params = {'text':position_info}
    fig_list.append(tplot_line(df['time'], [df['L']],
                           value_name_list=['L'],
                           trace_params=trace_params,
                           layout_params=layout_params,
                           showfig=False))
    
    # handle B component
    time = np.array(rbsp_b_component_data['Epoch'])
    b_component = np.array(rbsp_b_component_data['Mag'])
    df = pd.DataFrame({'B_x':b_component[:, 0],
                       'B_y':b_component[:, 1],
                       'B_z':b_component[:, 2],
                       'time':time})
    layout_params = {'yaxis':{'title':'B (nT)',
                              'range':[0, 1000]}}
    fig_list.append(tplot_line(df['time'], [df['B_x'], df['B_y'], df['B_z']],
                                    value_name_list=['B_x','B_y','B_z'],
                                    layout_params=layout_params,
                                    showfig=False))
    
    # handle mageis figs
    time = pd.Series(mageis_data['Epoch']) # use pandas to keep consistance with the figs above (important!)
    pa = [float(i.split(' ')[0]) for i in np.array(mageis_data['FEDU_PA_LABL'][0])]
    value = np.array(mageis_data['FEDU'])
    energy_list = [''.join(i.split(' ')[:2]) for i in np.array(mageis_data['FEDU_ENERGY_LABL'])[0]]
    for energy_index in [6, 9, 11, 14, 15]:
        value_selected = value[:,:,energy_index] # index0->time, index1->pa
        layout_params = {'yaxis':{'title':'{}'.format(energy_list[energy_index]),
                                  'ticktext':['0', '45', '90', '135', '180'],
                                  'tickvals':[0, 45, 90, 135, 180], 
                                  'range':[0,180]}}
        colorbar_params = {'title':'<br>PSD'}
        fig_list.append(tplot_particle(time, pa, value_selected.T,
                                       dist_normalize=dist_normalize,
                                       layout_params=layout_params,
                                       colorbar_params=colorbar_params,
                                       log=False,
                                       showfig=False))
        
    # handle rept figs
    time = pd.Series(rept_data['Epoch'])
    pa = [float(i.split(' ')[0]) for i in np.array(rept_data['FEDU_PA_LABL'][0])]
    value = np.array(rept_data['FEDU_0to180'])
    energy_list = [''.join(i.split(' ')[:2]) for i in np.array(rept_data['FEDU_ENERGY_LABL'])[0]]
    for energy_index in range(3):
        value_selected = value[:,:,energy_index]
        layout_params = {'yaxis':{'title':'{}'.format(energy_list[energy_index]),
                                  'ticktext':['0', '45', '90', '135', '180'],
                                  'tickvals':[0, 45, 90, 135, 180],
                                  'autorange':False,
                                  'range':[0,180]}}
        colorbar_params = {'title':'<br>PSD'}
        fig_list.append(tplot_particle(time, pa, value_selected.T,
                                       layout_params=layout_params,
                                       dist_normalize=dist_normalize,
                                       colorbar_params=colorbar_params,
                                       log=False,
                                       showfig=False))

    # stack all
    stack = stack_figs(copy.deepcopy(fig_list), showfig=False)
    stack['layout']['title'] = 'RBAP-A overview {}'.format(date)
    if dist_normalize:
        stack['layout']['title'] = stack['layout']['title'] + ' normalized'
    stack['layout']['height'] = stack['layout']['height']*0.5
    stack['layout']['showlegend'] = False
    
    # save
    if dist_normalize:
        save_file_path = os.path.join(save_path, 'rbspa_overview_{}_normalized.html'.format(date))
    else:
        save_file_path = os.path.join(save_path, 'rbspa_overview_{}.html'.format(date))
    offline.plot(stack, filename=save_file_path)
    
    return fig_list, stack

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

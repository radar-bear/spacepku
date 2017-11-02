import pandas as pd
import numpy as np
import os
from spacepy.pycdf import CDF
import plotly.offline as offline
from spacepku import plot

def rbsp_overview(rept_file_path, mageis_file_path, date, save_path):
    rept_data = CDF(rept_file_path)
    mageis_data = CDF(mageis_file_path)
    fig_list = []
    # handel B&L&MLT
    time = np.array(mageis_data['Epoch'])
    df = pd.DataFrame({'L':np.array(mageis_data['L']), 'MLT':np.array(mageis_data['MLT']),
                       'B_Calc':np.array(mageis_data['B_Calc']),
                       'B_Eq':np.array(mageis_data['B_Eq']), 'time':time})
    df.where(df>-1e30, np.nan, inplace=True)
    layout_params = {'yaxis':{'title':'L'}}
    fig_list.append(plot.tplot_line(df['time'], [df['L']],
                           value_name_list=['L'],
                           layout_params=layout_params,
                           showfig=False))
    layout_params = {'yaxis':{'title':'MLT'}}
    fig_list.append(plot.tplot_line(df['time'], [df['MLT']],
                           value_name_list=['MLT'],
                           layout_params=layout_params,
                           showfig=False))
    layout_params = {'yaxis':{'title':'B (nT)'}}
    fig_list.append(plot.tplot_line(df['time'], [df['B_Calc'], df['B_Eq']],
                                    value_name_list=['B_Calc','B_Eq'],
                                    layout_params=layout_params,
                                    showfig=False))
    # handel mageis figs
    time = np.array(mageis_data['Epoch'])
    pa = [float(i.split(' ')[0]) for i in np.array(mageis_data['FEDU_PA_LABL'][0])]
    value = np.array(mageis_data['FEDU'])
    energy_list = [''.join(i.split(' ')[:2]) for i in np.array(mageis_data['FEDU_ENERGY_LABL'])[0]]
    for energy_index in [6, 9, 11, 14, 15]:
        value_selected = value[:,:,energy_index]
        layout_params = {'yaxis':{'title':'MAGEIS FEDU <br> {}'.format(energy_list[energy_index]),
                                  'range':[0,180]}}
        fig_list.append(plot.tplot_particle(time, pa, value_selected.T,
                                            layout_params=layout_params, showfig=False))
    # handel rept figs
    time = np.array(rept_data['Epoch'])
    pa = [float(i.split(' ')[0]) for i in np.array(rept_data['FEDU_PA_LABL'][0])]
    value = np.array(rept_data['FEDU_0to180'])
    energy_list = [''.join(i.split(' ')[:2]) for i in np.array(rept_data['FEDU_ENERGY_LABL'])[0]]
    for energy_index in range(3):
        value_selected = value[:,:,energy_index]
        layout_params = {'yaxis':{'title':'ECT FEDU <br> {}'.format(energy_list[energy_index]),
                                  'range':[0,180]}}
        fig_list.append(plot.tplot_particle(time, pa, value_selected.T,
                                            layout_params=layout_params,showfig=False))
    # stack all
    stack = plot.stack_figs(fig_list.copy(),showfig=False)
    stack['layout']['title']='RBAP-A overview {}'.format(date)
    stack['layout']['height'] = stack['layout']['height']*0.5
    save_file_path = os.path.join(save_path, 'rbspa_overview_{}.html'.format(date))
    offline.plot(stack, filename=save_file_path)
    return stack

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
import numpy as np

def set_colorbar_sliders(fig, maxrange=[], minrange=[]):
    # set slider steps
    cmax = fig['data'][0]['zmax']
    cmin = fig['data'][0]['zmin']
    if len(maxrange) == 0:
        maxrange = np.linspace(cmax, cmax-(cmax-cmin)/3, 5)
    if len(minrange) == 0:
        minrange = np.linspace(cmin, cmin+(cmax-cmin)/3, 5)
    # set up slider
    up_sliders_dict = {
        'active': 0,
        'yanchor': 'bottom',
        'xanchor': 'right',
        'currentvalue': {
                'font': {'size': 10},
                'visible': True,
                'prefix': 'colorbar max: ',
                'xanchor': 'right'
            },
        'len': 0.4,
        'x': 1.0,
        'y': 1.2,
        'steps': []
    }
    for i in maxrange:
        slider_step = {'args': ['zmax',i],
                       'method': 'restyle',
                       'label': i}
        up_sliders_dict['steps'].append(slider_step)
    # set down slider
    down_sliders_dict = {
        'active': 0,
        'yanchor': 'up',
        'xanchor': 'right',
        'currentvalue': {
                'font': {'size': 15},
                'visible': True,
                'prefix': 'colorbar min: ',
                'xanchor': 'right'
            },
        'len': 0.4,
        'x': 1.0,
        'y': -0.2,
        'steps': []
    }
    for i in minrange:
        slider_step = {'args': ['zmin',i],
                       'method': 'restyle',
                       'label': i}
        down_sliders_dict['steps'].append(slider_step)
    if 'sliders' in fig['layout']:
        fig['layout']['sliders'] += [up_sliders_dict, down_sliders_dict]
    else:
        fig['layout']['sliders'] = [up_sliders_dict, down_sliders_dict]
        
def set_animation_buttons(fig, frame_interval, trans_interval, frame_mask=[]):
    # play and pause button
    animate_buttons = [
        {
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': frame_interval, 'redraw': False},
                             'fromcurrent': True, 'transition': {'duration': trans_interval, 'easing': 'cubic-in-out'}}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': frame_interval, 'redraw': False}, 'mode': 'immediate',
                    'transition': {'duration': trans_interval}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
#             'pad': {'r': 10, 't': 10},
            'showactive': False,
            'type': 'buttons',
            'x': 0,
            'xanchor': 'left',
            'y': 1.1,
            'yanchor': 'bottom'
        }
    ]
    # slider
    if len(frame_mask) == 0:
        frame_mask = np.ones(len(fig['frames']))
    assert len(frame_mask) == len(fig['frames'])
    sliders_dict = {
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 20},
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': trans_interval, 'easing': 'cubic-in-out'},
#         'pad': {'b': 10, 't': 50},
        'len': 1.0,
        'x': 0,
        'y': -0.1,
        'steps': []
    }
    for i, frame in enumerate(fig['frames']):
        if not frame['name']:
            frame['name'] = i
        slider_step = {'args': [
            [frame['name']],
            {'frame': {'duration': frame_interval, 'redraw': False},
             'mode': 'immediate',
           'transition': {'duration': trans_interval}}
         ],
         'label': frame['name'],
         'method': 'animate'}
        if frame_mask[i]:
            sliders_dict['steps'].append(slider_step)
    # update buttons and sliders
    fig['layout']['updatemenus'] = animate_buttons
    fig['layout']['sliders'] = [sliders_dict]
def make_animation(frame_list, background=None, frame_name_list=None, frame_mask=[], frame_interval=300, trans_interval=100):
    from copy import deepcopy
    fig = deepcopy(frame_list[0])
    if background:
        fig['data'] += background['data']
    if frame_name_list:
        assert len(frame_name_list) == len(fig_list)
        for frame, frame_name in zip(frame_list, frame_name_list):
            frame['name'] = frame_name
    fig['frames'] = frame_list
    set_animation_buttons(fig, frame_interval, trans_interval, frame_mask=frame_mask)
    return fig

def set_animation_buttons(fig, frame_interval, trans_interval, frame_mask=[]):
    # play and pause button
    animate_buttons = [
        {
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': frame_interval, 'redraw': False},
                             'fromcurrent': True, 'transition': {'duration': trans_interval, 'easing': 'quadratic-in-out'}}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                    'transition': {'duration': 0}}],
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
    
def save_gif(fig, file_name, duration=0.3, loop=False, scale=1):
    if file_name.split('.') != 'gif':
        file_name += '.gif'
    import imageio
    import os
    from datetime import datetime
    from copy import deepcopy
    from .utils import save_png
    images = []
    temp_fname = 'temp' + datetime.now().isoformat() + '.png'
    background = fig['data'][1:]
    for frame in fig['frames']:
        tempfig = deepcopy(frame)
        frame['data'] += background
        save_png(tempfig, temp_fname, scale=scale)
        images.append(imageio.imread(temp_fname))
    os.remove(temp_fname)
    imageio.mimsave(file_name, images, duration=duration, loop=loop)
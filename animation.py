import numpy as np
from .control import set_animation_buttons

def make_animation(frame_list, background=None, frame_name_list=None, frame_mask=[], frame_interval=300, trans_interval=100):
    from copy import deepcopy
    fig = deepcopy(frame_list[0])
    if background:
        fig['data'] += background['data']
    if frame_name_list:
        assert len(frame_name_list) == len(frame_list)
        for frame, frame_name in zip(frame_list, frame_name_list):
            frame['name'] = frame_name
    fig['frames'] = frame_list
    set_animation_buttons(fig, frame_interval, trans_interval, frame_mask=frame_mask)
    return fig
    
def save_gif(fig, file_name, duration=0.3, loop=False, scale=1):
    if file_name.split('.')[-1] != 'gif':
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
        tempfig['data'] += background
        save_png(tempfig, temp_fname, scale=scale)
        images.append(imageio.imread(temp_fname))
    os.remove(temp_fname)
    imageio.mimsave(file_name, images, duration=duration, loop=loop)
    
def save_movie(fig, file_name, duration, scale):
    from datetime import datetime
    temp_fname = 'temp' + datetime.now().isoformat() + '.gif'
    save_gif(fig, temp_fname, duration=duration, loop=1, scale=scale)
    gif_to_movie(temp_fname, file_name)
    os.remove(temp_fname)
               
def gif_to_movie(gif_file_name, movie_name):
    import moviepy.editor as mp
    clip = mp.VideoFileClip(gif_file_name)
    clip.write_videofile(movie_name)
   
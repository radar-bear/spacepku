# -*- coding: utf-8 -*-
from plotly.graph_objs import *
import numpy as np
import pandas as pd
import os

##################################
# version information

VERSION = '0.0.1'

##################################
# default key config

DEFAULT_TIME_KEY = ['Epoch', 'epoch', 'IsoTime', 'isotime', 'Time', 'time']
DEFAULT_FILLVAL_KEY = ['FILLVAL']


##################################
# env config

def pku_mag_init(jupyter=True):
    # set os env
    import os
    os.environ['CDF_LIB'] = '/lib'
    # set jupyter env for plotly
    if jupyter:
        from plotly.offline import init_notebook_mode
        init_notebook_mode()


##################################
# plot config

DEFAULT_MARGIN = 60
DEFAULT_WIDTH = 900
DEFAULT_HEIGHT = 350


def get_default_layout():
    default_layout = Layout(
        xaxis=XAxis(rangeslider=dict(visible=False),
                    showline=True,
                    showgrid=True,
                    zeroline=False,
                    nticks=10,
                    mirror='all'),
        yaxis=YAxis(autorange=True,
                    showline=True,
                    showgrid=True,
                    zeroline=False,
                    mirror='all'),
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        margin=dict(l=DEFAULT_MARGIN,
                    r=DEFAULT_MARGIN,
                    b=DEFAULT_MARGIN,
                    t=DEFAULT_MARGIN),
    )
    return default_layout


def get_default_colorbar():
    default_colorbar = ColorBar(
        thicknessmode='fraction',
        thickness=0.015,
        # lenmode='pixels',
        # len=DEFAULT_HEIGHT-2*DEFAULT_MARGIN,
        titleside='right'
    )
    return default_colorbar

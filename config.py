# -*- coding: utf-8 -*-
from plotly.graph_objs import *
import numpy as np
import pandas as pd
import os

DEFAULT_MARGIN = 60
DEFAULT_WIDTH = 900
DEFAULT_HEIGHT = 350
def get_default_layout():
    default_layout = Layout(
        xaxis=XAxis(rangeslider=dict(visible=False),
                    showline=True,
                    showgrid=True,
                    zeroline=False,
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
        #lenmode='pixels',
        #len=DEFAULT_HEIGHT-2*DEFAULT_MARGIN,
        titleside='right'
    )
    return default_colorbar

RBSP_PATH = '/data/ECT/rbsp-ect.lanl.gov/data_pub/rbspa/'
RBSP_B_COMPONENT_PATH = '/data/EMFISIS/emfisis.physics.uiowa.edu/Flight/RBSP-A/L3'



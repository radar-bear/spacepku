# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os

DEFAULT_MARGIN = 80
DEFAULT_WIDTH = 900
DEFAULT_HEIGHT = 350
DFAULT_TPLOT_LAYOUT = {
    'xaxis':{
        'rangeslider':{
            'visible':False
        }
    },
    'yaxis':{
        'autorange':True
    },
    'width':DEFAULT_WIDTH,
    'height':DEFAULT_HEIGHT,
    'margin':{
        'l':DEFAULT_MARGIN, 'r':DEFAULT_MARGIN,
        'b':DEFAULT_MARGIN, 't':DEFAULT_MARGIN
    }
}
DEFAULT_COLORBAR = {
    'thicknessmode':'fraction',
    'thickness':0.02,
    'lenmode':'pixels',
    'len':DEFAULT_HEIGHT-2*DEFAULT_MARGIN,
    'titleside':'right'
}
MAGEIS_PATH = '/data/ECT/rbsp-ect.lanl.gov/data_pub/rbspa/mageis/level3/pitchangle/'



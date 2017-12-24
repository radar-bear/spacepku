import pandas as pd
import numpy as np
import spacepy.omni as om

def get_omni(time_series, dbase='QDhourly'):
    return om.get_omni(time_series, dbase=dbase)
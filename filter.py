'''
实现rolling mean
'''
import numpy as np
import pandas as pd
from scipy.interpolate import spline

def rolling(df, window, func, center=False):
    '''
    By default, the result is set to the right edge of the window. This can be changed to the center of the window by setting ``center=True``
    '''
    if not isinstance(dr, (pd.DataFrame, pd.Series)):
        df = pd.DataFrame(df)
    return df.rolling(window, min_periods=1, center=center).apply(func).values

def moving_average(df, window, center=False):
    return rolling(df, window, lambda x: np.nanmean(x, axis=0))

def smooth(x, y, scale=5):
    '''
    smooth the x-y curve with scale*len(x) points
    '''
    xnew = np.linspace(np.max(x), np.min(x), len(x)*scale)
    ynew = spline(x, y, xnew)
    return xnew, ynew
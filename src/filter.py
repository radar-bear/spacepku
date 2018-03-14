'''
实现rolling mean
'''
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, interp2d


def rolling(df, window, func, center=True):
    '''
    By default, the result is set to the right edge of the window. This can be changed to the center of the window by setting ``center=True``
    '''
    if not isinstance(df, (pd.DataFrame, pd.Series)):
        df = pd.DataFrame(df)
    return df.rolling(window, min_periods=1, center=center).apply(func).values


def moving_average(df, window, center=True):
    return rolling(df, window, lambda x: np.nanmean(x, axis=0))


def smooth(value, scale=10):
    '''
    denoise list-like variable value using MA
    this function won't change len(x)
    '''
    return moving_average(pd.DataFrame(value), window=scale)


def smooth2d(value, scale=(10, 10)):
    assert len(scale) == 2
    # axis0 moving average
    df = moving_average(pd.DataFrame(value), window=scale[0])
    # axis1 moving average
    df = moving_average(pd.DataFrame(df).T, window=scale[1]).T
    return df


def resample(x, value, scale=1, kind='linear', xnew=np.array([])):
    '''
    resample x-y series
    scale > 1 for upsample
    scale < 1 for downsample
    this function won't smooth the curve
    this function will change len(x)
    fill nan if xnew is wider than x
    '''
    xnew = np.array(xnew)
    if len(xnew) == 0:
        xnew = np.linspace(np.nanmin(x), np.nanmax(x), int(len(x) * scale))
    bool_index = (xnew > np.nanmin(x)) & (xnew < np.nanmax(x))
    valueNew = np.zeros(len(xnew))
    valueNew.fill(np.nan)
    f = interp1d(x, value, kind=kind)
    valueNew[bool_index] = f(xnew[bool_index])
    return xnew, valueNew


def resample2d(x, y, value, xscale=1, yscale=1, kind='linear', xnew=[], ynew=[]):
    '''
    scale must be a two element tuple
    TODO: 使用nan填充超出原始范围的插值
    '''
    xnew = np.array(xnew)
    ynew = np.array(ynew)
    if len(xnew) == 0:
        xnew = np.linspace(np.nanmin(x), np.nanmax(x), int(len(x) * xscale))
    if len(ynew) == 0:
        ynew = np.linspace(np.nanmin(y), np.nanmax(x), int(len(x) * yscale))
    f = interp2d(x, y, value, kind=kind)
    valuenew = f(xnew, ynew)
    return xnew, ynew, valuenew


def polyfit(x, y, xnew, degree=3):
    z = np.polyfit(x, y, degree)
    f = np.poly1d(z)
    return f(xnew)

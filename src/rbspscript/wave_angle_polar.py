import spacepku as sp
import spacepku.rbsptool as rbsp
import pandas as pd
import numpy as np
import os
import re


def get_wave_info(date, twin='a'):

    data = sp.data_obj(rbsp.parse_rbsp_wave_matrix_dir(date, twin=twin))
    background = sp.data_obj(
        rbsp.parse_rbsp_wave_background_dir(date, twin=twin))
    lenb = len(background['Epoch'])
    lend = len(data['Epoch'])
    mag = background['Mag'][:]
    backgroundMag = np.array([mag[int(lenb * i / lend)] for i in range(lend)])
    BBmatrix = np.array([[data['BuBu'] + 1j * 0, data['BuBv'][:, 0, :] + 1j * data['BuBv'][:, 1, :], data['BuBw'][:, 0, :] + 1j * data['BuBw'][:, 1, :]],
                         [data['BuBv'][:, 0, :] - 1j * data['BuBv'][:, 1, :], data['BvBv'] +
                             1j * 0, data['BvBw'][:, 0, :] + 1j * data['BvBw'][:, 1, :]],
                         [data['BuBw'][:, 0, :] - 1j * data['BuBw'][:, 1, :], data['BvBw'][:, 0, :] - 1j * data['BvBw'][:, 1, :], data['BwBw'] + 1j * 0]])
    BBmatrix = np.transpose(BBmatrix, [2, 3, 0, 1])
    polar, angle = sp.wave_polar_and_angle(BBmatrix, backgroundMag)
    waveBSquare = data['BuBu'] + data['BvBv'] + data['BwBw']
    waveESquare = data['EuEu'] + data['EvEv'] + data['EwEw']

    res = {
        'Epoch': data['Epoch'],
        'Angle': angle,
        'Polar': polar,
        'BSquare': waveBSquare,
        'ESquare': waveESquare,
    }

    return res

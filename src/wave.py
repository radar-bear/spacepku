import numpy as np
import pandas as pd

# 把数据按照window划分，每个window内做fft，这一操作过程会对原始数据下采样，使得分辨率变为原始数据的1/window
# 返回fft复矩阵 (time * frequency * value)，


def wave_fft(data, time, window):
    fft = np.array([np.fft.fft(data[i * window:(i + 1) * window])
                    [:int(window / 2) + 1] for i in range(int(len(data) / window))])
    newtime = np.array([time[i * window]
                        for i in range(int(len(data) / window))])
    duration = (pd.to_datetime(np.max(time)) -
                pd.to_datetime(np.min(time))).total_seconds()
    sample_frequency = len(data) / duration
    frequency = np.array(
        [i * sample_frequency / window for i in range(fft.shape[1])])
    return fft, newtime, frequency

# 输入B*B的复数矩阵和背景磁场,得到极化率和波矢方向
# 两个矩阵对应元素相乘用np.multiply


def wave_polar_and_angle(BBmatrix, background):
    '''
    BBmatrix is a complex np.array with shape (time * frequency * 3 * 3)
    the 3*3 submatrix is
    Bx*Bx Bx*By Bx*Bz
    By*Bx By*By By*Bz
    Bz*Bx Bz*By Bz*Bz
    where Bx*Bx means conjugate Bx multiply Bx

    Background is the background magnetic field with shape (time * 3)
    '''
    from numpy import linalg as la

    RBBmatrix = BBmatrix.real
    IBBmatrix = BBmatrix.imag
    A = np.concatenate([RBBmatrix, IBBmatrix], axis=2)

    shape = A.shape[:2]
    angle = np.zeros(shape)
    polar = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            U, sigma, VT = la.svd(A[i, j])
            sigma = np.abs(sigma)
            sort_index = np.argsort(sigma)  # 从小到大
            k = VT[sort_index[-1], :]
            angle[i, j] = np.arccos(
                np.sum(k * background[i]) / (la.norm(k) * la.norm(background[i]))) * 180 / np.pi
            polar[i, j] = sigma[sort_index[1]] / sigma[sort_index[2]]
            if angle[i, j] > 90:
                polar[i, j] *= -1

    return polar, angle

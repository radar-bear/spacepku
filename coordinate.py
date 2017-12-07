import numpy as np

def field_aligned_coordinate(B, pos, window=50):
    assert B.shape == pos.shape
    new_B = np.array(np.zeros(B.shape))
    for i in range(len(B)):
        aver_B = np.mean(B[max(0, i-window):i+1], axis=0)
        xaxis = aver_B
        yaxis = pos[i]
        zaxis = np.cross(xaxis, yaxis)
        yaxis = np.cross(zaxis, xaxis)
        new_coor = np.array([xaxis, yaxis, zaxis]).T
        new_B[i] = transfer_3d_coordinate(B[i], new_coor)
    return new_B

def transfer_3d_coordinate(value, new_coor):
    value = np.array(value)
    new_coor = np.array(new_coor)
    assert value.shape[-1] == 3
    assert new_coor.shape == (3,3)
    new_coor = new_coor/np.linalg.norm(new_coor,axis=0)
    return np.dot(value, new_coor)


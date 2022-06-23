import numpy as np


def dci(self):
    mat = self.mat.astype('float32')
    np.fill_diagonal(mat, np.nan)
    return round(np.nansum(np.abs(mat - np.transpose(mat))) / 2 / np.nansum(mat), 4)
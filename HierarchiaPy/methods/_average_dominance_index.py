import numpy as np


def average_dominance_index(self):
    mat = self.mat.astype('float64')
    np.fill_diagonal(mat, np.nan)
    sum_mat = mat.copy()

    for idx in range(0, mat.shape[0]):
        for idy in range(idx + 1, mat.shape[0]):
            temp_sum = mat[idx, idy] + mat[idy, idx]
            if temp_sum > 0:
                sum_mat[idx, idy] = temp_sum
                sum_mat[idy, idx] = temp_sum
            else:
                sum_mat[idx, idy] = np.nan
                sum_mat[idy, idx] = np.nan

    prop_mat = mat / sum_mat
    var_w = np.nansum(prop_mat, axis=1)
    var_adi = var_w / np.count_nonzero(~np.isnan(prop_mat), axis=1)

    average_dominance_index_dict = {i: round(var_adi[idx], 4) for idx, i in enumerate(self.indices)}
    return average_dominance_index_dict

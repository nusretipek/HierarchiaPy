import numpy as np


def davids_score(self):
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
    var_l = np.nansum(prop_mat, axis=0)
    var_w = np.nansum(prop_mat, axis=1)
    var_l2 = np.nansum(np.transpose(prop_mat) * var_l, axis=1)
    var_w2 = np.nansum(prop_mat * var_w, axis=1)
    var_ds = var_w + var_w2 - var_l - var_l2

    davids_score_dict = {i: round(var_ds[idx], 4) for idx, i in enumerate(self.indices)}
    return davids_score_dict


import numpy as np
import pandas as pd


def _static_get_Dij(mat):
    total_mat = mat + np.transpose(mat)
    mat = np.divide(mat, total_mat, out=np.zeros_like(mat), where=total_mat != 0)
    mat -= np.divide((mat - 0.5), total_mat + 1, out=np.zeros_like(mat), where=total_mat != 0)
    return mat


def _static_davids_score(mat, method, indices, normalize=True):
    # Assertions
    assert method in ['Dij', 'Pij']
    assert type(normalize) == bool

    # Matrix manipulation
    mat = mat.astype('float64')
    if method == 'Dij':
        mat = _static_get_Dij(mat)

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

    # Calculation of matrix properties
    prop_mat = mat / sum_mat
    var_l = np.nansum(prop_mat, axis=0)
    var_w = np.nansum(prop_mat, axis=1)
    var_l2 = np.nansum(np.transpose(prop_mat) * var_l, axis=1)
    var_w2 = np.nansum(prop_mat * var_w, axis=1)
    var_ds = var_w + var_w2 - var_l - var_l2

    # Create David's score dictionary
    davids_score_dict = {i: round(var_ds[idx], 4) for idx, i in enumerate(indices)}

    if not normalize:
        return davids_score_dict
    else:
        normalised_davids_score_dict = {
            key: (davids_score_dict[key] + (len(davids_score_dict) * (len(davids_score_dict) - 1) / 2)) / len(
                davids_score_dict) for key in davids_score_dict}
        return normalised_davids_score_dict


def _static_steepness(mat, method, indices):
    # Get normalized David's score
    normalised_davids_score_dict = _static_davids_score(mat=mat, method=method, indices=indices, normalize=True)

    # Calculate slope
    y = sorted(list(normalised_davids_score_dict.values()), reverse=True)
    x = np.arange(1, len(y) + 1)
    mat_a = np.vstack([x, np.ones(len(y))]).T
    slope, constant = np.linalg.lstsq(mat_a, y, rcond=None)[0]

    # Return statement
    return round(abs(slope), 4)


def get_Dij(self):
    # Calculate Dij
    mat = self.mat.astype('float64')
    dij = _static_get_Dij(mat)
    # Return statement
    return dij.round(decimals=4, out=dij)


def get_steepness(self, method='Dij'):
    # Assertions
    assert method in ['Dij', 'Pij']

    # Return statement
    return _static_steepness(mat=self.mat, method=method, indices=self.indices)


def _randomize_mat(mat):
    # Randomize the matrix
    temp_mat = mat.copy()
    for idx in range(temp_mat.shape[0]):
        for idy in range(idx + 1, temp_mat.shape[0]):
            n_ij = temp_mat[idx, idy] + temp_mat[idy, idx]
            random_i = int(np.random.randint(0, n_ij + 1))
            random_j = int(n_ij - random_i)
            temp_mat[idx, idy] = random_i
            temp_mat[idy, idx] = random_j
    return temp_mat

def steepness_test(self, method='Dij', n=2000):
    # Assertions
    assert type(n) == int and (0 < n <= 1000000)

    # Declaration of variables
    abs_slope_list = []
    initial_steep = _static_steepness(mat=self.mat, method=method, indices=self.indices)

    # Loop n times to get_steepness
    for _ in range(n):
        temp_abs_slope = _static_steepness(mat=_randomize_mat(self.mat), method=method, indices=self.indices)
        abs_slope_list.append(temp_abs_slope)

    # Verbose Results
    steep_series = pd.Series(abs_slope_list)
    steep_desc = steep_series.describe()
    right_p = ((len(steep_series[steep_series > abs(initial_steep)])) / len(steep_series))
    left_p = ((len(steep_series[steep_series < abs(initial_steep)])) / len(steep_series))
    steepness_test_dict = {
        'steepness': round(initial_steep, 4),
        'p_value_r': round(right_p, 4),
        'p_value_l': round(left_p, 4),
        'mean': round(steep_desc['mean'], 4),
        'std_dev': round(steep_desc['std'], 4),
        'min': round(steep_desc['min'], 4),
        'max': round(steep_desc['max'], 4),
        'percentile_25': round(steep_desc['25%'], 4),
        'percentile_50': round(steep_desc['50%'], 4),
        'percentile_75': round(steep_desc['75%'], 4),
        'count': n
    }

    # Return statements
    return steepness_test_dict

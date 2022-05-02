from scipy.stats.distributions import chi2
from itertools import *
import numpy as np
import warnings


def get_ecdf(n, runs=100000):
    results = {}
    d_master = []
    for _ in range(runs):
        mat = np.random.randint(0, 1000, size=(n, n)).astype('float32')
        np.fill_diagonal(mat, 0)
        for idx in range(mat.shape[0]):
            for idy in range(idx + 1, mat.shape[0]):
                if mat[idx, idy] == mat[idy, idx]:
                    mat[idx, idy] = 0.5
                    mat[idy, idx] = 0.5
                elif mat[idx, idy] > mat[idy, idx]:
                    mat[idx, idy] = 1
                    mat[idy, idx] = 0
                else:
                    mat[idx, idy] = 0
                    mat[idy, idx] = 1
        d_master.append(((n * (n - 1) * (2 * n - 1)) / 12) - (0.5 * np.sum(np.sum(mat, axis=1) ** 2, axis=0)))

    sorted_d_master = np.sort(np.array(d_master))
    for d_idx in np.unique(sorted_d_master):
        if len(np.argwhere(sorted_d_master == d_idx)) > 0:
            results[d_idx] = round((np.argwhere(sorted_d_master == d_idx)[-1] / runs)[0], 3)

    return results


def kendall_k(self, odd_K=False):
    results = {}
    initial_ecdf_samples = 100000
    mat = self.mat.astype('float32')

    for idx in range(mat.shape[0]):
        for idy in range(idx + 1, mat.shape[0]):
            if mat[idx, idy] == mat[idy, idx]:
                mat[idx, idy] = 0.5
                mat[idy, idx] = 0.5
            elif mat[idx, idy] > mat[idy, idx]:
                mat[idx, idy] = 1
                mat[idy, idx] = 0
            else:
                mat[idx, idy] = 0
                mat[idy, idx] = 1

    results['d'] = ((mat.shape[0] * (mat.shape[0] - 1) * (2 * mat.shape[0] - 1)) / 12) - (0.5 * np.sum(
        np.sum(mat, axis=1) ** 2, axis=0))

    # Calculate ECDF
    ecdf_dict = get_ecdf(mat.shape[0], runs=initial_ecdf_samples)
    if results['d'] in ecdf_dict:
        results['ecdf_p_value'] = ecdf_dict[results['d']]
    else:
        print(str(initial_ecdf_samples) + ' samples for ECDF not enough for calculations, '
              'new ECDF is calculating with 10x new samples.')
        initial_ecdf_samples *= 10
        ecdf_dict = get_ecdf(mat.shape[0], runs=initial_ecdf_samples)
        results['ecdf_p_value'] = ecdf_dict[results['d']]

    # Chi-square approximation
    if mat.shape[0] < 10:
        warnings.warn('Chi-square could not calculated for small group, since it overestimates the significance',
                      RuntimeWarning)
        results['chi_sq'] = None
        results['df'] = None
        results['chi_sq_p_value'] = None
    else:
        results['chi_sq_df'] = ((mat.shape[0] * (mat.shape[0] - 1) * (mat.shape[0] - 2)) / (mat.shape[0] - 4) ** 2)
        results['chi_sq'] = (8/(mat.shape[0] - 4)) * (((mat.shape[0] * (mat.shape[0]-1) * (mat.shape[0] - 2)) / 24)
                                                      - results['d'] + 0.5) + results['chi_sq_df']
        results['chi_sq_p_value'] = chi2.sf(results['chi_sq'], results['chi_sq_df'])

    # Unbiased calculation using permutations
    mat = self.mat.astype('float32')
    unknown_triangle_upper = []
    for idx in range(mat.shape[0]):
        for idy in range(idx + 1, mat.shape[0]):
            if mat[idx, idy] == mat[idy, idx] == 0:
                unknown_triangle_upper.append((idx, idy))

    for idx in range(mat.shape[0]):
        for idy in range(idx + 1, mat.shape[0]):
            if mat[idx, idy] == mat[idy, idx] != 0:
                mat[idx, idy] = 0.5
                mat[idy, idx] = 0.5
            elif mat[idx, idy] > mat[idy, idx]:
                mat[idx, idy] = 1
                mat[idy, idx] = 0
            else:
                mat[idx, idy] = 0
                mat[idy, idx] = 1

    print('Computing, ' + str(2 ** len(unknown_triangle_upper)) + ' possible matrices for unknown relationships...')
    d_arr = []
    p_arr = []
    for permutation_idx in list(product([0, 1], repeat=len(unknown_triangle_upper))):
        temp_mat = mat.copy()
        for permute_id, (idx, idy) in enumerate(unknown_triangle_upper):
            temp_mat[idx, idy] = permutation_idx[permute_id]
            temp_mat[idy, idx] = 1 - permutation_idx[permute_id]

        temp_d = ((temp_mat.shape[0] * (temp_mat.shape[0] - 1) * (2 * temp_mat.shape[0] - 1)) / 12) - (0.5 * np.sum(
            np.sum(temp_mat, axis=1) ** 2, axis=0))
        d_arr.append(temp_d)
        if temp_d in ecdf_dict:
            p_arr.append(ecdf_dict[temp_d])
        else:
            print(str(initial_ecdf_samples) + ' samples for ECDF was enough for calculations, '
                                              'new ECDF is calculating with 10x new samples.')
            initial_ecdf_samples *= 10
            ecdf_dict = get_ecdf(mat.shape[0], runs=1000000)
            p_arr.append(ecdf_dict[temp_d])

    results['unbiased_d'] = sum(d_arr)/len(d_arr)
    results['unbiased_p_ecdf'] = sum(p_arr)/len(p_arr)

    if mat.shape[0] % 2 != 0 or odd_K:
        results['K'] = 1 - ((24 * results['d']) / (mat.shape[0] ** 3 - mat.shape[0]))
        results['unbiased_K'] = 1 - ((24 * results['unbiased_d']) / (mat.shape[0] ** 3 - mat.shape[0]))
    else:
        results['K'] = 1 - ((24 * results['d']) / (mat.shape[0] ** 3 - 4 * mat.shape[0]))
        results['unbiased_K'] = 1 - ((24 * results['unbiased_d']) / (mat.shape[0] ** 3 - 4 * mat.shape[0]))

    return results

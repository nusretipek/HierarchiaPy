from scipy.stats.distributions import chi2
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


def kendall_k(self, estimation_method='ecdf', ecdf_runs=100000):
    results = {}
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

    if mat.shape[0] % 2 != 0:
        results['K'] = 1 - ((24 * results['d']) / (mat.shape[0] ** 3 - mat.shape[0]))
    else:
        results['K'] = 1 - ((24 * results['d']) / (mat.shape[0] ** 3 - 4 * mat.shape[0]))

    if estimation_method == 'ecdf':
        if mat.shape[0] >= 10:
            warnings.warn('For quick approximation, consider using <estimation method="Chi-square">', RuntimeWarning)
        
        ecdf_dict = get_ecdf(mat.shape[0], runs=ecdf_runs)
        if results['d'] in ecdf_dict:
            results['ecdf_p_value'] = ecdf_dict[results['d']]
        else:
            ecdf_dict = get_ecdf(mat.shape[0], runs=10*ecdf_runs)
            if results['d'] in ecdf_dict:
                results['ecdf_p_value'] = ecdf_dict[results['d']]
            else:
                print('ECDF cannot attain the circular dyad value, p_value is calculated from the closest d!')
                idx_temp = (np.abs(np.array([k for k in ecdf_dict]) - results['d'])).argmin()
                results['ecdf_p_value'] = ecdf_dict[idx_temp]

    elif estimation_method == 'Chi-square':
        if mat.shape[0] < 10:
            warnings.warn('Chi-square could not calculated for small group, since it overestimates the significance'
                          'Please use <estimation method="ecdf">', RuntimeWarning)
        else:
            results['df'] = ((mat.shape[0] * (mat.shape[0] - 1) * (mat.shape[0] - 2)) / (mat.shape[0] - 4) ** 2)
            results['chi_sq'] = (8/(mat.shape[0] - 4)) * (((mat.shape[0] * (mat.shape[0]-1) * (mat.shape[0] - 2)) / 24)
                                                          - results['d'] + 0.5) + results['df']
            results['p_value'] = chi2.sf(results['chi_sq'], results['df'])
    else:
        warnings.warn('Invalid argument for the estimation_method, available options are ["ecdf" and "Chi-square"]', 
                      RuntimeWarning)

    return results

from scipy.stats.distributions import chi2
from itertools import *
import numpy as np
import warnings


def get_ecdf(n, runs=100000):

    # Parameter initialization
    results = {}
    d_master = []

    # Loop to calculate empirical CDF
    for _ in range(runs):
        mat = np.random.randint(0, 1000, size=(n, n)).astype('float64')
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

    # Calculate result dict
    sorted_d_master = np.sort(np.array(d_master))
    for d_idx in np.unique(sorted_d_master):
        if len(np.argwhere(sorted_d_master == d_idx)) > 0:
            results[d_idx] = round((np.argwhere(sorted_d_master == d_idx)[-1] / runs)[0], 3)

    # Return statement
    return results


def kendall_k(self, odd_K: bool = False) -> dict:

    """Function to calculate of circular dyads (d), Kendall K (coefficient K) and statistical tests of linearity

    Parameters
    ----------
    :param odd_K: bool
        Parameter to use odd N formula irrespective of the actual number of animals. For details see notes. (False)

    Returns
    -------
    results : dict
        The result dictionary depends on the number of individuals in the group. For N < 10, the Chi-square estimation
        cannot be used so that ECDF is calculated. The result dictionary contains unbiased d, unbiased p-value (ECDF),
         coefficient K and unbiased coefficient K. If N >= 10 then the result dictionary contains chi-square statistic,
         degree of freedom and p-value (chi-square) else these are equal to None. (rounded to 4 decimal places)

    See also
    --------
    https://en.wikipedia.org/wiki/Empirical_distribution_function
    https://en.wikipedia.org/wiki/Chi-squared_test
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html

    Notes
    -----
    1) de Vries (1995) argues that "However, evidently, Kendall’s K (for N odd) is identical to Landau’s h; therefore
    one could just as well say that, if ties are admitted the formula of Kendall’s K (for N odd) should be used
    in all cases, irrespective of the number of individuals." (de Vries, 1995)
    2) Appleby (1983) provided a table of selected values of d adapted from (Kendall 1962) yet, the table is not
    complete for N < 10 which makes it difficult to test the linearity for small groups. We calculate empirical
    CDF for estimate the p-value for groups N < 10. The estimates are tested against the provided table in the paper
    and found to be very accurate.

    References
    ----------
    * Appleby, Michael C. 1983. “The Probability of Linearity in Hierarchies.” Animal Behaviour 31: 600–608. https:
    doi.org/10.1016/S0003-3472(83)80084-0.
    * de Vries, H.1995. An improved test of linearity in dominance hierarchies containing unknown or tied relationships. Animal Behaviour, 50,1375e1389.
    """

    # Parameter initialization
    results = {}
    initial_ecdf_samples = 100000
    mat = self.mat.astype('float64')

    # Matrix manipulation
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

    # Calculate d
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
    mat = self.mat.astype('float64')
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

    # Compute permutations for unknown relationships
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

    # Return statement
    return results

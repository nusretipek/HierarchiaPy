import numpy as np
import pandas as pd


def get_Dij(self) -> np.ndarray:

    """Function to get Dij Matrix (Corrected version for chance)

    Parameters
    ----------

    Returns
    -------
    dij_matrix : np.ndarray
        Dij matrix, the initial order of the matrix kept intact and resulting corrected dominance indices
        (rounded to 4 decimal places)

    See also
    --------
    https://numpy.org/doc/stable/reference/generated/numpy.divide.html

    Notes
    -----
    When estimating A’s chances of defeating B we have to take the number of interactions into account. To this purpose
    proposed a dyadic dominance index dij in which the observed proportion of wins, Pij, is corrected for the chance
    occurrence of this observed outcome. de Vries proposed calculating the chance occurrence of the observed outcome
    on the basis of a binomial distribution with each animal having an equal chance of winning or losing in every
    dominance encounter. In the present paper we propose calculating the chance occurrence of the observed outcome on
    the basis of a uniform distribution, that is, given a certain number of observed dominance encounters, nij, then by
    chance every possible division of these encounters in wins and losses among the two animals is equally likely.
    (de Vries, 2006)

    References
    ----------
    * de Vries H, Stevens JMG, Vervaecke H (2006). “Measuring and testing the steepness of dominance hierarchies.”
      Animal Behaviour, 71, 585-592. doi: 10.1016/j.anbehav.2005.05.015.
    """

    # Calculate Dij
    mat = self.mat.astype('float64')
    total_mat = mat + np.transpose(mat)
    mat = np.divide(mat, total_mat, out=np.zeros_like(mat), where=total_mat != 0)
    mat -= np.divide((mat - 0.5), total_mat + 1, out=np.zeros_like(mat), where=total_mat != 0)
    dij_matrix = mat.round(decimals=4)

    # Return statement
    return dij_matrix


def get_steepness(self, method: str = 'Dij') -> float:

    """Function to get steepness measure from the dominance matrix

    Parameters
    ----------
    :param method: str
        Valid arguments are 'Dij' and 'Pij'. The method stands for the initial matrix state, the 'Dij' method
        use the corrected version for chance for dyadic dominance index (ref. de Vries (2006)). The 'Pij' method use
        the proportion of wins to compute David's Scores (Dij)

    Returns
    -------
     steepness : float
        Steepness measure from the dominance matrix (rounded to 4 decimal places)

    See also
    --------
    https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html

    Notes
    -----
    When the animals, ranked from the highest rank 1 to the lowest rank N in the rank order found by NormDS, are put
    on the X axis, and are given the normalized DS values on the Y axis, ordinary least-squares linear regression can be
    used to find the best-fitting straight line. We propose to use the absolute value of the slope of this line as a
    measure of steepness of the dominance hierarchy. In general, the steepness can vary between 0 and 1 when the
    normalized DS is used. When there is perfect linearity in the set of dominance relationships and when all
    proportions of wins Pij are 1, the slope equals -1, and steepness is thus at its maximum 1.
    (de Vries, 2006)

    References
    ----------
    * David, H. A. 1987. Ranking from unbalanced paired-comparison data. Biometrika, 74, 432–436.
    * de Vries H, Stevens JMG, Vervaecke H (2006). “Measuring and testing the steepness of dominance hierarchies.”
      Animal Behaviour, 71, 585-592. doi: 10.1016/j.anbehav.2005.05.015.
    """

    # Assertions
    assert (method in ['Dij', 'Pij'])

    # Get normalized David's scores
    n_ds = self.davids_score(method=method, normalize=True)

    # OLS regression
    y = sorted(list(n_ds.values()), reverse=True)
    coefficient_mat = np.vstack([np.arange(1, len(y) + 1), np.ones(len(y))]).T
    slope, constant = np.linalg.lstsq(coefficient_mat, y, rcond=None)[0]
    steepness = round(abs(slope), 4)

    # Return statement
    return steepness


def steepness_test(self, method: str = 'Dij', n: int = 2000) -> dict:

    """Function to test steepness measure from randomized dominance matrices

    Parameters
    ----------
    :param method: str
        Valid arguments are 'Dij' and 'Pij'. The method stands for the initial matrix state, the 'Dij' method
        use the corrected version for chance for dyadic dominance index (ref. de Vries (2006)). The 'Pij' method use
        the proportion of wins to compute David's Scores (Dij)
    :param n: int
        Parameter to adjust number of random matrices to use in the test. Higher numbers result in more stable test
        results. The maximum number is 1,000,000 while as low as 2,000 is good for robust test results. (2000)

    Returns
    -------
     steepness_test_dict : dict
        Summary dictionary of test measures calculated from the randomized process (all rounded to 4 decimal places)

    See also
    --------
    https://numpy.org/doc/stable/reference/generated/numpy.tile.html
    https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html

    Notes
    -----
    The original R implementation is 'steepness' package. Our implementation is marginally slower (2.8 times) but
    it is still less than 5 seconds to get results with n = 1,000,000. If n <= 100,000 the calculations are expected
    to be less than a second in a modern hardware.

    To test whether the observed steepness differs significantly from the steepness to be expected under the null
    hypothesis of random win chances for all pairs of individuals we can use the following randomization test procedure.
    Generate for each and every dyad (i,j ) a random number of wins r for individual i by randomly drawing a number
    from the integers 0, 1, 2 ... nij. Then nij - r will be the number of losses by i from j. Calculate the steepness
    for the resulting random win–loss matrix.
    (de Vries, 2006)

    References
    ----------
    * David, H. A. 1987. Ranking from unbalanced paired-comparison data. Biometrika, 74, 432–436.
    * de Vries H, Stevens JMG, Vervaecke H (2006). “Measuring and testing the steepness of dominance hierarchies.”
      Animal Behaviour, 71, 585-592. doi: 10.1016/j.anbehav.2005.05.015.
    """

    # Assertions
    assert type(n) == int and (0 < n <= 1000000)
    assert (method in ['Dij', 'Pij'])

    # Initial steepness
    initial_steep = self.get_steepness(method=method)

    # Matrix randomization
    mat = np.tile(self.mat.astype('float32'), (n, 1, 1))
    for idx in range(self.mat.shape[0]):
        for idy in range(idx + 1, self.mat.shape[0]):
            n_ij = self.mat[idx, idy] + self.mat[idy, idx]
            random_i = np.random.randint(0, n_ij + 1, n)
            random_j = n_ij - random_i
            mat[:, idx, idy] = random_i
            mat[:, idy, idx] = random_j

    # Fill the diagonal Np.nan
    i, j = np.diag_indices(self.mat.shape[0])
    mat[:, i, j] = np.nan

    # Method specific manipulations
    if method == 'Dij':
        total_mat = mat + np.rollaxis(mat, 2, 1)
        mat = np.divide(mat, total_mat, out=np.zeros_like(mat, dtype='float32'), where=total_mat != 0)
        mat -= np.divide((mat - 0.5), total_mat + 1, out=np.zeros_like(mat, dtype='float32'), where=total_mat != 0)
    else:
        total_mat = mat + np.rollaxis(mat, 2, 1)
        total_mat = np.where(total_mat == 0, np.nan, total_mat)
        mat = np.divide(mat, total_mat, out=np.zeros_like(mat, dtype='float32'), where=total_mat != 0)

    # Calculation of matrix properties
    var_l = np.nansum(mat, axis=1, dtype='float32')
    var_w = np.nansum(mat, axis=2, dtype='float32')
    var_l2 = np.nansum(np.rollaxis(mat, 2, 1) * var_l[:, np.newaxis, :], axis=2, dtype='float32')
    var_w2 = np.nansum(mat * var_w[:, np.newaxis, :], axis=2, dtype='float32')
    var_ds = ((var_w + var_w2 - var_l - var_l2) + (self.mat.shape[0] * self.mat.shape[0] - 1 / 2)) / self.mat.shape[0]
    var_ds.sort(axis=1)

    # OLS regression
    mat_x = np.vstack([np.arange(1, self.mat.shape[0] + 1, dtype='int32'), np.ones(self.mat.shape[0], dtype='int32')]).T
    steep_slopes = np.linalg.lstsq(mat_x, np.rollaxis(var_ds, 1, 0), rcond=None)[0][0]

    # Verbose Results
    steep_series = pd.Series(steep_slopes)
    steep_desc = steep_series.describe()
    right_p = ((len(steep_series[steep_series > abs(initial_steep)])) / len(steep_series))
    left_p = ((len(steep_series[steep_series < abs(initial_steep)])) / len(steep_series))
    steepness_test_dict = {
        'steepness': round(initial_steep, 4),
        'p_value_r': round(right_p, 4),
        'p_value_l': round(left_p, 4),
        'mean': round(steep_desc['mean'], 4),
        'std_dev': round(steep_desc['std'], 4),
        'variance': round(steep_desc['std']**2, 4),
        'min': round(steep_desc['min'], 4),
        'max': round(steep_desc['max'], 4),
        'percentile_25': round(steep_desc['25%'], 4),
        'percentile_50': round(steep_desc['50%'], 4),
        'percentile_75': round(steep_desc['75%'], 4),
        'count': n}

    # Return statements
    return steepness_test_dict

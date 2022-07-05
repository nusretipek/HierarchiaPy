import numpy as np


def davids_score(self, method: str = 'Pij', normalize: bool = False, order: bool = True) -> dict:
    
    """David's scores from an interaction dataframe/matrix.

    Parameters
    ----------
    :param method: str
        Valid arguments are 'Dij' and 'Pij'. The method stands for the initial matrix state, the 'Dij' method
        use the corrected version for chance for dyadic dominance index (ref. de Vries (2006)). The 'Pij' method use
        the proportion of wins to compute David's Scores
    :param normalize: bool
        Normalization of the David's scores using formula of NormDS = (DS+N(N −1)/2)/N (ref. de Vries (2006)) (False)
    :param order: bool
        If True, the resulting dictionary is sorted in descending order by David's scores (True)

    Returns
    -------
    davids_score_dict : dict
        David's scores, keys are individual names derived from either the Dataframe or name sequence (user provided,
        see class module for more details) and values are David's scores (rounded to 4 decimal places)

    See also
    --------
    https://numpy.org/doc/stable/reference/generated/numpy.nansum.html
    https://numpy.org/doc/stable/reference/generated/numpy.fill_diagonal.html

    Notes
    -----
    It is proposed that for ranking objects or players in an incomplete paired-comparison experiment or
    tournament with at most one comparison per pair, the score of a player, C, be the total number of (a)
    wins of players defeated by C minus losses of players to whom C lost, plus (b) C's wins minus C's losses.
    A tied match counts as half a win plus half a loss. More general tournaments can be treated similarly.
    (David, 1987)

    References
    ----------
    * David, H. A. 1987. Ranking from unbalanced paired-comparison data. Biometrika, 74, 432–436.
    * Gammell MP, de Vries H, Jennings DJ, Carlin CM, Hayden TJ (2003). “David's score: a more appropriate dominance
      ranking method than Clutton-Brock et al.'s index.” Animal Behaviour, 66, 601-605. doi: 10.1006/anbe.2003.2226.
    * de Vries H, Stevens JMG, Vervaecke H (2006). “Measuring and testing the steepness of dominance hierarchies.”
      Animal Behaviour, 71, 585-592. doi: 10.1016/j.anbehav.2005.05.015.
    """

    # Assertions
    assert method in ['Dij', 'Pij']
    assert type(normalize) == bool
    assert type(order) == bool

    # Matrix manipulation
    mat = self.mat.astype('float64')
    if method == 'Dij':
        total_mat = mat + np.transpose(mat)
        mat = np.divide(mat, total_mat, out=np.zeros_like(mat), where=total_mat != 0)
        mat -= np.divide((mat - 0.5), total_mat + 1, out=np.zeros_like(mat), where=total_mat != 0)

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
    davids_score_dict = {i: round(var_ds[idx], 4) for idx, i in enumerate(self.indices)}
    if normalize:
        davids_score_dict = {
            key: round((davids_score_dict[key] + (len(davids_score_dict) * (len(davids_score_dict) - 1) / 2)) / len(
                davids_score_dict), 4) for key in davids_score_dict}
    if order:
        davids_score_dict = {k: v for k, v in sorted(davids_score_dict.items(), key=lambda x: x[1], reverse=True)}

    # Return David's score dictionary
    return davids_score_dict

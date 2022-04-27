import numpy as np


def average_dominance_index(self):

    """Average Dominance Index (ADI) from an interaction dataframe/matrix.

    Parameters
    ----------
    :param self: reference to the current instance of the class

    Returns
    -------
    average_dominance_index_dict : dict
        Average dominance indices, keys are individual names derived from either the Dataframe or name sequence
        (user provided, see class module for more details) and values are ADI scores (rounded to 4 decimal places)

    See also
    --------
    https://numpy.org/doc/stable/reference/generated/numpy.nansum.html
    https://numpy.org/doc/stable/reference/generated/numpy.fill_diagonal.html

    Notes
    -----
    The average dominance index of an individual is the average of all its dominance indices with all its 
    interaction partners. A higher value indicates a higher dominance in the group. (Hemelrijk et al, 2005)

    References
    ----------
    * The Construction of Dominance Order: Comparing Performance of Five Methods Using an Individual Based Model
      C. K. Hemelrijk, J. Wantia and L. Gygax, Behaviour Vol. 142, No. 8 (Aug., 2005), pp. 1037-1058
      doi: 10.1163/156853905774405290

    """
    
    # Matrix manipulation
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
   
    # Calculation of matrix properties
    prop_mat = mat / sum_mat
    var_w = np.nansum(prop_mat, axis=1)
    var_adi = var_w / np.count_nonzero(~np.isnan(prop_mat), axis=1)
   
    # Create ADI dictionary
    average_dominance_index_dict = {i: round(var_adi[idx], 4) for idx, i in enumerate(self.indices)}
    return average_dominance_index_dict

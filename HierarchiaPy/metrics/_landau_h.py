import numpy as np
import warnings


# noinspection PyTypeChecker
def landau_h(self, improved: bool = True, n_random: int = 10000) -> dict:
    """Function to calculate Landau h, improved Landau h (h') and statistical tests of linearity

      Parameters
      ----------
      :param improved: bool
        The improved version of the Landau h (h'). Form ore details see de Vries (1998).
      :param n_random: int
        If improved version is calculated, it is the parameter to determine number of random matrices to calculate
        h' and corresponding p-values.

      Returns
      -------
      results : dict
          The result dictionary depends on the argument <improved>, the original version (improved=False) return a
          dictionary with single key named 'Landau_h'. If the improved version is asked (improved=True), the improved
          version of the Landau h (h') is returned with right and left p-values.

      References
      ----------
      * Landau, H. G. 1951a. On dominance relations and the structure of animal societies. I: effect of inherent
      characteristics. Bull. Math. Biophys., 13, 1-19
      * de Vries, H.1995. An improved test of linearity in dominance hierarchies containing unknown or tied relationships.
      Animal Behaviour, 50,1375e1389.
      """

    # Matrix manipulation
    mat = self.mat.astype('float64')

    # Original version
    if not improved:
        check_mat = False
        temp_mat = mat.copy()
        for idx in range(temp_mat.shape[0]):
            for idy in range(idx + 1, temp_mat.shape[0]):
                if temp_mat[idx, idy] == temp_mat[idy, idx] == 0:
                    check_mat = True
                    break
        if check_mat:
            warnings.warn("Original Landau's h needs all relationships to be known. Consider using improved version.")
            return {'Landau_h': None}
        else:
            temp_mat = mat.copy()
            for idx in range(temp_mat.shape[0]):
                for idy in range(idx + 1, temp_mat.shape[0]):
                    if temp_mat[idx, idy] == temp_mat[idy, idx]:
                        temp_mat[idx, idy] = 1 / 2
                        temp_mat[idy, idx] = 1 / 2
                    elif temp_mat[idx, idy] > temp_mat[idy, idx]:
                        temp_mat[idx, idy] = 1
                        temp_mat[idy, idx] = 0
                    else:
                        temp_mat[idx, idy] = 0
                        temp_mat[idy, idx] = 1

            row_sums = np.sum(temp_mat, axis=1)
            landaus_h = (12 / ((temp_mat.shape[0] ** 3) - temp_mat.shape[0])) * np.sum(
                ((row_sums - ((len(row_sums) - 1) / 2)) ** 2), axis=0)

            # Return statements
            return {'Landau_h': round(landaus_h, 4)}

    # Improved version
    if improved:
        upper_indices = np.triu_indices_from(mat, k=1)
        higher_indices = np.where(mat[upper_indices] > mat[upper_indices[1], upper_indices[0]])[0]
        lower_indices = np.where(mat[upper_indices] < mat[upper_indices[1], upper_indices[0]])[0]
        equal_indices = np.where((mat[upper_indices] == mat[upper_indices[1], upper_indices[0]]))[0]
        zero_indices = np.where((mat[upper_indices] == mat[upper_indices[1], 
                                                           upper_indices[0]]) & (mat[upper_indices] == 0))[0]

        # Expand the matrix to 3D
        mat = np.tile(mat, (n_random, 1, 1))

        # Landau h matrix with random tie breaking
        mat[:, np.hstack([upper_indices[0][equal_indices, ], upper_indices[1][equal_indices, ]]),
            np.hstack([upper_indices[1][equal_indices, ], upper_indices[0][equal_indices, ]])] = 0.5
        mat[:, np.hstack([upper_indices[0][higher_indices, ], upper_indices[1][lower_indices, ]]),
            np.hstack([upper_indices[1][higher_indices, ], upper_indices[0][lower_indices, ]])] = 1
        mat[:, np.hstack([upper_indices[1][higher_indices, ], upper_indices[0][lower_indices, ]]),
            np.hstack([upper_indices[0][higher_indices, ], upper_indices[1][lower_indices, ]])] = 0
        random_winners = np.random.randint(0, 2, (len(mat), len(zero_indices),))
        random_losers = 1 - random_winners
        mat[:, upper_indices[0][zero_indices, ], upper_indices[1][zero_indices, ]] = random_winners
        mat[:, upper_indices[1][zero_indices, ], upper_indices[0][zero_indices, ]] = random_losers
        row_sums = np.sum(mat, axis=2)
        improved_landau_h = (12 / ((mat.shape[1] ** 3) - mat.shape[1])) * np.sum(
            ((row_sums - ((row_sums.shape[1] - 1) / 2)) ** 2), axis=1)

        # Fully random matrix
        random_winners = np.random.randint(0, 2, (len(mat), len(upper_indices[0]),))
        random_losers = 1 - random_winners
        mat[:, upper_indices[0], upper_indices[1]] = random_winners
        mat[:, upper_indices[1], upper_indices[0]] = random_losers
        row_sums = np.sum(mat, axis=2)
        improved_landau_h_right = (12 / ((mat.shape[1] ** 3) - mat.shape[1])) * np.sum(
            ((row_sums - ((row_sums.shape[1] - 1) / 2)) ** 2), axis=1)
        right_p_value = len(np.where(improved_landau_h_right > improved_landau_h)[0]) / n_random

        # Create results dictionary
        results = {'Improved_Landau_h': round(np.mean(improved_landau_h), 4),
                   'p_value_r': round(right_p_value, 4),
                   'p_value_l': round(1 - right_p_value, 4)}

        # Return statements
        return results

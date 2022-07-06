import numpy as np
import warnings


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
            return None
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
        landau_h_master = []
        counter = 0
        for _ in range(n_random):
            temp_mat = mat.copy()
            for idx in range(temp_mat.shape[0]):
                for idy in range(idx + 1, temp_mat.shape[0]):
                    if temp_mat[idx, idy] == temp_mat[idy, idx] == 0:
                        random_winner = np.array([idx, idy])
                        np.random.shuffle(random_winner)
                        temp_mat[random_winner[0], random_winner[1]] = 1
                        temp_mat[random_winner[1], random_winner[0]] = 0
                    elif temp_mat[idx, idy] == temp_mat[idy, idx]:
                        temp_mat[idx, idy] = 1 / 2
                        temp_mat[idy, idx] = 1 / 2
                    elif temp_mat[idx, idy] > temp_mat[idy, idx]:
                        temp_mat[idx, idy] = 1
                        temp_mat[idy, idx] = 0
                    else:
                        temp_mat[idx, idy] = 0
                        temp_mat[idy, idx] = 1

            row_sums = np.sum(temp_mat, axis=1)
            temp_h = (12 / ((temp_mat.shape[0] ** 3) - temp_mat.shape[0])) * np.sum(
                ((row_sums - ((len(row_sums) - 1) / 2)) ** 2), axis=0)
            landau_h_master.append(temp_h)

            # step (ii)
            temp_mat = mat.copy()
            for idx in range(temp_mat.shape[0]):
                for idy in range(idx + 1, temp_mat.shape[0]):
                    random_winner = np.array([idx, idy])
                    np.random.shuffle(random_winner)
                    temp_mat[random_winner[0], random_winner[1]] = 1
                    temp_mat[random_winner[1], random_winner[0]] = 0

            row_sums = np.sum(temp_mat, axis=1)
            temp_h_r = (12 / ((temp_mat.shape[0] ** 3) - temp_mat.shape[0])) * np.sum(
                ((row_sums - ((len(row_sums) - 1) / 2)) ** 2), axis=0)
            if temp_h_r > temp_h:
                counter += 1

        # Refactor to a dictionary
        results = {'Improved_Landau_h': round(sum(landau_h_master) / len(landau_h_master), 4),
                   'p_value_r': round(counter / n_random, 4),
                   'p_value_l': round((n_random - counter) / n_random, 4)}

        # Return statements
        return results

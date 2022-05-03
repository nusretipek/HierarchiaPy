import numpy as np


def ISI98(self, runs=1000, verbose=False):

    """I&SI 1998 from an interaction dataframe/matrix.

    Parameters
    ----------
    :param self: reference to the current instance of the class

    :param runs: integer
        Parameter to adjust number of iterations for random ordering. Higher numbers result increase chance of
        finding the best sequence. Original paper suggests as low as 100 runs but our package use default 1000. (1000)

    :param verbose: boolean
        Print initial, intermediate and final inconsistencies, strength of inconsistencies and matrices. Used for
        detailed output of computational process. (False)

    Returns
    -------
    rank_dict : dict
        Rankings from the I&SI 1998 algorithm. Keys are identification of individuals (see name_seq) and 
        the values are the ranks. 

    See also
    --------
    https://numpy.org/doc/stable/reference/generated/numpy.triu.html

    Notes
    -----
    Two criteria are used in a prioritized way in reorganizing the dominance matrix to find an
    order that is most consistent with a linear hierarchy: first, minimization of the numbers of inconsistencies
    and, second, minimization of the total strength of the inconsistencies. The linear ordering
    procedure, which involves an iterative algorithm based on a generalized swapping rule, is feasible for
    matrices of up to 80 individuals. The procedure can be applied to any dominance matrix, since it does
    not make any assumptions about the form of the probabilities of winning and losing. The only
    assumption is the existence of a linear or near-linear hierarchy which can be verified by means of a
    linearity test. (de Vries, 1998)

    References
    ----------
    * de Vries, H. 1998 Finding a dominance order most consistent with a linear hierarchy:
      a new procedure and review. Animal Behaviour, 55, 827-843

    """

    mat = self.mat.astype('int64')

    for idx in range(mat.shape[0]):
        for idy in range(idx + 1, mat.shape[0]):
            if mat[idx, idy] == mat[idy, idx]:
                mat[idx, idy] = 0
                mat[idy, idx] = 0

    def swap_column_2d(arr, index_x, index_y):
        arr[:, [index_x, index_y]] = temp_mat[:, [index_y, index_x]]
        return arr

    def swap_row_2d(arr, index_x, index_y):
        arr[[index_x, index_y], :] = temp_mat[[index_y, index_x], :]
        return arr

    def swap_element_1d(arr, index_x, index_y):
        arr[index_x], arr[index_y] = arr[index_y], arr[index_x]
        return arr

    # calculate number of inconsistencies and number strength of inconsistencies
    diff_mat = mat - np.transpose(mat)
    inconsistencies = np.where(np.triu(diff_mat) < 0)
    str_i = sum([inconsistencies[1][idx] - inconsistencies[0][idx] for idx in range(len(inconsistencies[0]))])

    if verbose:
        print('Initial Phase\n-------------')
        print('Initial number of inconsistencies: ', len(inconsistencies[0]))
        print('Initial number of inconsistencies: ', str_i, '\n')

    # define parameters
    min_inconsistencies = len(inconsistencies[0])
    min_str_i = str_i

    temp_mat = mat.copy()
    temp_seq = self.indices.copy()
    best_mat = temp_mat.copy()
    best_seq = temp_seq.copy()

    # iterative process
    for _ in range(runs):

        flag = True
        while flag:
            flag = False
            inconsistencies = np.where(np.triu(temp_mat - np.transpose(temp_mat)) < 0)
            for idx in range(len(inconsistencies[0])):
                net_incs = 0
                for idy in range(inconsistencies[0][idx], inconsistencies[1][idx]):
                    net_incs += (temp_mat[inconsistencies[1][idx], idy] - temp_mat[idy, inconsistencies[1][idx]])
                if net_incs > 0:
                    temp_mat = swap_column_2d(temp_mat, inconsistencies[0][idx], inconsistencies[1][idx])
                    temp_mat = swap_row_2d(temp_mat, inconsistencies[0][idx], inconsistencies[1][idx])
                    temp_seq = swap_element_1d(temp_seq, inconsistencies[0][idx], inconsistencies[1][idx])
                    flag = True

        # compute number of inconsistencies and strength of inconsistencies
        inconsistencies = np.where(np.triu(temp_mat - np.transpose(temp_mat)) < 0)
        str_i = sum([inconsistencies[1][idx] - inconsistencies[0][idx] for idx in range(len(inconsistencies[0]))])

        if (len(inconsistencies[0]) < min_inconsistencies or
                (len(inconsistencies[0])) == min_inconsistencies and str_i < min_str_i):
            best_seq, best_mat = temp_seq.copy(), temp_mat.copy()
            min_inconsistencies, min_str_i = len(inconsistencies[0]), str_i
        else:
            if min_str_i > 0 and _ < runs - 1:
                for idx in range(len(inconsistencies[0])):
                    random_swap_idx = 0
                    if inconsistencies[1][idx] - 1 != 0:
                        random_swap_idx = np.random.randint(0, inconsistencies[1][idx] - 1)
                    temp_mat = swap_column_2d(temp_mat, random_swap_idx, inconsistencies[1][idx])
                    temp_mat = swap_row_2d(temp_mat, random_swap_idx, inconsistencies[1][idx])
                    temp_seq = swap_element_1d(temp_seq, random_swap_idx, inconsistencies[1][idx])
            else:
                if verbose:
                    print('End of Iterative Phase\n-------------')
                    print('Optimal or near-optimal linear ranking is found!')
                    print('Best sequence after iterative phase: ', best_seq)
                    print('Matrix after iterative phase: \n')
                    print(best_mat, '\n')
                break

    # final phase
    temp_mat = best_mat.copy()
    temp_seq = best_seq.copy()
    best_diff_mat = (best_mat - np.transpose(best_mat)).astype('float64')
    upper_triangle_indices = np.triu_indices_from(best_diff_mat, k=1)

    for idx in range(len(upper_triangle_indices[0])):
        if best_diff_mat[upper_triangle_indices[0][idx], upper_triangle_indices[1][idx]] == 0 and \
                upper_triangle_indices[1][idx] - upper_triangle_indices[0][idx] == 1:
            d_i = len(np.where(best_diff_mat[upper_triangle_indices[0][idx], :] > 0)[0])
            s_i = len(np.where(best_diff_mat[upper_triangle_indices[0][idx], :] < 0)[0])
            d_j = len(np.where(best_diff_mat[upper_triangle_indices[1][idx], :] > 0)[0])
            s_j = len(np.where(best_diff_mat[upper_triangle_indices[1][idx], :] < 0)[0])

            if d_i - s_i < d_j - s_j:
                temp_mat = swap_column_2d(temp_mat, upper_triangle_indices[0][idx], upper_triangle_indices[1][idx])
                temp_mat = swap_row_2d(temp_mat, upper_triangle_indices[0][idx], upper_triangle_indices[1][idx])
                temp_seq = swap_element_1d(temp_seq, upper_triangle_indices[0][idx], upper_triangle_indices[1][idx])
                temp_i = np.where(np.triu(temp_mat - np.transpose(temp_mat)) < 0)
                temp_str_i = sum([temp_i[1][idz] - temp_i[0][idz] for idz in range(len(temp_i[0]))])
                if not temp_str_i > min_str_i:
                    best_seq, best_mat = temp_seq.copy(), temp_mat.copy()

    inconsistencies = np.where(np.triu(best_mat - np.transpose(best_mat)) < 0)
    str_i = sum([inconsistencies[1][idx] - inconsistencies[0][idx] for idx in range(len(inconsistencies[0]))])

    if verbose:
        print('Final Phase\n-------------')
        print('Final number of inconsistencies: ', len(inconsistencies[0]))
        print('Final number of inconsistencies: ', str_i)
        print('Best Sequence: ', best_seq)
        print('Matrix after final phase: \n')
        print(best_mat)

    return {key: idx for idx, key in enumerate(best_seq)}

import numpy as np
import pandas as pd
from scipy.special import erfc


def randomized_elo(self, start_value=1000, K=100, n=1000, normal_probability=False):

    # transform matrix to df
    interactions = np.array([[self.indices[ix], self.indices[iy]] for ix, iy in np.ndindex(self.mat.shape)
                             for _ in range(int(self.mat[ix, iy]))])
    df = pd.DataFrame({'winner_col': interactions[:, 0],
                       'loser_col': interactions[:, 1]})

    # initialize elo dictionary
    elo_dict_master = {i: [] for i in self.indices}

    for _ in range(n):
        random_df = df.sample(frac=1)
        elo_dict_temp = {i: start_value for i in self.indices}

        for idx, row in random_df.iterrows():

            elo_diff = elo_dict_temp[row['winner_col']] - elo_dict_temp[row['loser_col']]
            if normal_probability:
                expected_winner = erfc(-elo_diff / ((2000 / 7) * (2 ** 0.5))) / 2
                expected_loser = erfc(elo_diff / ((2000 / 7) * (2 ** 0.5))) / 2
            else:
                expected_winner = 1 / (1 + 10 ** ((-elo_diff) / 400))
                expected_loser = 1 / (1 + 10 ** (elo_diff / 400))

            elo_dict_temp[row['winner_col']] += (K - K * expected_winner)
            elo_dict_temp[row['loser_col']] += (-K * expected_loser)

        for key in elo_dict_temp:
            elo_dict_master[key].append(elo_dict_temp[key])

    for key in elo_dict_master:
        elo_dict_master[key] = sum(elo_dict_master[key]) / len(elo_dict_master[key])

    return elo_dict_master

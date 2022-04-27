import numpy as np
import pandas as pd
from scipy.special import erfc


def randomized_elo(self, start_value=1000, K=100, n=1000, normal_probability=False):

    """Randomized Elo rating from an interaction dataframe/matrix.

    Parameters
    ----------
    :param self: reference to the current instance of the class
    
    :param start_value: float
        Parameter of the Elo function that determines the initial scores. It does not have
        an effect on relative differences after the calculation. (1000)
        
    :param K: float
        Parameter of the Elo function that acts as a factor and determines the speed at which scores change
        after an interaction. Optimization might be a good idea but not implemented yet. (100)
        
    :param n: integer
        Parameter to adjust number of iterations for random ordering. Higher numbers result in more stable Elo ratings.
        The number of random orders. (1000)
        
    :param normal_probability: Boolean
        Adjust the calculation of expected win/loss probabilities; default is Logistic,
        the normal probabilities are calculated using standard normal tables. For normalised probabilities,
        refer to https://handbook.fide.com (False)


    Returns
    -------
    elo_dict : dict
        Elo ratings, keys are individual names derived from either the Dataframe or name sequence (user provided,
        see class module for more details) and values are Elo scores (rounded to 4 decimal places)

    See also
    --------
    https://mathworld.wolfram.com/Erfc.html
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.erfc.html

    Notes
    -----
    A practical guide for inferring reliable dominance hierarchies and estimating their uncertainty
    However, most behavioural studies assume that individual dominance rank is relatively stable over time.
    We propose an improvement of the original Elo-rating based on randomizing the order in which interactions 
    occurred (n = 1 000 randomizations throughout). Randomising the order that interactions are recorded produces 
    slightly different individual Elo-ratings  each time, from which we can calculate a mean individual rank. 
    This method also allows estimating the 95% range of individual ranks when run on a single interaction dataset.
    (Sánchez-Tójar et al, 2017)
    
    References
    ----------
    * https://en.wikipedia.org/wiki/Elo_rating_system
    * Elo, A. E. 1978. The Rating of Chess Players, Past and Present. New York: Arco.
    * Sánchez-Tójar, Alfredo & Schroeder, Julia & Farine, Damien. (2017).
      A practical guide for inferring reliable dominance hierarchies and estimating their uncertainty.
      bioRxiv. 111146. 10.1101/111146.

    """

    # transform matrix to df
    interactions = np.array([[self.indices[ix], self.indices[iy]] for ix, iy in np.ndindex(self.mat.shape)
                             for _ in range(int(self.mat[ix, iy]))])
    df = pd.DataFrame({'winner_col': interactions[:, 0],
                       'loser_col': interactions[:, 1]})

    # initialize elo dictionary
    elo_dict_master = {i: [] for i in self.indices}

    # iterate n times
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
    
    # take the average of the elo ratings (n times)
    for key in elo_dict_master:
        elo_dict_master[key] = sum(elo_dict_master[key]) / len(elo_dict_master[key])

    return {key: round(elo_dict_master[key], 4) for key in elo_dict_master}

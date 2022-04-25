from scipy.special import erfc


def elo(self, start_value=1000, K=100, normal_probability=False):

    # check whether Pandas dataframe provided
    if not hasattr(self, 'df'):
        raise ValueError('Elo rating depends on sequence of wins/loses, computation uses Pandas dataframe, '
                         'consider using randomized elo')

    # initialize elo dictionary
    elo_dict = {i: start_value for i in self.indices}

    # iterate through the dataframe rows and compute elo scores
    for idx, row in self.df.iterrows():

        elo_diff = elo_dict[row[self.winner_col]] - elo_dict[row[self.loser_col]]
        if normal_probability:
            expected_winner = erfc(-elo_diff / ((2000 / 7) * (2 ** 0.5))) / 2
            expected_loser = erfc(elo_diff / ((2000 / 7) * (2 ** 0.5))) / 2
        else:
            expected_winner = 1 / (1 + 10 ** ((-elo_diff) / 400))
            expected_loser = 1 / (1 + 10 ** (elo_diff / 400))

        elo_dict[row[self.winner_col]] += (K - K * expected_winner)
        elo_dict[row[self.loser_col]] += (-K * expected_loser)

    # return final elo scores dictionary
    return elo_dict

from scipy.special import erfc


def elo(self, start_value=1000, K=100, normal_probability=False):

    """Elo rating from an interaction dataframe.

    Parameters
    ----------
    :param self: reference to the current instance of the class
    :param start_value: float
        Parameter of the Elo function that determines the initial scores. It does not have
        an effect on relative differences after the calculation. (1000)
    :param K: float
        Parameter of the Elo function that acts as a factor and determines the speed at which scores change
        after an interaction. Optimization might be a good idea but not implemented yet. (100)
    :param normal_probability: Boolean
        Adjust the calculation of expected win/loss probabilities; default is Logistic,
        the normal probabilities are calculated using standard normal tables. For normalised probabilities,
        refer to https://handbook.fide.com (False)

    Returns
    -------
    elo_dict : dict
        Elo ratings, keys are individual names derived from the Dataframe and values are Elo scores
        (rounded to 4 decimal places)

    See also
    --------
    https://mathworld.wolfram.com/Erfc.html
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.erfc.html

    Notes
    -----
    From Wikipedia:
    
    The Elo rating system is a method for calculating the relative skill levels of players
    in zero-sum games such as chess. It is named after its creator Arpad Elo, a Hungarian-American physics professor.
    The Elo system was originally invented as an improved chess-rating system over the previously used Harkness system,
    but is also used as a rating system in association football, American football, baseball, basketball, pool,
    table tennis, Go, board games such as Scrabble and Diplomacy, and esports.

    The difference in the ratings between two players serves as a predictor of the outcome of a match.
    Two players with equal ratings who play against each other are expected to score an equal number of wins.
    A player whose rating is 100 points greater than their opponent's is expected to score 64%;
    if the difference is 200 points, then the expected score for the stronger player is 76%.

    References
    ----------
    * https://en.wikipedia.org/wiki/Elo_rating_system
    * Elo, A. E. 1978. The Rating of Chess Players, Past and Present. New York: Arco.
    * Albers, P. C. H. & de Vries, H. 2001.
      Elo-rating as a tool in the sequential estimation of dominance strengths.
      Animal Behaviour, 61, 489-495. (DOI: 10.1006/anbe.2000.1571)

    """

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
    return {key: round(elo_dict[key], 4) for key in elo_dict}

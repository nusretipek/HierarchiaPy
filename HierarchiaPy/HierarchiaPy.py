# Import libraries
import numpy as np
import pandas as pd


# Define HierarchiaPy class
class HierarchiaPy:

    def __init__(self, *args, **kwargs):

        # initialize dataframe or matrix
        if len(args) > 0:
            if isinstance(args[0], pd.DataFrame):
                self.df = args[0]

            if isinstance(args[0], np.ndarray):
                self.mat = args[0]
                if self.mat.shape[0] != self.mat.shape[1]:
                    raise ValueError('Please provide symmetric 2D array')
        else:
            if 'df' in kwargs and isinstance(kwargs['df'], pd.DataFrame):
                self.df = kwargs['df']

            if 'mat' in kwargs and isinstance(kwargs['mat'], np.ndarray):
                self.mat = kwargs['mat']
                if self.mat.shape[0] != self.mat.shape[1]:
                    raise ValueError('Please provide symmetric 2D array')

        if not hasattr(self, 'df') and not hasattr(self, 'mat'):
            raise ValueError('Please provide valid Pandas Dataframe (argument: df) or NumPy array (argument: mat)')

        # initialize indices (if matrix provided)

        if hasattr(self, 'mat'):
            if len(args) > 1 and isinstance(args[1], (np.ndarray, list)):
                self.indices = args[1]
            elif 'name_seq' in kwargs and isinstance(kwargs['name_seq'], (np.ndarray, list)):
                self.indices = kwargs['name_seq']
            else:
                self.indices = np.arange(0, len(self.mat))
                print('Warning: Matrix indices will be used as name sequence, consider passing a name_seq')
            if len(self.indices) != self.mat.shape[0]:
                raise ValueError('Name sequence is not equal to the length of rows/columns')

        # initialize matrix from dataframe

        if hasattr(self, 'df'):
            if len(args) > 2 and isinstance(args[1], str) and isinstance(args[2], str):
                self.winner_col = args[1]
                self.loser_col = args[2]
                if self.winner_col not in self.df.columns or self.loser_col not in self.df.columns:
                    raise ValueError('Please provide valid winner and/or loser column names')

            elif len(args) == 2 and isinstance(args[1], str) and 'loser_col' in kwargs:
                self.winner_col = args[1]
                self.loser_col = kwargs['loser_col']
                if self.winner_col not in self.df.columns or self.loser_col not in self.df.columns:
                    raise ValueError('Please provide valid winner and/or loser column names')

            elif len(args) == 2 and isinstance(args[1], str) and 'winner_col' in kwargs:
                self.winner_col = kwargs['winner_col']
                self.loser_col = args[1]
                print('Warning: loser_col is provided with *args, please double check your column names')
                if self.winner_col not in self.df.columns or self.loser_col not in self.df.columns:
                    raise ValueError('Please provide valid winner and/or loser column names')

            elif 'winner_col' in kwargs and 'loser_col' in kwargs:
                self.winner_col = kwargs['winner_col']
                self.loser_col = kwargs['loser_col']
                if self.winner_col not in self.df.columns or self.loser_col not in self.df.columns:
                    raise ValueError('Please provide valid winner and/or loser column names')
            else:
                raise ValueError('Please provide valid winner and/or loser column names')

            # create matrix from dataframe

            self.indices = sorted(set(list(self.df[self.winner_col]) + list(self.df[self.loser_col])))
            self.cross_tab_df = pd.crosstab(index=self.df[self.winner_col],
                                            columns=self.df[self.loser_col],
                                            dropna=True).reindex(self.indices,
                                                                 fill_value=0,
                                                                 axis=0).reindex(self.indices,
                                                                                 fill_value=0,
                                                                                 axis=1)
            self.mat = self.cross_tab_df.to_numpy()
            self.indices = list(self.cross_tab_df.columns)

        # import methods

        from methods._elo import elo
        from methods._randomized_elo import randomized_elo

from HierarchiaPy import Hierarchia
import pandas as pd
import numpy as np
import pytest

# Simple Dataframe and Matrix

df = pd.DataFrame({'winner': ['c', 'a', 'a', 'b', 'd', 'b', 'a', 'c', 'b'],
                   'loser': ['a', 'b', 'b', 'a', 'c', 'd', 'b', 'b', 'a']})

mat = np.array([[0, 6, 9, 8, 5],
                [0, 0, 4, 6, 0],
                [0, 2, 0, 4, 7],
                [1, 0, 5, 0, 3],
                [0, 0, 2, 3, 0]], dtype='float32')

########################
## FICTIONAL DATASET ##
########################

# Randomized Elo test

def test_elo_logistic():
    hier_df = Hierarchia(df, 'winner', 'loser')
    elo_ranks = hier_df.randomized_elo(start_value=1000, K=100, n=500, normal_probability=False)
    assert (isinstance(elo_ranks, dict))
    assert (len(elo_ranks) == len(hier_df.indices))
    
def test_elo_normal():
    hier_mat = Hierarchia(mat)
    elo_ranks = hier_mat.randomized_elo(start_value=1000, K=100, n=500, normal_probability=True)
    assert (isinstance(elo_ranks, dict))
    assert (len(elo_ranks) == len(hier_mat.indices))

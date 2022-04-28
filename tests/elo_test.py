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

# Elo test

def test_elo_logistic():
    hier_df = Hierarchia(df, 'winner', 'loser')
    elo_ranks = hier_df.elo(start_value=1000, K=100, normal_probability=False)
    assert (isinstance(elo_ranks, dict))
    assert (len(elo_ranks) == len(hier_df.indices))
    assert(elo_ranks == {'a': 971.0724, 'b': 993.3937, 'c': 1040.421, 'd': 995.113})
    
def test_elo_normal():
    hier_df = Hierarchia(df, 'winner', 'loser')
    elo_ranks = hier_df.elo(start_value=1000, K=100, normal_probability=True)
    assert (isinstance(elo_ranks, dict))
    assert (len(elo_ranks) == len(hier_df.indices))
    assert(elo_ranks == {'a': 971.3928, 'b': 992.7994, 'c': 1040.6227, 'd': 995.1851})

# Value Error

def my_func_error():
    hier_mat = Hierarchia(mat)
    hier_mat.elo()
   
def elo_value_error():
    with pytest.raises(ValueError):
        my_func_error()

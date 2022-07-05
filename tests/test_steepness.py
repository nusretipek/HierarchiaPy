
from HierarchiaPy import Hierarchia
import pandas as pd
import numpy as np
import pytest

# Define test matrix

mat_hemelrijk_table_2_1 = np.array([[0, 6, 9, 8, 5],
                                    [0, 0, 4, 6, 0],
                                    [0, 2, 0, 4, 7],
                                    [1, 0, 5, 0, 3],
                                    [0, 0, 2, 3, 0]], dtype='int64')

###############################################################################################################
## Hemelrijk (2005) PAPER DATASET        - TABLE 2.1                                                         ##
## The construction of dominance order:comparing performance of five methods using an individual-based model ##
###############################################################################################################

# Test David's Score

def test_dij_steep():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    stp = hier_mat.get_steepness(method='Dij')
    assert (isinstance(stp, np.float64))
    assert(stp == 0.5262)

def test_pij_steep():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    stp = hier_mat.get_steepness(method='Pij')
    assert (isinstance(stp, np.float64))
    assert(stp == 0.6056)
    
def test_dij_steeptest():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    stp = hier_mat.steepness_test(method='Dij', n=100)
    assert (isinstance(stp, dict))
    assert(stp['steepness'] == 0.5262)
    
def test_pij_steeptest():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    stp = hier_mat.steepness_test(method='Pij', n=100)
    assert (isinstance(stp, dict))
    assert(stp['count'] == 100)
    assert(stp['steepness'] == 0.6056)
    
def test_get_dij():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    dij = hier_mat.get_Dij()
    assert (dij.shape == (5,5))
    assert (dij[0,0] == 0.0)
    assert (dij[1,2] == 0.6429)

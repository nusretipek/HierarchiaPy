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

def test_davids_scores():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    davids_scores = hier_mat.davids_score(order=False)
    assert (isinstance(davids_scores, dict))
    assert (len(davids_scores) == len(hier_mat.indices))
    assert(davids_scores == {'a': 8.4444, 'b': 1.6111, 'c': -2.3333, 'd': -3.6667, 'e': -4.0556})
    
def test_davids_scores_dij_no_normal():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    davids_scores = hier_mat.davids_score(method='Dij', normalize=False, order=False)
    assert (isinstance(davids_scores, dict))
    assert (len(davids_scores) == len(hier_mat.indices))
    assert(davids_scores == {'a': 7.381, 'b': 1.381, 'c': -2.0714, 'd': -3.2143, 'e': -3.4762})

def test_davids_scores_dij_normal():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    davids_scores = hier_mat.davids_score(method='Dij', normalize=True, order=False)
    assert (isinstance(davids_scores, dict))
    assert (len(davids_scores) == len(hier_mat.indices))
    assert(davids_scores == {'a': 3.4762, 'b': 2.2762, 'c': 1.5857, 'd': 1.3571, 'e': 1.3048})

def test_davids_scores_pij_no_normal():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    davids_scores = hier_mat.davids_score(method='Pij', normalize=False, order=False)
    assert (isinstance(davids_scores, dict))
    assert (len(davids_scores) == len(hier_mat.indices))
    assert(davids_scores == {'a': 8.4444, 'b': 1.6111, 'c': -2.3333, 'd': -3.6667, 'e': -4.0556})

def test_davids_scores_pij_normal():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    davids_scores = hier_mat.davids_score(method='Pij', normalize=True, order=False)
    assert (isinstance(davids_scores, dict))
    assert (len(davids_scores) == len(hier_mat.indices))
    assert(davids_scores == {'a': 3.6889, 'b': 2.3222, 'c': 1.5333, 'd': 1.2667, 'e': 1.1889})

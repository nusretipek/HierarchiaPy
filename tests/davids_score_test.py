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
    davids_scores = hier_mat.davids_score()
    assert (isinstance(davids_scores, dict))
    assert (len(davids_scores) == len(hier_mat.indices))
    assert(davids_scores == {'a': 8.4444, 'b': 1.6111, 'c': -2.3333, 'd': -3.6667, 'e': -4.0556})


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

################################################################################################################
## Hemelrijk (2005) PAPER DATASET        - TABLE 2.1                                                          ##
## The construction of dominance order: comparing performance of five methods using an individual-based model ##
################################################################################################################

# Test Average Dominance Index

def test_adi_scores():
    hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
    adi_scores = hier_mat.average_dominance_index()
    assert (isinstance(adi_scores, dict))
    assert (len(adi_scores) == len(hier_mat.indices))
    assert(adi_scores == {'a': 0.9722, 'b': 0.5556, 'c': 0.3889, 'd': 0.2917, 'e': 0.2407})

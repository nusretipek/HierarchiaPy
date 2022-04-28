from HierarchiaPy import Hierarchia
import pandas as pd
import numpy as np
import pytest

# Define test matrix

name_seq = np.array(['a', 'v', 'b', 'h', 'g', 'w', 'e', 'k', 'c', 'y'])
mat = np.array([[0, 5, 4, 6, 3, 0, 2, 2, 3, 1],
                [0, 0, 0, 0, 2, 1, 2, 0, 7, 7],
                [0, 0, 0, 0, 1, 1, 1, 2, 2, 2],
                [0, 3, 0, 0, 0, 0, 6, 0, 2, 5],
                [0, 0, 0, 1, 0, 2, 4, 0, 3, 0],
                [2, 0, 0, 3, 0, 0, 0, 0, 2, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
                [0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
                [0, 0, 0, 0, 0, 1, 0, 2, 0, 6],
                [0, 0, 0, 0, 0, 0, 0, 0, 2, 0]], dtype='int64')


###################################################################################################
## de Vries (1998) -          Figure 1                                                           ##
## Finding a dominance order most consistent with a linear hierarchy: a new procedure and review ##
###################################################################################################

# ISI98 Test

def test_ISI_no_verbose():
    hier_mat = Hierarchia(mat, name_seq)
    isi98 = hier_mat.ISI98(runs=1000, verbose=False)
    assert (isinstance(isi98, dict))
    assert (len(isi98) == len(hier_mat.indices))
    assert(isi98 == {'a': 0, 'b': 1, 'v': 2, 'g': 3, 'w': 4, 'h': 5, 'k': 6, 'e': 7, 'c': 8, 'y': 9})
    
def test_ISI_verbose():
    hier_mat = Hierarchia(mat, name_seq)
    isi98 = hier_mat.ISI98(runs=1000, verbose=True)
    assert (isinstance(isi98, dict))
    assert (len(isi98) == len(hier_mat.indices))
    assert(isi98 == {'a': 0, 'b': 1, 'v': 2, 'g': 3, 'w': 4, 'h': 5, 'k': 6, 'e': 7, 'c': 8, 'y': 9})
    

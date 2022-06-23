from HierarchiaPy import Hierarchia
import pandas as pd
import numpy as np
import pytest

# Simple Matrix

mat = np.array([[0, 6, 9, 8, 5],
                [0, 0, 4, 6, 0],
                [0, 2, 0, 4, 7],
                [1, 0, 5, 0, 3],
                [0, 0, 2, 3, 0]], dtype='float32')

########################
## FICTIONAL DATASET ##
########################

# DCI

def test_dci():
    hier_mat = Hierarchia(mat)
    dci = hier_mat.dci()
    assert (isinstance(dci, np.float64))
    assert (dci == 0.6308)
    

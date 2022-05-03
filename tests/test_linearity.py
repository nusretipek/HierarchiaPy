from HierarchiaPy import Hierarchia
import pandas as pd
import numpy as np
import pytest

# Test matrices from de Vries (1995) and Appleby (1962)

test_appleby_1 = np.array([[0, 6, 1, 4, 6, 8, 5],
                           [5, 0, 5, 0, 0, 2, 1],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [2, 0, 0, 2, 0, 1, 0],
                           [1, 15, 1, 0, 11, 0, 1],
                           [4, 2, 0, 0, 0, 0, 0]], dtype='float32')

old_landau_h = np.array([[0, 3, 10],
                         [2, 0, 1],
                         [0, 1, 0]], dtype='float32')


# Linearity Tests

def test_landau():
    hier_mat = Hierarchia(old_landau_h)
    landau_1 = hier_mat.landau_h(improved=False)
    assert landau_1["Landau_h"] == 0.75
    hier_mat = Hierarchia(test_appleby_1)
    landau_2 = hier_mat.landau_h(improved=True, n_random=10000)
    assert (isinstance(landau_2, dict))
    assert 0.70 < landau_2["Improved_Landau_h"] < 0.75
    assert landau_2["p_value_r"] < 0.10

    
def test_kendall():
    hier_mat = Hierarchia(test_appleby_1)
    kendall = hier_mat.kendall_k(odd_K=False)
    landau = hier_mat.landau_h(improved=True, n_random=10000)
    assert (isinstance(kendall, dict))
    assert kendall["d"] == 6.0
    assert kendall["unbiased_d"] == 4.0
    assert kendall["chi_sq"] == None
    assert abs(landau["Improved_Landau_h"] - kendall["unbiased_K"]) <= 0.01
   

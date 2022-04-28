from HierarchiaPy import Hierarchia
import pandas as pd
import numpy as np
import pytest

# Define test matrix

mat = np.array([[0, 1, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 1, 0, 2, 1, 0],
                [1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0]], dtype='int64')

##########################
## ADAGIO PAPER DATASET ##
##########################

# ADAGIO test

def test_adagio_topological():
    hier_mat = Hierarchia(mat, np.array(['a', 'b', 'c', 'd', 'e', 'f']))
    adagio = hier_mat.adagio(preprocessing=True, plot_network=False, rank='topological')
    assert (isinstance(adagio, dict))
    assert (len(adagio) == len(hier_mat.indices))
    assert(adagio == {'a': 0, 'f': 1, 'c': 2, 'd': 3, 'e': 4, 'b': 5})
    
def test_adagio_top():
    hier_mat = Hierarchia(mat, np.array(['a', 'b', 'c', 'd', 'e', 'f']))
    adagio = hier_mat.adagio(preprocessing=True, plot_network=False, rank='top')
    assert (isinstance(adagio, dict))
    assert (len(adagio) == len(hier_mat.indices))
    assert(adagio == {'a': 0, 'f': 0, 'c': 1, 'd': 2, 'e': 2, 'b': 3})
    
def test_adagio_bottom():
    hier_mat = Hierarchia(mat, np.array(['a', 'b', 'c', 'd', 'e', 'f']))
    adagio = hier_mat.adagio(preprocessing=True, plot_network=False, rank='bottom')
    assert (isinstance(adagio, dict))
    assert (len(adagio) == len(hier_mat.indices))
    assert(adagio == {'b': 3, 'e': 3, 'd': 2, 'c': 1, 'f': 1, 'a': 0})

def test_adagio_no_pre_bottom():
    hier_mat = Hierarchia(mat, np.array(['a', 'b', 'c', 'd', 'e', 'f']))
    adagio = hier_mat.adagio(preprocessing=False, plot_network=False, rank='bottom')
    assert (isinstance(adagio, dict))
    assert (len(adagio) == len(hier_mat.indices))
    assert(adagio == {'b': 3, 'e': 3, 'd': 2, 'c': 1, 'f': 1, 'a': 0})
    
def adagio_value_error():
    with pytest.raises(ValueError):
        hier_mat = Hierarchia(mat)
        adagio = hier_mat.adagio(preprocessing=True, plot_network=False, rank='')

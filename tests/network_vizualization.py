from HierarchiaPy import Hierarchia
import pandas as pd
import numpy as np
import matplotlib
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

def test_network_graph():
    hier_mat = Hierarchia(mat)
    fig = hier_mat.directed_network_graph(fig_size=(7, 7),
                                          node_color=['red', 'blue', 'green', 'orange', 'yellow'],
                                          font_size=12)
    assert (isinstance(fig, matplotlib.figure.Figure))
    

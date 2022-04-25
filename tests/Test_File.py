from __init__ import HierarchiaPy
import pandas as pd
import numpy as np

df = pd.DataFrame({'winner': ['c', 'a', 'a', 'b', 'd', 'b', 'a', 'c', 'b'],
                   'loser': ['a', 'b', 'b', 'a', 'c', 'd', 'b', 'b', 'a']})

test_matrix = np.array([[0, 6, 9, 8, 5],
                        [0, 0, 4, 6, 0],
                        [0, 2, 0, 4, 7],
                        [1, 0, 5, 0, 3],
                        [0, 0, 2, 3, 0]], dtype='float32')

a = HierarchiaPy(df, winner_col='winner', loser_col='loser')
print(a.elo())
#print(a.elo())
#print(a.elo(normal_probability=True))
#print(a.randomized_elo(normal_probability=True, n=1000))

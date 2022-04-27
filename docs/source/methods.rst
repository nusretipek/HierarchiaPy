Methods
===============================================

ELO Rating
-------------------------------

.. autofunction:: _elo.elo

The Hierarchia class should be initiated with a Pandas Dataframe since the method relies on the order of the interactions. 
:py:func:`_elo.elo` will raise an exception, if Hierarchia class  initiated with a matrix.

Example:

>>> test_matrix = np.array([[0, 6, 9, 8, 5],
                            [0, 0, 4, 6, 0],
                            [0, 2, 0, 4, 7],
                            [1, 0, 5, 0, 3],
                            [0, 0, 2, 3, 0]], dtype='float32')
                            
>>> {elo}                         
                        

Randomized ELO Rating
------------------------------

.. autofunction:: _randomized_elo.randomized_elo


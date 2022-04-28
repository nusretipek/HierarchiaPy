Methods
===============================================

ELO Rating
-------------------------------

.. autofunction:: _elo.elo

The Hierarchia class should be initiated with a Pandas Dataframe since the method relies on the order of the interactions. 
:py:func:`_elo.elo` will raise an exception, if Hierarchia class  initiated with a matrix.

Example:

.. code-block:: python
   :linenos:

   df = pd.DataFrame({'winner': ['c', 'a', 'a', 'b', 'd', 'b', 'a', 'c', 'b'],
                      'loser': ['a', 'b', 'b', 'a', 'c', 'd', 'b', 'b', 'a']})               
   hierarchia = Hierarchia(df, 'winner', 'loser')
   elo_ratings = hierarchia.elo(start_value=1000, K=100, normal_probability=False)                           
   print(elo_ratings)   

Result:

.. code-block:: python
  
   {'a': 971.0724, 'b': 993.3937, 'c': 1040.421, 'd': 995.113}
                        
                        
Randomized ELO Rating
------------------------------

.. autofunction:: _randomized_elo.randomized_elo

Example:

.. code-block:: python
   :linenos:

    mat = np.array([[0, 6, 9, 8, 5],
                    [0, 0, 4, 6, 0],
                    [0, 2, 0, 4, 7],
                    [1, 0, 5, 0, 3],
                    [0, 0, 2, 3, 0]], dtype='float32')
    hier_mat = Hierarchia(mat, name_seq=['a', 'b', 'c','d','e'])
    randomized_elo_ratings = hier_mat.randomized_elo(start_value=1000, K=100, n=2000, normal_probability=True)
    print(randomized_elo_ratings)
    
Result (random process):

.. code-block:: python
  
   {'a': 1373.0278, 'b': 1070.3446, 'c': 910.9598, 'd': 857.1167, 'e': 788.5511}
   
   
David's Scores
-------------------------------

.. autofunction:: _davids_score.davids_score 

Example:

.. code-block:: python
   :linenos:

    mat = np.array([[0, 6, 9, 8, 5],
                    [0, 0, 4, 6, 0],
                    [0, 2, 0, 4, 7],
                    [1, 0, 5, 0, 3],
                    [0, 0, 2, 3, 0]], dtype='float32')
    hier_mat = Hierarchia(mat, name_seq=['a', 'b', 'c','d','e'])
    davids_scores = hier_mat.davids_score()
    print(davids_scores)  

Result:

.. code-block:: python
  
   {'a': 8.4444, 'b': 1.6111, 'c': -2.3333, 'd': -3.6667, 'e': -4.0556}
  
  
Average Dominance Index (ADI)
-------------------------------

.. autofunction:: _average_dominance_index.average_dominance_index 

Example:

.. code-block:: python
   :linenos:

    mat = np.array([[0, 6, 9, 8, 5],
                    [0, 0, 4, 6, 0],
                    [0, 2, 0, 4, 7],
                    [1, 0, 5, 0, 3],
                    [0, 0, 2, 3, 0]], dtype='float32')
    hier_mat = Hierarchia(mat, name_seq=['a', 'b', 'c','d','e'])
    average_dominance_indices = hier_mat.average_dominance_index()
    print(average_dominance_indices)  

Result:

.. code-block:: python
  
   {'a': 0.9722, 'b': 0.5556, 'c': 0.3889, 'd': 0.2917, 'e': 0.2407}
   
   
ADAGIO
-------------------------------

.. autofunction:: _adagio.adagio 

Example:

.. code-block:: python
   :linenos:

    mat = np.array([[0, 6, 9, 8, 5],
                    [0, 0, 4, 6, 0],
                    [0, 2, 0, 4, 7],
                    [1, 0, 5, 0, 3],
                    [0, 0, 2, 3, 0]], dtype='float32')
    hier_mat = Hierarchia(mat, name_seq=['a', 'b', 'c','d','e'])
    adagio_ranks = hier_mat.adagio(preprocessing=True, plot_network=False, rank='top')
    print(adagio_ranks)  

Result:

.. code-block:: python
  
   {'a': 0, 'b': 1, 'd': 2, 'c': 3, 'e': 4}

                        
I&SI (1998)
-------------------------------

.. autofunction:: _ISI98.ISI98 

Example:

.. code-block:: python
   :linenos:

    mat = np.array([[0, 6, 9, 8, 5],
                    [0, 0, 4, 6, 0],
                    [0, 2, 0, 4, 7],
                    [1, 0, 5, 0, 3],
                    [0, 0, 2, 3, 0]], dtype='float32')
    hier_mat = Hierarchia(mat, name_seq=['a', 'b', 'c','d','e'])
    ISI98_ranks = hier_mat.ISI98(runs=1000, verbose=True)
    print(ISI98_ranks)  

Result:

.. code-block:: python
  
   Initial Phase
   -------------
   Initial number of inconsistencies:  1
   Initial number of inconsistencies:  1 

   End of Iterative Phase
   -------------
   Optimal or near-optimal linear ranking is found!
   Best sequence after iterative phase:  ['a', 'b', 'd', 'c', 'e']
   Matrix after iterative phase: 

   [[0 6 8 9 5]
    [0 0 6 4 0]
    [1 0 0 5 3]
    [0 2 4 0 7]
    [0 0 3 2 0]] 

   Final Phase
   -------------
   Final number of inconsistencies:  0
   Final number of inconsistencies:  0
   Best Sequence:  ['a', 'b', 'd', 'c', 'e']
   Matrix after final phase: 

   [[0 6 8 9 5]
    [0 0 6 4 0]
    [1 0 0 5 3]
    [0 2 4 0 7]
    [0 0 3 2 0]]
    
   {'a': 0, 'b': 1, 'd': 2, 'c': 3, 'e': 4}
                        

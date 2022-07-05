Methods
===============================================


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
   

Steepness Measure
-------------------------------

.. autofunction:: _steepness.get_steepness

Example:

.. code-block:: python
   :linenos:
   
   mat = np.array([[0, 58, 50, 61, 32, 37, 29, 39, 25],
                   [8, 0, 22, 22, 9, 27, 20, 10, 48],
                   [3, 3, 0, 19, 29, 12, 13, 19, 8],
                   [5, 8, 9, 0, 33, 38, 35, 32, 57],
                   [4, 7, 9, 1, 0, 28, 26, 16, 23],
                   [4, 3, 0, 0, 6, 0, 7, 6, 12],
                   [2, 0, 4, 1, 4, 4, 0, 5, 3],
                   [0, 2, 1, 1, 5, 8, 3, 0, 10],
                   [3, 1, 3, 0, 0, 4, 1, 2, 0]])
   name_arr = np.array(["V", "VS", "B", "FJ", "PR", "VB", "TOR", "MU", "ZV"]) 
   hier_mat = Hierarchia(mat, name_arr)
   steep_dij = hier_mat.get_steepness(method='Dij')                           
   print(steep_dij)   

Result:

.. code-block:: python
  
   0.7421


Steepness Test
-------------------------------

.. autofunction:: _steepness.steepness_test

Example:

.. code-block:: python
   :linenos:
   
   mat = np.array([[0, 58, 50, 61, 32, 37, 29, 39, 25],
                   [8, 0, 22, 22, 9, 27, 20, 10, 48],
                   [3, 3, 0, 19, 29, 12, 13, 19, 8],
                   [5, 8, 9, 0, 33, 38, 35, 32, 57],
                   [4, 7, 9, 1, 0, 28, 26, 16, 23],
                   [4, 3, 0, 0, 6, 0, 7, 6, 12],
                   [2, 0, 4, 1, 4, 4, 0, 5, 3],
                   [0, 2, 1, 1, 5, 8, 3, 0, 10],
                   [3, 1, 3, 0, 0, 4, 1, 2, 0]])
   name_arr = np.array(["V", "VS", "B", "FJ", "PR", "VB", "TOR", "MU", "ZV"]) 
   hier_mat = Hierarchia(mat, name_arr)
   steep_test = hier_mat.steepness_test(method='Dij', n=9999)                           
   print(steep_test)   

Result:

.. code-block:: python
  
   {'steepness': 0.7421, 
    'p_value_r': 0.0, 
    'p_value_l': 1.0, 
    'mean': 0.2943, 
    'std_dev': 0.0712, 
    'variance': 0.0051, 
    'min': 0.0661, 
    'max': 0.5756, 
    'percentile_25': 0.2444, 
    'percentile_50': 0.2919, 
    'percentile_75': 0.3416, 
    'count': 9999}


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

                         

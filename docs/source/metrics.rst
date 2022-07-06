Metrics
===============================================


Directional consistency index (DCI)
-------------------------------

.. autofunction:: _dci.dci

**Example:**

.. code-block:: python
   :linenos:
   
   mat = np.array([[0, 6, 1, 4, 6, 8, 5],
                   [5, 0, 5, 0, 0, 2, 1],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [2, 0, 0, 2, 0, 1, 0],
                   [1, 15, 1, 0, 11, 0, 1],
                   [4, 2, 0, 0, 0, 0, 0]], dtype='float32')

   hier_mat = Hierarchia(mat, np.arange(0, mat.shape[0]))
   dci = hier_mat.dci()
   print(dci)   

**Result:**

.. code-block:: python
  
   0.6145

                        
Landau h & h'
-------------------------------

.. autofunction:: _landau_h.landau_h

**Example:**

.. code-block:: python
   :linenos:
   
   mat = np.array([[0, 3, 10],
                   [2, 0, 1],
                   [0, 1, 0]], dtype='float32')

   hier_mat = Hierarchia(mat, np.arange(0, mat.shape[0]))
   landau_h = hier_mat.landau_h(improved=False)
   print(landau_h)

**Result:**

   {'Landau_h': 0.75}

**Example:**

.. code-block:: python
   :linenos:
   
   mat = np.array([[0, 6, 1, 4, 6, 8, 5],
                   [5, 0, 5, 0, 0, 2, 1],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [2, 0, 0, 2, 0, 1, 0],
                   [1, 15, 1, 0, 11, 0, 1],
                   [4, 2, 0, 0, 0, 0, 0]], dtype='float32')

   hier_mat = Hierarchia(mat, np.arange(0, mat.shape[0]))
   improved_landau_h = hier_mat.landau_h(improved=True, n_random=10000)
   print(improved_landau_h)

**Result:**

   {'Improved_Landau_h': 0.7138, 'p_value_r': 0.0582, 'p_value_l': 0.9418}


Circular dyads (d) & Kendall K
-------------------------------

.. autofunction:: _kendall_k.kendall_k

**Example:**

.. code-block:: python
   :linenos:
   
   mat = np.array([[0, 6, 1, 4, 6, 8, 5],
                   [5, 0, 5, 0, 0, 2, 1],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [2, 0, 0, 2, 0, 1, 0],
                   [1, 15, 1, 0, 11, 0, 1],
                   [4, 2, 0, 0, 0, 0, 0]], dtype='float32')

   hier_mat = Hierarchia(mat, np.arange(0, mat.shape[0]))
   kendall_k = hier_mat.kendall_k(odd_K=False)
   print(kendall_k)

**Result:**

   Computing, 256 possible matrices for unknown relationships...
   {'d': 6.0, 
    'ecdf_p_value': 0.196, 
    'chi_sq': None, 
    'df': None, 
    'chi_sq_p_value': None, 
    'unbiased_d': 4.0, 
    'unbiased_p_ecdf': 0.0948, 
    'K': 0.5714, 
    'unbiased_K': 0.7143}


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
    
 

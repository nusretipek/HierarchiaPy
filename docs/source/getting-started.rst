Quick Start
===============

Installation
-------------------------------

**Using the pip**

.. code-block:: console
   :linenos:
   
   $ pip install hierarchiapy
   
**Using the Git & Pip**

.. code-block:: console
   :linenos:
   
   $ !pip install git+https://github.com/nusretipek/HierarchiaPy.git


Hierarchia Class
-------------------------------

.. autoclass:: HierarchiaPy.Hierarchia

.. autofunction:: HierarchiaPy.Hierarchia.__init__

Examples: Pandas DataFrame Initialization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
  Initialization via Pandas Dataframe - Required to have two more arguments: Winner and Loser Column names
  
**Intialization with variable list of arguments**

.. code-block:: python
   :linenos:
   
   from HierarchiaPy import Hierarchia
   import pandas as pd
   
   df = pd.DataFrame({'winner': ['c', 'a', 'a', 'b', 'd', 'b', 'a', 'c', 'b'],
                      'loser': ['a', 'b', 'b', 'a', 'c', 'd', 'b', 'b', 'a']})
   
   hier_df = Hierarchia(df, 'winner', 'loser')
   
   print(hier_df.mat)
   print(hier_df.indices)

Result:

.. code-block:: python

   [[0 3 0 0]
    [2 0 0 1]
    [1 1 0 0]
    [0 0 1 0]]
   ['a', 'b', 'c', 'd']

**Intialization with keyword list of arguments**

.. code-block:: python
   :linenos:
   
   from HierarchiaPy import Hierarchia
   import pandas as pd

   df = pd.DataFrame({'winner': ['c', 'a', 'a', 'b', 'd', 'b', 'a', 'c', 'b'],
                      'loser': ['a', 'b', 'b', 'a', 'c', 'd', 'b', 'b', 'a']})
                      
   hier_df = Hierarchia(df, winner_col='winner', loser_col='loser')
   
   print(hier_df.mat)
   print(hier_df.indices)
   
Result:

.. code-block:: python

   [[0 3 0 0]
    [2 0 0 1]
    [1 1 0 0]
    [0 0 1 0]]
   ['a', 'b', 'c', 'd']
   
Examples: 2D NumPy (Matrix) Initialization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
.. note::

  Initialization via 2D Numpy - Required to be symmetric (n x n)

**Intialization with only NumPy 2D array**

.. code-block:: python
   :linenos:
   
   from HierarchiaPy import Hierarchia
   import numpy as np
  
   mat = np.array([[0, 6, 9, 8, 5],
                   [0, 0, 4, 6, 0],
                   [0, 2, 0, 4, 7],
                   [1, 0, 5, 0, 3],
                   [0, 0, 2, 3, 0]], dtype='float32') 
                   
   hier_mat = Hierarchia(mat)
   
   print(hier_mat.mat)
   print(hier_mat.indices)  
   
Result:

.. code-block:: python

   [[0. 6. 9. 8. 5.]
    [0. 0. 4. 6. 0.]
    [0. 2. 0. 4. 7.]
    [1. 0. 5. 0. 3.]
    [0. 0. 2. 3. 0.]]
   [0 1 2 3 4]

**Intialization with NumPy 2D array and name sequence**

.. code-block:: python
   :linenos:
   
   from HierarchiaPy import Hierarchia
   import numpy as np
  
   mat = np.array([[0, 6, 9, 8, 5],
                   [0, 0, 4, 6, 0],
                   [0, 2, 0, 4, 7],
                   [1, 0, 5, 0, 3],
                   [0, 0, 2, 3, 0]], dtype='float32') 
                   
   hier_mat = Hierarchia(mat, name_seq=['a', 'b', 'c', 'd', 'e'])
   
   print(hier_mat.mat)
   print(hier_mat.indices)  
   
Result:

.. code-block:: python

   [[0. 6. 9. 8. 5.]
    [0. 0. 4. 6. 0.]
    [0. 2. 0. 4. 7.]
    [1. 0. 5. 0. 3.]
    [0. 0. 2. 3. 0.]]
   ['a', 'b', 'c', 'd', 'e']
   

Basic Usage
-------------------------------

*See methods section for the comprehenssive list of available methods*

.. code-block:: python
   :linenos:
   
   from HierarchiaPy import Hierarchia
   import numpy as np
  
   mat = np.array([[0, 6, 9, 8, 5],
                   [0, 0, 4, 6, 0],
                   [0, 2, 0, 4, 7],
                   [1, 0, 5, 0, 3],
                   [0, 0, 2, 3, 0]], dtype='float32') 
                   
   hier_mat = Hierarchia(mat, name_seq=['a', 'b', 'c', 'd', 'e'])
   
   davids_scores = hier_mat.davids_score()
   print(davids_scores) 
   
Result:

.. code-block:: python
  
   {'a': 8.4444, 'b': 1.6111, 'c': -2.3333, 'd': -3.6667, 'e': -4.0556}
    

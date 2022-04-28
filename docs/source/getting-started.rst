Getting Started
===============

Installation
-------------------------------

To install the HierarchiaPy library, use the pip;

.. code-block:: console
   :linenos:
   
   $ pip install hierarchiapy


Hierarchia Class
-------------------------------

.. autoclass:: HierarchiaPy.Hierarchia

.. autofunction:: HierarchiaPy.Hierarchia.__init__

**Examples: Pandas DataFrame Initialization** 

.. note::
  Initialization via Pandas Dataframe - Required to have two more arguments: Winner and Loser Column names
  

.. code-block:: python
   :linenos:
   
   from HierarchiaPy import Hierarchia
   import pandas as pd
   
   df = pd.DataFrame({'winner': ['c', 'a', 'a', 'b', 'd', 'b', 'a', 'c', 'b'],
                   'loser': ['a', 'b', 'b', 'a', 'c', 'd', 'b', 'b', 'a']})
   hier_df = Hierarchia(df, 'winner', 'loser')
   print(hier_df.mat)
   print(hier_df.indices)

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
   
**Examples: 2D NumPy (Matrix) Initialization** 
    
.. note::

  Initialization via 2D Numpy - Require to be symmetric (n x n)
  
  

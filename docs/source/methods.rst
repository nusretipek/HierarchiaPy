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

.. code-block:: python
  :linenos:
  
  {'a': 971.0723573778384, 'b': 993.3936875304955, 'c': 1040.4209641361497, 'd': 995.1129909555166}
                        
                        
Randomized ELO Rating
------------------------------

.. autofunction:: _randomized_elo.randomized_elo


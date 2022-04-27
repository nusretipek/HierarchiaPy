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
   :linenos:
  
   {'a': 971.0724, 'b': 993.3937, 'c': 1040.421, 'd': 995.113}
                        
                        
Randomized ELO Rating
------------------------------

.. autofunction:: _randomized_elo.randomized_elo


Utilities
===============================================


Dij Matrix
-------------------------------

.. autofunction:: _metrics.get_Dij

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
   dij_matrix = hier_mat.get_Dij()                           
   print(dij_matrix)   

Result:

.. code-block:: python
  
   [[0.     0.8731 0.9352 0.9179 0.8784 0.8929 0.9219 0.9875 0.8793]
    [0.1269 0.     0.8654 0.7258 0.5588 0.8871 0.9762 0.8077 0.97  ]
    [0.0648 0.1346 0.     0.6724 0.7564 0.9615 0.75   0.9286 0.7083]
    [0.0821 0.2742 0.3276 0.     0.9571 0.9872 0.9595 0.9559 0.9914]
    [0.1216 0.4412 0.2436 0.0429 0.     0.8143 0.8548 0.75   0.9792]
    [0.1071 0.1129 0.0385 0.0128 0.1857 0.     0.625  0.4333 0.7353]
    [0.0781 0.0238 0.25   0.0405 0.1452 0.375  0.     0.6111 0.7   ]
    [0.0125 0.1923 0.0714 0.0441 0.25   0.5667 0.3889 0.     0.8077]
    [0.1207 0.03   0.2917 0.0086 0.0208 0.2647 0.3    0.1923 0.    ]]

                        
Directed Network Plot (Planar Layout)
-------------------------------

.. autofunction:: _utilities.directed_network_graph

Example:

.. code-block:: python
   :linenos:
   
   mat = np.array([[0, 6, 9, 8, 5],
                   [0, 0, 4, 6, 0],
                   [0, 2, 0, 4, 7],
                   [1, 0, 5, 0, 3],
                   [0, 0, 2, 3, 0]], dtype='float32')
   hier_mat = Hierarchia(mat)
   fig = hier_mat.directed_network_graph(fig_size=(7, 7),
                                         node_color=['red', 'blue', 'green', 'orange', 'yellow'],
                                         font_size=12)

Result:

.. image:: https://raw.githubusercontent.com/nusretipek/HierarchiaPy/master/docs/pictures/example_network_graph_2.png
  :width: 500
  :alt: Directed networkk graph (Planar layout)

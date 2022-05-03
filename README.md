[![Build Status](https://app.travis-ci.com/nusretipek/HierarchiaPy.svg?branch=master)](https://app.travis-ci.com/nusretipek/HierarchiaPy)
[![LICENCE](https://img.shields.io/github/license/nusretipek/HierarchiaPy)](https://github.com/nusretipek/HierarchiaPy/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/nusretipek/HierarchiaPy/branch/master/graph/badge.svg?token=vJeHuZ2Znv)](https://codecov.io/gh/nusretipek/HierarchiaPy)
[![Documentation Status](https://readthedocs.org/projects/hierarchiapy/badge/?version=latest)](https://hierarchiapy.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/HierarchiaPy.svg)](https://badge.fury.io/py/HierarchiaPy)

------------------------------------------------
<p align="center">
  <img src="https://raw.githubusercontent.com/nusretipek/HierarchiaPy/master/docs/pictures/logo.png" width="500">
</p>


Introduction
-----------

**HierarchiaPy** is an optimized statistical package for hierarchy/dominance analysis methds. It is purely written in Python and mainly built on Pandas and NumPy. Interarction data can be parsed both from Pandas DataFrame and 2D Numpy array. The methods are implemented based on the original published papers and tests module designed to cross-check the results with the examples from the reference papers.

Dominance and hierarchy is one of the core concepts in the research field of animal social behaviour. The hierarchy (dominance) can be derived from the interactions between the individuals (dyadic relationships). There are numerous techniques to derive the dominance from such dataset. We can classify them into two categories; numerical matrix optimization for certain criteria which results in a rank order (1) and calculation of a certain dominance measure for each individual from which a rank can be computed (2).

The HierarchiaPy statistical python package aims to implement available methods from both categories, allowing the animal social scientists to derive dominance efficiently, easily and in a reproducible way.

**Methods: Stable release**

1. ELO rating
2. Randomized ELO rating
3. David's Scores
4. Average Dominance Index
5. Adagio
6. I&SI 98

**Linearity Tests: Stable release**

1. Landau's h
2. Improved Landau's h
3. Kendall's K (Chi-square approximation & ECDF for n<10)
4. Unbiased Kendall's K (permutation of unknown relationships)


-----------------------------------------------

**Methods: Under Development**

3. I&SI 13 

Quick Start
-----------

**Installation**

PyPI publication is under process, for now use pip + git

```python
!pip install HierarchiaPy
```

**Basic Usage**

```python
from HierarchiaPy import Hierarchia
import numpy as np

mat_hemelrijk_table_2_1 = np.array([[0, 6, 9, 8, 5],
                                    [0, 0, 4, 6, 0],
                                    [0, 2, 0, 4, 7],
                                    [1, 0, 5, 0, 3],
                                    [0, 0, 2, 3, 0]], dtype='int64')

hier_mat = Hierarchia(mat_hemelrijk_table_2_1, np.array(['a', 'b', 'c', 'd', 'e']))
davids_scores = hier_mat.davids_score()

print(davids_scores)
```

Output:

```python
{'a': 8.4444, 'b': 1.6111, 'c': -2.3333, 'd': -3.6667, 'e': -4.0556}
```

Documentation
-------------

For full functionality and reference, see the [documentation](https://hierarchiapy.readthedocs.io/en/latest/)

Change Log
---------

v 0.1.0 - Initial release <br>
v 0.2.0 - Inclusion of linearity statistics & tests <br>
v 0.2.1 - Hot-fix for linearity tests <br>
v 0.2.2 - I&SI 98, performance improvement
v 0.2.3 - Landau's h classic improvement

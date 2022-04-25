from HierarchiaPy import Hierarchia
import pandas as pd
import numpy as np
import pytest

# Simple Dataframe and Matrix

df = pd.DataFrame({'winner': ['c', 'a', 'a', 'b', 'd', 'b', 'a', 'c', 'b'],
                   'loser': ['a', 'b', 'b', 'a', 'c', 'd', 'b', 'b', 'a']})

mat = np.array([[0, 6, 9, 8, 5],
                [0, 0, 4, 6, 0],
                [0, 2, 0, 4, 7],
                [1, 0, 5, 0, 3],
                [0, 0, 2, 3, 0]], dtype='float32')


# Create Hierarchia Obj - DataFrame

def test_hierarchia_df_args():
	hier_df = Hierarchia(df, 'winner', 'loser')
  assert(isinstance(hier_df, Hierarchia))

def test_hierarchia_df_kwargs():
	hier_df = Hierarchia(df, winner_col='winner', loser_col='loser')
  assert(isinstance(hier_df, Hierarchia))

def test_hierarchia_df_args_kwargs():
	hier_df = Hierarchia(df, winner_col='winner', 'loser')
  assert(isinstance(hier_df, Hierarchia))
  
def test_hierarchia_df_args_kwargs_2():
	hier_df = Hierarchia(df, loser_col='loser', winner')
  assert(isinstance(hier_df, Hierarchia))
                       
def test_hierarchia_df_args_kwargs_extra_args():
	hier_df = Hierarchia(df, winner_col='winner', loser_col='loser', 0)
  assert(isinstance(hier_df, Hierarchia))

def test_hierarchia_df_args_kwargs_extra_kwargs():
	hier_df = Hierarchia(df, test='test', winner_col='winner', loser_col='loser')
  assert(isinstance(hier_df, Hierarchia))
                       
# Create Hierarchia Obj - Matrix

def test_hierarchia_mat_args():
	hier_mat = Hierarchia(mat, ['a', 'b', 'c', 'd', 'e'])
  assert(isinstance(hier_mat, Hierarchia))                       

def test_hierarchia_mat_args_nonameseq():
	hier_mat = Hierarchia(mat)
  assert(isinstance(hier_mat, Hierarchia))  
                       
def test_hierarchia_mat_kwargs():
	hier_mat = Hierarchia(mat=mat, name_seq=['a', 'b', 'c', 'd', 'e'])
  assert(isinstance(hier_mat, Hierarchia))

def test_hierarchia_args_kwargs():
	hier_mat = Hierarchia(mat, name_seq=['a', 'b', 'c', 'd', 'e'])
  assert(isinstance(hier_mat, Hierarchia))
                       
# Elo test
                       
def test_elo():
	hier_mat = Hierarchia(mat, name_seq=['a', 'b', 'c', 'd', 'e'])
  elo_ranks = hier_mat.elo()
  assert(isinstance(elo_ranks, Dict))    
  assert(len(elo_ranks) == len(hier_mat.indices))
                       
                      

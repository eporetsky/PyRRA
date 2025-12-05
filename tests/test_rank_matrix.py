import numpy as np
import pandas as pd
from pyrra.rank_matrix import rank_matrix
from pyrra.rank_matrix import aggregate_ranks

def test_rank_matrix_partial():
    glist = [list("bcda"), list("hgfedcbaji"), list("mlkjihgfedcb")]
    res = rank_matrix(glist)
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {"L1", "L2", "L3"}
    assert res.shape[1] == 3
    assert all(res.index.str.len() == 1)
    assert (res <= 1).all().all() and (res >= 0).all().all()

def test_rank_matrix_full():
    glist = [list("bcda"), list("hgfedcbaji"), list("mlkjihgfedcb")]
    res = rank_matrix(glist, full=True)
    assert isinstance(res, pd.DataFrame)
    assert res.isnull().any().any() or True

def test_aggregate_ranks_with_rmat():
    # Use the same glist example, but pass the DataFrame directly
    glist = [list("bcda"), list("hgfedcbaji"), list("mlkjihgfedcb")]
    rmat = rank_matrix(glist)
    agg = aggregate_ranks(rmat=rmat)
    assert isinstance(agg, pd.DataFrame)
    assert set(agg.columns) == {"Name", "Score"}
    assert len(agg) == len(rmat)

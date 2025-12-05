import random
import pytest
from pyrra.rank_matrix import aggregate_ranks

def test_aggregate_ranks_RRA():
    glists = [list("abc"), list("bca"), list("cab")]
    result = aggregate_ranks(glist=glists, method="RRA")
    assert "Score" in result.columns
    assert result.shape[0] >= 3  # Should cover all unique genes

def test_aggregate_ranks_min():
    glists = [list("abcd"), list("bcda"), list("cdab")]
    result = aggregate_ranks(glist=glists, method="min")
    assert (result["Score"] >= 0).all()

def test_empty_input_raises():
    with pytest.raises(ValueError):
        aggregate_ranks(glist=[])

def test_singleton_list():
    glists = [["gene1"]]
    result = aggregate_ranks(glist=glists)
    assert result.shape[0] == 1

def test_identical_lists():
    glists = [list("abcdefghij")] * 100
    result = aggregate_ranks(glist=glists)
    assert result.shape[0] == 10


def shuffled_lists(base, n):
    lists = []
    for _ in range(n):
        l = base[:]
        random.shuffle(l)
        lists.append(list(l))
    return lists

def test_shuffled_lists():
    base = list("abcdefghij")
    glists = shuffled_lists(base, 10)
    result = aggregate_ranks(glist=glists)
    assert result.shape[0] == 10
    # All unique elements should be present
    assert set(result["Name"]) == set(base)

def test_large_N_handling():
    base = list("abcdefghij")
    glists = shuffled_lists(base, 10)
    result = aggregate_ranks(glist=glists, N=30)
    assert result.shape[0] == 10

def test_output_differs_with_N():
    base = list("abcdefghij")
    glists = shuffled_lists(base, 10)
    res_default = aggregate_ranks(glist=glists)
    res_largeN = aggregate_ranks(glist=glists, N=1000)
    assert set(res_default["Name"]) == set(res_largeN["Name"])
    assert not all(res_default["Score"].values == res_largeN["Score"].values)

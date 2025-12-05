import numpy as np
from pyrra.beta_scores import beta_scores

def test_beta_scores_basic():
    np.random.seed(0)
    arr = np.random.uniform(size=15)
    pvals = beta_scores(arr)
    assert len(pvals) == len(arr)
    assert np.all((pvals >= 0) & (pvals <= 1))

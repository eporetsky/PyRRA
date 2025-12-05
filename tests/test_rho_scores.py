import numpy as np
from pyrra.rho_scores import rho_scores

def test_rho_scores_basic():
    np.random.seed(0)
    arr = np.random.uniform(size=15)
    rho = rho_scores(arr)
    assert 0 <= rho <= 1
    # Check edge (very small values biasing minimum)
    arr2 = np.concatenate([arr, np.array([1e-8])])
    rho2 = rho_scores(arr2)
    assert rho2 <= rho

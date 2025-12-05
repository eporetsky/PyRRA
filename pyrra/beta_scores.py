import numpy as np
from scipy.stats import beta
from typing import Sequence

def beta_scores(r: Sequence[float]):
    """Port of R's betaScores. Args: r is a sequence of numbers in [0,1], possibly with some NaN (missing). Returns: Array of p-values, NA pushed to end."""
    r = np.array(r, dtype=float)
    r = r[~np.isnan(r)]  # Remove NA
    n = len(r)
    if n == 0:
        return np.array([])
    r_sorted = np.sort(r)
    p = beta.cdf(r_sorted, np.arange(1, n+1), n - np.arange(1, n+1) + 1)
    return p

def threshold_beta_score(r, k=None, n=None, sigma=None):
    """
    Port of R's thresholdBetaScore: handles thresholding for beta scoring.
    """
    import numpy as np
    from scipy.stats import beta
    r = np.asarray(r, dtype=float)
    if n is None:
        n = len(r)
    if k is None:
        k = np.arange(1, n+1)
    if sigma is None:
        sigma = np.ones(n)
    sigma = np.asarray(sigma, dtype=float)
    if len(sigma) != n:
        raise ValueError("Length of sigma does not match n")
    if len(r) != n:
        raise ValueError("Length of r does not match n")
    if np.nanmin(sigma) < 0 or np.nanmax(sigma) > 1:
        raise ValueError("Elements of sigma not in [0,1]")
    if np.any(~np.isnan(r) & (r > sigma)):
        raise ValueError("Elements of r must be smaller than elements of sigma")
    x = np.sort(r[~np.isnan(r)])
    sigma_sorted = np.sort(sigma)[::-1]
    beta_vec = np.full(len(k), np.nan, dtype=float)
    for i, ki in enumerate(k):
        if ki > n:
            beta_vec[i] = 0
            continue
        if ki > len(x):
            beta_vec[i] = 1
            continue
        if sigma_sorted[n-1] >= x[ki-1]:
            beta_vec[i] = beta.cdf(x[ki-1], ki, n+1-ki)
            continue
        # Non-trivial: find last index n0 such that sigma[n0] < x[ki] (in 1-indexing)
        n0s = np.where(sigma_sorted < x[ki-1])[0]
        n0 = n0s[0] if len(n0s) > 0 else 0  # python 0-based
        if n0 == 0:
            B = np.zeros(ki + 1, dtype=float)
            B[0] = 1
        elif ki > n0:
            B = np.zeros(ki + 1, dtype=float)
            B[0] = 1
            B[1:n0+1] = beta.cdf(x[ki-1], np.arange(1, n0+1), n0 - np.arange(0, n0) + 1)
        else:
            B = np.zeros(ki + 1, dtype=float)
            B[0] = 1
            B[1:ki+1] = beta.cdf(x[ki-1], np.arange(1, ki+1), n0 + 1 - np.arange(1, ki+1))
        z = sigma_sorted[n0:]
        for j in range(len(z)):
            # B[1:] = (1 - z[j]) * B[1:] + z[j] * B[:-1]
            B[1:] = (1 - z[j]) * B[1:] + z[j] * B[:-1]
        beta_vec[i] = B[ki]
    # names are k
    return beta_vec

def correct_beta_pvalues(p, k):
    """
    Port of R's correctBetaPvalues. Applies multiple hypothesis correction.
    """
    p = np.minimum(p * k, 1.0)
    return p

def correct_beta_pvalues_exact(p, k, stuart_func=None):
    """
    Port of R's correctBetaPvaluesExact. Needs stuart function for computation.
    """
    import numpy as np
    from scipy.stats import beta
    # compute 1 - t(sapply(p, qbeta, 1:k, k - 1:k + 1))
    # R: rm = 1 - t(sapply(p, qbeta, 1:k, k - 1:k + 1))
    pb = np.array([beta.ppf(pi, i+1, k-i) for i, pi in enumerate(np.full(k, p))])
    rm = 1 - pb  # shape: (k,)
    if stuart_func is None:
        raise ValueError("stuart_func must be supplied")
    res = 1 - stuart_func(rm.reshape(1, -1))
    return res[0] if hasattr(res, '__getitem__') else res

__all__ = [
    'beta_scores',
    'threshold_beta_score',
    'correct_beta_pvalues',
    'correct_beta_pvalues_exact',
]

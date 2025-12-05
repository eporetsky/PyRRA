import numpy as np
from .beta_scores import beta_scores, threshold_beta_score, correct_beta_pvalues, correct_beta_pvalues_exact
from .rank_matrix import stuart

def rho_scores(r, top_cutoff=None, exact=False):
    """
    Calculate Rho score for normalized rank vector (like R's rhoScores).
    If top_cutoff given, uses threshold_beta_score helper. If exact, uses correct_beta_pvalues_exact.
    """
    r = np.array(r, dtype=float)
    if top_cutoff is None or (isinstance(top_cutoff, float) and np.isnan(top_cutoff)):
        x = beta_scores(r)
    else:
        valid = ~np.isnan(r)
        r_clean = r[valid]
        r_clean[r_clean == 1] = np.nan
        # R vectorized topCutoff handling (sigma)
        sigma = top_cutoff
        x = threshold_beta_score(r_clean, sigma=sigma)
    min_x = np.nanmin(x)
    k = np.sum(~np.isnan(x))
    if exact:
        rho = correct_beta_pvalues_exact(min_x, k, stuart_func=stuart)
    else:
        rho = correct_beta_pvalues(min_x, k)
    return rho

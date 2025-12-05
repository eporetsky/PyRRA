import math
import numpy as np
import pandas as pd
from typing import List, Any, Optional, Union

def rank_matrix(
    glist: List[List[Any]], 
    N: Optional[Union[int, List[int]]] = None, 
    full: bool = False
) -> pd.DataFrame:
    """
    Converts a set of ranked lists into a rank matrix, replicating R's rankMatrix.
    If partial ranking, missing values are filled with 1 (max rank N later), else full uses NaN for structural missing.
    """
    # Use pd.Index to remove duplicates but preserve order efficiently
    seen = set()
    u = [item for l in glist for item in l if not (item in seen or seen.add(item))]
    u = pd.Index(u)
    if N is None:
        N_calc = len(u)
    else:
        N_calc = N
    if not full:
        rmat = pd.DataFrame(1.0, index=u, columns=[f"L{i+1}" for i in range(len(glist))])
        if isinstance(N_calc, int):
            N_list = [N_calc] * len(glist)
        else:
            N_list = list(N_calc)
    else:
        rmat = pd.DataFrame(np.nan, index=u, columns=[f"L{i+1}" for i in range(len(glist))])
        N_list = [len(x) for x in glist]
    for i, lst in enumerate(glist):
        rmat.loc[lst, rmat.columns[i]] = (np.arange(1, len(lst)+1) / N_list[i])
    return rmat

def sum_stuart(v, r):
    """
    Stuart-Aerts sumStuart helper from R: for computing combination coefficients.
    v: coefficients vector
    r: scalar or vector (used in raising to power)
    """
    k = len(v)
    l_k = np.arange(1, k+1)
    ones = (-1)**(l_k + 1)
    f = np.array([math.factorial(i) for i in l_k])
    p = r ** l_k
    # R: return(ones %*% (rev(v) * p / f))
    # rev(v): reverse v
    result = np.dot(ones, np.array(list(reversed(v))) * p / f)
    return result

def q_stuart(r):
    """
    Stuart-Aerts qStuart from R. Calculates the special polynomial expansion for Stuart p-values.
    r: rank vector (1D np.array), may contain nan for missing
    """
    N = np.sum(~np.isnan(r))
    v = np.ones(N + 1)
    for k in range(1, N + 1):
        v[k] = sum_stuart(v[:k], r[N - k])
    return math.factorial(N) * v[N]

def stuart(rmat):
    """
    Stuart-Aerts overall p-value calculation. rmat: 2D array, each row a rank vector. Returns 1D vector of scores for each row.
    """
    # Sort non-nan values in each row
    rmat_sorted = np.apply_along_axis(lambda x: np.sort(x[~np.isnan(x)]), 1, rmat)
    scores = np.apply_along_axis(q_stuart, 1, rmat_sorted)
    return scores

def format_output(scores, score_names, ordering="ascending"):
    """
    Formats output into a pandas DataFrame sorted by score, ascending or descending order.
    Args:
        scores: 1D array-like of scores
        score_names: array-like of names
        ordering: "ascending" (default) or "descending"
    Returns:
        pd.DataFrame with columns ['Name', 'Score'], sorted.
    """
    import pandas as pd
    res = pd.DataFrame({'Name': score_names, 'Score': scores})
    ascending = ordering == "ascending"
    res = res.sort_values('Score', ascending=ascending, ignore_index=True)
    return res

def aggregate_ranks(
    glist=None, 
    rmat=None, 
    N=None, 
    method='RRA', 
    full=False, 
    exact=None, 
    top_cutoff=None
):
    """
    Aggregates ranked lists (main RRA method).
    Args:
        glist: List of input rankings (outermost interface)
        rmat: Provide your own rank matrix if available (otherwise generated from glist)
        N: Number of rankable elements. Defaults to number of unique elements
        method: 'RRA', 'mean', 'min', 'median', 'geom.mean', or 'stuart'
        full: Input lists represent full rankings (structural missing as NaN)
        exact: Use exact for RRA (None: auto, set True or False for override)
        top_cutoff: optional; used when list cutoffs are known in advance
    Returns:
        DataFrame with ['Name', 'Score'] columns, sorted appropriately
    """
    import numpy as np
    import pandas as pd
    from .rho_scores import rho_scores
    # Compose or receive rank matrix
    if rmat is None:
        if glist is None:
            raise ValueError('Must provide either glist (rank lists) or rmat (rank matrix)')
        rmat = rank_matrix(glist, N=N, full=full)
    if N is None:
        N = rmat.shape[0]
    # Default names
    if rmat.index is None or rmat.index.empty:
        index_names = [str(i+1) for i in range(rmat.shape[0])]
    else:
        index_names = rmat.index.tolist()
    # Choose method logic
    if method == 'min':
        a = rmat.min(axis=1, skipna=True)
        return format_output(a.values, index_names, ordering='ascending')
    elif method == 'median':
        a = rmat.median(axis=1, skipna=True)
        return format_output(a.values, index_names, ordering='ascending')
    elif method == 'geom.mean':
        a = np.exp(np.log(rmat).mean(axis=1, skipna=True))
        return format_output(a.values, index_names, ordering='ascending')
    elif method == 'mean':
        a = rmat.mean(axis=1, skipna=True)
        n = rmat.notna().sum(axis=1)
        b = (a - 0.5) / np.sqrt(1/12/n)
        from scipy.stats import norm
        pvals = norm.cdf(b)
        return format_output(pvals, index_names, ordering='ascending')
    elif method == 'stuart':
        a = stuart(rmat.values)
        return format_output(a, index_names, ordering='ascending')
    elif method == 'RRA':
        # Handle exact/pValue logic per R (if 10 or fewer lists: default exact)
        if exact is None:
            exact = rmat.shape[1] <= 10
        # Each row: use rho_scores()
        a = rmat.apply(lambda row: rho_scores(row.values, top_cutoff=top_cutoff, exact=exact), axis=1)
        a.index = rmat.index
        return format_output(a.values, index_names, ordering='ascending')
    else:
        raise ValueError(f"Unknown aggregation method: {method}")

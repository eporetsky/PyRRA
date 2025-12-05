# PyRRA: Python Implementation of the RobustRankAggreg R package

> **Disclaimer:** The PyRRA (Python Robust Rank Aggregation) project is an attempted port of the RobustRankAggreg R package (v1.2.1; cran.r-project.org/web/packages/RobustRankAggreg). PyRRA is under development and the outputs between the original R package and this Python implementation are not guaranteed to be identical. This python reimplementation is independent of the original authors and code maintainers (DOI: 10.1093/bioinformatics/btr709).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python port of the [RobustRankAggreg (RRA) package](https://bioconductor.org/packages/release/bioc/html/RobustRankAggreg.html) for robust aggregation of ranked lists with missing/unmatched elements. PyRRA enables reproducible meta-analyses, gene integration, and other robust ranking applications right from Python.

---

## Features
- **PyRRA is still under development**
- Robust aggregation of partial or full ranked lists (no requirement that sets overlap)
- Ports of RRA's `rankMatrix`, `betaScores`, `rhoScores`, and all aggregation methods (`RRA`, `stuart`, `mean`, `min`, `median`, `geom.mean`)
- Validated with cross-language testing against the original R package
- Helper utilities for thresholding, multiple testing correction, and Stuart p-value computation

---

## Installation

Suggested Conda environment:

```bash 
conda env create -f environment.yml 
conda activate pyrra
```

Install from PyPi (recommended):

```bash
pip install pyrra
```

Install directly from source via pip:

```bash
pip install .
```

---

## Usage

```python
from pyrra import rank_matrix, aggregate_ranks

# A list of ranked gene symbols (or any unique items)
glists = [
    ['b', 'c', 'd', 'a'],
    ['h', 'b', 'f', 'e', 'd', 'c', 'g', 'a', 'j', 'i'],
    ['m', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b']
]

rank_mat = rank_matrix(glists)
print(rank_mat)
#           L1   L2   L3
# a  1.000000 0.125  NaN
# b  0.250000 0.175 0.917
# ...

# Aggregate with the default RRA method
agg = aggregate_ranks(glist=glists, method='RRA')
print(agg.head())
#     Name     Score
# 0      ...     ...
```

> You can also pass a pandas DataFrame rank matrix to `aggregate_ranks` via `rmat=...`.

### Aggregation Methods
- `RRA` (**default**)
- `stuart`: Stuart-Aerts p-value
- `min`, `mean`, `median`, `geom.mean`: Aggregate using these statistics

### Advanced Arguments
- `full` (default=False): Set True if all input lists are full rankings (for structural NA treatment)
- `N`: Total number of rankable items (overrides default: union of elements)
- `exact` (default: auto): Use exact p-value (slower, may be numerically unstable for many lists)
- `top_cutoff`: Vector of cutoff values (for sensitivity when lists are truncated at different points)

---

## API Reference
### rank_matrix(glist, N=None, full=False)
- Converts ranked lists to a normalized rank matrix.
- Parameters:
    - `glist`: list of lists
    - `N`: total number of rankable elements (default: union of glist)
    - `full`: If True, treat all as full-length rankings with NA for structural gaps
- Returns: pandas DataFrame

### aggregate_ranks(glist=None, rmat=None, N=None, method='RRA', full=False, exact=None, top_cutoff=None)
- Main aggregation method (RRA, mean, min, etc).
- Returns: pandas DataFrame of scores, sorted.

---

## Citing
- Original algorithm: [RobustRankAggreg Bioinformatics 2012](https://doi.org/10.1093/bioinformatics/btr709)

---

## Contributors
Elly Poretsky (@eporetsky) — Python port, test suite, data validation.

---

## See Also
- [RobustRankAggreg (R Package)](https://bioconductor.org/packages/release/bioc/html/RobustRankAggreg.html)

---

## Comparison with the R implementation

For users seeking direct comparison and validation against the original R RobustRankAggreg package, see the output in `compare/comprehensive_comparison.txt` or follow the instructions below to run your own validations:

```bash 
cd compare

# Conda environment with Python and R
conda env create -f environment.yml 
conda activate pyrra_compare
pip install pyrra

# Run tests to comparee
python comprehensive_comparison.py
```
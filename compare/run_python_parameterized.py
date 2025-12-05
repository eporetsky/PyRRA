#!/usr/bin/env python3
"""Run Python rank_matrix with specified parameters and save output."""
import pandas as pd
from pyrra.rank_matrix import rank_matrix
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: run_python_parameterized.py <dataset> <full> [N]")
        sys.exit(1)
    
    dataset = sys.argv[1]
    full = sys.argv[2].lower() == 'true'
    N = None
    if len(sys.argv) >= 4 and sys.argv[3] != 'None':
        N = int(sys.argv[3])
    
    # Load data based on dataset
    if dataset == 'letters':
        glist = [list("bcda"), list("hgfedcbaji"), list("mlkjihgfedcb")]
    elif dataset == 'cellCycleKO':
        # Load from longform CSV
        df = pd.read_csv("export_cellCycleKO_longform.csv")
        glist = []
        for list_name in df['List'].unique():
            genes = df[df['List'] == list_name].sort_values('Rank')['Gene'].tolist()
            glist.append(genes)
    else:
        raise ValueError(f"Unknown dataset: {dataset}")
    
    # Run rank_matrix with parameters
    kwargs = {'full': full}
    if N is not None:
        kwargs['N'] = N
    
    result = rank_matrix(glist, **kwargs)
    
    # Save output
    result.to_csv("temp_python_output.csv")

if __name__ == "__main__":
    main()


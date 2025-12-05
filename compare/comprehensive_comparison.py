#!/usr/bin/env python3
"""
Comprehensive comparison of Python and R rank_matrix implementations.
Tests multiple parameter combinations on different datasets.
"""
import pandas as pd
import numpy as np
import subprocess
import os
from pathlib import Path

# Change to compare directory
os.chdir(Path(__file__).parent)

def run_comparison(dataset, full, N):
    """Run Python and R with given parameters and compare outputs."""
    
    # Prepare arguments
    full_str = 'True' if full else 'False'
    N_str = str(N) if N is not None else 'None'
    
    # Run Python
    try:
        result = subprocess.run(
            ['python3', 'run_python_parameterized.py', dataset, full_str, N_str],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        return False, f"Python error: {e.stderr}"
    
    # Run R
    try:
        result = subprocess.run(
            ['Rscript', 'run_r_parameterized.R', dataset, full_str, N_str],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        return False, f"R error: {e.stderr}"
    
    # Compare outputs
    try:
        py_res = pd.read_csv("temp_python_output.csv", index_col=0)
        r_res = pd.read_csv("temp_r_output.csv", index_col=0)
        
        # Check indices match
        if set(py_res.index) != set(r_res.index):
            return False, f"Row indices don't match! Python has {len(py_res)} rows, R has {len(r_res)} rows"
        
        # Align indices
        py_res = py_res.loc[r_res.index]
        
        # Check columns match (as sets, order doesn't matter)
        if set(py_res.columns) != set(r_res.columns):
            return False, f"Column names don't match! Python: {list(py_res.columns)}, R: {list(r_res.columns)}"
        
        # Reorder Python columns to match R (R sorts alphabetically)
        py_res = py_res[r_res.columns]
        
        # Compare values
        pd.testing.assert_frame_equal(py_res, r_res, check_dtype=False, atol=1e-12)
        
        # Clean up temp files
        os.remove("temp_python_output.csv")
        os.remove("temp_r_output.csv")
        
        return True, "Identical results"
        
    except AssertionError as e:
        # Try to see how different they are
        max_diff = np.abs(py_res.values - r_res.values).max()
        
        # Clean up temp files
        if os.path.exists("temp_python_output.csv"):
            os.remove("temp_python_output.csv")
        if os.path.exists("temp_r_output.csv"):
            os.remove("temp_r_output.csv")
        
        return False, f"Values differ (max diff: {max_diff:.2e}): {str(e)[:100]}"
    except Exception as e:
        # Clean up temp files
        if os.path.exists("temp_python_output.csv"):
            os.remove("temp_python_output.csv")
        if os.path.exists("temp_r_output.csv"):
            os.remove("temp_r_output.csv")
        
        return False, f"Comparison error: {str(e)}"

def main():
    """Run all parameter combinations and report results."""
    
    print("=" * 80)
    print("COMPREHENSIVE PYTHON vs R COMPARISON TEST")
    print("=" * 80)
    print()
    
    # Define test cases
    test_cases = []
    
    # Letters dataset tests
    test_cases.append(('letters', False, None, "Basic letters, full=False, N=None"))
    test_cases.append(('letters', True, None, "Letters, full=True, N=None"))
    test_cases.append(('letters', False, 15, "Letters, full=False, N=15"))
    test_cases.append(('letters', False, 20, "Letters, full=False, N=20"))
    
    # cellCycleKO dataset tests
    test_cases.append(('cellCycleKO', False, None, "cellCycleKO, full=False, N=None"))
    test_cases.append(('cellCycleKO', True, None, "cellCycleKO, full=True, N=None"))
    # Note: cellCycleKO uses N=length(ref) in the R package example
    test_cases.append(('cellCycleKO', False, 6178, "cellCycleKO, full=False, N=6178"))
    
    passed = 0
    failed = 0
    results = []
    
    for dataset, full, N, description in test_cases:
        print(f"Testing: {description}")
        print(f"  Parameters: dataset={dataset}, full={full}, N={N}")
        
        success, message = run_comparison(dataset, full, N)
        
        if success:
            print(f"  ✓ PASS: {message}")
            passed += 1
        else:
            print(f"  ✗ FAIL: {message}")
            failed += 1
        
        results.append({
            'description': description,
            'dataset': dataset,
            'full': full,
            'N': N,
            'status': 'PASS' if success else 'FAIL',
            'message': message
        })
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total tests: {len(test_cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()
    
    if failed > 0:
        print("Failed tests:")
        for r in results:
            if r['status'] == 'FAIL':
                print(f"  - {r['description']}")
                print(f"    {r['message']}")
        print()
    
    if passed == len(test_cases):
        print("🎉 ALL TESTS PASSED! Python and R implementations are identical.")
    else:
        print(f"⚠️  {failed} test(s) failed. See details above.")
    
    print("=" * 80)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit(main())


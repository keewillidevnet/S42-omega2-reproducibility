#!/usr/bin/env python3
"""
CPU Benchmark Script for S₄,₂(x)
================================

Reproduces Table 1 from the paper: comparison of series vs closed-form evaluation
at various precisions.

Usage:
    python scripts/benchmark_cpu.py --precision 120 --target all
    python scripts/benchmark_cpu.py --precision 80 --target 1/2 --trials 100
"""

import argparse
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mpmath import mp
import pandas as pd

from s42 import (
    evaluate_series,
    evaluate_closed_form,
    compute_omega2_basis,
    AVAILABLE_X_VALUES,
)


def benchmark_single(x_val: float, precision: int, num_trials: int = 10) -> dict:
    """
    Benchmark series vs closed form for a single x value.
    
    Returns dictionary with timing and accuracy results.
    """
    mp.dps = precision
    
    # Pre-compute basis (one-time cost)
    t0 = time.time()
    basis = compute_omega2_basis(precision=precision)
    basis_time = time.time() - t0
    
    # Benchmark series
    series_times = []
    for _ in range(num_trials):
        t0 = time.time()
        series_val = evaluate_series(x_val, precision=precision)
        series_times.append(time.time() - t0)
    
    series_time_mean = sum(series_times) / len(series_times)
    
    # Benchmark closed form (per-evaluation, basis already computed)
    from s42.closed_form import S42_closed_form
    closed_times = []
    
    for _ in range(num_trials):
        t0 = time.time()
        closed_val = S42_closed_form(x_val, basis=basis, precision=precision)
        closed_times.append(time.time() - t0)
    
    closed_time_mean = sum(closed_times) / len(closed_times)
    
    # Compute error
    abs_error = abs(series_val - closed_val)
    
    return {
        "x": x_val,
        "precision": precision,
        "basis_time_ms": basis_time * 1000,
        "series_time_ms": series_time_mean * 1000,
        "closed_time_us": closed_time_mean * 1e6,
        "per_eval_ratio": series_time_mean / closed_time_mean,
        "abs_error": float(abs_error),
        "num_trials": num_trials,
    }


def run_benchmark(
    targets: list,
    precision: int,
    num_trials: int = 10,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Run benchmark for multiple targets.
    """
    results = []
    
    for x_str in targets:
        if x_str not in AVAILABLE_X_VALUES:
            print(f"Warning: Skipping unknown target {x_str}")
            continue
        
        x_val = float(AVAILABLE_X_VALUES[x_str])
        
        if verbose:
            print(f"\nBenchmarking S₄,₂({x_str}) at {precision} decimal places...")
        
        result = benchmark_single(x_val, precision, num_trials)
        results.append(result)
        
        if verbose:
            print(f"  Series:    {result['series_time_ms']:.3f} ms")
            print(f"  Closed:    {result['closed_time_us']:.3f} μs")
            print(f"  Ratio:     {result['per_eval_ratio']:.1f}×")
            print(f"  Error:     {result['abs_error']:.3e}")
    
    return pd.DataFrame(results)


def precision_scaling_study(
    x_val: float,
    precisions: list,
    num_trials: int = 10,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Study how performance scales with precision.
    """
    results = []
    
    for prec in precisions:
        if verbose:
            print(f"\nPrecision: {prec} decimal places")
        
        result = benchmark_single(x_val, prec, num_trials)
        results.append(result)
        
        if verbose:
            print(f"  Speedup: {result['per_eval_ratio']:.1f}×")
    
    return pd.DataFrame(results)


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark S₄,₂(x) evaluation: series vs closed form"
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=120,
        help="Decimal precision (default: 120)"
    )
    parser.add_argument(
        "--target",
        type=str,
        default="all",
        help="Target x value: '1/2', '1/4', '-1/2', or 'all' (default: all)"
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=10,
        help="Number of trials per benchmark (default: 10)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV file (default: None, print to stdout)"
    )
    parser.add_argument(
        "--precision-scaling",
        action="store_true",
        help="Run precision scaling study instead of single precision"
    )
    parser.add_argument(
        "--scaling-precisions",
        type=str,
        default="50,80,120,160",
        help="Precisions for scaling study (comma-separated, default: 50,80,120,160)"
    )
    
    args = parser.parse_args()
    
    # Determine targets
    if args.target.lower() == "all":
        targets = list(AVAILABLE_X_VALUES.keys())
    else:
        targets = [args.target]
    
    print("=" * 70)
    print("S₄,₂(x) CPU Benchmark")
    print("=" * 70)
    
    if args.precision_scaling:
        # Precision scaling study
        precisions = [int(p) for p in args.scaling_precisions.split(",")]
        
        print(f"\nPrecision Scaling Study")
        print(f"Target: S₄,₂({targets[0]})")
        print(f"Precisions: {precisions}")
        print(f"Trials per precision: {args.trials}")
        
        x_val = float(AVAILABLE_X_VALUES[targets[0]])
        df = precision_scaling_study(x_val, precisions, args.trials, verbose=True)
    else:
        # Single precision benchmark
        print(f"\nConfiguration:")
        print(f"  Precision: {args.precision} decimal places")
        print(f"  Targets: {targets}")
        print(f"  Trials: {args.trials}")
        
        df = run_benchmark(targets, args.precision, args.trials, verbose=True)
    
    # Print results table
    print("\n" + "=" * 70)
    print("Results:")
    print("=" * 70)
    print(df.to_string(index=False))
    
    # Save to file if requested
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()

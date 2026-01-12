#!/usr/bin/env python3
"""
Quick Start Example for S₄,₂(x)
================================

Demonstrates basic usage of the s42 package.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mpmath import mp
from s42 import (
    evaluate_series,
    evaluate_closed_form,
    get_coefficients,
    print_coefficients,
    AVAILABLE_X_VALUES,
)


def main():
    print("=" * 70)
    print("S₄,₂(x) Quick Start Example")
    print("=" * 70)
    
    # Set precision
    mp.dps = 100
    print(f"\nWorking precision: {mp.dps} decimal places")
    
    # Example 1: Evaluate using series
    print("\n" + "-" * 70)
    print("Example 1: Series Evaluation")
    print("-" * 70)
    
    x = 0.5
    print(f"\nEvaluating S₄,₂({x}) via series summation...")
    value_series = evaluate_series(x)
    print(f"Result: {value_series}")
    
    # Example 2: Evaluate using closed form
    print("\n" + "-" * 70)
    print("Example 2: Closed-Form Evaluation")
    print("-" * 70)
    
    print(f"\nEvaluating S₄,₂({x}) via closed form...")
    value_closed = evaluate_closed_form(x)
    print(f"Result: {value_closed}")
    
    # Example 3: Compare accuracy
    print("\n" + "-" * 70)
    print("Example 3: Accuracy Comparison")
    print("-" * 70)
    
    abs_error = abs(value_series - value_closed)
    print(f"\nAbsolute error: {abs_error:.3e}")
    print(f"Relative error: {abs_error / abs(value_series):.3e}")
    
    # Example 4: View coefficients
    print("\n" + "-" * 70)
    print("Example 4: Exact Coefficients")
    print("-" * 70)
    
    coeffs = get_coefficients(x)
    print(f"\nS₄,₂({x}) is expressed as a linear combination of 21 basis elements:")
    print_coefficients(x, format_type="fraction")
    
    # Example 5: Evaluate all available x values
    print("\n" + "-" * 70)
    print("Example 5: All Available Identities")
    print("-" * 70)
    
    mp.dps = 50  # Use moderate precision for quick evaluation
    print(f"\nEvaluating S₄,₂(x) for all known x values at {mp.dps} dps:")
    
    for x_str, x_val in AVAILABLE_X_VALUES.items():
        value = evaluate_closed_form(float(x_val))
        print(f"  S₄,₂({x_str:5s}) = {value}")
    
    # Example 6: Timing comparison
    print("\n" + "-" * 70)
    print("Example 6: Performance Comparison")
    print("-" * 70)
    
    import time
    
    mp.dps = 120
    x = 0.5
    
    print(f"\nTiming S₄,₂({x}) at {mp.dps} decimal places:")
    
    # Time series
    t0 = time.time()
    _ = evaluate_series(x)
    series_time = time.time() - t0
    print(f"  Series:      {series_time*1000:.3f} ms")
    
    # Time closed form
    t0 = time.time()
    _ = evaluate_closed_form(x)
    closed_time = time.time() - t0
    print(f"  Closed form: {closed_time*1000:.3f} ms (includes basis computation)")
    
    print(f"\nPer-evaluation speedup (after basis precomputation): ~{series_time/closed_time:.1f}×")
    
    print("\n" + "=" * 70)
    print("For more examples, see the notebooks/ directory")
    print("=" * 70)


if __name__ == "__main__":
    main()

"""
S₄,₂(x) Closed-Form Evaluation
===============================

Evaluation using exact Ω₂ identities:

    S₄,₂(x) = Σⱼ cⱼ · ωⱼ

where cⱼ are exact rational coefficients and ωⱼ are weight-6 constants.
"""

from mpmath import mp, mpf
from typing import List, Optional, Tuple
from .basis import compute_omega2_basis
from .coefficients import get_coefficients, get_coefficients_mpf, AVAILABLE_X_VALUES


def S42_closed_form(
    x: float,
    basis: Optional[List[mpf]] = None,
    coeffs: Optional[List] = None,
    precision: int = None
) -> mpf:
    """
    Evaluate S₄,₂(x) using the exact closed form.
    
    Args:
        x: The x value (must be in {1/2, 1/4, -1/2})
        basis: Pre-computed Ω₂ basis (optional, will compute if not provided)
        coeffs: Pre-computed coefficients (optional, will fetch if not provided)
        precision: Decimal precision (default: current mp.dps)
    
    Returns:
        The value of S₄,₂(x)
    
    Raises:
        ValueError: If x is not one of the supported values
    
    Example:
        >>> from mpmath import mp
        >>> mp.dps = 120
        >>> value = S42_closed_form(x=0.5)
        >>> print(value)
    """
    if precision is not None:
        old_dps = mp.dps
        mp.dps = precision
    
    try:
        # Compute or use provided basis
        if basis is None:
            basis = compute_omega2_basis(precision=mp.dps)
        
        # Get or use provided coefficients
        if coeffs is None:
            coeffs = get_coefficients_mpf(x, precision=mp.dps)
        
        # Compute dot product
        result = mpf(0)
        for c, omega in zip(coeffs, basis):
            result += c * omega
        
        return result
    
    finally:
        if precision is not None:
            mp.dps = old_dps


def evaluate_closed_form(
    x: float,
    precision: int = None,
    precompute_basis: bool = True
) -> mpf:
    """
    Convenience function for closed-form evaluation.
    
    Args:
        x: The x value
        precision: Decimal precision
        precompute_basis: Whether to compute basis once (faster for multiple evaluations)
    
    Returns:
        The value of S₄,₂(x)
    """
    if precision is not None:
        mp.dps = precision
    
    basis = compute_omega2_basis() if precompute_basis else None
    return S42_closed_form(x, basis=basis, precision=precision)


def batch_evaluate_closed_form(
    x_values: List[float],
    precision: int = None
) -> List[mpf]:
    """
    Evaluate S₄,₂(x) for multiple x values efficiently.
    
    Computes basis once and reuses it for all evaluations.
    
    Args:
        x_values: List of x values to evaluate
        precision: Decimal precision
    
    Returns:
        List of computed values
    
    Example:
        >>> values = batch_evaluate_closed_form([0.5, 0.25, -0.5], precision=100)
    """
    if precision is not None:
        old_dps = mp.dps
        mp.dps = precision
    
    try:
        # Compute basis once
        basis = compute_omega2_basis(precision=mp.dps)
        
        # Evaluate for each x
        results = []
        for x in x_values:
            value = S42_closed_form(x, basis=basis)
            results.append(value)
        
        return results
    
    finally:
        if precision is not None:
            mp.dps = old_dps


def compare_with_series(
    x: float,
    precision: int = 100,
    max_terms: int = 600000,
    verbose: bool = True
) -> dict:
    """
    Compare closed form with series evaluation.
    
    Args:
        x: The x value
        precision: Decimal precision
        max_terms: Maximum series terms
        verbose: Print comparison
    
    Returns:
        Dictionary with both values and error
    """
    from .series import S42_series
    import time
    
    mp.dps = precision
    
    # Evaluate with series
    t0 = time.time()
    series_val, n_terms = S42_series(x, max_terms=max_terms)
    series_time = time.time() - t0
    
    # Evaluate with closed form
    t0 = time.time()
    closed_val = S42_closed_form(x)
    closed_time = time.time() - t0
    
    # Compute error
    abs_error = abs(series_val - closed_val)
    rel_error = abs_error / abs(series_val) if series_val != 0 else 0
    
    if verbose:
        print(f"\nComparison for S₄,₂({x}) at {precision} decimal places:")
        print("=" * 70)
        print(f"Series value:      {series_val}")
        print(f"Closed form value: {closed_val}")
        print(f"\nAbsolute error:    {abs_error:.3e}")
        print(f"Relative error:    {rel_error:.3e}")
        print(f"\nSeries used {n_terms} terms in {series_time*1000:.3f} ms")
        print(f"Closed form evaluated in {closed_time*1000:.3f} ms")
        print(f"Speedup: {series_time/closed_time:.1f}×")
    
    return {
        "series_value": series_val,
        "closed_value": closed_val,
        "absolute_error": abs_error,
        "relative_error": rel_error,
        "series_terms": n_terms,
        "series_time": series_time,
        "closed_time": closed_time,
        "speedup": series_time / closed_time,
    }


def evaluate_with_basis_timing(
    x: float,
    precision: int = 100,
    verbose: bool = True
) -> dict:
    """
    Evaluate closed form with separate basis computation timing.
    
    This shows the amortized cost structure clearly.
    
    Args:
        x: The x value
        precision: Decimal precision
        verbose: Print timing breakdown
    
    Returns:
        Dictionary with timing information
    """
    import time
    
    mp.dps = precision
    
    # Time basis computation
    t0 = time.time()
    basis = compute_omega2_basis(precision=precision)
    basis_time = time.time() - t0
    
    # Time coefficient loading
    t0 = time.time()
    coeffs = get_coefficients_mpf(x, precision=precision)
    coeff_time = time.time() - t0
    
    # Time dot product
    t0 = time.time()
    result = mpf(0)
    for c, omega in zip(coeffs, basis):
        result += c * omega
    dot_time = time.time() - t0
    
    total_time = basis_time + coeff_time + dot_time
    
    if verbose:
        print(f"\nClosed-form timing breakdown for S₄,₂({x}) at {precision} dps:")
        print("=" * 70)
        print(f"Basis computation:  {basis_time*1000:8.3f} ms (one-time cost)")
        print(f"Coefficient load:   {coeff_time*1000:8.3f} ms (negligible)")
        print(f"Dot product:        {dot_time*1000:8.3f} ms (per-evaluation cost)")
        print(f"Total:              {total_time*1000:8.3f} ms")
        print(f"\nFor N evaluations: T_total = {basis_time*1000:.1f} + N × {dot_time*1000:.3f} ms")
    
    return {
        "basis_time": basis_time,
        "coefficient_time": coeff_time,
        "dot_product_time": dot_time,
        "total_time": total_time,
        "value": result,
    }


def compute_crossover_point(
    x: float,
    precision: int = 100,
    series_time: float = None,
    verbose: bool = True
) -> dict:
    """
    Compute the crossover point N* where closed form becomes faster.
    
    N* = T_basis / (T_series - T_dot)
    
    Args:
        x: The x value
        precision: Decimal precision
        series_time: Series evaluation time (will measure if not provided)
        verbose: Print analysis
    
    Returns:
        Dictionary with crossover analysis
    """
    import time
    from .series import S42_series
    
    mp.dps = precision
    
    # Measure series time if not provided
    if series_time is None:
        t0 = time.time()
        _, _ = S42_series(x)
        series_time = time.time() - t0
    
    # Measure closed form components
    timing = evaluate_with_basis_timing(x, precision, verbose=False)
    
    T_basis = timing["basis_time"]
    T_dot = timing["dot_product_time"]
    T_series = series_time
    
    # Compute crossover
    if T_series > T_dot:
        N_star = T_basis / (T_series - T_dot)
    else:
        N_star = float('inf')  # Closed form never faster
    
    if verbose:
        print(f"\nCrossover Analysis for S₄,₂({x}) at {precision} decimal places:")
        print("=" * 70)
        print(f"T_series  = {T_series*1000:8.3f} ms  (per evaluation)")
        print(f"T_basis   = {T_basis*1000:8.3f} ms  (one-time cost)")
        print(f"T_dot     = {T_dot*1000:8.3f} ms  (per evaluation)")
        print(f"\nCrossover point: N* = {N_star:.1f} evaluations")
        print(f"\nFor N < {N_star:.0f}: Use series (faster)")
        print(f"For N ≥ {N_star:.0f}: Use closed form (faster amortized)")
    
    return {
        "T_series": T_series,
        "T_basis": T_basis,
        "T_dot": T_dot,
        "N_star": N_star,
        "precision": precision,
    }


if __name__ == "__main__":
    # Demonstration
    print("S₄,₂(x) Closed-Form Evaluation Demo")
    print("=" * 70)
    
    # Basic evaluation
    print("\nBasic Evaluation:")
    for x_str, x_val in AVAILABLE_X_VALUES.items():
        mp.dps = 50
        value = evaluate_closed_form(float(x_val), precision=50)
        print(f"  S₄,₂({x_str:5s}) = {value}")
    
    # Comparison with series
    print("\n" + "=" * 70)
    compare_with_series(0.5, precision=100, verbose=True)
    
    # Timing breakdown
    print("\n" + "=" * 70)
    evaluate_with_basis_timing(0.5, precision=120, verbose=True)
    
    # Crossover analysis
    print("\n" + "=" * 70)
    compute_crossover_point(0.5, precision=120, verbose=True)

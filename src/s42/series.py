"""
S₄,₂(x) Series Evaluation
=========================

Direct evaluation of the Euler sum via series summation:

    S₄,₂(x) = Σ(n=1 to ∞) [H_{n-1} · x^n] / n^5

where H_n = Σ(k=1 to n) 1/k are the harmonic numbers.
"""

from mpmath import mp, mpf, fabs
from typing import Tuple, Optional
from .utils import harmonic, convergence_check


def S42_series(
    x,
    max_terms: int = 600000,
    convergence_threshold: float = None,
    convergence_window: int = 35,
    verbose: bool = False
) -> Tuple[mpf, int]:
    """
    Evaluate S₄,₂(x) via direct series summation.
    
    Args:
        x: The x value
        max_terms: Maximum number of terms (hard cutoff)
        convergence_threshold: Stop when |term| < threshold for convergence_window iterations
                             (default: 10^(-T) where T = mp.dps + 10)
        convergence_window: Number of consecutive small terms required
        verbose: Print convergence information
    
    Returns:
        Tuple of (value, num_terms_used)
    
    Example:
        >>> from mpmath import mp
        >>> mp.dps = 100
        >>> value, n_terms = S42_series(x=0.5)
        >>> print(f"Converged after {n_terms} terms")
    """
    x = mpf(x)
    
    # Set convergence threshold
    if convergence_threshold is None:
        convergence_threshold = mpf(10) ** (-(mp.dps + 10))
    
    # Initialize accumulation
    result = mpf(0)
    H = mpf(0)  # H_0 = 0
    consecutive_small = 0
    
    for n in range(1, max_terms + 1):
        # Compute nth term: H_{n-1} * x^n / n^5
        term = H * (x ** n) / (n ** 5)
        result += term
        
        # Update harmonic number: H_n = H_{n-1} + 1/n
        H += mpf(1) / mpf(n)
        
        # Check convergence
        if fabs(term) < convergence_threshold:
            consecutive_small += 1
            if consecutive_small >= convergence_window:
                if verbose:
                    print(f"Converged after {n} terms")
                    print(f"Final term magnitude: {fabs(term)}")
                return result, n
        else:
            consecutive_small = 0
        
        # Progress reporting for long computations
        if verbose and n % 10000 == 0:
            print(f"  n = {n:6d}, |term| = {fabs(term):.3e}, sum = {result}")
    
    # Reached max_terms without convergence
    if verbose:
        print(f"Warning: Reached max_terms = {max_terms} without convergence")
        print(f"Final term magnitude: {fabs(term)}")
    
    return result, max_terms


def evaluate_series(
    x: float,
    precision: int = None,
    max_terms: int = 600000,
    verbose: bool = False
) -> mpf:
    """
    Evaluate S₄,₂(x) with automatic precision handling.
    
    Args:
        x: The x value
        precision: Decimal precision (default: current mp.dps)
        max_terms: Maximum number of terms
        verbose: Print progress information
    
    Returns:
        The computed value of S₄,₂(x)
    """
    if precision is not None:
        old_dps = mp.dps
        mp.dps = precision
    
    try:
        value, n_terms = S42_series(x, max_terms=max_terms, verbose=verbose)
        return value
    finally:
        if precision is not None:
            mp.dps = old_dps


def estimate_terms_needed(x: float, target_precision: int) -> int:
    """
    Estimate number of terms needed for target precision.
    
    The nth term of S₄,₂(x) has magnitude approximately:
        |term_n| ≈ (log n + γ) · |x|^n / n^5
    
    We need |term_n| < 10^(-target_precision).
    
    Args:
        x: The x value
        target_precision: Target decimal precision
    
    Returns:
        Estimated number of terms
    """
    from math import log, exp
    
    x_abs = abs(x)
    
    if x_abs >= 1:
        return max_terms  # Series doesn't converge
    
    # Rough estimate: solve (log n) * x^n / n^5 < 10^(-p)
    # This is approximate - actual convergence can vary
    
    # For x = 1/2, empirically we need:
    #   50 digits  → ~50-100 terms
    #   100 digits → ~100-150 terms  
    #   200 digits → ~200-300 terms
    
    # Heuristic formula
    if x_abs <= 0.5:
        return int(target_precision * 1.5 + 50)
    elif x_abs <= 0.75:
        return int(target_precision * 3 + 100)
    else:
        return int(target_precision * 10 + 500)


def analyze_convergence(
    x: float,
    precision: int = 100,
    num_terms: int = 200
) -> dict:
    """
    Analyze convergence properties of the series.
    
    Args:
        x: The x value
        precision: Working precision
        num_terms: Number of terms to analyze
    
    Returns:
        Dictionary with convergence statistics
    """
    mp.dps = precision
    x = mpf(x)
    
    result = mpf(0)
    H = mpf(0)
    
    terms = []
    partial_sums = []
    
    for n in range(1, num_terms + 1):
        term = H * (x ** n) / (n ** 5)
        result += term
        
        terms.append(float(fabs(term)))
        partial_sums.append(float(result))
        
        H += mpf(1) / mpf(n)
    
    import numpy as np
    
    # Compute convergence rate
    log_terms = np.log10(np.array(terms) + 1e-100)
    
    # Find where terms drop below various thresholds
    thresholds = [1e-20, 1e-40, 1e-60, 1e-80, 1e-100]
    threshold_n = {}
    
    for thresh in thresholds:
        for i, t in enumerate(terms):
            if t < thresh:
                threshold_n[thresh] = i + 1
                break
    
    return {
        "terms": terms,
        "partial_sums": partial_sums,
        "final_value": partial_sums[-1],
        "final_term_magnitude": terms[-1],
        "threshold_crossings": threshold_n,
        "convergence_rate": {
            "mean": np.mean(np.diff(log_terms)),
            "std": np.std(np.diff(log_terms)),
        }
    }


def plot_convergence(x: float, precision: int = 100, num_terms: int = 200):
    """
    Plot convergence behavior.
    
    Requires matplotlib.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    stats = analyze_convergence(x, precision, num_terms)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot term magnitudes
    ax1.semilogy(range(1, num_terms + 1), stats["terms"])
    ax1.set_xlabel("Term number n")
    ax1.set_ylabel("|term_n|")
    ax1.set_title(f"Term Magnitude for S₄,₂({x})")
    ax1.grid(True, alpha=0.3)
    
    # Plot partial sums
    ax2.plot(range(1, num_terms + 1), stats["partial_sums"])
    ax2.set_xlabel("Number of terms")
    ax2.set_ylabel("Partial sum")
    ax2.set_title(f"Partial Sums for S₄,₂({x})")
    ax2.axhline(stats["final_value"], color='r', linestyle='--', 
                label=f"Final value: {stats['final_value']:.6f}")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    # Demonstration
    print("S₄,₂(x) Series Evaluation Demo")
    print("=" * 70)
    
    # Test at different precisions
    for prec in [50, 80, 100]:
        mp.dps = prec
        print(f"\nPrecision: {prec} decimal places")
        
        for x_val in [0.5, 0.25, -0.5]:
            value, n_terms = S42_series(x_val, verbose=False)
            print(f"  S₄,₂({x_val:5.2f}) = {value} (used {n_terms} terms)")
    
    # Convergence analysis
    print("\n" + "=" * 70)
    print("Convergence Analysis for x = 1/2")
    print("=" * 70)
    
    mp.dps = 100
    stats = analyze_convergence(0.5, precision=100, num_terms=150)
    
    print(f"\nFinal value: {stats['final_value']}")
    print(f"Final term magnitude: {stats['final_term_magnitude']:.3e}")
    
    print("\nTerms needed to reach threshold:")
    for thresh, n in sorted(stats['threshold_crossings'].items()):
        print(f"  |term| < {thresh:.0e}: n = {n}")

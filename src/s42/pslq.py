"""
PSLQ Verification
=================

Tools for verifying and discovering integer relations using the PSLQ algorithm.

PSLQ finds integer relations between real numbers, i.e., given x₁, ..., x_n,
finds integers a₁, ..., a_n such that Σ a_i x_i ≈ 0.
"""

from mpmath import mp, mpf, sqrt, fabs
from typing import List, Tuple, Optional
import numpy as np


def verify_pslq_identity(
    x: float,
    precision: int = 200,
    residual_threshold: float = 1e-96,
    verbose: bool = True
) -> Tuple[mpf, List]:
    """
    Verify the PSLQ-discovered identity for S₄,₂(x).
    
    Computes:
        residual = |S₄,₂(x) - Σ c_j ω_j|
    
    Args:
        x: The x value
        precision: Working precision
        residual_threshold: Expected residual threshold
        verbose: Print verification details
    
    Returns:
        Tuple of (residual, coefficients)
    
    Example:
        >>> residual, coeffs = verify_pslq_identity(x=0.5, precision=200)
        >>> print(f"Residual: {residual}")
    """
    from .series import S42_series
    from .closed_form import S42_closed_form
    from .basis import compute_omega2_basis
    from .coefficients import get_coefficients, get_coefficients_mpf
    
    mp.dps = precision
    
    # Compute target value via series
    if verbose:
        print(f"\nVerifying PSLQ identity for S₄,₂({x}) at {precision} decimal places")
        print("=" * 70)
        print("Computing target value via series...")
    
    target_value, n_terms = S42_series(x, max_terms=600000, verbose=False)
    
    if verbose:
        print(f"  Used {n_terms} terms")
        print(f"  Target value: {target_value}")
    
    # Compute basis
    if verbose:
        print("\nComputing Ω₂ basis...")
    
    basis = compute_omega2_basis(precision=precision)
    
    # Get coefficients
    coeffs = get_coefficients(x)
    coeffs_mpf = get_coefficients_mpf(x, precision=precision)
    
    if verbose:
        print(f"  Using {len(coeffs)} basis elements")
    
    # Compute closed form
    closed_value = mpf(0)
    for c, omega in zip(coeffs_mpf, basis):
        closed_value += c * omega
    
    # Compute residual
    residual = fabs(target_value - closed_value)
    
    if verbose:
        print(f"\nClosed form value: {closed_value}")
        print(f"Residual: {residual:.3e}")
        
        if residual < residual_threshold:
            print(f"✓ Residual < {residual_threshold:.0e}: PASS")
        else:
            print(f"✗ Residual ≥ {residual_threshold:.0e}: FAIL")
    
    return residual, coeffs


def find_pslq_relation(
    target: mpf,
    basis: List[mpf],
    precision: int = 200,
    max_coefficient: int = 10000,
    verbose: bool = True
) -> Optional[List[int]]:
    """
    Use PSLQ to find an integer relation.
    
    Finds integers a₀, a₁, ..., a_n such that:
        a₀ · target + a₁ · basis[0] + ... + a_n · basis[n-1] ≈ 0
    
    Then extracts coefficients: basis[i] coefficient = -a_{i+1} / a_0
    
    Args:
        target: The target value
        basis: List of basis constants
        precision: Working precision
        max_coefficient: Maximum allowed coefficient magnitude
        verbose: Print search progress
    
    Returns:
        List of coefficients [c_1, ..., c_n] or None if no relation found
    
    Note:
        Requires high precision (200+ digits) for reliable results.
    """
    mp.dps = precision
    
    # Construct input vector: [target, basis[0], basis[1], ...]
    x = [target] + list(basis)
    
    if verbose:
        print(f"\nSearching for PSLQ relation with {len(x)} elements")
        print(f"Working precision: {precision} decimal places")
        print(f"Max coefficient: ±{max_coefficient}")
    
    try:
        # Run PSLQ
        relation = mp.pslq(x, maxcoeff=max_coefficient, maxsteps=10000)
        
        if relation is None:
            if verbose:
                print("  No relation found")
            return None
        
        # Check if first coefficient is nonzero
        if relation[0] == 0:
            if verbose:
                print("  Degenerate relation (first coefficient is zero)")
            return None
        
        # Extract coefficients: c_i = -relation[i+1] / relation[0]
        coeffs = []
        for i in range(1, len(relation)):
            c = -relation[i] / relation[0]
            coeffs.append(c)
        
        # Compute residual
        test_val = mpf(0)
        for c, b in zip(coeffs, basis):
            test_val += c * b
        
        residual = fabs(target - test_val)
        
        if verbose:
            print(f"\n  Found relation:")
            print(f"  Residual: {residual:.3e}")
            print(f"  Coefficient range: [{min(coeffs):.3f}, {max(coeffs):.3f}]")
        
        return coeffs
    
    except Exception as e:
        if verbose:
            print(f"  PSLQ error: {e}")
        return None


def analyze_pslq_stability(
    x: float,
    precisions: List[int] = None,
    verbose: bool = True
) -> dict:
    """
    Analyze how PSLQ residual varies with precision.
    
    This helps verify that the identity is genuinely exact
    (residual should decay exponentially with precision).
    
    Args:
        x: The x value
        precisions: List of precisions to test
        verbose: Print analysis
    
    Returns:
        Dictionary with residuals at each precision
    """
    if precisions is None:
        precisions = [100, 150, 200, 250, 300]
    
    results = {}
    
    for prec in precisions:
        residual, _ = verify_pslq_identity(x, precision=prec, verbose=False)
        results[prec] = float(residual)
        
        if verbose:
            print(f"  Precision {prec:3d}: residual = {residual:.3e}")
    
    # Check if residual decays exponentially
    import numpy as np
    log_residuals = np.log10([r for r in results.values() if r > 0])
    
    if len(log_residuals) > 1:
        # Fit linear trend in log space
        x_vals = np.array([p for p, r in results.items() if r > 0])
        slope = np.polyfit(x_vals, log_residuals, 1)[0]
        
        if verbose:
            print(f"\nResidual decay rate: ~10^({slope:.3f} × precision)")
            if slope < -0.5:
                print("  ✓ Exponential decay suggests genuine identity")
            else:
                print("  ⚠ Slow decay - may not be exact")
    
    return results


def coefficient_numerator_denominator_bounds(coeffs: List) -> dict:
    """
    Analyze numerator and denominator sizes in coefficient list.
    
    Args:
        coeffs: List of Fraction coefficients
    
    Returns:
        Dictionary with statistics
    """
    from fractions import Fraction
    
    numerators = [abs(c.numerator) for c in coeffs]
    denominators = [c.denominator for c in coeffs]
    
    return {
        "max_numerator": max(numerators),
        "max_denominator": max(denominators),
        "min_numerator": min(numerators),
        "min_denominator": min(denominators),
        "mean_numerator": sum(numerators) / len(numerators),
        "mean_denominator": sum(denominators) / len(denominators),
    }


if __name__ == "__main__":
    # Demonstration
    print("PSLQ Verification Demo")
    print("=" * 70)
    
    # Verify identity for x = 1/2
    print("\nVerification for x = 1/2:")
    residual, coeffs = verify_pslq_identity(x=0.5, precision=200, verbose=True)
    
    # Analyze coefficient sizes
    from .coefficients import get_coefficients
    coeffs_exact = get_coefficients(0.5)
    bounds = coefficient_numerator_denominator_bounds(coeffs_exact)
    
    print("\nCoefficient size analysis:")
    print(f"  Max numerator: {bounds['max_numerator']}")
    print(f"  Max denominator: {bounds['max_denominator']}")
    
    # Stability analysis
    print("\n" + "=" * 70)
    print("PSLQ Stability Analysis:")
    analyze_pslq_stability(0.5, precisions=[100, 150, 200, 250], verbose=True)

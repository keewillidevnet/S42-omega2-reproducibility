"""
Exact Rational Coefficients for S₄,₂(x) Identities
===================================================

This module contains the PSLQ-discovered exact rational coefficients for
S₄,₂(x) at x ∈ {1/2, 1/4, -1/2} in the canonical 21-element Ω₂ basis.

All coefficients are exact rationals certified with PSLQ residuals < 10^-96.
"""

from fractions import Fraction
from typing import Dict, List, Tuple
from mpmath import mp, mpf

# Available x values with exact identities
AVAILABLE_X_VALUES = {
    "1/2": mpf("0.5"),
    "1/4": mpf("0.25"),
    "-1/2": mpf("-0.5"),
}

# Exact rational coefficients from PSLQ
# Order corresponds to Ω₂ basis: ω₁, ω₂, ..., ω₂₁

COEFFICIENTS_HALF = [
    Fraction(15683, 14280),    # ω₁:  ζ(6)
    Fraction(-5743, 14280),    # ω₂:  ζ(3)²
    Fraction(-1593, 4760),     # ω₃:  ζ(5)log2
    Fraction(-34213, 14280),   # ω₄:  ζ(3)log³2
    Fraction(-653, 357),       # ω₅:  π⁴log²2
    Fraction(107, 7140),       # ω₆:  π²log⁴2
    Fraction(933, 595),        # ω₇:  log⁶2
    Fraction(-4129, 14280),    # ω₈:  Li₆(1/2)
    Fraction(-5221, 4760),     # ω₉:  Li₆(1/4)
    Fraction(457, 595),        # ω₁₀: Li₅(1/2)log2
    Fraction(457, 595),        # ω₁₁: Li₅(1/4)log2
    Fraction(-1868, 1785),     # ω₁₂: Li₄(1/2)log²2
    Fraction(291, 476),        # ω₁₃: Li₄(1/4)log²2
    Fraction(-911, 408),       # ω₁₄: π²Li₄(1/2)
    Fraction(167, 7140),       # ω₁₅: π²Li₄(1/4)
    Fraction(-619, 408),       # ω₁₆: Cl₆(π/3)
    Fraction(-3869, 3570),     # ω₁₇: π²Cl₄(π/3)
    Fraction(15359, 14280),    # ω₁₈: π⁴Cl₂(π/3)
    Fraction(1007, 2856),      # ω₁₉: π²Cl₂(π/3)²
    Fraction(-7613, 7140),     # ω₂₀: Cl₂(π/3)³
    Fraction(-141, 2380),      # ω₂₁: 1
]

COEFFICIENTS_QUARTER = [
    Fraction(6037, 23939),     # ω₁:  ζ(6)
    Fraction(540, 23939),      # ω₂:  ζ(3)²
    Fraction(-9470, 23939),    # ω₃:  ζ(5)log2
    Fraction(16159, 23939),    # ω₄:  ζ(3)log³2
    Fraction(-24385, 23939),   # ω₅:  π⁴log²2
    Fraction(18371, 23939),    # ω₆:  π²log⁴2
    Fraction(20947, 23939),    # ω₇:  log⁶2
    Fraction(1027, 23939),     # ω₈:  Li₆(1/2)
    Fraction(-8180, 23939),    # ω₉:  Li₆(1/4)
    Fraction(-39717, 23939),   # ω₁₀: Li₅(1/2)log2
    Fraction(565, 23939),      # ω₁₁: Li₅(1/4)log2
    Fraction(13069, 23939),    # ω₁₂: Li₄(1/2)log²2
    Fraction(-6410, 23939),    # ω₁₃: Li₄(1/4)log²2
    Fraction(22392, 23939),    # ω₁₄: π²Li₄(1/2)
    Fraction(-55113, 23939),   # ω₁₅: π²Li₄(1/4)
    Fraction(9961, 23939),     # ω₁₆: Cl₆(π/3)
    Fraction(3040, 23939),     # ω₁₇: π²Cl₄(π/3)
    Fraction(391, 647),        # ω₁₈: π⁴Cl₂(π/3)
    Fraction(-29476, 23939),   # ω₁₉: π²Cl₂(π/3)²
    Fraction(-31660, 23939),   # ω₂₀: Cl₂(π/3)³
    Fraction(-6389, 23939),    # ω₂₁: 1
]

COEFFICIENTS_NEG_HALF = [
    Fraction(2879, 58060),     # ω₁:  ζ(6)
    Fraction(139667, 116120),  # ω₂:  ζ(3)²
    Fraction(-44803, 116120),  # ω₃:  ζ(5)log2
    Fraction(-20309, 29030),   # ω₄:  ζ(3)log³2
    Fraction(5495, 23224),     # ω₅:  π⁴log²2
    Fraction(-31603, 58060),   # ω₆:  π²log⁴2
    Fraction(-112611, 116120), # ω₇:  log⁶2
    Fraction(5441, 29030),     # ω₈:  Li₆(1/2)
    Fraction(9087, 116120),    # ω₉:  Li₆(1/4)
    Fraction(-8581, 116120),   # ω₁₀: Li₅(1/2)log2
    Fraction(46081, 116120),   # ω₁₁: Li₅(1/4)log2
    Fraction(-26413, 58060),   # ω₁₂: Li₄(1/2)log²2
    Fraction(-61269, 116120),  # ω₁₃: Li₄(1/4)log²2
    Fraction(57493, 58060),    # ω₁₄: π²Li₄(1/2)
    Fraction(-14287, 11612),   # ω₁₅: π²Li₄(1/4)
    Fraction(-47941, 116120),  # ω₁₆: Cl₆(π/3)
    Fraction(-9771, 29030),    # ω₁₇: π²Cl₄(π/3)
    Fraction(4109, 58060),     # ω₁₈: π⁴Cl₂(π/3)
    Fraction(-83559, 58060),   # ω₁₉: π²Cl₂(π/3)²
    Fraction(-6695, 23224),    # ω₂₀: Cl₂(π/3)³
    Fraction(-181073, 116120), # ω₂₁: 1
]

# Coefficient dictionary
COEFFICIENTS_DICT = {
    "1/2": COEFFICIENTS_HALF,
    "1/4": COEFFICIENTS_QUARTER,
    "-1/2": COEFFICIENTS_NEG_HALF,
}


def get_coefficients(x: float) -> List[Fraction]:
    """
    Get exact rational coefficients for S₄,₂(x).
    
    Args:
        x: The x value (must be in {1/2, 1/4, -1/2})
    
    Returns:
        List of 21 Fraction objects representing exact coefficients
    
    Raises:
        ValueError: If x is not one of the supported values
    
    Example:
        >>> coeffs = get_coefficients(0.5)
        >>> print(coeffs[0])  # First coefficient (ζ(6))
        15683/14280
    """
    # Convert float to string key
    if abs(x - 0.5) < 1e-10:
        key = "1/2"
    elif abs(x - 0.25) < 1e-10:
        key = "1/4"
    elif abs(x + 0.5) < 1e-10:
        key = "-1/2"
    else:
        raise ValueError(
            f"No exact identity known for x={x}. "
            f"Available values: {list(AVAILABLE_X_VALUES.keys())}"
        )
    
    return COEFFICIENTS_DICT[key]


def get_coefficients_mpf(x: float, precision: int = None) -> List:
    """
    Get coefficients as mpmath mpf objects at specified precision.
    
    Args:
        x: The x value
        precision: Decimal precision (default: current mp.dps)
    
    Returns:
        List of mpf coefficient values
    """
    if precision is not None:
        old_dps = mp.dps
        mp.dps = precision
    
    try:
        coeffs = get_coefficients(x)
        result = [mpf(c.numerator) / mpf(c.denominator) for c in coeffs]
        return result
    finally:
        if precision is not None:
            mp.dps = old_dps


def print_coefficients(x: float, format_type: str = "fraction") -> None:
    """
    Pretty-print coefficients for S₄,₂(x).
    
    Args:
        x: The x value
        format_type: "fraction" or "decimal"
    """
    from .basis import OMEGA2_BASIS_NAMES
    
    coeffs = get_coefficients(x)
    
    print(f"\nCoefficients for S₄,₂({x}):")
    print("=" * 60)
    
    for i, (coeff, name) in enumerate(zip(coeffs, OMEGA2_BASIS_NAMES), 1):
        if format_type == "fraction":
            print(f"ω_{i:2d} ({name:20s}): {coeff}")
        else:
            decimal = float(coeff)
            print(f"ω_{i:2d} ({name:20s}): {decimal:+.6f}")


def analyze_coefficient_patterns(x: float) -> Dict[str, any]:
    """
    Analyze interesting patterns in the coefficients.
    
    Returns dictionary with:
    - denominators: List of unique denominators
    - denominator_counts: Frequency of each denominator
    - signs: Distribution of positive/negative coefficients
    - magnitudes: Min, max, mean, std of absolute values
    """
    import numpy as np
    from collections import Counter
    
    coeffs = get_coefficients(x)
    
    # Denominators
    denominators = [c.denominator for c in coeffs]
    denominator_counts = Counter(denominators)
    
    # Signs
    positive = sum(1 for c in coeffs if c > 0)
    negative = sum(1 for c in coeffs if c < 0)
    zero = sum(1 for c in coeffs if c == 0)
    
    # Magnitudes
    magnitudes = [abs(float(c)) for c in coeffs]
    
    return {
        "denominators": sorted(set(denominators)),
        "denominator_counts": dict(denominator_counts),
        "most_common_denominator": denominator_counts.most_common(1)[0],
        "signs": {"positive": positive, "negative": negative, "zero": zero},
        "magnitudes": {
            "min": min(magnitudes),
            "max": max(magnitudes),
            "mean": np.mean(magnitudes),
            "std": np.std(magnitudes),
        },
        "repeated_coefficients": [
            (i, j, coeffs[i]) 
            for i in range(len(coeffs)) 
            for j in range(i+1, len(coeffs)) 
            if coeffs[i] == coeffs[j]
        ],
    }


if __name__ == "__main__":
    # Print coefficient analysis for all x values
    for x_str, x_val in AVAILABLE_X_VALUES.items():
        print(f"\n{'='*60}")
        print(f"Analysis for x = {x_str}")
        print(f"{'='*60}")
        
        print_coefficients(float(x_val), format_type="fraction")
        
        patterns = analyze_coefficient_patterns(float(x_val))
        print(f"\nDenominator patterns:")
        print(f"  Unique denominators: {patterns['denominators']}")
        print(f"  Most common: {patterns['most_common_denominator']}")
        
        print(f"\nSign distribution:")
        print(f"  Positive: {patterns['signs']['positive']}")
        print(f"  Negative: {patterns['signs']['negative']}")
        
        print(f"\nMagnitude statistics:")
        print(f"  Range: [{patterns['magnitudes']['min']:.3f}, {patterns['magnitudes']['max']:.3f}]")
        print(f"  Mean: {patterns['magnitudes']['mean']:.3f}")
        print(f"  Std:  {patterns['magnitudes']['std']:.3f}")
        
        if patterns['repeated_coefficients']:
            print(f"\nRepeated coefficients:")
            for i, j, val in patterns['repeated_coefficients']:
                print(f"  ω_{i+1} = ω_{j+1} = {val}")

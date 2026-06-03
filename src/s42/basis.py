"""
Corrected bases for S_{4,2}(x) at dyadic arguments.

This module supersedes the withdrawn v1 21-element ``Omega2`` basis.  The old
basis included level-6 Clausen constants at pi/3 and omitted the unique
irreducible depth-2 generator of the weight-6 level-2 space.  The corrected
closed form for S_{4,2}(1/2) uses the 13-element dyadic basis below.

For x=1/4 the revised result is a certified exact relation in a depth-2
multiple-polylogarithm basis.  It is intentionally not labeled as a reduction to
independently known constants because it contains unreduced depth-2 MPLs,
including Li_{5,1}(-1/2) = S_{4,2}(-1/2), whose closed form remains open.
"""

from __future__ import annotations

from typing import Dict, List
from mpmath import mp, mpf

DYADIC_W6_BASIS_NAMES = [
    "zeta(6)",
    "zeta(3)^2",
    "zeta(5)*log2",
    "zeta(3)*log2^3",
    "pi^2*zeta(3)*log2",
    "pi^4*log2^2",
    "pi^2*log2^4",
    "log2^6",
    "Li6(1/2)",
    "Li5(1/2)*log2",
    "Li4(1/2)*log2^2",
    "pi^2*Li4(1/2)",
    "S42(-1)",
]

QUARTER_RELATION_BASIS_NAMES = [
    "zeta(3)^2",
    "zeta(3)*log2^3",
    "pi^2*zeta(3)*log2",
    "pi^4*log2^2",
    "pi^2*log2^4",
    "log2^6",
    "Li3(-1/2)*log2^3",
    "pi^2*Li3(-1/2)*log2",
    "zeta(3)*Li3(-1/2)",
    "Li_{3,3}(-1/2)",
    "Li_{4,2}(-1/2)",
    "Li_{5,1}(-1/2)",
    "Li_{3,3}(1/4)",
    "Li_{4,2}(1/4)",
]

# Backward-compatible alias used by older scripts.  It now points to the
# corrected 13-element dyadic basis, not the withdrawn 21-element v1 basis.
OMEGA2_BASIS_NAMES = DYADIC_W6_BASIS_NAMES


def Li_ab(a: int, b: int, z, precision: int | None = None) -> mpf:
    """Evaluate Li_{a,b}(z,1) = sum_{m>n>=1} z^m/(m^a n^b).

    For the dyadic arguments used here, |z| <= 1/2, so direct summation is
    geometrically convergent and does not require a computer-algebra system.
    """
    if precision is None:
        precision = mp.dps
    z = mpf(z)
    az = abs(z)
    if az >= 1:
        raise ValueError("Li_ab direct evaluator is intended for |z| < 1")

    with mp.workdps(precision + 20):
        n_terms = 8
        tail_target = mpf(10) ** (-(precision + 12))
        while az ** (n_terms + 1) / (1 - az) > tail_target:
            n_terms = int(n_terms * 1.4) + 1

        total = mpf(0)
        harmonic_b = mpf(0)
        z_power = mpf(1)
        for m in range(1, n_terms + 1):
            z_power *= z
            total += z_power * harmonic_b / mpf(m) ** a
            harmonic_b += mpf(1) / mpf(m) ** b
        return +total


def _s42_alt_irreducible(precision: int) -> mpf:
    """Compute S_{4,2}(-1), the canonical depth-2 irreducible generator.

    This boundary value is not geometrically convergent, so we use mpmath's
    alternating-series summation with harmonic numbers.
    """
    with mp.workdps(precision + 20):
        n_cache = int(1.7 * (precision + 20)) + 80
        harmonic = [mpf(0)] * (n_cache + 2)
        h = mpf(0)
        for n in range(1, n_cache + 2):
            harmonic[n] = h
            h += mpf(1) / n

        def term(n):
            n = int(n)
            h_prev = harmonic[n] if n <= n_cache else (mp.psi(0, n) + mp.euler)
            return (-1) ** n * h_prev / mp.power(n, 5)

        return +mp.nsum(term, [1, mp.inf])


def compute_dyadic_w6_basis(precision: int | None = None) -> List[mpf]:
    """Compute the corrected 13-element weight-6 level-2 dyadic basis."""
    if precision is None:
        precision = mp.dps
    with mp.workdps(precision + 20):
        log2 = mp.log(2)
        half = mpf(1) / 2
        return [
            mp.zeta(6),
            mp.zeta(3) ** 2,
            mp.zeta(5) * log2,
            mp.zeta(3) * log2 ** 3,
            mp.pi ** 2 * mp.zeta(3) * log2,
            mp.pi ** 4 * log2 ** 2,
            mp.pi ** 2 * log2 ** 4,
            log2 ** 6,
            mp.polylog(6, half),
            mp.polylog(5, half) * log2,
            mp.polylog(4, half) * log2 ** 2,
            mp.pi ** 2 * mp.polylog(4, half),
            _s42_alt_irreducible(precision),
        ]


def compute_quarter_relation_basis(precision: int | None = None) -> List[mpf]:
    """Compute the basis for the certified S_{4,2}(1/4) depth-2 relation."""
    if precision is None:
        precision = mp.dps
    with mp.workdps(precision + 20):
        log2 = mp.log(2)
        li3m = mp.polylog(3, mpf(-1) / 2)
        return [
            mp.zeta(3) ** 2,
            mp.zeta(3) * log2 ** 3,
            mp.pi ** 2 * mp.zeta(3) * log2,
            mp.pi ** 4 * log2 ** 2,
            mp.pi ** 2 * log2 ** 4,
            log2 ** 6,
            li3m * log2 ** 3,
            mp.pi ** 2 * li3m * log2,
            mp.zeta(3) * li3m,
            Li_ab(3, 3, mpf(-1) / 2, precision),
            Li_ab(4, 2, mpf(-1) / 2, precision),
            Li_ab(5, 1, mpf(-1) / 2, precision),
            Li_ab(3, 3, mpf(1) / 4, precision),
            Li_ab(4, 2, mpf(1) / 4, precision),
        ]


def compute_basis_for_x(x: float, precision: int | None = None) -> List[mpf]:
    """Return the appropriate corrected basis/relation basis for x."""
    if abs(float(x) - 0.5) < 1e-12:
        return compute_dyadic_w6_basis(precision)
    if abs(float(x) - 0.25) < 1e-12:
        return compute_quarter_relation_basis(precision)
    raise ValueError(
        "No certified closed-form/relation basis is implemented for this x. "
        "S_{4,2}(-1/2) remains open in the revised manuscript."
    )


def compute_basis_dict_for_x(x: float, precision: int | None = None) -> Dict[str, mpf]:
    names = DYADIC_W6_BASIS_NAMES if abs(float(x) - 0.5) < 1e-12 else QUARTER_RELATION_BASIS_NAMES
    return dict(zip(names, compute_basis_for_x(x, precision)))


def compute_omega2_basis(precision: int | None = None) -> List[mpf]:
    """Backward-compatible alias for the corrected 13-element dyadic basis."""
    return compute_dyadic_w6_basis(precision)


def compute_omega2_basis_dict(precision: int | None = None) -> Dict[str, mpf]:
    return dict(zip(DYADIC_W6_BASIS_NAMES, compute_dyadic_w6_basis(precision)))

"""Corrected S_{4,2}(x) evaluation helpers.

Terminology matters in the corrected revision:
- S_{4,2}(1/2) has an exact closed form in a corrected 13-element dyadic basis.
- S_{4,2}(1/4) has a certified exact relation in a depth-2 MPL basis, not a
  reduction to independently known constants.
- S_{4,2}(-1/2) remains open and is not implemented as a closed form.
"""

from __future__ import annotations

from typing import List, Optional
from mpmath import mp, mpf

from .basis import compute_basis_for_x
from .coefficients import get_coefficients_mpf, get_relation_status


def evaluate_relation(
    x: float,
    basis: Optional[List[mpf]] = None,
    coeffs: Optional[List[mpf]] = None,
    precision: int | None = None,
) -> mpf:
    """Evaluate the implemented corrected closed form/relation by dot product."""
    if precision is not None:
        old_dps = mp.dps
        mp.dps = precision
    else:
        old_dps = None

    try:
        if basis is None:
            basis = compute_basis_for_x(x, precision=mp.dps)
        if coeffs is None:
            coeffs = get_coefficients_mpf(x, precision=mp.dps)
        if len(basis) != len(coeffs):
            raise ValueError(f"Basis length {len(basis)} does not match coefficient length {len(coeffs)}")
        return mp.fsum(c * b for c, b in zip(coeffs, basis))
    finally:
        if old_dps is not None:
            mp.dps = old_dps


def S42_closed_form(x: float, *args, **kwargs) -> mpf:
    """Backward-compatible wrapper.

    This name is exact terminology only for x=1/2. For x=1/4 it evaluates the
    certified depth-2 relation. For x=-1/2 it raises because the value is open.
    """
    return evaluate_relation(x, *args, **kwargs)


def evaluate_closed_form(x: float, precision: int | None = None, precompute_basis: bool = True) -> mpf:
    basis = compute_basis_for_x(x, precision=precision) if precompute_basis else None
    return evaluate_relation(x, basis=basis, precision=precision)


def batch_evaluate_closed_form(x_values: List[float], precision: int | None = None) -> List[mpf]:
    return [evaluate_closed_form(x, precision=precision) for x in x_values]


def compare_with_series(x: float, precision: int = 100, max_terms: int = 600000, verbose: bool = True) -> dict:
    from .series import S42_series
    import time

    mp.dps = precision
    t0 = time.time(); series_val, n_terms = S42_series(x, max_terms=max_terms); series_time = time.time() - t0
    t0 = time.time(); relation_val = evaluate_relation(x); relation_time = time.time() - t0
    abs_error = abs(series_val - relation_val)
    rel_error = abs_error / abs(series_val) if series_val != 0 else mpf(0)

    if verbose:
        print(f"\nComparison for S_{{4,2}}({x}) at {precision} decimal places")
        print("=" * 72)
        print(f"Status:          {get_relation_status(x)}")
        print(f"Series value:    {series_val}")
        print(f"Relation value:  {relation_val}")
        print(f"Absolute error:  {mp.nstr(abs_error, 8)}")
        print(f"Relative error:  {mp.nstr(rel_error, 8)}")
        print(f"Series terms/time: {n_terms} terms / {series_time*1000:.3f} ms")
        print(f"Relation time:     {relation_time*1000:.3f} ms")

    return {
        "series_value": series_val,
        "relation_value": relation_val,
        "absolute_error": abs_error,
        "relative_error": rel_error,
        "series_terms": n_terms,
        "series_time": series_time,
        "relation_time": relation_time,
        "status": get_relation_status(x),
    }


def evaluate_with_basis_timing(x: float, precision: int = 100, verbose: bool = True) -> dict:
    import time
    mp.dps = precision
    t0 = time.time(); basis = compute_basis_for_x(x, precision=precision); basis_time = time.time() - t0
    t0 = time.time(); coeffs = get_coefficients_mpf(x, precision=precision); coeff_time = time.time() - t0
    t0 = time.time(); value = mp.fsum(c * b for c, b in zip(coeffs, basis)); dot_time = time.time() - t0
    if verbose:
        print(f"\nCorrected relation timing for S_{{4,2}}({x}) at {precision} dps")
        print("=" * 72)
        print(f"Status:            {get_relation_status(x)}")
        print(f"Basis computation: {basis_time*1000:8.3f} ms")
        print(f"Coefficient load:  {coeff_time*1000:8.3f} ms")
        print(f"Dot product:       {dot_time*1000:8.3f} ms")
    return {"basis_time": basis_time, "coefficient_time": coeff_time, "dot_product_time": dot_time, "value": value}

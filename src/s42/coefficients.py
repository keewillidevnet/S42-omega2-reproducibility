"""Certified coefficients for the corrected S_{4,2} revision.

Implemented statuses:
- x = 1/2: corrected exact closed form in the 13-element dyadic weight-6 basis.
- x = 1/4: certified exact relation in a depth-2 MPL basis; not a reduction to
  independently known constants.
- x = -1/2: open; no exact closed form is implemented.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Dict, List
from mpmath import mp, mpf

AVAILABLE_X_VALUES = {
    "1/2": mpf("0.5"),
    "1/4": mpf("0.25"),
}

OPEN_X_VALUES = {"-1/2": mpf("-0.5")}

S42_HALF_EXACT_COEFFS = [
    Fraction(-51, 32),
    Fraction(-1, 4),
    Fraction(-1, 32),
    Fraction(-1, 6),
    Fraction(1, 12),
    Fraction(1, 1440),
    Fraction(1, 144),
    Fraction(-1, 240),
    Fraction(2, 1),
    Fraction(1, 1),
    Fraction(0, 1),
    Fraction(0, 1),
    Fraction(-1, 2),
]

S42_QUARTER_RELATION_COEFFS = [
    Fraction(49, 48),
    Fraction(7, 18),
    Fraction(-7, 36),
    Fraction(1, 108),
    Fraction(-1, 27),
    Fraction(1, 27),
    Fraction(4, 9),
    Fraction(-2, 9),
    Fraction(7, 3),
    Fraction(8, 3),
    Fraction(8, 1),
    Fraction(16, 1),
    Fraction(-1, 6),
    Fraction(-1, 2),
]

COEFFICIENTS_DICT: Dict[str, List[Fraction]] = {
    "1/2": S42_HALF_EXACT_COEFFS,
    "1/4": S42_QUARTER_RELATION_COEFFS,
}

RELATION_STATUS = {
    "1/2": "corrected exact closed form in the 13-element dyadic basis",
    "1/4": "certified exact relation in a depth-2 MPL basis, not a reduction to independently known constants",
    "-1/2": "open; no certified closed form implemented",
}


def x_to_key(x: float) -> str:
    if abs(float(x) - 0.5) < 1e-12:
        return "1/2"
    if abs(float(x) - 0.25) < 1e-12:
        return "1/4"
    if abs(float(x) + 0.5) < 1e-12:
        return "-1/2"
    raise ValueError("Supported revised arguments are 1/2 and 1/4; -1/2 is open.")


def get_coefficients(x: float) -> List[Fraction]:
    key = x_to_key(x)
    if key == "-1/2":
        raise ValueError("S_{4,2}(-1/2) remains open in the revised manuscript; no coefficients are provided.")
    return COEFFICIENTS_DICT[key]


def get_coefficients_mpf(x: float, precision: int | None = None) -> List[mpf]:
    if precision is not None:
        old_dps = mp.dps
        mp.dps = precision
    else:
        old_dps = None
    try:
        return [mpf(c.numerator) / mpf(c.denominator) for c in get_coefficients(x)]
    finally:
        if old_dps is not None:
            mp.dps = old_dps


def get_relation_status(x: float) -> str:
    return RELATION_STATUS[x_to_key(x)]

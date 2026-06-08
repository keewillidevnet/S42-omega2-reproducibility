"""Public regression tests for the corrected S42 revision.

These exercise only the public ``s42`` package and have no dependency on any
private package. They mirror the verification example in the README.
"""

import pytest
from mpmath import mp, mpf

from s42 import evaluate_series, evaluate_relation, get_relation_status


def test_half_relation_matches_series():
    """x = 1/2: corrected exact closed form should match the series to the floor."""
    mp.dps = 80
    diff = abs(evaluate_series(0.5) - evaluate_relation(0.5))
    assert diff < mpf(10) ** -70


def test_quarter_relation_matches_series():
    """x = 1/4: certified relation should match the series to the floor."""
    mp.dps = 80
    diff = abs(evaluate_series(0.25) - evaluate_relation(0.25))
    assert diff < mpf(10) ** -70


def test_half_status_is_closed_form():
    assert "closed form" in get_relation_status(0.5).lower()


def test_quarter_status_is_relation():
    assert "relation" in get_relation_status(0.25).lower()


def test_minus_half_is_open():
    """x = -1/2 is open and must not return a value."""
    with pytest.raises(ValueError):
        evaluate_relation(-0.5)

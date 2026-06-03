"""S4,2(1/2) regression and an exactness probe.

The published coefficients reproduce S4,2(1/2) to about 98 digits, then the
residual plateaus. So we assert agreement to ~95 digits (true), and SEPARATELY
assert that the strict certifier does NOT accept them as exact, because the
residual does not fall to the precision floor. See FINDINGS.md.
"""
from fractions import Fraction as F
import mpmath as mp
from reduction_engine.kernels import EulerSumS42
from reduction_engine.bases import build_omega2, OMEGA2_LABELS
from reduction_engine.certify import certify

from reduction_engine.reference import S42_HALF_COEFFS as COEFFS_HALF


def test_s42_half_agrees_to_95_digits():
    dps = 130
    mp.mp.dps = dps + 10
    value = EulerSumS42().evaluate(mp.mpf(1) / 2, dps)
    basis = build_omega2(dps)
    closed = sum(mp.mpf(c.numerator) / c.denominator * w
                 for c, w in zip(COEFFS_HALF, basis))
    assert abs(value - closed) < mp.mpf(10) ** (-95)


def test_s42_half_is_NOT_certified_exact():
    cert = certify(EulerSumS42(), mp.mpf(1) / 2, COEFFS_HALF,
                   build_omega2, OMEGA2_LABELS, check_dps=240)
    assert not cert.accepted        # residual plateaus near 1e-98
    assert not cert.near_floor

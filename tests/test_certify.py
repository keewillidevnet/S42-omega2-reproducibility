"""The certifier accepts a genuinely exact identity and rejects an approximate
or perturbed one."""
from fractions import Fraction as F
import mpmath as mp
from reduction_engine.kernels.base import Kernel
from reduction_engine.bases import build_omega2, OMEGA2_LABELS
from reduction_engine.certify import certify
from reduction_engine.reference import S42_HALF_COEFFS as COEFFS_HALF


class SyntheticExact(Kernel):
    """A kernel whose value is, by construction, an exact rational combination
    of the Omega2 basis. Certification must accept it."""
    name = "synthetic_exact"

    def __init__(self, coeffs):
        self.coeffs = coeffs

    def evaluate(self, arg, dps):
        with mp.workdps(dps + 15):
            basis = build_omega2(dps)
            return sum(mp.mpf(c.numerator) / c.denominator * w
                       for c, w in zip(self.coeffs, basis))

    def tail_bound(self, arg, n_terms, dps):
        return mp.mpf(0)


def test_accepts_exact_construction():
    coeffs = [F(3, 1)] + [F(0, 1)] * 19 + [F(-7, 5)]   # 3*omega1 - 7/5
    k = SyntheticExact(coeffs)
    cert = certify(k, 0, coeffs, build_omega2, OMEGA2_LABELS, check_dps=200)
    assert cert.accepted
    assert cert.near_floor and cert.tracks_precision


def test_rejects_perturbed():
    coeffs = [F(3, 1)] + [F(0, 1)] * 19 + [F(-7, 5)]
    k = SyntheticExact(coeffs)
    bad = list(coeffs); bad[0] = bad[0] + F(1, 7)
    cert = certify(k, 0, bad, build_omega2, OMEGA2_LABELS, check_dps=200)
    assert not cert.accepted

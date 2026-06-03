"""The corrected S4,2(1/2) identity must certify as exact (residual tracks
precision), unlike the paper's published coefficients."""
import mpmath as mp
from reduction_engine.kernels import EulerSumS42
from reduction_engine.bases.dyadic_w6 import build_dyadic_w6, DYADIC_W6_LABELS
from reduction_engine.certify import certify
from reduction_engine.reference import S42_HALF_EXACT


def test_corrected_identity_certifies_exact():
    cert = certify(EulerSumS42(), mp.mpf(1) / 2, S42_HALF_EXACT,
                   build_dyadic_w6, DYADIC_W6_LABELS, check_dps=200, step=60)
    assert cert.accepted
    assert cert.near_floor and cert.tracks_precision

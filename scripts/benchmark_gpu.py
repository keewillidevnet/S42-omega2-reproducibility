#!/usr/bin/env python3
"""Optional GPU benchmark for the corrected x=1/2 13-element vector.

This script intentionally benchmarks only x=1/2 because that is the corrected
closed form in an independently stated 13-element dyadic basis. The x=1/4 result
is a certified depth-2 relation, and x=-1/2 remains open.
"""
from pathlib import Path
import sys, time
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

try:
    import torch
except ImportError as exc:
    raise SystemExit("PyTorch is required for the optional GPU benchmark.") from exc

from mpmath import mp
from s42.basis import compute_dyadic_w6_basis
from s42.coefficients import get_coefficients

mp.dps = 80
basis = [float(v) for v in compute_dyadic_w6_basis(80)]
coeffs = [float(c) for c in get_coefficients(0.5)]
assert len(basis) == len(coeffs) == 13

device = "cuda" if torch.cuda.is_available() else "cpu"
omega = torch.tensor(basis, dtype=torch.float64, device=device)
coef = torch.tensor(coeffs, dtype=torch.float64, device=device)
for batch in (1, 1024, 65536):
    t0=time.time()
    vals = (omega * coef).sum().repeat(batch)
    if device == "cuda": torch.cuda.synchronize()
    dt=time.time()-t0
    print(f"batch={batch:>7} device={device} elapsed={dt:.6f}s value={vals[0].item():.16g}")

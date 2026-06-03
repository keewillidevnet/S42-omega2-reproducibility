#!/usr/bin/env python3
"""Quick smoke test for the corrected S42 revision."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mpmath import mp
from s42.series import S42_series
from s42.closed_form import evaluate_relation
from s42.basis import DYADIC_W6_BASIS_NAMES, QUARTER_RELATION_BASIS_NAMES
from s42.coefficients import get_relation_status

mp.dps = 80
for x in (0.5, 0.25):
    sv, _ = S42_series(x)
    rv = evaluate_relation(x)
    print(f"S_{{4,2}}({x})")
    print(f"  status:   {get_relation_status(x)}")
    print(f"  residual: {mp.nstr(abs(sv-rv), 10)}")

print(f"\nCorrected x=1/2 basis length: {len(DYADIC_W6_BASIS_NAMES)}")
print(f"x=1/4 relation basis length: {len(QUARTER_RELATION_BASIS_NAMES)}")
print("x=-1/2 remains open; no closed form is implemented.")

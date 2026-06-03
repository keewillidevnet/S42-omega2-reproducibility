#!/usr/bin/env python3
"""Generate a corrected CPU speedup plot."""
from pathlib import Path
import sys, time
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mpmath import mp
import matplotlib.pyplot as plt
from s42.series import S42_series
from s42.closed_form import evaluate_relation
from s42.basis import compute_basis_for_x

precisions=[40,60,80]
for x,label in [(0.5,"x=1/2"),(0.25,"x=1/4")]:
    speedups=[]
    for p in precisions:
        mp.dps=p
        basis=compute_basis_for_x(x,p)
        t0=time.time(); S42_series(x); ts=time.time()-t0
        t0=time.time(); evaluate_relation(x,basis=basis); tr=time.time()-t0
        speedups.append(ts/tr)
    plt.plot(precisions, speedups, marker="o", label=label)
plt.xlabel("working precision, decimal digits")
plt.ylabel("series time / relation time")
plt.title("Corrected constant-folding speedup")
plt.legend()
plt.tight_layout()
plt.savefig("S42_speedup_vs_precision.png", dpi=200)
print("wrote S42_speedup_vs_precision.png")

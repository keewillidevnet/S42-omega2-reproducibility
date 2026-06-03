#!/usr/bin/env python3
"""Generate a corrected residual-tracking plot."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mpmath import mp
import matplotlib.pyplot as plt
from s42.series import S42_series
from s42.closed_form import evaluate_relation

precisions = [40, 60, 80, 100]
for x, label in [(0.5, "x=1/2 exact closed form"), (0.25, "x=1/4 depth-2 relation")]:
    residuals=[]
    for p in precisions:
        mp.dps=p
        sv,_=S42_series(x)
        rv=evaluate_relation(x)
        residuals.append(float(abs(sv-rv)))
    plt.semilogy(precisions, residuals, marker="o", label=label)
plt.xlabel("working precision, decimal digits")
plt.ylabel("absolute residual")
plt.title("Corrected residual tracking")
plt.legend()
plt.tight_layout()
plt.savefig("S42_error_vs_precision.png", dpi=200)
print("wrote S42_error_vs_precision.png")

#!/usr/bin/env python3
"""CPU benchmark for corrected S42 relations."""
from pathlib import Path
import argparse, sys, time
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mpmath import mp
from s42.series import S42_series
from s42.closed_form import evaluate_relation
from s42.basis import compute_basis_for_x
from s42.coefficients import AVAILABLE_X_VALUES, get_relation_status


def bench(x: float, precision: int, trials: int) -> dict:
    mp.dps = precision
    t0 = time.time(); basis = compute_basis_for_x(x, precision); basis_s = time.time() - t0
    series_times=[]; relation_times=[]
    for _ in range(trials):
        t0=time.time(); sv,_=S42_series(x); series_times.append(time.time()-t0)
        t0=time.time(); rv=evaluate_relation(x, basis=basis); relation_times.append(time.time()-t0)
    sm=sum(series_times)/trials; rm=sum(relation_times)/trials
    return {"x":x,"status":get_relation_status(x),"basis_ms":basis_s*1e3,"series_ms":sm*1e3,"relation_us":rm*1e6,"speedup":sm/rm,"residual":abs(sv-rv)}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--precision", type=int, default=80)
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--target", default="all", choices=["all","1/2","1/4"])
    args=ap.parse_args()
    targets = ["1/2","1/4"] if args.target == "all" else [args.target]
    for key in targets:
        r=bench(float(AVAILABLE_X_VALUES[key]), args.precision, args.trials)
        print(f"S_{{4,2}}({key}) — {r['status']}")
        print(f"  basis:    {r['basis_ms']:.3f} ms")
        print(f"  series:   {r['series_ms']:.3f} ms")
        print(f"  relation: {r['relation_us']:.3f} us")
        print(f"  speedup:  {r['speedup']:.1f}x")
        print(f"  residual: {mp.nstr(r['residual'], 8)}")

if __name__ == "__main__":
    main()

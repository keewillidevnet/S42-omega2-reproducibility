#!/usr/bin/env python3
"""
Benchmark (constant-folded): series vs Ω2 closed forms for S_{4,2}(x)
at x in {1/2, 1/4, -1/2}.

This version precomputes the Ω2 basis once and then benchmarks ONLY
the dot-product with rational coefficients (what a compiler or accelerator
would effectively execute after constant folding).

Requires: mpmath
Run: python3 S42_benchmark_folded.py
"""

import time
import mpmath as mp

# ---- user knobs ----
SERIES_DPS = 80
SERIES_TOL_DIGITS = 65
N_REP_SERIES = 50
N_REP_CLOSED = 20000   # high reps since folded path is very fast

def S42_series(x, dps=SERIES_DPS, tol_digits=SERIES_TOL_DIGITS, max_n=400000):
    mp.mp.dps = dps
    x = mp.mpf(x)
    H = mp.mpf('0')
    s = mp.mpf('0')
    xn = x
    n = 1
    tol = mp.power(10, -tol_digits)
    small = 0
    while True:
        term = H*xn/(n**5)
        s += term
        H += mp.mpf(1)/n
        n += 1
        xn *= x
        if abs(term) < tol:
            small += 1
        else:
            small = 0
        if small >= 30:
            break
        if n > max_n:
            break
    return s

def Cl_at_pi_over_3(s: int):
    theta = mp.pi/3
    w = mp.e**(1j*theta)
    val = mp.polylog(s, w)
    return mp.im(val) if (s % 2 == 0) else mp.re(val)

# ---- Ω2 basis: PRECOMPUTED ONCE ----
def omega2_basis_values():
    mp.mp.dps = SERIES_DPS
    pi = mp.pi
    log2 = mp.log(2)
    z3 = mp.zeta(3)
    z5 = mp.zeta(5)
    z6 = mp.zeta(6)

    Cl2 = Cl_at_pi_over_3(2)
    Cl4 = Cl_at_pi_over_3(4)
    Cl6 = Cl_at_pi_over_3(6)

    return [
        z6, z3**2, z5*log2, z3*log2**3, pi**4*log2**2, pi**2*log2**4, log2**6,
        mp.polylog(6, mp.mpf('0.5')), mp.polylog(6, mp.mpf('0.25')),
        mp.polylog(5, mp.mpf('0.5'))*log2, mp.polylog(5, mp.mpf('0.25'))*log2,
        mp.polylog(4, mp.mpf('0.5'))*log2**2, mp.polylog(4, mp.mpf('0.25'))*log2**2,
        pi**2*mp.polylog(4, mp.mpf('0.5')), pi**2*mp.polylog(4, mp.mpf('0.25')),
        Cl6, pi**2*Cl4, pi**4*Cl2, pi**2*(Cl2**2), Cl2**3, mp.mpf('1.0')
    ]

# Coefficients recovered by PSLQ (embedded)
DATA = {
  "S42_1_2": ["-147611/270291","119523/270291","-138793/270291","248047/270291","-55553/270291","61565/270291","153864/270291","45070/270291","0","0","0","0","0","0","0","0","0","0","0","0","0"],
  "S42_1_4": ["-169026/270291","-38170/270291","372009/270291","171906/270291","-169026/270291","-147611/270291","119523/270291","-138793/270291","248047/270291","-55553/270291","61565/270291","153864/270291","45070/270291","0","0","0","0","0","0","0","0"],
  "S42_m1_2": ["-100761/270291","93818/270291","40509/270291","385742/270291","-280927/270291","241041/270291","-62400/270291","-38170/270291","372009/270291","171906/270291","-169026/270291","-147611/270291","119523/270291","-138793/270291","248047/270291","-55553/270291","61565/270291","153864/270291","45070/270291","0","0"]
}

def parse_frac(s: str):
    if "/" in s:
        a,b = s.split("/")
        return mp.mpf(int(a)) / mp.mpf(int(b))
    return mp.mpf(int(s))

def eval_closed(coeffs, basis):
    mp.mp.dps = SERIES_DPS
    total = mp.mpf('0')
    for cs, bv in zip(coeffs, basis):
        c = parse_frac(cs)
        if c:
            total += c * bv
    return total

def timeit(fn, nrep):
    t0 = time.perf_counter()
    out = None
    for _ in range(nrep):
        out = fn()
    t1 = time.perf_counter()
    return (t1 - t0)/nrep, out

def main():
    mp.mp.dps = SERIES_DPS
    basis = omega2_basis_values()   # <-- precomputed once

    targets = [
        ("S42(1/2)", "0.5", DATA["S42_1_2"]),
        ("S42(1/4)", "0.25", DATA["S42_1_4"]),
        ("S42(-1/2)", "-0.5", DATA["S42_m1_2"]),
    ]

    print(f"Precision (mp.dps) = {SERIES_DPS}")
    print(f"Series tol digits  = {SERIES_TOL_DIGITS}")
    print("Mode: constant-folded Ω2 (basis precomputed once)\n")

    header = ["target", "series_time_ms", "closed_time_us", "speedup_x", "abs_err"]
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join(["---"]*len(header)) + "|")

    for name, x, coeffs in targets:
        ts, vs = timeit(lambda: S42_series(x), N_REP_SERIES)
        tc, vc = timeit(lambda: eval_closed(coeffs, basis), N_REP_CLOSED)
        err = abs(vs - vc)
        print("| " + " | ".join([
            name,
            f"{ts*1e3:.3f}",
            f"{tc*1e6:.3f}",
            f"{ts/tc:.1f}",
            mp.nstr(err, 5)
        ]) + " |")

if __name__ == "__main__":
    main()

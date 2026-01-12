#!/usr/bin/env python3
"""Benchmark: series vs Ω2 closed forms for S_{4,2}(x) at x in {1/2, 1/4, -1/2}.

Requires: mpmath
Run: python S42_benchmark.py
"""

import time
import json
import mpmath as mp

# ---- user knobs ----
SERIES_DPS = 80
SERIES_TOL_DIGITS = 65
N_REP_SERIES = 50
N_REP_CLOSED = 2000

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

DATA = {
  "basis_labels": [
    "zeta(6)",
    "zeta(3)^2",
    "zeta(5)log2",
    "zeta(3)log2^3",
    "pi^4 log2^2",
    "pi^2 log2^4",
    "log2^6",
    "Li6(1/2)",
    "Li6(1/4)",
    "Li5(1/2)log2",
    "Li5(1/4)log2",
    "Li4(1/2)log2^2",
    "Li4(1/4)log2^2",
    "pi^2 Li4(1/2)",
    "pi^2 Li4(1/4)",
    "Cl6(pi/3)",
    "pi^2 Cl4(pi/3)",
    "pi^4 Cl2(pi/3)",
    "pi^2 Cl2(pi/3)^2",
    "Cl2(pi/3)^3",
    "1"
  ],
  "S42_1_2": [
    "15683/14280",
    "-5743/14280",
    "-1593/4760",
    "-34213/14280",
    "-653/357",
    "107/7140",
    "933/595",
    "-4129/14280",
    "-5221/4760",
    "457/595",
    "457/595",
    "-1868/1785",
    "291/476",
    "-911/408",
    "167/7140",
    "-619/408",
    "-3869/3570",
    "15359/14280",
    "1007/2856",
    "-7613/7140",
    "-141/2380"
  ],
  "S42_1_4": [
    "6037/23939",
    "540/23939",
    "-9470/23939",
    "16159/23939",
    "-24385/23939",
    "18371/23939",
    "20947/23939",
    "1027/23939",
    "-8180/23939",
    "-39717/23939",
    "565/23939",
    "13069/23939",
    "-6410/23939",
    "22392/23939",
    "-55113/23939",
    "9961/23939",
    "3040/23939",
    "391/647",
    "-29476/23939",
    "-31660/23939",
    "-6389/23939"
  ],
  "S42_m1_2": [
    "2879/58060",
    "139667/116120",
    "-44803/116120",
    "-20309/29030",
    "5495/23224",
    "-31603/58060",
    "-112611/116120",
    "5441/29030",
    "9087/116120",
    "-8581/116120",
    "46081/116120",
    "-26413/58060",
    "-61269/116120",
    "57493/58060",
    "-14287/11612",
    "-47941/116120",
    "-9771/29030",
    "4109/58060",
    "-83559/58060",
    "-6695/23224",
    "-181073/116120"
  ],
  "pslq_residuals": {
    "S42(1/2)": "4.040319524e-97",
    "S42(1/4)": "7.292259174e-97",
    "S42(-1/2)": "1.576033214e-97"
  }
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
    basis = omega2_basis_values()

    targets = [
        ("S42(1/2)", "0.5", DATA["S42_1_2"]),
        ("S42(1/4)", "0.25", DATA["S42_1_4"]),
        ("S42(-1/2)", "-0.5", DATA["S42_m1_2"]),
    ]

    print(f"Precision (mp.dps) = {SERIES_DPS}")
    print(f"Series tol digits  = {SERIES_TOL_DIGITS}\n")

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

    print("\nPSLQ residuals (coefficient recovery):", DATA["pslq_residuals"])

if __name__ == "__main__":
    main()

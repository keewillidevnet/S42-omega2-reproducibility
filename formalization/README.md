# Lean Formalization of S4,2(1/2)

Lean 4 / Mathlib formalization of the closed-form identity for the weight-6 Euler sum S4,2(1/2).

## Status

The main theorem S42_half is machine-checked modulo a single functional equation (functionalEquation), the only remaining sorry. All supporting lemmas are fully kernel-verified with no sorryAx:

- F_zero: base case F0(x) = -x log(1-x)/(1-x)
- F_hasDerivAt: differentiation ladder, d/dx F_s = F_(s-1)/x
- Li_hasDerivAt: the same ladder for the polylogarithm
- Li_neg_one: Li_n(-1) = -(1 - 2^(1-n)) zeta(n)
- args_at_z0: argument specializations at z0 = (1/2) log 2
- S42_half_conditional: the closed form given the functional equation

S42_half therefore carries sorryAx tracing solely to functionalEquation. See AXIOMS.txt for the #print axioms output.

## Not yet proved

functionalEquation is the weight-induction tower of functional equations (weights about 2 to 6, integration constants fixed at interior base points). It is stated and used, not proved. This is the remaining work.

## Reproducing

Requires the toolchain pinned in lean-toolchain and the Mathlib revision pinned in lake-manifest.json.

    lake exe cache get
    lake build

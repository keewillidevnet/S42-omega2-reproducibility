# Lean Formalization of S4,2(1/2)

Lean 4 / Mathlib formalization of the closed-form identity for the weight-6 Euler sum S4,2(1/2).

## Status

The main theorem S42_half is machine-checked modulo exactly two functional-equation obligations, on the corrected domain Ioc 0 z0 = (0, z0] with z0 = (log 2)/2. Axiom audit by `#print axioms` under `lake env lean` (Lean v4.31.0-rc1); see AXIOMS.txt for the raw output.

CLEAN below means `[propext, Classical.choice, Quot.sound]`: kernel-verified, no sorryAx.

### Verified, kernel-clean

Building blocks:

- F_zero: base case F0(x) = -x log(1-x)/(1-x)
- F_hasDerivAt: differentiation ladder, d/dx F_s = F_(s-1)/x
- Li_hasDerivAt: the same ladder for the polylogarithm
- Li_neg_one: Li_n(-1) = -(1 - 2^(1-n)) zeta(n)
- args_at_z0: argument specializations at z0 = (log 2)/2
- S42_half_conditional: the closed form given the functional equation

Boundary continuity at z0 (closes the right endpoint of the domain):

- abel_neg_one: Abel's limit theorem at -1, obtained from the +1 form by x to -x
- Li_tendsto_neg_one: Li_s left-continuous at -1 (s >= 2)
- F_tendsto_neg_one: F_s left-continuous at -1 (s >= 3)
- a_tendsto: a(z) = 1 - e^(2z) tends to -1 from above as z tends to z0 from below
- feLHS_continuousWithinAt_z0, feRHS_continuousWithinAt_z0: both sides left-continuous at z0

Supporting helpers z0_args, shifted_series_tendsto, summable_base are also CLEAN.

### Verified modulo the two obligations below

- functionalEquation_open: equality on the open interval (0, z0), by constancy from fe_deriv_match and fe_basepoint
- functionalEquation: equality on (0, z0], the open part plus the endpoint z0 by left-continuity (limit uniqueness on the left-neighborhood filter)
- S42_half: the closed form, via functionalEquation at z0

These three are sorry-free in their own bodies; their sorryAx flows only through the two obligations below.

## Not yet proved

Two genuine open obligations, the entire remaining content:

- fe_deriv_eq: d feLHS = d feRHS on (0, z0), the weight-5 functional equation that heads the weight-induction tower
- fe_basepoint: feLHS zBase = feRHS zBase, the tower's integration constant at zBase = (log 2)/4

Both are numerically certified to several hundred digits with residuals that track precision; neither is yet machine-proved. Discharging them requires formalizing the weight-2 through weight-5 polylogarithm functional equations on the anharmonic orbit, together with Nielsen polylogarithms, which Mathlib does not yet contain.

## Domain correction (v2)

An earlier statement of functionalEquation carried a z0 <= z branch covering (z0, log 2). That region is divergent: the argument a = 1 - e^(2z) leaves the unit disk there, so the defining series is not summable and the branch was provably false. The statement is now restricted to exactly the convergence region (0, z0], and the endpoint z = z0 is recovered by the boundary-continuity lemmas above rather than assumed.

## Reproducing

Requires the toolchain pinned in lean-toolchain and the Mathlib revision pinned in lake-manifest.json.

    lake exe cache get
    lake build

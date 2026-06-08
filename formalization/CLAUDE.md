# S4,2(1/2) Lean formalization, project context

## Goal
Formalize in Lean 4 against Mathlib the closed form

  S4,2(1/2) = -51/32 zeta(6) - 1/4 zeta(3)^2 - 1/32 zeta(5) log2
            - 1/6 zeta(3) log^3 2 + 1/12 pi^2 zeta(3) log2 + 1/1440 pi^4 log^2 2
            + 1/144 pi^2 log^4 2 - 1/240 log^6 2 + 2 Li6(1/2) + Li5(1/2) log2
            - 1/2 S4,2(-1)

where S4,2(x) = sum over n >= 1 of H_{n-1} x^n / n^5 and H is the harmonic number.
S4,2(-1) is the single irreducible generator; carry it opaque and never reduce it.

## Math spec (read first)
- S42_symbolic_derivation.md is the complete, CAS-verified derivation. Every
  rational coefficient is verified exactly. The functional equation it relies on
  is certified numerically to 250 digits. Read it before writing Lean.
- S42_lean_skeleton.lean is a blueprint with named `sorry` obligations. It has
  NOT been typechecked. Treat it as a starting structure, not ground truth.

## Verified Mathlib facts (grepped from mathlib4 master; reconfirm with #check)
- harmonic : N -> Q   in Mathlib/NumberTheory/Harmonic/Defs.lean. Cast to R.
- NO polylogarithm, Nielsen polylog, Euler sum, or multiple zeta exist in
  Mathlib. Define Li and F from their series.
- riemannZeta : C -> C. Even values: riemannZeta_two, riemannZeta_four,
  riemannZeta_two_mul_nat (Mathlib/NumberTheory/LSeries/HurwitzZetaValues.lean).
  zeta(3), zeta(5) have no closed form; carry as (riemannZeta k).re.
- Series differentiation engine: hasDerivAt_tsum and
  hasDerivAt_tsum_of_isPreconnected (Mathlib/Analysis/Calculus/SmoothSeries.lean).
  Both need a summable bound on term derivatives.
- Constant from zero derivative: is_const_of_deriv_eq_zero
  (Mathlib/Analysis/Calculus/MeanValue.lean).
- TEMPLATE: Mathlib/NumberTheory/ZetaValues.lean proves zeta special values by
  exactly the differentiate-and-evaluate pattern this proof needs. Read it.

## Work order (strict; do not let a later step block an earlier one)
1. Definitions Li, F, S42 and all theorem statements compile.
2. S42_half_conditional: prove the closed form GIVEN the functional equation at
   z0 = (1/2) log 2 and the Li_n(-1) reductions as hypotheses. THIS IS THE
   PRIORITY. The final step is rational arithmetic (ring / linarith / field_simp)
   after rewriting with args_at_z0, the reductions, and the even-zeta values.
   When this builds with no sorry, STOP and report.
3. Li_neg_one reductions, proved from the alternating series.
4. F_hasDerivAt (the ladder). Try the analytic-function route
   (HasFPowerSeriesOnBall) as well as raw hasDerivAt_tsum.
5. ATTEMPT functionalEquation (the weight-induction tower). This is the hard
   part and may not close. It is acceptable to leave it as a single, precisely
   stated sorry.

## Rules
- Verify against the checker. After every change run
  `lake env lean S42Mathlib/S42.lean` and read the actual output. Never assume a
  tactic or lemma works.
- Never invent lemma names. Confirm with #check, by grepping
  .lake/packages/mathlib, or with Loogle. If a name errors, find the real one
  before proceeding.
- Do not paper over gaps. A clearly stated conditional theorem or a named sorry
  is correct. A fabricated unconditional theorem, or an `axiom` disguised as a
  result, is worse than useless. Honesty about what is proven is the whole point.
- Keep sorries named and isolated. Target state: everything builds with
  functionalEquation (and possibly the reductions) as the only sorry(s).

## How to check
- Single file: `lake env lean S42Mathlib/S42.lean`
- Full build: `lake build`
- First Mathlib load is slow (seconds to a minute); later checks are faster.

## Tooling: how to iterate (lean-lsp-mcp is available)

Prefer the LSP tools over cold `lake env lean` for all iteration. Reloading
Mathlib per check is the main time cost and the LSP server is warm.

- Inspect goal state with `lean_goal` at the line/column you are working on.
- Get errors and warnings with `lean_diagnostic`, not by grepping raw output.
- Try candidate tactics with `lean_multi_attempt` (several snippets on a line,
  returns goal state + diagnostics for each). Use this for trial and error.
- Find lemmas with `leansearch`, `loogle`, `lean_state_search`, `lean_hammer`
  before guessing names or grepping the Mathlib source.
- Use `lean_hover_info` for signatures and docs.

Do NOT shell out to `lake env lean <file>` after every small edit. Reserve a
full `lake env lean` run for final confirmation of a completed lemma.

## Definition of done (unchanged, enforce strictly)

A lemma is proven only when `#print axioms <name>` shows
`[propext, Classical.choice, Quot.sound]` with no `sorryAx`. Run that as the
final check before marking anything done. Never report a lemma as proven on a
green build alone.
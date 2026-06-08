/-
S4,2(1/2) closed form: Lean 4 / Mathlib formalization.

Work order (CLAUDE.md):
  1. Definitions Li, F, S42 and all theorem statements compile.            [this file]
  2. S42_half_conditional: closed form GIVEN the functional equation at
     z0 = (1/2) log 2 and the Li_n(-1) reductions as hypotheses.  PRIORITY.
  3. Li_neg_one reductions.
  4. F_hasDerivAt ladder.
  5. functionalEquation (the weight-induction tower) -- may stay a named sorry.

Source-verified Mathlib facts:
  - harmonic : ℕ → ℚ      (Mathlib/NumberTheory/Harmonic/Defs.lean)
  - riemannZeta : ℂ → ℂ;   riemannZeta_two, riemannZeta_four
                          (Mathlib/NumberTheory/LSeries/HurwitzZetaValues.lean)
  - Real.sinh_eq, Real.exp_log, Real.log_exp, Real.exp_neg, Real.exp_add
                          (Mathlib/Analysis/Complex/Trigonometric.lean, ...)
  - NO polylogarithm / Nielsen polylog / Euler sum in Mathlib; Li and F are
    defined here from their series.
-/

import Mathlib

open scoped BigOperators
open Real

noncomputable section

/-- Polylogarithm Li_s(x) for real x in [-1,1], by its series. -/
def Li (s : ℕ) (x : ℝ) : ℝ := ∑' n : ℕ, x ^ (n + 1) / ((n + 1 : ℝ) ^ s)

/-- The weight-(s) Euler-sum generating function F_s(x) = Σ H_{n-1} x^n / n^s.
    `harmonic n = H_n`; the (n+1)th summand carries H_{(n+1)-1} = H_n. S4,2 = F 5. -/
def F (s : ℕ) (x : ℝ) : ℝ :=
  ∑' n : ℕ, (harmonic n : ℝ) * x ^ (n + 1) / ((n + 1 : ℝ) ^ s)

/-- S4,2(x) := F 5 x. -/
def S42 (x : ℝ) : ℝ := F 5 x

/- ------------------------------------------------------------------ -/
/-  Step 1: the differential ladder and base case (statements only)   -/
/- ------------------------------------------------------------------ -/

/-- Base case: F_0(x) = - x log(1-x) / (1-x) on (-1,1).
    Proof: Cauchy product of `-log(1-x) = Σ xᵏ⁺¹/(k+1)` and `1/(1-x) = Σ xʲ`, whose
    nth antidiagonal coefficient is `H_{n+1} xⁿ⁺¹`; then `F 0 x = x · Σ Hₙ xⁿ`. -/
theorem F_zero (x : ℝ) (hx : |x| < 1) :
    F 0 x = - x * Real.log (1 - x) / (1 - x) := by
  have hxn : ‖x‖ < 1 := by rwa [Real.norm_eq_abs]
  -- summability of the two factors' norms
  have hgeom1 : Summable (fun k : ℕ => |x| ^ (k + 1)) := by
    have hg : Summable (fun k : ℕ => |x| ^ k) :=
      (hasSum_geometric_of_lt_one (abs_nonneg x) hx).summable
    refine (hg.mul_left |x|).congr (fun k => ?_)
    rw [pow_succ]; ring
  have hnf : Summable (fun k : ℕ => ‖x ^ (k + 1) / ((k : ℝ) + 1)‖) := by
    refine Summable.of_nonneg_of_le (fun k => norm_nonneg _) (fun k => ?_) hgeom1
    simp only [norm_div, norm_pow, Real.norm_eq_abs]
    refine div_le_self (by positivity) ?_
    rw [abs_of_pos (by positivity)]
    linarith [Nat.cast_nonneg (α := ℝ) k]
  have hng : Summable (fun j : ℕ => ‖x ^ j‖) := by
    simp only [norm_pow, Real.norm_eq_abs]
    exact (hasSum_geometric_of_lt_one (abs_nonneg x) hx).summable
  -- nth antidiagonal coefficient of the Cauchy product
  have hcoeff : ∀ n : ℕ,
      (∑ kl ∈ Finset.antidiagonal n, x ^ (kl.1 + 1) / ((kl.1 : ℝ) + 1) * x ^ kl.2)
      = (harmonic (n + 1) : ℝ) * x ^ (n + 1) := by
    intro n
    rw [Finset.Nat.sum_antidiagonal_eq_sum_range_succ
          (fun k l => x ^ (k + 1) / ((k : ℝ) + 1) * x ^ l) n]
    simp only [harmonic]
    push_cast
    rw [Finset.sum_mul]
    refine Finset.sum_congr rfl (fun k hk => ?_)
    rw [Finset.mem_range, Nat.lt_succ_iff] at hk
    rw [div_mul_eq_mul_div, ← pow_add, show k + 1 + (n - k) = n + 1 from by omega]
    ring
  -- Cauchy product as a HasSum, then rewrite coefficients to H_{n+1} xⁿ⁺¹
  have hP : HasSum (fun n => (harmonic (n + 1) : ℝ) * x ^ (n + 1))
      (-Real.log (1 - x) * (1 - x)⁻¹) := by
    have hval := tsum_mul_tsum_eq_tsum_sum_antidiagonal_of_summable_norm hnf hng
    rw [(hasSum_pow_div_log_of_abs_lt_one hx).tsum_eq,
        (hasSum_geometric_of_norm_lt_one hxn).tsum_eq] at hval
    have hsm := (summable_sum_mul_antidiagonal_of_summable_norm'
      hnf hnf.of_norm hng hng.of_norm).hasSum
    rw [← hval] at hsm
    exact hsm.congr_fun (fun n => (hcoeff n).symm)
  -- shift back to F 0 x = x · Σ Hₙ xⁿ
  have hP2 : HasSum (fun n => (harmonic (n + 1) : ℝ) * x ^ (n + 1 + 1))
      (x * (-Real.log (1 - x) * (1 - x)⁻¹)) := by
    refine (hP.mul_left x).congr_fun (fun n => ?_)
    rw [pow_succ]; ring
  have hFsum : HasSum (fun n => (harmonic n : ℝ) * x ^ (n + 1))
      (x * (-Real.log (1 - x) * (1 - x)⁻¹)) := by
    rw [← hasSum_nat_add_iff' 1]
    simpa only [Finset.sum_range_one, harmonic_zero, Rat.cast_zero, zero_mul, sub_zero] using hP2
  -- assemble
  have hFeq : F 0 x = ∑' n, (harmonic n : ℝ) * x ^ (n + 1) := by
    simp only [F, pow_zero, div_one]
  rw [hFeq, hFsum.tsum_eq]
  ring

/-- Ladder: d/dx F_s(x) = F_{s-1}(x) / x on (-1,1)\{0}, for s ≥ 1.
    Term-by-term differentiation via `hasDerivAt_tsum_of_isPreconnected` on a
    sub-ball of radius r = (|x|+1)/2 < 1, with summable derivative bound
    `‖g' n y‖ ≤ harmonic n · rⁿ`. -/
theorem F_hasDerivAt (s : ℕ) (hs : 1 ≤ s) (x : ℝ) (hx : |x| < 1) (hx0 : x ≠ 0) :
    HasDerivAt (F s) (F (s - 1) x / x) x := by
  set r : ℝ := (|x| + 1) / 2 with hr_def
  have hr0 : 0 < r := by rw [hr_def]; positivity
  have hrlt : r < 1 := by rw [hr_def]; linarith
  have hxr : |x| < r := by rw [hr_def]; linarith
  have hrnn : ‖r‖ < 1 := by rw [Real.norm_eq_abs, abs_of_pos hr0]; exact hrlt
  -- harmonic is nonnegative and ≤ n+1
  have hHnn : ∀ n : ℕ, (0:ℝ) ≤ (harmonic n : ℝ) := by
    intro n
    have h : (0:ℚ) ≤ harmonic n := by
      simp only [harmonic]; exact Finset.sum_nonneg (fun i _ => by positivity)
    exact_mod_cast h
  have hHbound : ∀ n : ℕ, (harmonic n : ℝ) ≤ (n : ℝ) + 1 := by
    intro n
    have hle : (harmonic n : ℝ) ≤ n := by
      simp only [harmonic]; push_cast
      calc ∑ i ∈ Finset.range n, ((i : ℝ) + 1)⁻¹
          ≤ ∑ _i ∈ Finset.range n, (1 : ℝ) := by
            refine Finset.sum_le_sum (fun i _ => ?_)
            rw [inv_le_one₀ (by positivity)]
            linarith [Nat.cast_nonneg (α := ℝ) i]
        _ = n := by simp
    linarith
  -- summable derivative bound
  have hpoly : Summable (fun n : ℕ => ((n : ℝ) + 1) * r ^ n) := by
    have h1 := summable_pow_mul_geometric_of_norm_lt_one 1 hrnn
    have h2 := (hasSum_geometric_of_lt_one hr0.le hrlt).summable
    refine (h1.add h2).congr (fun n => ?_); ring
  have husum : Summable (fun n : ℕ => (harmonic n : ℝ) * r ^ n) :=
    Summable.of_nonneg_of_le (fun n => mul_nonneg (hHnn n) (by positivity))
      (fun n => mul_le_mul_of_nonneg_right (hHbound n) (by positivity)) hpoly
  -- per-term derivative: d/dz [Hₙ zⁿ⁺¹/(n+1)ˢ] = Hₙ zⁿ/(n+1)ˢ⁻¹
  have hghd : ∀ (n : ℕ) (y : ℝ), y ∈ Metric.ball (0:ℝ) r →
      HasDerivAt (fun z => (harmonic n : ℝ) * z ^ (n + 1) / ((n : ℝ) + 1) ^ s)
        ((harmonic n : ℝ) * y ^ n / ((n : ℝ) + 1) ^ (s - 1)) y := by
    intro n y _
    have hd := (((hasDerivAt_pow (n + 1) y).const_mul (harmonic n : ℝ)).div_const
      (((n : ℝ) + 1) ^ s))
    simp only [Nat.add_sub_cancel] at hd
    convert hd using 1
    have hne : ((n : ℝ) + 1) ≠ 0 := by positivity
    rw [show ((n : ℝ) + 1) ^ s = ((n : ℝ) + 1) ^ (s - 1) * ((n : ℝ) + 1) from by
      rw [← pow_succ, Nat.sub_add_cancel hs]]
    push_cast
    field_simp
  -- the derivative bound on the sub-ball
  have hg'b : ∀ (n : ℕ) (y : ℝ), y ∈ Metric.ball (0:ℝ) r →
      ‖(harmonic n : ℝ) * y ^ n / ((n : ℝ) + 1) ^ (s - 1)‖ ≤ (harmonic n : ℝ) * r ^ n := by
    intro n y hy
    rw [Metric.mem_ball, Real.dist_eq, sub_zero] at hy
    rw [Real.norm_eq_abs, abs_div, abs_mul, abs_pow, abs_of_nonneg (hHnn n),
        abs_of_pos (show (0:ℝ) < ((n : ℝ) + 1) ^ (s - 1) by positivity)]
    calc (harmonic n : ℝ) * |y| ^ n / ((n : ℝ) + 1) ^ (s - 1)
        ≤ (harmonic n : ℝ) * |y| ^ n :=
          div_le_self (mul_nonneg (hHnn n) (by positivity))
            (one_le_pow₀ (by linarith [Nat.cast_nonneg (α := ℝ) n]))
      _ ≤ (harmonic n : ℝ) * r ^ n :=
          mul_le_mul_of_nonneg_left (pow_le_pow_left₀ (abs_nonneg y) hy.le n) (hHnn n)
  -- convergence at 0
  have hg0 : Summable (fun n : ℕ => (harmonic n : ℝ) * (0:ℝ) ^ (n + 1) / ((n : ℝ) + 1) ^ s) := by
    have : (fun n : ℕ => (harmonic n : ℝ) * (0:ℝ) ^ (n + 1) / ((n : ℝ) + 1) ^ s) = fun _ => 0 := by
      funext n; rw [zero_pow (by omega : n + 1 ≠ 0)]; ring
    rw [this]; exact summable_zero
  have hy0 : (0:ℝ) ∈ Metric.ball (0:ℝ) r := by rw [Metric.mem_ball, dist_self]; exact hr0
  have hxm : x ∈ Metric.ball (0:ℝ) r := by
    rw [Metric.mem_ball, Real.dist_eq, sub_zero]; exact hxr
  -- assemble the engine
  have key := hasDerivAt_tsum_of_isPreconnected husum Metric.isOpen_ball
    ((convex_ball (0:ℝ) r).isPreconnected) hghd hg'b hy0 hg0 hxm
  -- identify the derivative with F (s-1) x / x
  have hval : (∑' n, (harmonic n : ℝ) * x ^ n / ((n : ℝ) + 1) ^ (s - 1)) = F (s - 1) x / x := by
    simp only [F]
    rw [div_eq_mul_inv, ← tsum_mul_right]
    refine tsum_congr (fun n => ?_)
    have hD : ((n : ℝ) + 1) ^ (s - 1) ≠ 0 := by positivity
    rw [pow_succ]
    field_simp
  rw [← hval]
  exact key

/-- Same ladder specialized to Li (harmonic ≡ 1). Same proof as `F_hasDerivAt`
    with the constant `1` in place of `harmonic n`; the bound is just `rⁿ`. -/
theorem Li_hasDerivAt (s : ℕ) (hs : 1 ≤ s) (x : ℝ) (hx : |x| < 1) (hx0 : x ≠ 0) :
    HasDerivAt (Li s) (Li (s - 1) x / x) x := by
  set r : ℝ := (|x| + 1) / 2 with hr_def
  have hr0 : 0 < r := by rw [hr_def]; positivity
  have hrlt : r < 1 := by rw [hr_def]; linarith
  have hxr : |x| < r := by rw [hr_def]; linarith
  have hrnn : ‖r‖ < 1 := by rw [Real.norm_eq_abs, abs_of_pos hr0]; exact hrlt
  have husum : Summable (fun n : ℕ => r ^ n) := (hasSum_geometric_of_lt_one hr0.le hrlt).summable
  -- per-term derivative
  have hghd : ∀ (n : ℕ) (y : ℝ), y ∈ Metric.ball (0:ℝ) r →
      HasDerivAt (fun z => z ^ (n + 1) / ((n : ℝ) + 1) ^ s)
        (y ^ n / ((n : ℝ) + 1) ^ (s - 1)) y := by
    intro n y _
    have hd := (hasDerivAt_pow (n + 1) y).div_const (((n : ℝ) + 1) ^ s)
    simp only [Nat.add_sub_cancel] at hd
    convert hd using 1
    rw [show ((n : ℝ) + 1) ^ s = ((n : ℝ) + 1) ^ (s - 1) * ((n : ℝ) + 1) from by
      rw [← pow_succ, Nat.sub_add_cancel hs]]
    have hne : ((n : ℝ) + 1) ≠ 0 := by positivity
    push_cast
    field_simp
  -- derivative bound
  have hg'b : ∀ (n : ℕ) (y : ℝ), y ∈ Metric.ball (0:ℝ) r →
      ‖y ^ n / ((n : ℝ) + 1) ^ (s - 1)‖ ≤ r ^ n := by
    intro n y hy
    rw [Metric.mem_ball, Real.dist_eq, sub_zero] at hy
    rw [Real.norm_eq_abs, abs_div, abs_pow,
        abs_of_pos (show (0:ℝ) < ((n : ℝ) + 1) ^ (s - 1) by positivity)]
    calc |y| ^ n / ((n : ℝ) + 1) ^ (s - 1)
        ≤ |y| ^ n := div_le_self (by positivity)
          (one_le_pow₀ (by linarith [Nat.cast_nonneg (α := ℝ) n]))
      _ ≤ r ^ n := pow_le_pow_left₀ (abs_nonneg y) hy.le n
  have hg0 : Summable (fun n : ℕ => (0:ℝ) ^ (n + 1) / ((n : ℝ) + 1) ^ s) := by
    have : (fun n : ℕ => (0:ℝ) ^ (n + 1) / ((n : ℝ) + 1) ^ s) = fun _ => 0 := by
      funext n; rw [zero_pow (by omega : n + 1 ≠ 0)]; ring
    rw [this]; exact summable_zero
  have hy0 : (0:ℝ) ∈ Metric.ball (0:ℝ) r := by rw [Metric.mem_ball, dist_self]; exact hr0
  have hxm : x ∈ Metric.ball (0:ℝ) r := by
    rw [Metric.mem_ball, Real.dist_eq, sub_zero]; exact hxr
  have key := hasDerivAt_tsum_of_isPreconnected husum Metric.isOpen_ball
    ((convex_ball (0:ℝ) r).isPreconnected) hghd hg'b hy0 hg0 hxm
  have hval : (∑' n : ℕ, x ^ n / ((n : ℝ) + 1) ^ (s - 1)) = Li (s - 1) x / x := by
    simp only [Li]
    rw [div_eq_mul_inv, ← tsum_mul_right]
    refine tsum_congr (fun n => ?_)
    have hD : ((n : ℝ) + 1) ^ (s - 1) ≠ 0 := by positivity
    rw [pow_succ]
    field_simp
  rw [← hval]
  exact key

/- ------------------------------------------------------------------ -/
/-  Step 2: the functional equation                                   -/
/- ------------------------------------------------------------------ -/

/-- z0 = (1/2) log 2. -/
def z0 : ℝ := Real.log 2 / 2

/-- The right-hand side of the functional equation as a function of z.
    `riemannZeta` is ℂ-valued, so the real special values are taken via `.re`;
    ζ(2), ζ(4) are reduced to π powers in the proof. -/
def feRHS (z : ℝ) : ℝ :=
  2 * (Li 6 (1 - Real.exp (2*z)) + Li 6 (1 - Real.exp (-2*z)) + Li 6 (Real.exp (-2*z)))
    - z * (2 * Li 5 (1 - Real.exp (2*z)) - 2 * Li 5 (1 - Real.exp (-2*z))
            - Li 5 (Real.exp (-2*z)))
    - Real.log (2 * Real.sinh z) * Li 5 (Real.exp (-2*z))
    + Real.log (2 * Real.sinh z)
        * (2*z^5/15 + (riemannZeta 5).re - 2*z*(riemannZeta 4).re
            + 2*z^2*(riemannZeta 3).re - 4*z^3/3*(riemannZeta 2).re)
    - z^4/3 * (Real.log (2 * Real.sinh z))^2
    - z^6/15 - 2*z^3/3*(riemannZeta 3).re - 3*z^2/2*(riemannZeta 4).re
    + 2*z*(riemannZeta 2).re*(riemannZeta 3).re - z*(riemannZeta 5).re
    - 5/4*(riemannZeta 6).re - ((riemannZeta 3).re)^2/2

/-- The left-hand side. -/
def feLHS (z : ℝ) : ℝ :=
  S42 (1 - Real.exp (2*z)) + S42 (1 - Real.exp (-2*z)) + S42 (Real.exp (-2*z))

/-- Interior base point for the integration-constant step. `zBase = (log 2)/4`
    lies strictly inside `(0, log 2)`, and there `e^{2 zBase} = √2 ∈ (1,2)`, so
    all three Li arguments `1 - e^{±2z}, e^{-2z}` are strictly inside `(-1,1)` and
    the defining series converge. (See BLUEPRINT.md for why `z = 0` is unusable.) -/
def zBase : ℝ := Real.log 2 / 4

/-- `zBase` is an interior point of the interval. (Glue fact, fully proved.) -/
theorem zBase_mem : zBase ∈ Set.Ioo (0 : ℝ) (Real.log 2) := by
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  rw [zBase, Set.mem_Ioo]; constructor <;> linarith

/- ------------------------------------------------------------------ -/
/-  The functional-equation tower (intermediate lemmas, all `sorry`).  -/
/-                                                                     -/
/-  `functionalEquation` is DERIVED below from exactly two intermediate -/
/-  obligations by the mean-value/constancy argument:                  -/
/-    (A) `fe_deriv_match` : on the open interval the two sides are     -/
/-        differentiable with a COMMON derivative — so their difference -/
/-        has derivative 0.  This is the analytic heart (the weight-    -/
/-        induction tower; see BLUEPRINT.md), and uses the proven       -/
/-        ladders `F_hasDerivAt` / `Li_hasDerivAt`.                     -/
/-    (B) `fe_basepoint` : the equation holds at the regular interior   -/
/-        point `zBase` (the constant of integration), proved from the  -/
/-        low-weight base case.                                         -/
/-  Neither is proved here; both stay `sorry`.                          -/
/- ------------------------------------------------------------------ -/

/-- Range facts on the CORRECTED domain `Ioo 0 z0` (z0 = log2/2): all three
    Li/F arguments lie strictly in `(-1,1)` and are nonzero, and `2 sinh z ≠ 0`.
    The `a = 1 - e^{2z}` bound is the one needing `z < z0`; `b, c` need only
    `z > 0`. Fully proved (mechanical). -/
theorem args_mem {z : ℝ} (hz : z ∈ Set.Ioo (0 : ℝ) z0) :
    |1 - Real.exp (2*z)| < 1 ∧ (1 - Real.exp (2*z)) ≠ 0 ∧
    |1 - Real.exp (-2*z)| < 1 ∧ (1 - Real.exp (-2*z)) ≠ 0 ∧
    |Real.exp (-2*z)| < 1 ∧ Real.exp (-2*z) ≠ 0 ∧ (2 * Real.sinh z) ≠ 0 := by
  obtain ⟨hpos, hlt⟩ := hz
  have hz2 : z < Real.log 2 / 2 := by rwa [z0] at hlt
  have he2lt : Real.exp (2*z) < 2 := by
    have h : Real.exp (2*z) < Real.exp (Real.log 2) := Real.exp_lt_exp.mpr (by linarith)
    rwa [Real.exp_log (by norm_num : (0:ℝ) < 2)] at h
  have he2gt : 1 < Real.exp (2*z) := by
    have h : Real.exp 0 < Real.exp (2*z) := Real.exp_lt_exp.mpr (by linarith)
    rwa [Real.exp_zero] at h
  have hemlt : Real.exp (-2*z) < 1 := by
    have h : Real.exp (-2*z) < Real.exp 0 := Real.exp_lt_exp.mpr (by linarith)
    rwa [Real.exp_zero] at h
  have hempos : 0 < Real.exp (-2*z) := Real.exp_pos _
  refine ⟨?_, sub_ne_zero.mpr (ne_of_lt he2gt), ?_,
    (by linarith : (0:ℝ) < 1 - Real.exp (-2*z)).ne', ?_, hempos.ne', ?_⟩
  · rw [abs_lt]; constructor <;> linarith
  · rw [abs_lt]; constructor <;> linarith
  · rw [abs_lt]; constructor <;> linarith
  · have := Real.sinh_pos_iff.mpr hpos; positivity

/-- LHS differentiable on `Ioo 0 z0`.  Each `S42(arg) = F 5 (arg)` differentiates
    by `F_hasDerivAt` composed (chain rule) with the elementary inner map; the
    derivative term is left as inferred (unsimplified).  Fully proved. -/
theorem feLHS_differentiableAt {z : ℝ} (hz : z ∈ Set.Ioo (0 : ℝ) z0) :
    DifferentiableAt ℝ feLHS z := by
  obtain ⟨hba, hane_a, hbb, hane_b, hbc, hane_c, _⟩ := args_mem hz
  have hinner_a := (((hasDerivAt_id z).const_mul (2:ℝ)).exp).const_sub 1
  have hinner_b := (((hasDerivAt_id z).const_mul (-2:ℝ)).exp).const_sub 1
  have hinner_c := ((hasDerivAt_id z).const_mul (-2:ℝ)).exp
  have hSa := (F_hasDerivAt 5 (by norm_num) _ hba hane_a).comp z hinner_a
  have hSb := (F_hasDerivAt 5 (by norm_num) _ hbb hane_b).comp z hinner_b
  have hSc := (F_hasDerivAt 5 (by norm_num) _ hbc hane_c).comp z hinner_c
  exact ((hSa.add hSb).add hSc).differentiableAt

/-- RHS differentiable on `Ioo 0 z0`.  The six `Li`-composites and
    `L = log(2 sinh z)` (using `2 sinh z > 0` here) are differentiated explicitly;
    the remaining polynomial/ζ-constant structure is closed by `fun_prop`.
    Fully proved. -/
theorem feRHS_differentiableAt {z : ℝ} (hz : z ∈ Set.Ioo (0 : ℝ) z0) :
    DifferentiableAt ℝ feRHS z := by
  obtain ⟨hba, hane_a, hbb, hane_b, hbc, hane_c, hsinh⟩ := args_mem hz
  -- elementary inner maps (differentiable everywhere)
  have hfa : DifferentiableAt ℝ (fun w => 1 - Real.exp (2*w)) z := by fun_prop
  have hfb : DifferentiableAt ℝ (fun w => 1 - Real.exp (-2*w)) z := by fun_prop
  have hfc : DifferentiableAt ℝ (fun w => Real.exp (-2*w)) z := by fun_prop
  -- Li ladders at the (in-range) arguments, composed with the inner maps
  have hLi6a : DifferentiableAt ℝ (fun w => Li 6 (1 - Real.exp (2*w))) z := by
    have hg : DifferentiableAt ℝ (Li 6) (1 - Real.exp (2*z)) :=
      (Li_hasDerivAt 6 (by norm_num) _ hba hane_a).differentiableAt
    exact hg.comp z hfa
  have hLi6b : DifferentiableAt ℝ (fun w => Li 6 (1 - Real.exp (-2*w))) z := by
    have hg : DifferentiableAt ℝ (Li 6) (1 - Real.exp (-2*z)) :=
      (Li_hasDerivAt 6 (by norm_num) _ hbb hane_b).differentiableAt
    exact hg.comp z hfb
  have hLi6c : DifferentiableAt ℝ (fun w => Li 6 (Real.exp (-2*w))) z := by
    have hg : DifferentiableAt ℝ (Li 6) (Real.exp (-2*z)) :=
      (Li_hasDerivAt 6 (by norm_num) _ hbc hane_c).differentiableAt
    exact hg.comp z hfc
  have hLi5a : DifferentiableAt ℝ (fun w => Li 5 (1 - Real.exp (2*w))) z := by
    have hg : DifferentiableAt ℝ (Li 5) (1 - Real.exp (2*z)) :=
      (Li_hasDerivAt 5 (by norm_num) _ hba hane_a).differentiableAt
    exact hg.comp z hfa
  have hLi5b : DifferentiableAt ℝ (fun w => Li 5 (1 - Real.exp (-2*w))) z := by
    have hg : DifferentiableAt ℝ (Li 5) (1 - Real.exp (-2*z)) :=
      (Li_hasDerivAt 5 (by norm_num) _ hbb hane_b).differentiableAt
    exact hg.comp z hfb
  have hLi5c : DifferentiableAt ℝ (fun w => Li 5 (Real.exp (-2*w))) z := by
    have hg : DifferentiableAt ℝ (Li 5) (Real.exp (-2*z)) :=
      (Li_hasDerivAt 5 (by norm_num) _ hbc hane_c).differentiableAt
    exact hg.comp z hfc
  have hL : DifferentiableAt ℝ (fun w => Real.log (2 * Real.sinh w)) z :=
    (((Real.hasDerivAt_sinh z).const_mul 2).log hsinh).differentiableAt
  unfold feRHS
  fun_prop

/-- INTERMEDIATE (sorry) — the ONLY remaining mathematical content. On `Ioo 0 z0`
    the derivatives of the two sides coincide.  This is exactly the weight-5
    functional equation (the analytic heart; see BLUEPRINT.md).  Everything
    around it — the differentiability of each side — is now discharged. -/
theorem fe_deriv_eq {z : ℝ} (hz : z ∈ Set.Ioo (0 : ℝ) z0) :
    deriv feLHS z = deriv feRHS z := by
  sorry

/-- Assembled on the CORRECTED domain `Ioo 0 z0`: both sides are differentiable
    (proved) and share a common derivative (the single open obligation
    `fe_deriv_eq`). -/
theorem fe_deriv_match {z : ℝ} (hz : z ∈ Set.Ioo (0 : ℝ) z0) :
    ∃ d : ℝ, HasDerivAt feLHS d z ∧ HasDerivAt feRHS d z := by
  refine ⟨deriv feLHS z, (feLHS_differentiableAt hz).hasDerivAt, ?_⟩
  rw [fe_deriv_eq hz]
  exact (feRHS_differentiableAt hz).hasDerivAt

/-- INTERMEDIATE (sorry) — the integration constant. The equation holds at the
    regular interior base point `zBase`, where every argument is strictly inside
    `(-1,1)` so all defining series converge. Discharged by the low-weight base
    case of the tower (NOT at `z0`, which would be circular — see BLUEPRINT.md). -/
theorem fe_basepoint : feLHS zBase = feRHS zBase := by
  sorry

/-- The three argument values at `z0` (a local copy of the relevant part of
    `args_at_z0`, which is stated later in the file). -/
theorem z0_args :
    (1 - Real.exp (2 * z0) = -1) ∧ (1 - Real.exp (-2 * z0) = 1 / 2) ∧
      (Real.exp (-2 * z0) = 1 / 2) := by
  have he2 : Real.exp (2 * z0) = 2 := by
    rw [show (2 : ℝ) * z0 = Real.log 2 by rw [z0]; ring, Real.exp_log (by norm_num)]
  have he2' : Real.exp (-2 * z0) = 1 / 2 := by
    rw [show (-2 : ℝ) * z0 = -Real.log 2 by rw [z0]; ring, Real.exp_neg,
        Real.exp_log (by norm_num)]; norm_num
  exact ⟨by rw [he2]; norm_num, by rw [he2']; norm_num, he2'⟩

/-- **Abel's limit theorem at −1** (real, approached from the right), derived from
    the Mathlib `+1`-version by the `x ↦ −x` substitution.  If `∑ f n (−1)ⁿ`
    converges then `∑ f n xⁿ → ∑ f n (−1)ⁿ` as `x → −1⁺`. -/
theorem abel_neg_one {f : ℕ → ℝ} (hf : Summable (fun n => f n * (-1 : ℝ) ^ n)) :
    Filter.Tendsto (fun x => ∑' n, f n * x ^ n) (nhdsWithin (-1 : ℝ) (Set.Ioi (-1)))
      (nhds (∑' n, f n * (-1 : ℝ) ^ n)) := by
  have hsum : Filter.Tendsto (fun N => ∑ i ∈ Finset.range N, f i * (-1 : ℝ) ^ i)
      Filter.atTop (nhds (∑' n, f n * (-1 : ℝ) ^ n)) := hf.hasSum.tendsto_sum_nat
  have habel := Real.tendsto_tsum_powerSeries_nhdsWithin_lt hsum
  have hneg : Filter.Tendsto (Neg.neg : ℝ → ℝ) (nhdsWithin (-1 : ℝ) (Set.Ioi (-1)))
      (nhdsWithin (1 : ℝ) (Set.Iio 1)) := by
    have h := tendsto_neg_nhdsGT (a := (-1 : ℝ)); rwa [neg_neg] at h
  have hcomp := habel.comp hneg
  refine hcomp.congr (fun x => ?_)
  simp only [Function.comp_apply]
  refine tsum_congr (fun n => ?_)
  rw [mul_assoc, ← mul_pow, neg_one_mul, neg_neg]

/-- Boundary tendsto for the `x · (power series)` shape that both `Li` and `F`
    take after pulling out one factor of `x`. -/
theorem shifted_series_tendsto {f : ℕ → ℝ} (hf : Summable (fun n => f n * (-1 : ℝ) ^ n)) :
    Filter.Tendsto (fun x => x * ∑' n, f n * x ^ n) (nhdsWithin (-1 : ℝ) (Set.Ioi (-1)))
      (nhds ((-1 : ℝ) * ∑' n, f n * (-1 : ℝ) ^ n)) := by
  have hid : Filter.Tendsto (fun x : ℝ => x) (nhdsWithin (-1 : ℝ) (Set.Ioi (-1))) (nhds (-1)) :=
    (continuous_id.tendsto (-1)).mono_left nhdsWithin_le_nhds
  exact hid.mul (abel_neg_one hf)

/-- Base summable majorant `∑ 1/(n+1)²`. -/
theorem summable_base : Summable (fun n : ℕ => 1 / ((n : ℝ) + 1) ^ 2) := by
  have hg : Summable (fun m : ℕ => 1 / ((m : ℝ)) ^ 2) := summable_one_div_nat_pow.mpr (by norm_num)
  have hsh := hg.comp_injective (add_left_injective 1)
  refine hsh.congr (fun k => ?_)
  simp only [Function.comp_apply]; push_cast; ring

/-- `Li_s` is left-continuous at the boundary `x = -1` (approached from the right),
    for `s ≥ 2`.  By the `x · (power series)` factoring and `abel_neg_one`. -/
theorem Li_tendsto_neg_one (s : ℕ) (hs : 2 ≤ s) :
    Filter.Tendsto (fun x => Li s x) (nhdsWithin (-1 : ℝ) (Set.Ioi (-1))) (nhds (Li s (-1))) := by
  have hsumm : Summable (fun n : ℕ => (1 / ((n : ℝ) + 1) ^ s) * (-1 : ℝ) ^ n) := by
    refine Summable.of_norm_bounded summable_base (fun n => ?_)
    rw [norm_mul, norm_pow, norm_neg, norm_one, one_pow, mul_one, Real.norm_eq_abs,
        abs_of_pos (by positivity)]
    exact one_div_le_one_div_of_le (by positivity)
      (pow_le_pow_right₀ (by linarith [Nat.cast_nonneg (α := ℝ) n]) hs)
  have hLi : ∀ x : ℝ, Li s x = x * ∑' (n : ℕ), (1 / ((n : ℝ) + 1) ^ s) * x ^ n := by
    intro x; unfold Li; rw [← tsum_mul_left]; exact tsum_congr (fun n => by rw [pow_succ]; ring)
  have key := shifted_series_tendsto hsumm
  rw [← hLi (-1)] at key
  exact key.congr (fun x => (hLi x).symm)

/-- `F_s` is left-continuous at the boundary `x = -1` (approached from the right),
    for `s ≥ 3`.  Same factoring; summability uses `harmonic n ≤ n + 1`. -/
theorem F_tendsto_neg_one (s : ℕ) (hs : 3 ≤ s) :
    Filter.Tendsto (fun x => F s x) (nhdsWithin (-1 : ℝ) (Set.Ioi (-1))) (nhds (F s (-1))) := by
  have hHb : ∀ n : ℕ, (harmonic n : ℝ) ≤ (n : ℝ) + 1 := by
    intro n
    have hle : (harmonic n : ℝ) ≤ n := by
      simp only [harmonic]; push_cast
      calc ∑ i ∈ Finset.range n, ((i : ℝ) + 1)⁻¹ ≤ ∑ _i ∈ Finset.range n, (1 : ℝ) := by
            refine Finset.sum_le_sum (fun i _ => ?_)
            rw [inv_le_one₀ (by positivity)]; linarith [Nat.cast_nonneg (α := ℝ) i]
        _ = n := by simp
    linarith
  have hsumm : Summable (fun n : ℕ => ((harmonic n : ℝ) / ((n : ℝ) + 1) ^ s) * (-1 : ℝ) ^ n) := by
    refine Summable.of_norm_bounded summable_base (fun n => ?_)
    have hnn : (0 : ℝ) ≤ (harmonic n : ℝ) := by
      have h : (0 : ℚ) ≤ harmonic n := by
        simp only [harmonic]; exact Finset.sum_nonneg (fun i _ => by positivity)
      exact_mod_cast h
    rw [norm_mul, norm_pow, norm_neg, norm_one, one_pow, mul_one, Real.norm_eq_abs,
        abs_of_nonneg (div_nonneg hnn (by positivity))]
    rw [div_le_iff₀ (show (0 : ℝ) < ((n : ℝ) + 1) ^ s by positivity), one_div, inv_mul_eq_div,
        le_div_iff₀ (show (0 : ℝ) < ((n : ℝ) + 1) ^ 2 by positivity)]
    calc (harmonic n : ℝ) * ((n : ℝ) + 1) ^ 2
        ≤ ((n : ℝ) + 1) * ((n : ℝ) + 1) ^ 2 := mul_le_mul_of_nonneg_right (hHb n) (by positivity)
      _ = ((n : ℝ) + 1) ^ 3 := by ring
      _ ≤ ((n : ℝ) + 1) ^ s := pow_le_pow_right₀ (by linarith [Nat.cast_nonneg (α := ℝ) n]) hs
  have hF : ∀ x : ℝ, F s x = x * ∑' (n : ℕ), ((harmonic n : ℝ) / ((n : ℝ) + 1) ^ s) * x ^ n := by
    intro x; unfold F; rw [← tsum_mul_left]; exact tsum_congr (fun n => by rw [pow_succ]; ring)
  have key := shifted_series_tendsto hsumm
  rw [← hF (-1)] at key
  exact key.congr (fun x => (hF x).symm)

/-- As `z → z0⁻`, the boundary argument `a = 1 - e^{2z}` tends to `-1` from the
    right (it stays `> -1` for `z < z0`).  This feeds the Abel boundary lemmas. -/
theorem a_tendsto :
    Filter.Tendsto (fun z => 1 - Real.exp (2 * z)) (nhdsWithin z0 (Set.Iio z0))
      (nhdsWithin (-1 : ℝ) (Set.Ioi (-1))) := by
  obtain ⟨ha, _, _⟩ := z0_args
  rw [tendsto_nhdsWithin_iff]
  refine ⟨?_, ?_⟩
  · have hcont : Filter.Tendsto (fun z => 1 - Real.exp (2 * z)) (nhds z0)
        (nhds (1 - Real.exp (2 * z0))) := Continuous.tendsto (by fun_prop) z0
    rw [ha] at hcont
    exact hcont.mono_left nhdsWithin_le_nhds
  · filter_upwards [self_mem_nhdsWithin] with z hz
    simp only [Set.mem_Ioi]
    have hlt : z < z0 := hz
    have hlt2 : Real.exp (2 * z) < 2 := by
      have h2 : Real.exp (2 * z) < Real.exp (Real.log 2) := by
        apply Real.exp_lt_exp.mpr; rw [z0] at hlt; linarith
      rwa [Real.exp_log (by norm_num)] at h2
    linarith

/-- The left side is left-continuous at `z0`: the `b, c` arguments hit the interior
    point `1/2` (continuity from `F_hasDerivAt`), the `a` argument hits `-1`
    (`F_tendsto_neg_one`). -/
theorem feLHS_continuousWithinAt_z0 : ContinuousWithinAt feLHS (Set.Iio z0) z0 := by
  obtain ⟨ha, hb, hc⟩ := z0_args
  have hF5half : ContinuousAt (F 5) (1 / 2 : ℝ) :=
    (F_hasDerivAt 5 (by norm_num) (1 / 2) (by norm_num) (by norm_num)).continuousAt
  have hTa : Filter.Tendsto (fun z => S42 (1 - Real.exp (2 * z)))
      (nhdsWithin z0 (Set.Iio z0)) (nhds (S42 (-1))) :=
    (F_tendsto_neg_one 5 (by norm_num)).comp a_tendsto
  have hbt : Filter.Tendsto (fun z => 1 - Real.exp (-2 * z)) (nhdsWithin z0 (Set.Iio z0))
      (nhds (1 / 2)) := by
    have h : Filter.Tendsto (fun z => 1 - Real.exp (-2 * z)) (nhds z0)
        (nhds (1 - Real.exp (-2 * z0))) := Continuous.tendsto (by fun_prop) z0
    rw [hb] at h; exact h.mono_left nhdsWithin_le_nhds
  have hct : Filter.Tendsto (fun z => Real.exp (-2 * z)) (nhdsWithin z0 (Set.Iio z0))
      (nhds (1 / 2)) := by
    have h : Filter.Tendsto (fun z => Real.exp (-2 * z)) (nhds z0)
        (nhds (Real.exp (-2 * z0))) := Continuous.tendsto (by fun_prop) z0
    rw [hc] at h; exact h.mono_left nhdsWithin_le_nhds
  have hTb : Filter.Tendsto (fun z => S42 (1 - Real.exp (-2 * z)))
      (nhdsWithin z0 (Set.Iio z0)) (nhds (S42 (1 / 2))) := hF5half.tendsto.comp hbt
  have hTc : Filter.Tendsto (fun z => S42 (Real.exp (-2 * z)))
      (nhdsWithin z0 (Set.Iio z0)) (nhds (S42 (1 / 2))) := hF5half.tendsto.comp hct
  have hfe : feLHS z0 = S42 (-1) + S42 (1 / 2) + S42 (1 / 2) := by unfold feLHS; rw [ha, hb, hc]
  change Filter.Tendsto feLHS (nhdsWithin z0 (Set.Iio z0)) (nhds (feLHS z0))
  rw [hfe]; unfold feLHS
  exact (hTa.add hTb).add hTc

/-- The right side is left-continuous at `z0`.  Split into the two boundary
    `a`-terms (`Li 6 (a)`, `Li 5 (a)` → `±1` via `Li_tendsto_neg_one`) and the
    `ContinuousAt` remainder (all `b, c`-arguments interior, `log (2 sinh z)`
    finite since `sinh z0 > 0`, polynomials/ζ continuous). -/
theorem feRHS_continuousWithinAt_z0 : ContinuousWithinAt feRHS (Set.Iio z0) z0 := by
  obtain ⟨ha, hb, hc⟩ := z0_args
  -- boundary a-terms
  have ha6 : ContinuousWithinAt (fun z => Li 6 (1 - Real.exp (2 * z))) (Set.Iio z0) z0 := by
    change Filter.Tendsto _ _ (nhds (Li 6 (1 - Real.exp (2 * z0))))
    rw [ha]; exact (Li_tendsto_neg_one 6 (by norm_num)).comp a_tendsto
  have ha5 : ContinuousWithinAt (fun z => Li 5 (1 - Real.exp (2 * z))) (Set.Iio z0) z0 := by
    change Filter.Tendsto _ _ (nhds (Li 5 (1 - Real.exp (2 * z0))))
    rw [ha]; exact (Li_tendsto_neg_one 5 (by norm_num)).comp a_tendsto
  -- interior continuity facts
  have hib : ContinuousAt (fun z => 1 - Real.exp (-2 * z)) z0 := by fun_prop
  have hic : ContinuousAt (fun z => Real.exp (-2 * z)) z0 := by fun_prop
  have h1_6b : ContinuousAt (Li 6) (1 - Real.exp (-2 * z0)) :=
    (Li_hasDerivAt 6 (by norm_num) _ (by rw [hb]; norm_num) (by rw [hb]; norm_num)).continuousAt
  have h1_6c : ContinuousAt (Li 6) (Real.exp (-2 * z0)) :=
    (Li_hasDerivAt 6 (by norm_num) _ (by rw [hc]; norm_num) (by rw [hc]; norm_num)).continuousAt
  have h1_5b : ContinuousAt (Li 5) (1 - Real.exp (-2 * z0)) :=
    (Li_hasDerivAt 5 (by norm_num) _ (by rw [hb]; norm_num) (by rw [hb]; norm_num)).continuousAt
  have h1_5c : ContinuousAt (Li 5) (Real.exp (-2 * z0)) :=
    (Li_hasDerivAt 5 (by norm_num) _ (by rw [hc]; norm_num) (by rw [hc]; norm_num)).continuousAt
  have _hb6 : ContinuousAt (fun z => Li 6 (1 - Real.exp (-2 * z))) z0 :=
    h1_6b.tendsto.comp hib.tendsto
  have _hc6 : ContinuousAt (fun z => Li 6 (Real.exp (-2 * z))) z0 :=
    h1_6c.tendsto.comp hic.tendsto
  have _hb5 : ContinuousAt (fun z => Li 5 (1 - Real.exp (-2 * z))) z0 :=
    h1_5b.tendsto.comp hib.tendsto
  have _hc5 : ContinuousAt (fun z => Li 5 (Real.exp (-2 * z))) z0 :=
    h1_5c.tendsto.comp hic.tendsto
  have hLc : ContinuousAt (fun z => Real.log (2 * Real.sinh z)) z0 := by
    have hz0pos : 0 < z0 := by
      rw [z0]; have := Real.log_pos (by norm_num : (1 : ℝ) < 2); linarith
    have hsp := Real.sinh_pos_iff.mpr hz0pos
    have hsinh : (2 * Real.sinh z0) ≠ 0 := by positivity
    exact (((Real.hasDerivAt_sinh z0).const_mul 2).log hsinh).continuousAt
  -- the remainder (no boundary terms) is continuous at z0
  have hrest : ContinuousAt (fun z =>
      2 * (Li 6 (1 - Real.exp (-2 * z)) + Li 6 (Real.exp (-2 * z)))
        - z * (-2 * Li 5 (1 - Real.exp (-2 * z)) - Li 5 (Real.exp (-2 * z)))
        - Real.log (2 * Real.sinh z) * Li 5 (Real.exp (-2 * z))
        + Real.log (2 * Real.sinh z)
            * (2 * z ^ 5 / 15 + (riemannZeta 5).re - 2 * z * (riemannZeta 4).re
                + 2 * z ^ 2 * (riemannZeta 3).re - 4 * z ^ 3 / 3 * (riemannZeta 2).re)
        - z ^ 4 / 3 * (Real.log (2 * Real.sinh z)) ^ 2
        - z ^ 6 / 15 - 2 * z ^ 3 / 3 * (riemannZeta 3).re - 3 * z ^ 2 / 2 * (riemannZeta 4).re
        + 2 * z * (riemannZeta 2).re * (riemannZeta 3).re - z * (riemannZeta 5).re
        - 5 / 4 * (riemannZeta 6).re - ((riemannZeta 3).re) ^ 2 / 2) z0 := by
    fun_prop
  have hsplit : feRHS = fun z =>
      (2 * Li 6 (1 - Real.exp (2 * z)) - z * (2 * Li 5 (1 - Real.exp (2 * z))))
      + (2 * (Li 6 (1 - Real.exp (-2 * z)) + Li 6 (Real.exp (-2 * z)))
        - z * (-2 * Li 5 (1 - Real.exp (-2 * z)) - Li 5 (Real.exp (-2 * z)))
        - Real.log (2 * Real.sinh z) * Li 5 (Real.exp (-2 * z))
        + Real.log (2 * Real.sinh z)
            * (2 * z ^ 5 / 15 + (riemannZeta 5).re - 2 * z * (riemannZeta 4).re
                + 2 * z ^ 2 * (riemannZeta 3).re - 4 * z ^ 3 / 3 * (riemannZeta 2).re)
        - z ^ 4 / 3 * (Real.log (2 * Real.sinh z)) ^ 2
        - z ^ 6 / 15 - 2 * z ^ 3 / 3 * (riemannZeta 3).re - 3 * z ^ 2 / 2 * (riemannZeta 4).re
        + 2 * z * (riemannZeta 2).re * (riemannZeta 3).re - z * (riemannZeta 5).re
        - 5 / 4 * (riemannZeta 6).re - ((riemannZeta 3).re) ^ 2 / 2) := by
    funext z; unfold feRHS; ring
  have hbdry : ContinuousWithinAt (fun z =>
      2 * Li 6 (1 - Real.exp (2 * z)) - z * (2 * Li 5 (1 - Real.exp (2 * z))))
      (Set.Iio z0) z0 :=
    (ha6.const_mul 2).sub (continuousWithinAt_id.mul (ha5.const_mul 2))
  rw [hsplit]
  exact hbdry.add hrest.continuousWithinAt

/-- The OPEN-region equality on `(0, z0)`: DERIVED (no `sorry`) from
    `fe_deriv_match` and `fe_basepoint` by the constancy argument. -/
theorem functionalEquation_open {w : ℝ} (hw : w ∈ Set.Ioo (0 : ℝ) z0) :
    feLHS w = feRHS w := by
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  set s : Set ℝ := Set.Ioo (0 : ℝ) z0 with hs_def
  have hbs : zBase ∈ s := by
    rw [hs_def, zBase, z0, Set.mem_Ioo]; constructor <;> linarith
  have hg0 : ∀ u ∈ s, HasDerivAt (fun u => feLHS u - feRHS u) 0 u := by
    intro u hu
    obtain ⟨d, hL, hR⟩ := fe_deriv_match hu
    have h := hL.sub hR
    rwa [sub_self] at h
  have hdiff : DifferentiableOn ℝ (fun u => feLHS u - feRHS u) s :=
    fun u hu => (hg0 u hu).differentiableAt.differentiableWithinAt
  have hfd : Set.EqOn (fderiv ℝ (fun u => feLHS u - feRHS u)) 0 s := by
    intro u hu
    simpa using (hg0 u hu).hasFDerivAt.fderiv
  have hconst := IsOpen.is_const_of_fderiv_eq_zero isOpen_Ioo isPreconnected_Ioo
    hdiff hfd hw hbs
  have hbase : feLHS zBase - feRHS zBase = 0 := by rw [fe_basepoint]; ring
  have hval : feLHS w - feRHS w = 0 := by rw [hconst]; exact hbase
  linarith [hval]

/-- The functional equation on the CORRECTED domain `Ioc 0 z0 = (0, z0]`.  The
    open part is `functionalEquation_open`; the endpoint `z = z0` is obtained by
    left-continuity of both sides at `z0` (`feLHS/feRHS_continuousWithinAt_z0`)
    together with the open-part equality, via limit uniqueness on `𝓝[<] z0`.
    The previously-false `z0 ≤ z` branch (the series diverge above `z0`) is gone:
    the statement is now exactly the convergence region. -/
theorem functionalEquation {z : ℝ} (hz : z ∈ Set.Ioc (0 : ℝ) z0) :
    feLHS z = feRHS z := by
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hz0pos : 0 < z0 := by rw [z0]; linarith
  rcases lt_or_eq_of_le hz.2 with hlt | heq
  · exact functionalEquation_open ⟨hz.1, hlt⟩
  · rw [heq]
    -- eventually-equal on the left, both sides left-continuous ⇒ equal at z0
    have hev : feLHS =ᶠ[nhdsWithin z0 (Set.Iio z0)] feRHS := by
      have hmem : Set.Ioo (0 : ℝ) z0 ∈ nhdsWithin z0 (Set.Iio z0) := by
        rw [← Set.Ioi_inter_Iio, Set.inter_comm]
        exact inter_mem_nhdsWithin _ (Ioi_mem_nhds hz0pos)
      filter_upwards [hmem] with w hw using functionalEquation_open hw
    have hTL : Filter.Tendsto feLHS (nhdsWithin z0 (Set.Iio z0)) (nhds (feLHS z0)) :=
      feLHS_continuousWithinAt_z0
    have hTL' : Filter.Tendsto feLHS (nhdsWithin z0 (Set.Iio z0)) (nhds (feRHS z0)) :=
      (feRHS_continuousWithinAt_z0 : Filter.Tendsto feRHS _ _).congr' hev.symm
    exact tendsto_nhds_unique hTL hTL'

/- ------------------------------------------------------------------ -/
/-  Step 3: reductions                                                -/
/- ------------------------------------------------------------------ -/

/-- Li_n(-1) = -(1 - 2^{1-n}) ζ(n), proved from the series via an even/odd split:
    ζ(n) + Li_n(-1) = 2^{1-n} ζ(n). -/
theorem Li_neg_one (n : ℕ) (hn : 2 ≤ n) :
    Li n (-1) = -(1 - (2:ℝ)^(1 - (n:ℤ))) * (riemannZeta n).re := by
  have hn1 : 1 < n := by omega
  set Z : ℕ → ℝ := fun k => 1 / ((k:ℝ) + 1) ^ n with hZdef
  set L : ℕ → ℝ := fun k => (-1:ℝ) ^ (k + 1) / ((k:ℝ) + 1) ^ n with hLdef
  -- ζ(n) as a real series
  have hs : (1:ℝ) < (↑n : ℂ).re := by simp only [Complex.natCast_re]; exact_mod_cast hn1
  have hz : riemannZeta (n:ℂ) = ((∑' k : ℕ, Z k : ℝ) : ℂ) := by
    rw [zeta_eq_tsum_one_div_nat_add_one_cpow hs, Complex.ofReal_tsum]
    refine tsum_congr (fun k => ?_)
    simp only [hZdef]
    rw [Complex.cpow_natCast]
    push_cast
    ring
  have hzeta : (riemannZeta (n:ℂ)).re = ∑' k : ℕ, Z k := by rw [hz, Complex.ofReal_re]
  -- summability of Z and L
  have hZsum : Summable Z := by
    have hg : Summable (fun m : ℕ => 1 / ((m:ℝ)) ^ n) := summable_one_div_nat_pow.mpr hn1
    have hsh := hg.comp_injective (add_left_injective 1)
    refine hsh.congr (fun k => ?_)
    simp only [hZdef, Function.comp_apply]
    push_cast
    ring
  have hLsum : Summable L := by
    refine Summable.of_norm_bounded hZsum (fun k => ?_)
    have h2 : |((k:ℝ) + 1) ^ n| = ((k:ℝ) + 1) ^ n := abs_of_pos (by positivity)
    simp only [hLdef, hZdef, Real.norm_eq_abs, abs_div, abs_pow, abs_neg, abs_one, one_pow, h2]
    exact le_rfl
  -- Li n (-1) is the L-series
  have hLi : Li n (-1) = ∑' k : ℕ, L k := by
    simp only [Li]
    refine tsum_congr (fun k => ?_)
    simp only [hLdef]
  -- even/odd subseries are summable
  have hZe := hZsum.comp_injective (mul_right_injective₀ (two_ne_zero' ℕ))
  have hZo := hZsum.comp_injective
    (show Function.Injective (fun j : ℕ => 2 * j + 1) by intro a b h; dsimp only at h; omega)
  have hLe := hLsum.comp_injective (mul_right_injective₀ (two_ne_zero' ℕ))
  have hLo := hLsum.comp_injective
    (show Function.Injective (fun j : ℕ => 2 * j + 1) by intro a b h; dsimp only at h; omega)
  have hZsplit := tsum_even_add_odd (f := Z) hZe hZo
  have hLsplit := tsum_even_add_odd (f := L) hLe hLo
  -- L on even/odd indices in terms of Z
  have hLeven : ∀ j : ℕ, L (2 * j) = - Z (2 * j) := by
    intro j
    simp only [hLdef, hZdef]
    rw [Odd.neg_one_pow (show Odd (2 * j + 1) from ⟨j, by ring⟩)]
    ring
  have hLodd : ∀ j : ℕ, L (2 * j + 1) = Z (2 * j + 1) := by
    intro j
    simp only [hLdef, hZdef]
    rw [Even.neg_one_pow (show Even (2 * j + 1 + 1) from ⟨j + 1, by ring⟩)]
  have hLE : (∑' j : ℕ, L (2 * j)) = -(∑' j : ℕ, Z (2 * j)) := by
    rw [tsum_congr hLeven, tsum_neg]
  have hLO : (∑' j : ℕ, L (2 * j + 1)) = (∑' j : ℕ, Z (2 * j + 1)) := tsum_congr hLodd
  -- the odd part of Z is 2^{-n} ζ(n)
  have hOterm : ∀ j : ℕ, Z (2 * j + 1) = (1 / (2:ℝ) ^ n) * Z j := by
    intro j
    have hb : ((2 * j + 1 : ℕ) : ℝ) + 1 = 2 * ((j:ℝ) + 1) := by push_cast; ring
    simp only [hZdef]
    rw [hb, mul_pow, div_mul_div_comm, one_mul]
  have hO : (∑' j : ℕ, Z (2 * j + 1)) = (1 / (2:ℝ) ^ n) * (∑' k : ℕ, Z k) := by
    rw [tsum_congr hOterm]
    exact Summable.tsum_mul_left _ hZsum
  -- combine the two splittings
  have hsum2 : (∑' k : ℕ, Z k) + (∑' k : ℕ, L k) = 2 * (∑' j : ℕ, Z (2 * j + 1)) := by
    rw [← hZsplit, ← hLsplit, hLE, hLO]; ring
  have hcombine : (∑' k : ℕ, Z k) + (∑' k : ℕ, L k)
      = 2 * (1 / (2:ℝ) ^ n) * (∑' k : ℕ, Z k) := by
    rw [hsum2, hO]; ring
  -- finish
  have hzp : (2:ℝ) ^ (1 - (n:ℤ)) = 2 / (2:ℝ) ^ n := by
    rw [zpow_sub₀ (by norm_num : (2:ℝ) ≠ 0), zpow_one, zpow_natCast]
  rw [hLi, hzeta, hzp]
  linear_combination hcombine

/- ------------------------------------------------------------------ -/
/-  Step 4: specialization and final assembly                         -/
/- ------------------------------------------------------------------ -/

/-- At z0 the three arguments are -1, 1/2, 1/2, and 2 sinh z0 = 1/√2. -/
theorem args_at_z0 :
    1 - Real.exp (2*z0) = -1 ∧ 1 - Real.exp (-2*z0) = 1/2 ∧
    Real.exp (-2*z0) = 1/2 ∧ Real.log (2 * Real.sinh z0) = -(Real.log 2)/2 := by
  have e2 : Real.exp (2 * z0) = 2 := by
    have h : (2 * z0) = Real.log 2 := by rw [z0]; ring
    rw [h, Real.exp_log (by norm_num : (0:ℝ) < 2)]
  have e2' : Real.exp (-2 * z0) = 1/2 := by
    have h : (-2 * z0) = -(Real.log 2) := by rw [z0]; ring
    rw [h, Real.exp_neg, Real.exp_log (by norm_num : (0:ℝ) < 2)]; norm_num
  refine ⟨by rw [e2]; norm_num, by rw [e2']; norm_num, e2', ?_⟩
  -- 2 sinh z0 = exp(-z0), hence log = -z0 = -(log 2)/2.
  have hexp : Real.exp z0 = 2 * Real.exp (-z0) := by
    rw [← e2, ← Real.exp_add]; congr 1; ring
  have key : 2 * Real.sinh z0 = Real.exp (-z0) := by
    rw [Real.sinh_eq, hexp]; ring
  rw [key, Real.log_exp, z0]; ring

/-- STAGE-1, the honest near-finished artifact. Given the functional-equation
    instance at z0 and the two Li_n(-1) reductions, the remaining content is the
    rational-arithmetic assembly (the even-zeta values are proved inline from
    Mathlib). -/
theorem S42_half_conditional
    (hFE : feLHS z0 = feRHS z0)
    (hLi6 : Li 6 (-1) = -(31 / 32) * (riemannZeta 6).re)
    (hLi5 : Li 5 (-1) = -(15 / 16) * (riemannZeta 5).re) :
    S42 (1/2) =
      -51/32 * (riemannZeta 6).re
      - 1/4 * ((riemannZeta 3).re)^2
      - 1/32 * (riemannZeta 5).re * Real.log 2
      - 1/6 * (riemannZeta 3).re * (Real.log 2)^3
      + 1/12 * Real.pi^2 * (riemannZeta 3).re * Real.log 2
      + 1/1440 * Real.pi^4 * (Real.log 2)^2
      + 1/144 * Real.pi^2 * (Real.log 2)^4
      - 1/240 * (Real.log 2)^6
      + 2 * Li 6 (1/2)
      + Li 5 (1/2) * Real.log 2
      - 1/2 * S42 (-1) := by
  obtain ⟨ha, hb, hc, hL⟩ := args_at_z0
  -- even-zeta real values from Mathlib
  have hz2 : (riemannZeta 2).re = Real.pi ^ 2 / 6 := by
    have h : riemannZeta 2 = ((Real.pi ^ 2 / 6 : ℝ) : ℂ) := by
      rw [riemannZeta_two]; push_cast; ring
    rw [h, Complex.ofReal_re]
  have hz4 : (riemannZeta 4).re = Real.pi ^ 4 / 90 := by
    have h : riemannZeta 4 = ((Real.pi ^ 4 / 90 : ℝ) : ℂ) := by
      rw [riemannZeta_four]; push_cast; ring
    rw [h, Complex.ofReal_re]
  -- unfold the equation and specialize all arguments
  unfold feLHS feRHS at hFE
  rw [ha, hb, hc, hL, hLi6, hLi5, hz2, hz4] at hFE
  -- expand the remaining z0 in the polynomial terms
  simp only [z0] at hFE
  -- hFE is now a linear equation in the basis; solve for S42 (1/2)
  linear_combination hFE / 2

/-- MAIN THEOREM (unconditional). Depends on `functionalEquation`. -/
theorem S42_half :
    S42 (1/2) =
      -51/32 * (riemannZeta 6).re
      - 1/4 * ((riemannZeta 3).re)^2
      - 1/32 * (riemannZeta 5).re * Real.log 2
      - 1/6 * (riemannZeta 3).re * (Real.log 2)^3
      + 1/12 * Real.pi^2 * (riemannZeta 3).re * Real.log 2
      + 1/1440 * Real.pi^4 * (Real.log 2)^2
      + 1/144 * Real.pi^2 * (Real.log 2)^4
      - 1/240 * (Real.log 2)^6
      + 2 * Li 6 (1/2)
      + Li 5 (1/2) * Real.log 2
      - 1/2 * S42 (-1) := by
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hz0 : z0 ∈ Set.Ioc (0 : ℝ) z0 := by
    rw [Set.mem_Ioc]; refine ⟨?_, le_refl _⟩; rw [z0]; linarith
  have hLi6 : Li 6 (-1) = -(31 / 32) * (riemannZeta 6).re := by
    rw [Li_neg_one 6 (by norm_num)]; norm_num
  have hLi5 : Li 5 (-1) = -(15 / 16) * (riemannZeta 5).re := by
    rw [Li_neg_one 5 (by norm_num)]; norm_num
  exact S42_half_conditional (functionalEquation hz0) hLi6 hLi5

end

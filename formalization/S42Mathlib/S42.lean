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

/-- The functional equation on an interval around z0 where all three arguments
    stay in (-1,1]. This is the weight-induction tower; left as a named sorry. -/
theorem functionalEquation {z : ℝ} (hz : z ∈ Set.Ioo (0:ℝ) (Real.log 2)) :
    feLHS z = feRHS z := by
  sorry

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
    (hLi6 : Li 6 (-1) = -(31/32) * (riemannZeta 6).re)
    (hLi5 : Li 5 (-1) = -(15/16) * (riemannZeta 5).re) :
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
  have hz0 : z0 ∈ Set.Ioo (0:ℝ) (Real.log 2) := by
    rw [z0, Set.mem_Ioo]; constructor <;> linarith
  have hLi6 : Li 6 (-1) = -(31/32) * (riemannZeta 6).re := by
    rw [Li_neg_one 6 (by norm_num)]; norm_num
  have hLi5 : Li 5 (-1) = -(15/16) * (riemannZeta 5).re := by
    rw [Li_neg_one 5 (by norm_num)]; norm_num
  exact S42_half_conditional (functionalEquation hz0) hLi6 hLi5

end

/-
Copyright (c) 2026 Lluís Eriksson.
Released under the GNU Affero General Public License v3.0.
-/

import RiemannPrimeResolvent.PrimeTail

/-!
# Integer-cutoff von Mangoldt tail

This file closes the elementary analytic part of RF-1.  For `δ > 0` and an
integer cutoff `N ≥ 3`, it proves

`sum_{n>N} Λ(n) exp (-(1+δ) log n) ≤ primeTailMajorant δ N`.

For positive integers the summand is exactly `Λ(n) / n^(1+δ)`.  The proof
uses only `Λ(n) ≤ log n`, monotonicity after `3`, sum--integral comparison,
and an explicit antiderivative.  No zero-free region or RH input is used.
-/

open scoped ArithmeticFunction
open Set MeasureTheory

namespace RiemannPrimeResolvent

noncomputable def primeTailIntegrand (δ x : ℝ) : ℝ :=
  Real.log x * Real.exp (-(1 + δ) * Real.log x)

lemma hasDerivAt_primeTailIntegrand {δ x : ℝ} (hx : x ≠ 0) :
    HasDerivAt (primeTailIntegrand δ)
      (Real.exp (-(1 + δ) * Real.log x) / x *
        (1 - (1 + δ) * Real.log x)) x := by
  unfold primeTailIntegrand
  have hlog := Real.hasDerivAt_log hx
  have hexp := (hlog.const_mul (-(1 + δ))).exp
  convert hlog.mul hexp using 1 <;> try {rfl}
  field_simp [hx]
  ring_nf

lemma primeTailIntegrand_antitoneOn {δ : ℝ} (hδ : 0 < δ) :
    AntitoneOn (primeTailIntegrand δ) (Ici 3) := by
  apply antitoneOn_of_deriv_nonpos (convex_Ici (3 : ℝ))
  · unfold primeTailIntegrand
    have hlogcont : ContinuousOn Real.log (Ici (3 : ℝ)) :=
      continuousOn_id.log fun x hx => by
        have hxpos : 0 < x := lt_of_lt_of_le (by norm_num) hx
        exact hxpos.ne'
    intro x hx
    have hinner : ContinuousWithinAt (fun y => -(1 + δ) * Real.log y)
        (Ici (3 : ℝ)) x := (hlogcont x hx).const_mul _
    have hexp : ContinuousWithinAt (fun y => Real.exp (-(1 + δ) * Real.log y))
        (Ici (3 : ℝ)) x := Real.continuous_exp.continuousAt.comp_continuousWithinAt hinner
    exact (hlogcont x hx).mul hexp
  · rw [interior_Ici]
    intro x hx
    have hxpos : 0 < x := lt_trans (by norm_num) hx
    exact (hasDerivAt_primeTailIntegrand hxpos.ne').differentiableAt.differentiableWithinAt
  · rw [interior_Ici]
    intro x hx
    have hxpos : 0 < x := lt_trans (by norm_num) hx
    rw [(hasDerivAt_primeTailIntegrand hxpos.ne').deriv]
    have hlog : 1 < Real.log x :=
      (Real.lt_log_iff_exp_lt hxpos).2
        (Real.exp_one_lt_three.trans hx)
    have hbracket : 1 - (1 + δ) * Real.log x ≤ 0 := by
      nlinarith
    have hprefactor : 0 ≤ Real.exp (-(1 + δ) * Real.log x) / x :=
      div_nonneg (Real.exp_pos _).le hxpos.le
    exact mul_nonpos_of_nonneg_of_nonpos hprefactor hbracket

noncomputable def vonMangoldtTailTerm (δ : ℝ) (n : ℕ) : ℝ :=
  ArithmeticFunction.vonMangoldt n *
    Real.exp (-(1 + δ) * Real.log (n : ℝ))

lemma vonMangoldtTailTerm_le_integrand (δ : ℝ) (n : ℕ) :
    vonMangoldtTailTerm δ n ≤ primeTailIntegrand δ n := by
  unfold vonMangoldtTailTerm primeTailIntegrand
  exact mul_le_mul_of_nonneg_right
    ArithmeticFunction.vonMangoldt_le_log (Real.exp_pos _).le

/-- Finite integer-cutoff von Mangoldt tail, bounded by its integral envelope. -/
theorem finite_vonMangoldt_tail_le_integral {δ : ℝ} {N M : ℕ}
    (hδ : 0 < δ) (hN : 3 ≤ N) (hNM : N ≤ M) :
    (∑ n ∈ Finset.Ico N M, vonMangoldtTailTerm δ (n + 1)) ≤
      ∫ x in (N : ℝ)..(M : ℝ), primeTailIntegrand δ x := by
  calc
    (∑ n ∈ Finset.Ico N M, vonMangoldtTailTerm δ (n + 1)) ≤
        ∑ n ∈ Finset.Ico N M,
          primeTailIntegrand δ ((n + 1 : ℕ) : ℝ) := by
      exact Finset.sum_le_sum fun n _ => vonMangoldtTailTerm_le_integrand δ (n + 1)
    _ ≤ ∫ x in (N : ℝ)..(M : ℝ), primeTailIntegrand δ x := by
      apply AntitoneOn.sum_le_integral_Ico hNM
      refine (primeTailIntegrand_antitoneOn hδ).mono ?_
      intro x hx
      exact le_trans (by exact_mod_cast hN) hx.1

noncomputable def primeTailPrimitive (δ x : ℝ) : ℝ :=
  -Real.exp (-δ * Real.log x) *
    (Real.log x / δ + 1 / δ ^ 2)

lemma hasDerivAt_primeTailPrimitive {δ x : ℝ} (hδ : δ ≠ 0) (hx : 0 < x) :
    HasDerivAt (primeTailPrimitive δ) (primeTailIntegrand δ x) x := by
  unfold primeTailPrimitive primeTailIntegrand
  have hlog := Real.hasDerivAt_log hx.ne'
  have hexp := (hlog.const_mul (-δ)).exp
  have hbracket := (hlog.div_const δ).add_const (1 / δ ^ 2)
  have hexp_div :
      Real.exp (-δ * Real.log x) / x =
        Real.exp (-(1 + δ) * Real.log x) := by
    calc
      Real.exp (-δ * Real.log x) / x =
          Real.exp (-δ * Real.log x) * Real.exp (-Real.log x) := by
            rw [div_eq_mul_inv, Real.exp_neg, Real.exp_log hx]
      _ = Real.exp (-δ * Real.log x + -Real.log x) := by rw [Real.exp_add]
      _ = Real.exp (-(1 + δ) * Real.log x) := by
        congr 1
        ring_nf
  convert hexp.neg.mul hbracket using 1 <;> try {rfl}
  rw [← hexp_div]
  field_simp [hδ, hx.ne']
  simp
  ring_nf

lemma integral_primeTailIntegrand_le_majorant {δ : ℝ} {N M : ℕ}
    (hδ : 0 < δ) (hN : 3 ≤ N) (hNM : N ≤ M) :
    (∫ x in (N : ℝ)..(M : ℝ), primeTailIntegrand δ x) ≤
      primeTailMajorant δ N := by
  have hNMreal : (N : ℝ) ≤ (M : ℝ) := by exact_mod_cast hNM
  have h3Nreal : (3 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have hderiv : ∀ x ∈ uIcc (N : ℝ) (M : ℝ),
      HasDerivAt (primeTailPrimitive δ) (primeTailIntegrand δ x) x := by
    rw [uIcc_of_le hNMreal]
    intro x hx
    have hxpos : 0 < x :=
      lt_of_lt_of_le (by norm_num : (0 : ℝ) < 3) (h3Nreal.trans hx.1)
    exact hasDerivAt_primeTailPrimitive hδ.ne' hxpos
  have hcont : ContinuousOn (primeTailIntegrand δ) (uIcc (N : ℝ) (M : ℝ)) := by
    rw [uIcc_of_le hNMreal]
    intro x hx
    have hxpos : 0 < x :=
      lt_of_lt_of_le (by norm_num : (0 : ℝ) < 3) (h3Nreal.trans hx.1)
    unfold primeTailIntegrand
    have hlogcont : ContinuousAt Real.log x := Real.continuousAt_log hxpos.ne'
    have hinner : ContinuousAt (fun y => -(1 + δ) * Real.log y) x :=
      hlogcont.const_mul _
    have hexp : ContinuousAt (fun y => Real.exp (-(1 + δ) * Real.log y)) x :=
      Real.continuous_exp.continuousAt.comp hinner
    exact (hlogcont.mul hexp).continuousWithinAt
  have hint : IntervalIntegrable (primeTailIntegrand δ) volume (N : ℝ) (M : ℝ) :=
    hcont.intervalIntegrable
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint]
  have hM3 : (3 : ℝ) ≤ (M : ℝ) := by exact_mod_cast hN.trans hNM
  have hlogM : 0 ≤ Real.log (M : ℝ) :=
    Real.log_nonneg (by linarith)
  have hbracket :
      0 ≤ Real.log (M : ℝ) / δ + 1 / δ ^ 2 :=
    add_nonneg (div_nonneg hlogM hδ.le)
      (div_nonneg zero_le_one (sq_pos_of_pos hδ).le)
  have hprimitiveM : primeTailPrimitive δ (M : ℝ) ≤ 0 := by
    unfold primeTailPrimitive
    exact mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (Real.exp_pos _).le) hbracket
  calc
    primeTailPrimitive δ (M : ℝ) - primeTailPrimitive δ (N : ℝ) ≤
        0 - primeTailPrimitive δ (N : ℝ) := sub_le_sub_right hprimitiveM _
    _ = primeTailMajorant δ N := by
      unfold primeTailPrimitive primeTailMajorant
      ring

/-- Every finite integer-cutoff von Mangoldt tail is bounded by the closed form. -/
theorem finite_vonMangoldt_tail_le_majorant {δ : ℝ} {N M : ℕ}
    (hδ : 0 < δ) (hN : 3 ≤ N) (hNM : N ≤ M) :
    (∑ n ∈ Finset.Ico N M, vonMangoldtTailTerm δ (n + 1)) ≤
      primeTailMajorant δ N :=
  (finite_vonMangoldt_tail_le_integral hδ hN hNM).trans
    (integral_primeTailIntegrand_le_majorant hδ hN hNM)

/-- Unconditional infinite integer-cutoff von Mangoldt tail bound. -/
theorem vonMangoldt_tail_tsum_le_majorant {δ : ℝ} {N : ℕ}
    (hδ : 0 < δ) (hN : 3 ≤ N) :
    (∑' k : ℕ, vonMangoldtTailTerm δ (N + k + 1)) ≤
      primeTailMajorant δ N := by
  apply Real.tsum_le_of_sum_range_le
  · intro k
    unfold vonMangoldtTailTerm
    exact mul_nonneg ArithmeticFunction.vonMangoldt_nonneg (Real.exp_pos _).le
  · intro K
    have hfinite := finite_vonMangoldt_tail_le_majorant
      (δ := δ) (N := N) (M := N + K) hδ hN (Nat.le_add_right N K)
    simpa [Finset.sum_Ico_eq_sum_range, add_assoc] using hfinite

end RiemannPrimeResolvent

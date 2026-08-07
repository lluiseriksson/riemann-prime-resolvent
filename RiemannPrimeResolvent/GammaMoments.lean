import Mathlib.Probability.Distributions.Gamma
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-!
# Moments of gamma laws

This file proves directly from Mathlib's gamma density the general real-power
moment formula.  The `Gamma(2, 1)` identities used in the mean-corrected gamma
approximation to Riemann Xi are then immediate special cases.  It makes no
statement about zeta zeros.
-/

open MeasureTheory Real Set
open scoped ENNReal NNReal

noncomputable section

namespace RiemannPrimeResolvent

open ProbabilityTheory

/-- Every real-power moment of a gamma law above the integrability threshold.

The distribution uses shape `a` and rate `r`, so the answer contains
`r ^ (-q)`. -/
theorem gamma_rpow_moment {a r q : ℝ} (ha : 0 < a) (hr : 0 < r)
    (haq : 0 < a + q) :
    (∫ x : ℝ, x ^ q ∂gammaMeasure a r) =
      r ^ (-q) * Gamma (a + q) / Gamma a := by
  have hpdf_meas : Measurable (gammaPDF a r) :=
    (measurable_gammaPDFReal a r).ennreal_ofReal
  have hpdf_top : ∀ᵐ x : ℝ ∂volume, gammaPDF a r x < ∞ := by
    filter_upwards with x
    simp [gammaPDF]
  rw [gammaMeasure,
    integral_withDensity_eq_integral_toReal_smul hpdf_meas hpdf_top]
  have hpdf_nonneg : ∀ x : ℝ, 0 ≤ gammaPDFReal a r x :=
    gammaPDFReal_nonneg ha hr
  simp_rw [gammaPDF, ENNReal.toReal_ofReal (hpdf_nonneg _)]
  simp only [smul_eq_mul]
  calc
    (∫ x : ℝ, gammaPDFReal a r x * x ^ q) =
        ∫ x : ℝ in Ici 0, gammaPDFReal a r x * x ^ q := by
      rw [← integral_indicator measurableSet_Ici]
      apply integral_congr_ae
      filter_upwards with x
      rw [indicator_apply]
      split_ifs with hx
      · rfl
      · simp only [mem_Ici, not_le] at hx
        simp [gammaPDFReal, not_le.mpr hx]
    _ = ∫ x : ℝ in Ioi 0,
          (r ^ a / Gamma a) * (x ^ (a + q - 1) * exp (-(r * x))) := by
      rw [integral_Ici_eq_integral_Ioi]
      apply setIntegral_congr_fun measurableSet_Ioi
      intro x hx
      change 0 < x at hx
      simp only [gammaPDFReal, if_pos hx.le]
      rw [show a + q - 1 = (a - 1) + q by ring,
        Real.rpow_add hx (a - 1) q]
      ring
    _ = (r ^ a / Gamma a) * ((1 / r) ^ (a + q) * Gamma (a + q)) := by
      rw [integral_const_mul, integral_rpow_mul_exp_neg_mul_Ioi haq hr]
    _ = r ^ (-q) * Gamma (a + q) / Gamma a := by
      rw [one_div, inv_rpow hr.le, ← Real.rpow_neg hr.le]
      have hrpow : r ^ a * r ^ (-(a + q)) = r ^ (-q) := by
        rw [← Real.rpow_add hr]
        congr 1
        ring
      rw [div_mul_eq_mul_div, ← mul_assoc, hrpow]

/-- The mean of a gamma law with shape `a` and rate `r` is `a / r`. -/
theorem gamma_firstMoment {a r : ℝ} (ha : 0 < a) (hr : 0 < r) :
    (∫ x : ℝ, x ∂gammaMeasure a r) = a / r := by
  have h := gamma_rpow_moment (a := a) (r := r) (q := 1)
    ha hr (by linarith)
  have hGamma : Gamma a ≠ 0 := (Gamma_pos_of_pos ha).ne'
  have h' : (∫ x : ℝ, x ∂gammaMeasure a r) = r⁻¹ * a := by
    simpa [Real.rpow_one, Real.rpow_neg_one, Gamma_add_one ha.ne', hGamma,
      div_eq_mul_inv, mul_assoc] using h
  calc
    (∫ x : ℝ, x ∂gammaMeasure a r) = r⁻¹ * a := h'
    _ = a / r := by field_simp

/-- The second moment of a gamma law with shape `a` and rate `r`. -/
theorem gamma_secondMoment {a r : ℝ} (ha : 0 < a) (hr : 0 < r) :
    (∫ x : ℝ, x ^ (2 : ℕ) ∂gammaMeasure a r) = a * (a + 1) / r ^ 2 := by
  have h := gamma_rpow_moment (a := a) (r := r) (q := 2)
    ha hr (by linarith)
  have ha1 : a + 1 ≠ 0 := by linarith
  have hGamma : Gamma a ≠ 0 := (Gamma_pos_of_pos ha).ne'
  rw [show a + (2 : ℝ) = (a + 1) + 1 by ring,
    Gamma_add_one ha1, Gamma_add_one ha.ne'] at h
  have h' : (∫ x : ℝ, x ^ (2 : ℕ) ∂gammaMeasure a r) =
      r ^ (-2 : ℝ) * ((a + 1) * (a * Gamma a)) / Gamma a := by
    simpa [Real.rpow_two] using h
  calc
    (∫ x : ℝ, x ^ (2 : ℕ) ∂gammaMeasure a r) =
        r ^ (-2 : ℝ) * ((a + 1) * (a * Gamma a)) / Gamma a := h'
    _ = a * (a + 1) / r ^ 2 := by
      rw [show (-2 : ℝ) = -(2 : ℝ) by norm_num,
        Real.rpow_neg hr.le, Real.rpow_two]
      field_simp [hGamma, hr.ne']

/-- The variance of a gamma law with shape `a` and rate `r` is `a / r ^ 2`. -/
theorem gamma_centeredSecondMoment {a r : ℝ} (ha : 0 < a) (hr : 0 < r) :
    (∫ x : ℝ, (x - a / r) ^ 2 ∂gammaMeasure a r) = a / r ^ 2 := by
  letI : IsProbabilityMeasure (gammaMeasure a r) :=
    isProbabilityMeasure_gammaMeasure ha hr
  have hmean_pos : 0 < a / r := div_pos ha hr
  have hsecond_pos : 0 < a * (a + 1) / r ^ 2 := by positivity
  have hInt1 : Integrable (fun x : ℝ => x) (gammaMeasure a r) := by
    by_contra h
    have hz := integral_undef h
    rw [gamma_firstMoment ha hr] at hz
    exact hmean_pos.ne' hz
  have hInt2 : Integrable (fun x : ℝ => x ^ 2) (gammaMeasure a r) := by
    by_contra h
    have hz := integral_undef h
    rw [gamma_secondMoment ha hr] at hz
    exact hsecond_pos.ne' hz
  have hIntLinear : Integrable (fun x : ℝ => (2 * (a / r)) * x)
      (gammaMeasure a r) := hInt1.const_mul _
  calc
    (∫ x : ℝ, (x - a / r) ^ 2 ∂gammaMeasure a r) =
        ∫ x : ℝ, (x ^ 2 - (2 * (a / r)) * x) + (a / r) ^ 2
          ∂gammaMeasure a r := by
      apply integral_congr_ae
      filter_upwards with x
      ring
    _ = (∫ x : ℝ, x ^ 2 ∂gammaMeasure a r) -
          (2 * (a / r)) * (∫ x : ℝ, x ∂gammaMeasure a r) + (a / r) ^ 2 := by
      have hConst : Integrable (fun _ : ℝ => (a / r) ^ 2)
          (gammaMeasure a r) := integrable_const _
      have hAdd := integral_add (hInt2.sub hIntLinear) hConst
      change (∫ x : ℝ, (x ^ 2 - (2 * (a / r)) * x) + (a / r) ^ 2
          ∂gammaMeasure a r) =
        (∫ x : ℝ, x ^ 2 - (2 * (a / r)) * x ∂gammaMeasure a r) +
          ∫ _x : ℝ, (a / r) ^ 2 ∂gammaMeasure a r at hAdd
      have hSub := integral_sub hInt2 hIntLinear
      change (∫ x : ℝ, x ^ 2 - (2 * (a / r)) * x ∂gammaMeasure a r) =
        (∫ x : ℝ, x ^ 2 ∂gammaMeasure a r) -
          ∫ x : ℝ, (2 * (a / r)) * x ∂gammaMeasure a r at hSub
      rw [hAdd, hSub, integral_const_mul]
      simp
    _ = a / r ^ 2 := by
      rw [gamma_firstMoment ha hr, gamma_secondMoment ha hr]
      field_simp [hr.ne']
      ring

/-- Every real-power moment of `Gamma(2, 1)` above the integrability threshold. -/
theorem gammaTwoOne_rpow_moment (q : ℝ) (hq : -2 < q) :
    (∫ x : ℝ, x ^ q ∂gammaMeasure 2 1) = Gamma (q + 2) := by
  have h := gamma_rpow_moment (a := 2) (r := 1) (q := q)
    (by norm_num) (by norm_num) (by linarith)
  simpa [add_comm] using h

/-- The inverse moment used in the corrected-tail Taylor estimate. -/
theorem gammaTwoOne_inverseMoment (a : ℝ) (ha : 0 < a) :
    (∫ x : ℝ, x ^ (a - 2) ∂gammaMeasure 2 1) = Gamma a := by
  simpa only [sub_add_cancel] using gammaTwoOne_rpow_moment (a - 2) (by linarith)

/-- The first real-power moment of `Gamma(2, 1)` is two. -/
theorem gammaTwoOne_firstMoment :
    (∫ x : ℝ, x ∂gammaMeasure 2 1) = 2 := by
  simpa using gamma_firstMoment (a := 2) (r := 1) (by norm_num) (by norm_num)

/-- The second real-power moment of `Gamma(2, 1)` is six. -/
theorem gammaTwoOne_secondMoment :
    (∫ x : ℝ, x ^ (2 : ℕ) ∂gammaMeasure 2 1) = 6 := by
  have h := gamma_secondMoment (a := 2) (r := 1) (by norm_num) (by norm_num)
  norm_num at h ⊢
  exact h

/-- The centered second moment, hence the variance, of `Gamma(2, 1)` is two. -/
theorem gammaTwoOne_centeredSecondMoment :
    (∫ x : ℝ, (x - 2) ^ 2 ∂gammaMeasure 2 1) = 2 := by
  simpa using gamma_centeredSecondMoment (a := 2) (r := 1)
    (by norm_num) (by norm_num)

end RiemannPrimeResolvent

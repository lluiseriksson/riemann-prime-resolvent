import Mathlib.Probability.Distributions.Gamma
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-!
# Moments of the `Gamma(2, 1)` law

This file proves directly from Mathlib's gamma density the real-power moment
formula used in the mean-corrected gamma approximation to Riemann Xi.  It
makes no statement about zeta zeros.
-/

open MeasureTheory Real Set
open scoped ENNReal NNReal

noncomputable section

namespace RiemannPrimeResolvent

open ProbabilityTheory

/-- The `Gamma(2, 1)` density is `x * exp (-x)` on the positive half-line. -/
theorem gammaPDFReal_two_one (x : ℝ) :
    gammaPDFReal 2 1 x = if 0 ≤ x then x * exp (-x) else 0 := by
  rw [gammaPDFReal]
  have hGamma : Gamma (2 : ℝ) = 1 := by
    have h := Real.Gamma_nat_eq_factorial 1
    norm_num at h ⊢
  rw [hGamma]
  split_ifs with hx
  · rw [show (1 : ℝ) ^ (2 : ℝ) = 1 by simp]
    rw [show x ^ ((2 : ℝ) - 1) = x by norm_num [Real.rpow_one]]
    ring_nf
  · rfl

/-- Every real-power moment of `Gamma(2, 1)` above the integrability threshold. -/
theorem gammaTwoOne_rpow_moment (q : ℝ) (hq : -2 < q) :
    (∫ x : ℝ, x ^ q ∂gammaMeasure 2 1) = Gamma (q + 2) := by
  have hpdf_meas : Measurable (gammaPDF 2 1) :=
    (measurable_gammaPDFReal 2 1).ennreal_ofReal
  have hpdf_top : ∀ᵐ x : ℝ ∂volume, gammaPDF 2 1 x < ∞ := by
    filter_upwards with x
    simp [gammaPDF]
  rw [gammaMeasure,
    integral_withDensity_eq_integral_toReal_smul hpdf_meas hpdf_top]
  have hpdf_nonneg : ∀ x : ℝ, 0 ≤ gammaPDFReal 2 1 x :=
    gammaPDFReal_nonneg (by norm_num) (by norm_num)
  simp_rw [gammaPDF, ENNReal.toReal_ofReal (hpdf_nonneg _)]
  simp only [smul_eq_mul]
  calc
    (∫ x : ℝ, gammaPDFReal 2 1 x * x ^ q) =
        ∫ x : ℝ in Ioi 0, x ^ (q + 1) * exp (-x) := by
      rw [← integral_indicator measurableSet_Ioi]
      apply integral_congr_ae
      filter_upwards with x
      rw [indicator_apply]
      split_ifs with hx
      · rw [gammaPDFReal_two_one, if_pos hx.le]
        rw [Real.rpow_add hx q 1, Real.rpow_one]
        ring
      · by_cases hx0 : x = 0
        · simp [hx0, gammaPDFReal_two_one]
        · have hxneg : x < 0 := lt_of_le_of_ne (not_lt.mp hx) hx0
          rw [gammaPDFReal_two_one, if_neg (not_le.mpr hxneg)]
          simp
    _ = Gamma (q + 2) := by
      have h := Real.integral_rpow_mul_exp_neg_mul_Ioi (a := q + 2) (r := 1)
        (by linarith) (by norm_num)
      convert h using 1 <;> ring_nf
      simp

/-- The inverse moment used in the corrected-tail Taylor estimate. -/
theorem gammaTwoOne_inverseMoment (a : ℝ) (ha : 0 < a) :
    (∫ x : ℝ, x ^ (a - 2) ∂gammaMeasure 2 1) = Gamma a := by
  simpa only [sub_add_cancel] using gammaTwoOne_rpow_moment (a - 2) (by linarith)

/-- The first real-power moment of `Gamma(2, 1)` is two. -/
theorem gammaTwoOne_firstMoment :
    (∫ x : ℝ, x ∂gammaMeasure 2 1) = 2 := by
  have hGamma : Gamma (3 : ℝ) = 2 := by
    have h := Real.Gamma_nat_eq_factorial 2
    norm_num at h ⊢
  have h := gammaTwoOne_rpow_moment 1 (by norm_num)
  norm_num at h
  exact h

/-- The second real-power moment of `Gamma(2, 1)` is six. -/
theorem gammaTwoOne_secondMoment :
    (∫ x : ℝ, x ^ (2 : ℕ) ∂gammaMeasure 2 1) = 6 := by
  have hGamma : Gamma (4 : ℝ) = 6 := by
    have h := Real.Gamma_nat_eq_factorial 3
    norm_num at h ⊢
  have h := gammaTwoOne_rpow_moment 2 (by norm_num)
  norm_num at h
  exact h

/-- The centered second moment, hence the variance, of `Gamma(2, 1)` is two. -/
theorem gammaTwoOne_centeredSecondMoment :
    (∫ x : ℝ, (x - 2) ^ 2 ∂gammaMeasure 2 1) = 2 := by
  letI : IsProbabilityMeasure (gammaMeasure 2 1) :=
    isProbabilityMeasure_gammaMeasure (by norm_num) (by norm_num)
  have hInt1 : Integrable (fun x : ℝ => x) (gammaMeasure 2 1) := by
    by_contra h
    have hz := integral_undef h
    rw [gammaTwoOne_firstMoment] at hz
    norm_num at hz
  have hInt2 : Integrable (fun x : ℝ => x ^ 2) (gammaMeasure 2 1) := by
    by_contra h
    have hz := integral_undef h
    rw [gammaTwoOne_secondMoment] at hz
    norm_num at hz
  have hInt4x : Integrable (fun x : ℝ => 4 * x) (gammaMeasure 2 1) :=
    hInt1.const_mul 4
  calc
    (∫ x : ℝ, (x - 2) ^ 2 ∂gammaMeasure 2 1) =
        ∫ x : ℝ, (x ^ 2 - 4 * x) + 4 ∂gammaMeasure 2 1 := by
      apply integral_congr_ae
      filter_upwards with x
      ring
    _ = (∫ x : ℝ, x ^ 2 ∂gammaMeasure 2 1) -
          (∫ x : ℝ, 4 * x ∂gammaMeasure 2 1) + 4 := by
      have hAdd :
          (∫ x : ℝ, (x ^ 2 - 4 * x) + 4 ∂gammaMeasure 2 1) =
            (∫ x : ℝ, x ^ 2 - 4 * x ∂gammaMeasure 2 1) +
              ∫ _x : ℝ, 4 ∂gammaMeasure 2 1 := by
        have h := integral_add (hInt2.sub hInt4x) (integrable_const 4)
        change (∫ x : ℝ, (x ^ 2 - 4 * x) + 4 ∂gammaMeasure 2 1) =
          (∫ x : ℝ, x ^ 2 - 4 * x ∂gammaMeasure 2 1) +
            ∫ _x : ℝ, 4 ∂gammaMeasure 2 1 at h
        exact h
      have hSub :
          (∫ x : ℝ, x ^ 2 - 4 * x ∂gammaMeasure 2 1) =
            (∫ x : ℝ, x ^ 2 ∂gammaMeasure 2 1) -
              ∫ x : ℝ, 4 * x ∂gammaMeasure 2 1 := by
        simpa only [Pi.sub_apply] using integral_sub hInt2 hInt4x
      rw [hAdd, hSub]
      simp
    _ = 2 := by
      rw [gammaTwoOne_secondMoment, integral_const_mul 4,
        gammaTwoOne_firstMoment]
      norm_num

end RiemannPrimeResolvent

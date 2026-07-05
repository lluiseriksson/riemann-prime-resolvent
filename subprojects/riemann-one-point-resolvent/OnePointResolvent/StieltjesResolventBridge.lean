import OnePointResolvent.StieltjesCompactBound
import Mathlib.MeasureTheory.Measure.ResolventTransform

/-!
# Finite Stieltjes sums as Mathlib resolvent transforms

Positive finite atomic Stieltjes sums are represented exactly by Mathlib's
`MeasureTheory.resolventTransform`.  Mathlib uses the kernel `(t - a)⁻¹`, so
our convention `(t + z)⁻¹` is obtained at the sign-changed argument `a = -z`.
-/

set_option autoImplicit false

namespace OnePointResolvent

open scoped BigOperators

/-- The finite positive atomic measure associated with weights and spectral
locations. Negative weights are truncated by `Real.toNNReal`; the bridge theorem
assumes nonnegativity on the active finset, so no truncation occurs there. -/
noncomputable def finitePositiveStieltjesMeasure
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ) : MeasureTheory.Measure ℝ :=
  ∑ i ∈ s, (weight i).toNNReal • MeasureTheory.Measure.dirac (spectrum i)

/-- Exact convention bridge to Mathlib's resolvent transform. -/
theorem resolventTransform_finitePositiveStieltjesMeasure
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ) (z : ℂ)
    (hweight : ∀ i ∈ s, 0 ≤ weight i) :
    MeasureTheory.resolventTransform
        (finitePositiveStieltjesMeasure s weight spectrum) (-z) =
      finitePositiveStieltjes s weight spectrum z := by
  classical
  rw [MeasureTheory.resolventTransform_apply, finitePositiveStieltjesMeasure,
    MeasureTheory.integral_finsetSum_measure]
  · unfold finitePositiveStieltjes
    apply Finset.sum_congr rfl
    intro i hi
    rw [MeasureTheory.integral_smul_nnreal_measure,
      MeasureTheory.integral_dirac]
    simp [NNReal.smul_def, Real.coe_toNNReal (weight i) (hweight i hi),
      resolvent, Ring.inverse_eq_inv', div_eq_mul_inv]
  · intro i hi
    exact (MeasureTheory.integrable_dirac (by simp)).smul_measure_nnreal

end OnePointResolvent

import PrimeResolvent.HausdorffFinite

/-!
# Resolvent compactification

For `x₀ > 0` and spectral parameter `λ ≥ 0`, the map

`λ ↦ x₀ / (λ + x₀)`

lands in `[0,1]`.  Together with the positive weight
`(λ+x₀)⁻¹`, it turns finite squared-resolvent moments into finite Hausdorff
moments.
-/

set_option autoImplicit false

namespace PrimeResolvent

open scoped BigOperators

/-- Positive resolvent weight at base point `x₀`. -/
def resolventWeight (x₀ λ : ℝ) : ℝ :=
  (λ + x₀)⁻¹

/-- Compactified spectral coordinate. -/
def compactifiedPoint (x₀ λ : ℝ) : ℝ :=
  x₀ / (λ + x₀)

/-- Finite resolvent moment sequence at a fixed base point. -/
def finiteResolventMoment
    {ι : Type*} [Fintype ι]
    (x₀ : ℝ) (spectrum : ι → ℝ) (n : ℕ) : ℝ :=
  atomicMoment
    (fun i => resolventWeight x₀ (spectrum i))
    (fun i => compactifiedPoint x₀ (spectrum i)) n

lemma spectrum_shift_pos {x₀ λ : ℝ} (hx₀ : 0 < x₀) (hλ : 0 ≤ λ) :
    0 < λ + x₀ := by
  linarith

/-- Resolvent weights are nonnegative on a nonnegative spectrum. -/
theorem resolventWeight_nonneg {x₀ λ : ℝ}
    (hx₀ : 0 < x₀) (hλ : 0 ≤ λ) :
    0 ≤ resolventWeight x₀ λ := by
  unfold resolventWeight
  exact inv_nonneg.mpr (le_of_lt (spectrum_shift_pos hx₀ hλ))

/-- Compactified spectral coordinates are nonnegative. -/
theorem compactifiedPoint_nonneg {x₀ λ : ℝ}
    (hx₀ : 0 < x₀) (hλ : 0 ≤ λ) :
    0 ≤ compactifiedPoint x₀ λ := by
  unfold compactifiedPoint
  exact div_nonneg (le_of_lt hx₀)
    (le_of_lt (spectrum_shift_pos hx₀ hλ))

/-- Compactified spectral coordinates are at most one. -/
theorem compactifiedPoint_le_one {x₀ λ : ℝ}
    (hx₀ : 0 < x₀) (hλ : 0 ≤ λ) :
    compactifiedPoint x₀ λ ≤ 1 := by
  unfold compactifiedPoint
  apply (div_le_one (spectrum_shift_pos hx₀ hλ)).2
  linarith

/-- Every finite nonnegative spectrum gives a completely monotone resolvent
moment sequence. -/
theorem finiteResolventMoment_isHausdorffCompletelyMonotone
    {ι : Type*} [Fintype ι]
    (x₀ : ℝ) (spectrum : ι → ℝ)
    (hx₀ : 0 < x₀)
    (hspectrum : ∀ i, 0 ≤ spectrum i) :
    IsHausdorffCompletelyMonotone
      (finiteResolventMoment x₀ spectrum) := by
  unfold finiteResolventMoment
  apply atomicMoment_isHausdorffCompletelyMonotone
  · intro i
    exact resolventWeight_nonneg hx₀ (hspectrum i)
  · intro i
    exact compactifiedPoint_nonneg hx₀ (hspectrum i)
  · intro i
    exact compactifiedPoint_le_one hx₀ (hspectrum i)

/-- Explicit nonnegativity of every finite Hausdorff difference of a finite
resolvent moment sequence. -/
theorem finiteResolventMoment_hausdorffDiff_nonneg
    {ι : Type*} [Fintype ι]
    (x₀ : ℝ) (spectrum : ι → ℝ)
    (hx₀ : 0 < x₀)
    (hspectrum : ∀ i, 0 ≤ spectrum i)
    (k n : ℕ) :
    0 ≤ hausdorffDiff k (finiteResolventMoment x₀ spectrum) n :=
  finiteResolventMoment_isHausdorffCompletelyMonotone
    x₀ spectrum hx₀ hspectrum k n

end PrimeResolvent

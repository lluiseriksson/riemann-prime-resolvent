import PrimeResolvent.Basic

/-!
# Finite atomic Hausdorff moments

For a finite positive measure supported in `[0,1]`, every signed forward
difference of its moment sequence is nonnegative.  The proof exposes the exact
identity

`D^k b_n = Σ_i w_i p_i^n (1-p_i)^k`.
-/

set_option autoImplicit false

namespace PrimeResolvent

open scoped BigOperators

/-- Exact finite atomic formula for the signed Hausdorff differences. -/
theorem hausdorffDiff_atomicMoment
    {ι : Type*} [Fintype ι]
    (weight point : ι → ℝ) (k n : ℕ) :
    hausdorffDiff k (atomicMoment weight point) n =
      ∑ i, weight i * point i ^ n * (1 - point i) ^ k := by
  classical
  induction k generalizing n with
  | zero =>
      simp [hausdorffDiff, atomicMoment]
  | succ k ih =>
      simp only [hausdorffDiff]
      rw [ih n, ih (n + 1), ← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro i hi
      simp only [pow_succ]
      ring

/-- A finite positive atomic measure supported in `[0,1]` has a completely
monotone moment sequence. -/
theorem atomicMoment_isHausdorffCompletelyMonotone
    {ι : Type*} [Fintype ι]
    (weight point : ι → ℝ)
    (hweight : ∀ i, 0 ≤ weight i)
    (hpoint0 : ∀ i, 0 ≤ point i)
    (hpoint1 : ∀ i, point i ≤ 1) :
    IsHausdorffCompletelyMonotone (atomicMoment weight point) := by
  intro k n
  rw [hausdorffDiff_atomicMoment]
  classical
  apply Finset.sum_nonneg
  intro i hi
  exact mul_nonneg
    (mul_nonneg (hweight i) (pow_nonneg (hpoint0 i) n))
    (pow_nonneg (sub_nonneg.mpr (hpoint1 i)) k)

/-- Pointwise version of the preceding theorem. -/
theorem hausdorffDiff_atomicMoment_nonneg
    {ι : Type*} [Fintype ι]
    (weight point : ι → ℝ)
    (hweight : ∀ i, 0 ≤ weight i)
    (hpoint0 : ∀ i, 0 ≤ point i)
    (hpoint1 : ∀ i, point i ≤ 1)
    (k n : ℕ) :
    0 ≤ hausdorffDiff k (atomicMoment weight point) n :=
  atomicMoment_isHausdorffCompletelyMonotone
    weight point hweight hpoint0 hpoint1 k n

end PrimeResolvent

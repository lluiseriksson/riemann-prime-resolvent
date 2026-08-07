import Mathlib.Algebra.Order.Group.PosPart
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Signed balance versus a nonnegative lift

The adelic product formula is a signed cancellation law.  Reflection-positive
models, by contrast, start from nonnegative weights.  This file isolates the
finite algebraic obstruction: replacing a signed balanced family by its
positive and negative masses turns exact cancellation into total variation.
-/

open scoped BigOperators

namespace RiemannPrimeResolvent

/-- In a balanced finite real family, total positive mass equals total
negative mass. -/
theorem sum_posPart_eq_sum_negPart_of_sum_eq_zero
    {ι : Type*} (s : Finset ι) (a : ι → ℝ)
    (hbalance : ∑ i ∈ s, a i = 0) :
    (∑ i ∈ s, (a i)⁺) = ∑ i ∈ s, (a i)⁻ := by
  have hdecomp :
      (∑ i ∈ s, (a i)⁺) - (∑ i ∈ s, (a i)⁻) = 0 := by
    rw [← Finset.sum_sub_distrib]
    simpa only [posPart_sub_negPart] using hbalance
  linarith

/-- For a balanced family, the total variation is twice its positive mass. -/
theorem sum_abs_eq_two_mul_sum_posPart_of_sum_eq_zero
    {ι : Type*} (s : Finset ι) (a : ι → ℝ)
    (hbalance : ∑ i ∈ s, a i = 0) :
    (∑ i ∈ s, |a i|) = 2 * ∑ i ∈ s, (a i)⁺ := by
  have hparts := sum_posPart_eq_sum_negPart_of_sum_eq_zero s a hbalance
  calc
    (∑ i ∈ s, |a i|) = ∑ i ∈ s, ((a i)⁺ + (a i)⁻) := by
      apply Finset.sum_congr rfl
      intro i hi
      exact (posPart_add_negPart (a i)).symm
    _ = (∑ i ∈ s, (a i)⁺) + ∑ i ∈ s, (a i)⁻ := by
      rw [Finset.sum_add_distrib]
    _ = 2 * ∑ i ∈ s, (a i)⁺ := by rw [← hparts]; ring

/-- A nonzero signed balance has zero squared total but strictly positive
total variation.  Thus taking absolute values/nonnegative weights is not a
faithful route from the product formula to a positive quadratic form. -/
theorem signedBalance_square_zero_but_totalVariation_pos
    {ι : Type*} (s : Finset ι) (a : ι → ℝ)
    (hbalance : ∑ i ∈ s, a i = 0)
    (hnontrivial : ∃ i ∈ s, a i ≠ 0) :
    (∑ i ∈ s, a i) ^ 2 = 0 ∧ 0 < ∑ i ∈ s, |a i| := by
  constructor
  · rw [hbalance]
    norm_num
  · apply Finset.sum_pos'
    · intro i hi
      exact abs_nonneg (a i)
    · obtain ⟨i, hi, hne⟩ := hnontrivial
      exact ⟨i, hi, abs_pos.mpr hne⟩

end RiemannPrimeResolvent

import Mathlib

/-!
# Variance rigidity for positive finite lifts

This module formalizes the finite algebraic obstruction behind a positive
"black center plus red children" replacement.  Matching mass and barycenter
forces the second-moment defect to be a sum of nonnegative squares.  It makes
no claim about the infinite prime measure or the Riemann hypothesis.
-/

namespace RiemannPrimeResolvent

open scoped BigOperators

/-- The second-moment defect of a finite weighted cloud with prescribed mass
and barycenter is exactly its weighted central second moment. -/
theorem secondMoment_sub_mass_mul_center_sq_eq_variance
    {ι : Type*} (s : Finset ι) (weight point : ι → ℝ) (mass center : ℝ)
    (hmass : ∑ i ∈ s, weight i = mass)
    (hbarycenter : ∑ i ∈ s, weight i * point i = mass * center) :
    (∑ i ∈ s, weight i * point i ^ 2) - mass * center ^ 2 =
      ∑ i ∈ s, weight i * (point i - center) ^ 2 := by
  have hexpand :
      (∑ i ∈ s, weight i * (point i - center) ^ 2) =
        ∑ i ∈ s,
          (weight i * point i ^ 2 - 2 * center * (weight i * point i) +
            center ^ 2 * weight i) := by
    apply Finset.sum_congr rfl
    intro i hi
    ring
  rw [hexpand, Finset.sum_add_distrib, Finset.sum_sub_distrib]
  have hcenterSum :
      (∑ i ∈ s, center ^ 2 * weight i) = center ^ 2 * (∑ i ∈ s, weight i) := by
    rw [Finset.mul_sum]
  have hcrossSum :
      (∑ i ∈ s, 2 * center * (weight i * point i)) =
        2 * center * (∑ i ∈ s, weight i * point i) := by
    rw [Finset.mul_sum]
  rw [hcenterSum, hcrossSum, hmass, hbarycenter]
  ring

/-- A positive finite lift with fixed mass and barycenter cannot have a
negative second-moment defect. -/
theorem secondMoment_sub_mass_mul_center_sq_nonneg
    {ι : Type*} (s : Finset ι) (weight point : ι → ℝ) (mass center : ℝ)
    (hweight : ∀ i ∈ s, 0 ≤ weight i)
    (hmass : ∑ i ∈ s, weight i = mass)
    (hbarycenter : ∑ i ∈ s, weight i * point i = mass * center) :
    0 ≤ (∑ i ∈ s, weight i * point i ^ 2) - mass * center ^ 2 := by
  rw [secondMoment_sub_mass_mul_center_sq_eq_variance s weight point mass center
    hmass hbarycenter]
  exact Finset.sum_nonneg fun i hi => mul_nonneg (hweight i hi) (sq_nonneg _)

/-- If a positive finite lift also matches the black atom's second moment,
then every child of strictly positive weight lies at the black center. -/
theorem point_eq_center_of_secondMoment_eq
    {ι : Type*} (s : Finset ι) (weight point : ι → ℝ) (mass center : ℝ)
    (hweight : ∀ i ∈ s, 0 ≤ weight i)
    (hmass : ∑ i ∈ s, weight i = mass)
    (hbarycenter : ∑ i ∈ s, weight i * point i = mass * center)
    (hsecond : ∑ i ∈ s, weight i * point i ^ 2 = mass * center ^ 2)
    {i : ι} (hi : i ∈ s) (hwi : 0 < weight i) :
    point i = center := by
  have hvariance : ∑ j ∈ s, weight j * (point j - center) ^ 2 = 0 := by
    rw [← secondMoment_sub_mass_mul_center_sq_eq_variance s weight point mass center
      hmass hbarycenter, hsecond]
    ring
  have hterm : weight i * (point i - center) ^ 2 = 0 := by
    have hall : ∀ j ∈ s, 0 ≤ weight j * (point j - center) ^ 2 :=
      fun j hj => mul_nonneg (hweight j hj) (sq_nonneg _)
    exact (Finset.sum_eq_zero_iff_of_nonneg hall).mp hvariance i hi
  have hsquare : (point i - center) ^ 2 = 0 := (mul_eq_zero.mp hterm).resolve_left (ne_of_gt hwi)
  nlinarith [sq_nonneg (point i - center)]

end RiemannPrimeResolvent

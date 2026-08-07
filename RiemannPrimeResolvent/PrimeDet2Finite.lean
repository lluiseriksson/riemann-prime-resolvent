import Mathlib.Analysis.Complex.Exponential

/-!
# Finite Carleman--Fredholm cancellation for Euler factors

This module records the exact finite identity underlying the `det₂` reduction.
It does **not** construct an infinite regularized determinant and makes no
claim about analytic continuation or the Riemann hypothesis.
-/

open scoped BigOperators

namespace RiemannPrimeResolvent

noncomputable section

variable {ι : Type*}

/-- Finite inverse Euler product associated with complex activities `q`. -/
def finiteEulerInverse (S : Finset ι) (q : ι → ℂ) : ℂ :=
  ∏ i ∈ S, (1 - q i)⁻¹

/-- Finite order-two regularized determinant factor. -/
def finiteDet2 (S : Finset ι) (q : ι → ℂ) : ℂ :=
  ∏ i ∈ S, (1 - q i) * Complex.exp (q i)

/-- The inverse Euler product times its order-two regularized determinant is
exactly the exponential of the first cumulant. -/
theorem finiteEulerInverse_mul_finiteDet2 (S : Finset ι) (q : ι → ℂ)
    (hunit : ∀ i ∈ S, 1 - q i ≠ 0) :
    finiteEulerInverse S q * finiteDet2 S q =
      Complex.exp (∑ i ∈ S, q i) := by
  rw [Complex.exp_sum]
  simp only [finiteEulerInverse, finiteDet2, ← Finset.prod_mul_distrib]
  apply Finset.prod_congr rfl
  intro i hi
  rw [← mul_assoc, inv_mul_cancel₀ (hunit i hi), one_mul]

/-- Every finite regularized determinant factor is nonzero when none of the
activities equals one. -/
theorem finiteDet2_ne_zero (S : Finset ι) (q : ι → ℂ)
    (hunit : ∀ i ∈ S, 1 - q i ≠ 0) :
    finiteDet2 S q ≠ 0 := by
  apply Finset.prod_ne_zero_iff.mpr
  intro i hi
  exact mul_ne_zero (hunit i hi) (Complex.exp_ne_zero (q i))

end

end RiemannPrimeResolvent

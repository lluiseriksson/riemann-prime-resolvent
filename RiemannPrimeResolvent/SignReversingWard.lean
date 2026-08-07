import Mathlib.Algebra.BigOperators.Group.Finset.Defs
import Mathlib.Tactic

/-!
# Finite sign-reversing Ward cancellation

This module formalizes the finite involution principle used by the self-dual
divisor block.  It is deliberately abstract and finite; it makes no claim
that the required multiscale arithmetic involution exists.
-/

open scoped BigOperators

namespace RiemannPrimeResolvent

/-- A sign-reversing involution cancels every invariant observable.

This is the finite algebraic content of the divisor-complement Ward identity.
The hard analytic issue is coverage: constructing such involutions on the
full critical band with a controlled displacement is not asserted here. -/
theorem sum_weight_mul_value_eq_zero_of_signReversingInvolution
    {ι : Type*} [Fintype ι]
    (tau : ι → ι) (htau : Function.Involutive tau)
    (weight value : ι → ℝ)
    (hweight : ∀ i, weight (tau i) = -weight i)
    (hvalue : ∀ i, value (tau i) = value i) :
    ∑ i, weight i * value i = 0 := by
  let e : ι ≃ ι :=
    { toFun := tau
      invFun := tau
      left_inv := htau
      right_inv := htau }
  have hreindex :
      (∑ i, weight (e i) * value (e i)) = ∑ i, weight i * value i :=
    e.sum_comp (fun i => weight i * value i)
  have hneg :
      (∑ i, weight (e i) * value (e i)) = -(∑ i, weight i * value i) := by
    calc
      (∑ i, weight (e i) * value (e i)) = ∑ i, (-weight i) * value i := by
        apply Finset.sum_congr rfl
        intro i _
        change weight (tau i) * value (tau i) = (-weight i) * value i
        rw [hweight, hvalue]
      _ = -(∑ i, weight i * value i) := by
        simp only [neg_mul, Finset.sum_neg_distrib]
  linarith

end RiemannPrimeResolvent

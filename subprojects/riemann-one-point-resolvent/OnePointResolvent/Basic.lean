import Mathlib

/-!
# Atomic moments and signed forward differences

This file contains finite sums only. It is independent of the Riemann zeta function and measure theory.
-/

set_option autoImplicit false

namespace OnePointResolvent

open scoped BigOperators

/-- Finite atomic moment sequence associated with weights and points. -/
def atomicMoment {ι : Type*} [Fintype ι]
    (weight point : ι → ℝ) (n : ℕ) : ℝ :=
  ∑ i, weight i * point i ^ n

/-- `hausdorffDiff k a n` is `(-1)^k Δ^k a_n`, recursively as `a_n - a_{n+1}`. -/
def hausdorffDiff : ℕ → (ℕ → ℝ) → ℕ → ℝ
  | 0, a, n => a n
  | k + 1, a, n => hausdorffDiff k a n - hausdorffDiff k a (n + 1)

/-- Discrete complete monotonicity used by the Hausdorff moment criterion. -/
def IsHausdorffCompletelyMonotone (a : ℕ → ℝ) : Prop :=
  ∀ k n, 0 ≤ hausdorffDiff k a n

@[simp] theorem hausdorffDiff_zero (a : ℕ → ℝ) (n : ℕ) :
    hausdorffDiff 0 a n = a n := rfl

@[simp] theorem hausdorffDiff_succ (k : ℕ) (a : ℕ → ℝ) (n : ℕ) :
    hausdorffDiff (k + 1) a n =
      hausdorffDiff k a n - hausdorffDiff k a (n + 1) := rfl

end OnePointResolvent

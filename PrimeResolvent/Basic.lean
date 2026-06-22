/-!
# Atomic moments and signed forward differences

This file contains only finite sums.  It is independent of the Riemann zeta
function and of measure theory.
-/

import Mathlib

set_option autoImplicit false

namespace PrimeResolvent

open scoped BigOperators

/-- The finite atomic moment sequence associated with weights `weight` and
points `point`. -/
def atomicMoment {ι : Type*} [Fintype ι]
    (weight point : ι → ℝ) (n : ℕ) : ℝ :=
  ∑ i, weight i * point i ^ n

/-- The signed forward difference used by the Hausdorff moment criterion.

`hausdorffDiff k a n` is `(-1)^k Δ^k a_n`, implemented recursively as
successive differences `a_n - a_{n+1}`. -/
def hausdorffDiff : ℕ → (ℕ → ℝ) → ℕ → ℝ
  | 0, a, n => a n
  | k + 1, a, n => hausdorffDiff k a n - hausdorffDiff k a (n + 1)

/-- A sequence is completely monotone in the discrete Hausdorff sense when
all signed forward differences are nonnegative. -/
def IsHausdorffCompletelyMonotone (a : ℕ → ℝ) : Prop :=
  ∀ k n, 0 ≤ hausdorffDiff k a n

@[simp] theorem hausdorffDiff_zero (a : ℕ → ℝ) (n : ℕ) :
    hausdorffDiff 0 a n = a n := rfl

@[simp] theorem hausdorffDiff_succ (k : ℕ) (a : ℕ → ℝ) (n : ℕ) :
    hausdorffDiff (k + 1) a n =
      hausdorffDiff k a n - hausdorffDiff k a (n + 1) := rfl

end PrimeResolvent

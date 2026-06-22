import Mathlib

/-!
# Three-part comparison budget

The concrete spectral programme naturally separates a comparison into a
spectral/Galerkin error, a model-normalization error, and an arithmetic prime-
tail error.  This file verifies the elementary deterministic glue.
-/

set_option autoImplicit false

namespace PrimeResolvent

/-- Triangle inequality through two intermediate targets. -/
theorem abs_sub_le_three (a b c d : ℝ) :
    |a - d| ≤ |a - b| + |b - c| + |c - d| := by
  calc
    |a - d| = |(a - b) + (b - c) + (c - d)| := by
      congr 1
      ring
    _ ≤ |(a - b) + (b - c)| + |c - d| := abs_add _ _
    _ ≤ (|a - b| + |b - c|) + |c - d| := by
      gcongr
      exact abs_add _ _
    _ = |a - b| + |b - c| + |c - d| := by ring

/-- Named version of the three-error budget used in the paper. -/
theorem primeResolvent_errorBudget
    (spectral model prime target : ℝ) :
    |spectral - target| ≤
      |spectral - model| + |model - prime| + |prime - target| :=
  abs_sub_le_three spectral model prime target

end PrimeResolvent

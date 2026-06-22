import Mathlib

/-!
# Deterministic comparison budget
-/

set_option autoImplicit false

namespace OnePointResolvent

/-- Triangle inequality through two intermediate targets. -/
theorem abs_sub_le_three (a b c d : ℝ) :
    |a - d| ≤ |a - b| + |b - c| + |c - d| := by
  calc
    |a - d| = |(a - b) + (b - c) + (c - d)| := by
      congr 1
      ring
    _ ≤ |(a - b) + (b - c)| + |c - d| := abs_add_le _ _
    _ ≤ (|a - b| + |b - c|) + |c - d| :=
      add_le_add_right (abs_add_le _ _) _
    _ = |a - b| + |b - c| + |c - d| := rfl

/-- Named three-error budget used by the cross-repository interface. -/
theorem resolvent_errorBudget
    (spectral model prime target : ℝ) :
    |spectral - target| ≤
      |spectral - model| + |model - prime| + |prime - target| :=
  abs_sub_le_three spectral model prime target

end OnePointResolvent

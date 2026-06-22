/-
Copyright (c) 2026 Lluís Eriksson.
Released under the GNU Affero General Public License v3.0.
-/

import Mathlib

/-!
# Basic error bookkeeping

This file contains only elementary, unconditional inequalities.  It does not
assert the Riemann hypothesis and it does not assume the existence of a
Hilbert--Pólya operator.
-/

namespace RiemannPrimeResolvent

/-- The three contributions in the proposed prime--resolvent comparison. -/
structure ErrorBudget where
  spectral : ℝ
  prolate : ℝ
  prime : ℝ

/-- Total error assigned to an `ErrorBudget`. -/
def ErrorBudget.total (E : ErrorBudget) : ℝ :=
  E.spectral + E.prolate + E.prime

/-- A nonnegative componentwise budget has nonnegative total cost. -/
theorem ErrorBudget.total_nonneg (E : ErrorBudget)
    (hs : 0 ≤ E.spectral) (hp : 0 ≤ E.prolate) (hprime : 0 ≤ E.prime) :
    0 ≤ E.total := by
  dsimp [ErrorBudget.total]
  linarith

/-- Three-step triangle inequality used by the research decomposition. -/
theorem three_step_triangle (spectral prolate target prime : ℝ) :
    |spectral - prime| ≤
      |spectral - prolate| + |prolate - target| + |target - prime| := by
  have hdecomp :
      spectral - prime =
        (spectral - prolate) + (prolate - target) + (target - prime) := by
    ring
  rw [hdecomp]
  calc
    |(spectral - prolate) + (prolate - target) + (target - prime)|
        ≤ |(spectral - prolate) + (prolate - target)| + |target - prime| :=
      abs_add_le _ _
    _ ≤ (|spectral - prolate| + |prolate - target|) + |target - prime| :=
      add_le_add_right (abs_add_le _ _) _
    _ = |spectral - prolate| + |prolate - target| + |target - prime| := rfl

/-- Replace each term of the three-step triangle inequality by a declared budget. -/
theorem error_le_budget
    (spectral prolate target prime : ℝ) (E : ErrorBudget)
    (hs : |spectral - prolate| ≤ E.spectral)
    (hp : |prolate - target| ≤ E.prolate)
    (hprime : |target - prime| ≤ E.prime) :
    |spectral - prime| ≤ E.total := by
  calc
    |spectral - prime| ≤
        |spectral - prolate| + |prolate - target| + |target - prime| :=
      three_step_triangle spectral prolate target prime
    _ ≤ E.spectral + E.prolate + E.prime := by linarith
    _ = E.total := rfl

end RiemannPrimeResolvent

import Mathlib.Tactic

/-!
# Black diagonal and red off-diagonal pairs

This file formalizes the literal finite count behind the `3 + 6 = 9`
picture.  It is a combinatorial identity only and makes no analytic or RH
claim.
-/

namespace RiemannPrimeResolvent

/-- For a nonempty collection of `r` labels, its ordered pairs split into
`r` diagonal pairs and `r*(r-1)` off-diagonal pairs. -/
theorem blackDiagonal_add_redOffDiagonal (r : ℕ) (hr : 0 < r) :
    r ^ 2 = r + r * (r - 1) := by
  have hsplit : 1 + (r - 1) = r := by omega
  calc
    r ^ 2 = r * r := by simp [pow_two]
    _ = r * (1 + (r - 1)) := by rw [hsplit]
    _ = r + r * (r - 1) := by rw [Nat.mul_add]; simp

end RiemannPrimeResolvent

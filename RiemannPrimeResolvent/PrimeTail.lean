/-
Copyright (c) 2026 Lluís Eriksson.
Released under the GNU Affero General Public License v3.0.
-/

import Mathlib

/-!
# Closed-form model for the omitted-prime tail

The theorem identifying this expression with an upper bound for the von
Mangoldt tail is a future analytic milestone.  The present file formalizes the
closed-form majorant and its elementary sign properties.
-/

namespace RiemannPrimeResolvent

/-- The elementary integral majorant
`X⁻δ (log X / δ + 1 / δ²)`, written without real-power notation. -/
noncomputable def primeTailMajorant (δ X : ℝ) : ℝ :=
  Real.exp (-δ * Real.log X) *
    (Real.log X / δ + 1 / δ ^ 2)

/-- The closed-form tail majorant is nonnegative in its intended range. -/
theorem primeTailMajorant_nonneg {δ X : ℝ}
    (hδ : 0 < δ) (hX : 1 ≤ X) :
    0 ≤ primeTailMajorant δ X := by
  have hlog : 0 ≤ Real.log X := Real.log_nonneg hX
  have hδsq : 0 < δ ^ 2 := sq_pos_of_pos hδ
  unfold primeTailMajorant
  exact mul_nonneg (Real.exp_pos _).le
    (add_nonneg (div_nonneg hlog hδ.le)
      (div_nonneg zero_le_one hδsq.le))

/-- Resolvent-scaled prime tail associated with `a > 1/2` and cutoff `λ²`. -/
noncomputable def resolventPrimeTailMajorant (a λ : ℝ) : ℝ :=
  primeTailMajorant (a - 1 / 2) (λ ^ 2) / (2 * a)

/-- Nonnegativity of the scaled majorant. -/
theorem resolventPrimeTailMajorant_nonneg {a λ : ℝ}
    (ha : 1 / 2 < a) (hλ : 1 ≤ λ) :
    0 ≤ resolventPrimeTailMajorant a λ := by
  have hδ : 0 < a - 1 / 2 := by linarith
  have hλsq : 1 ≤ λ ^ 2 := by nlinarith [sq_nonneg (λ - 1)]
  have ha0 : 0 < 2 * a := by linarith
  unfold resolventPrimeTailMajorant
  exact div_nonneg (primeTailMajorant_nonneg hδ hλsq) ha0.le

end RiemannPrimeResolvent

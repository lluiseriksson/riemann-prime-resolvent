import RiemannPrimeResolvent.TraceZeroPSD
import Mathlib.Tactic

/-!
# Oriented observables and positivity

Spectral data are even in the signed cross term.  To recover its orientation
one must use an odd observable.  This file proves the finite-dimensional
tradeoff: a nonzero linear oriented observable cannot be nonnegative on all
kernels.  The cross term is also exactly a difference of the two reflection
sector compressions, hence a polarization difference rather than a norm.
-/

namespace RiemannPrimeResolvent

/-- General real linear observable on the diagonal balance `a` and oriented
cross term `c`. -/
def orientedLinearObservable (u v a c : ℝ) : ℝ :=
  u * a + v * c

/-- A real linear observable is globally nonnegative only when it is zero. -/
theorem orientedLinearObservable_nonnegative_iff (u v : ℝ) :
    (∀ a c : ℝ, 0 ≤ orientedLinearObservable u v a c) ↔ u = 0 ∧ v = 0 := by
  constructor
  · intro h
    have hu : 0 ≤ u := by
      simpa [orientedLinearObservable] using h 1 0
    have hnu : 0 ≤ -u := by
      simpa [orientedLinearObservable] using h (-1) 0
    have hv : 0 ≤ v := by
      simpa [orientedLinearObservable] using h 0 1
    have hnv : 0 ≤ -v := by
      simpa [orientedLinearObservable] using h 0 (-1)
    exact ⟨by linarith, by linarith⟩
  · rintro ⟨rfl, rfl⟩ a c
    simp [orientedLinearObservable]

/-- Every genuinely cross-sensitive linear observable has a concrete negative
input, independently of its diagonal coefficient. -/
theorem orientedLinearObservable_negative_witness_of_cross_sensitive
    (u : ℝ) {v : ℝ} (hv : v ≠ 0) :
    orientedLinearObservable u v 0 (-v) < 0 := by
  have hs : 0 < v ^ 2 := sq_pos_of_ne_zero hv
  simp only [orientedLinearObservable, mul_zero, zero_add]
  nlinarith

/-- The elementary polarization identity: a signed cross term is a
difference of two nonnegative squares, not itself a square. -/
theorem real_polarization_difference (x y : ℝ) :
    (x + y) ^ 2 - (x - y) ^ 2 = 4 * x * y := by
  ring

/-- For the trace-zero kernel, the difference between symmetric and
antisymmetric reflection compressions is exactly four times the oriented
cross term. -/
theorem traceZeroQuad_reflection_difference (a c : ℝ) :
    traceZeroQuad a c 1 1 - traceZeroQuad a c 1 (-1) = 4 * c := by
  rw [traceZeroQuad_symmetric, traceZeroQuad_antisymmetric]
  ring

/-- Ordering the two reflection sectors is precisely the sign condition on
the cross term.  It is not supplied by positivity of either square alone. -/
theorem traceZeroQuad_reflection_order_iff_cross_nonnegative (a c : ℝ) :
    traceZeroQuad a c 1 (-1) ≤ traceZeroQuad a c 1 1 ↔ 0 ≤ c := by
  rw [traceZeroQuad_symmetric, traceZeroQuad_antisymmetric]
  constructor <;> intro h <;> linarith

end RiemannPrimeResolvent

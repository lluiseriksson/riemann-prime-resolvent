import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Trace-zero two-sector kernels

The rational product formula balances an Archimedean sector against a finite
place sector.  The simplest operator lift is therefore a symmetric `2 x 2`
kernel with zero trace.  This file proves that such a kernel cannot be
positive semidefinite unless it is the zero kernel, even when an arbitrary
cross term is allowed.
-/

namespace RiemannPrimeResolvent

/-- Quadratic form of the general real symmetric trace-zero `2 x 2` matrix
`[[a,c],[c,-a]]`. -/
def traceZeroQuad (a c x y : ℝ) : ℝ :=
  a * x ^ 2 + 2 * c * x * y - a * y ^ 2

/-- A symmetric trace-zero two-sector kernel is PSD exactly when both its
diagonal balance and its cross term vanish. -/
theorem traceZeroQuad_nonnegative_iff (a c : ℝ) :
    (∀ x y : ℝ, 0 ≤ traceZeroQuad a c x y) ↔ a = 0 ∧ c = 0 := by
  constructor
  · intro h
    have ha : 0 ≤ a := by
      simpa [traceZeroQuad] using h 1 0
    have hna : 0 ≤ -a := by
      simpa [traceZeroQuad] using h 0 1
    have ha0 : a = 0 := by linarith
    subst a
    have hc : 0 ≤ 2 * c := by
      simpa [traceZeroQuad] using h 1 1
    have hnc : 0 ≤ -(2 * c) := by
      simpa [traceZeroQuad] using h 1 (-1)
    exact ⟨rfl, by linarith⟩
  · rintro ⟨rfl, rfl⟩ x y
    simp [traceZeroQuad]

/-- Every nonzero symmetric trace-zero two-sector kernel has an explicit
negative direction (existentially extracted from the exact characterization). -/
theorem exists_traceZeroQuad_neg_of_nontrivial {a c : ℝ}
    (h : a ≠ 0 ∨ c ≠ 0) :
    ∃ x y : ℝ, traceZeroQuad a c x y < 0 := by
  by_contra hnone
  push Not at hnone
  have hall : ∀ x y : ℝ, 0 ≤ traceZeroQuad a c x y := by
    intro x y
    exact hnone x y
  have hzero := (traceZeroQuad_nonnegative_iff a c).1 hall
  exact h.elim (fun ha => ha hzero.1) (fun hc => hc hzero.2)

/-- Cross terms cannot repair a nonzero signed diagonal balance: if `a` is
nonzero, the trace-zero kernel is necessarily indefinite for every `c`. -/
theorem exists_traceZeroQuad_neg_of_balance_ne_zero {a c : ℝ} (ha : a ≠ 0) :
    ∃ x y : ℝ, traceZeroQuad a c x y < 0 :=
  exists_traceZeroQuad_neg_of_nontrivial (Or.inl ha)

/-- Compression to the reflection-symmetric line erases the diagonal balance
and retains only twice the cross term. -/
theorem traceZeroQuad_symmetric (a c : ℝ) :
    traceZeroQuad a c 1 1 = 2 * c := by
  simp [traceZeroQuad]

/-- Compression to the reflection-antisymmetric line also erases the diagonal
balance and flips the sign of the cross term. -/
theorem traceZeroQuad_antisymmetric (a c : ℝ) :
    traceZeroQuad a c 1 (-1) = -(2 * c) := by
  simp [traceZeroQuad]

/-- Positivity after symmetric compression is exactly positivity of the
inserted cross term; it is not a consequence of trace-zero balance. -/
theorem traceZeroQuad_symmetric_nonnegative_iff (a c : ℝ) :
    0 ≤ traceZeroQuad a c 1 1 ↔ 0 ≤ c := by
  rw [traceZeroQuad_symmetric]
  constructor <;> intro h <;> linarith

/-- Requiring both reflection sectors to be nonnegative forces the cross term
to vanish, so the compression contains no signed interaction. -/
theorem traceZeroQuad_both_reflection_sectors_nonnegative_iff (a c : ℝ) :
    (0 ≤ traceZeroQuad a c 1 1 ∧ 0 ≤ traceZeroQuad a c 1 (-1)) ↔ c = 0 := by
  rw [traceZeroQuad_symmetric, traceZeroQuad_antisymmetric]
  constructor <;> intro h
  · linarith
  · subst c
    norm_num

end RiemannPrimeResolvent

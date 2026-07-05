/-
Copyright (c) 2026 Lluís Eriksson.
Released under the GNU Affero General Public License v3.0.
-/

import RiemannPrimeResolvent.Convergence
import RiemannPrimeResolvent.SpectralDefect
import RiemannPrimeResolvent.XiInterface

/-!
# Publication frontier

This file contains typed frontier interfaces rather than unproved declarations.
It makes the frontier machine-readable without adding axioms to Lean.

Process checks such as CI status, oracle review and no-circularity audits live
in the repository tooling and documentation.  The Lean gate below only records
mathematical data and proofs about that data.
-/

namespace RiemannPrimeResolvent

open Filter Topology

/-- A sequence of scalar spectral defects beats the critical `1/2` threshold. -/
def BeatsHalfThreshold (η : ℕ → ℝ) : Prop :=
  ∃ q : ℝ, 1 / 2 < q ∧
    ∃ C : ℝ, 0 ≤ C ∧
      ∀ n : ℕ,
        |η n| ≤ C * Real.exp (-q * Real.log (n + 1 : ℝ))

/-- `BeatsHalfThreshold` is satisfiable: the sequence `(n + 1)⁻¹` beats the
critical threshold with exponent and constant both equal to `1`. -/
theorem beatsHalfThreshold_witness :
    BeatsHalfThreshold (fun n => ((n : ℝ) + 1)⁻¹) := by
  refine ⟨1, by norm_num, 1, by norm_num, fun n => ?_⟩
  have hpos : 0 < (n : ℝ) + 1 := by positivity
  have hexp :
      Real.exp (-(1 : ℝ) * Real.log ((n : ℝ) + 1)) =
        ((n : ℝ) + 1)⁻¹ := by
    rw [neg_one_mul, Real.exp_neg, Real.exp_log hpos]
  rw [hexp, one_mul, abs_of_nonneg (inv_nonneg.mpr hpos.le)]

/-- Exact convergence endpoint that the concrete operator layer must supply. -/
def PrimeResolventConvergence (E : ℕ → ℝ) : Prop :=
  Tendsto E atTop (𝓝 0)

/-- Minimal mathematical package required before the project can claim a
complete prime--resolvent argument.

Every field is either concrete model data or a statement tied to that data.
The `defect` field is the meeting point for the future concrete operator layer:
`SpectralDefect.lean` supplies scalar defect formulas today, while RF-3/RF-4
must eventually instantiate this sequence from a certified model. -/
structure PublicationGate where
  xiBridge : XiStieltjesExtensionTarget → XiOnlyRealZeros
  defect : ℕ → ℝ
  budget : ℕ → ErrorBudget
  spectralRate : BeatsHalfThreshold defect
  budgetVanishes : VanishingBudget budget

/-- The publication gate is consumed explicitly: once the Stieltjes-extension
target is supplied, the gate's bridge delivers the claimed zero-location
conclusion.  This theorem deliberately does not manufacture the extension
target; that remains part of the open analytic frontier. -/
theorem publicationGate_delivers (g : PublicationGate)
    (hext : XiStieltjesExtensionTarget) : XiOnlyRealZeros :=
  g.xiBridge hext

end RiemannPrimeResolvent

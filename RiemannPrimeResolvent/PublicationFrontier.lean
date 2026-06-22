/-
Copyright (c) 2026 Lluís Eriksson.
Released under the GNU Affero General Public License v3.0.
-/

import RiemannPrimeResolvent.Convergence
import RiemannPrimeResolvent.SpectralDefect
import RiemannPrimeResolvent.XiInterface

/-!
# Publication frontier

This file contains named propositions rather than unproved declarations.  It
makes the frontier machine-readable without adding axioms to Lean.
-/

namespace RiemannPrimeResolvent

open Filter Topology

/-- A sequence of scalar spectral defects beats the critical `1/2` threshold. -/
def BeatsHalfThreshold (η : ℕ → ℝ) : Prop :=
  ∃ q : ℝ, 1 / 2 < q ∧
    ∃ C : ℝ, 0 ≤ C ∧
      ∀ n : ℕ,
        |η n| ≤ C * Real.exp (-q * Real.log (n + 1 : ℝ))

/-- Exact convergence endpoint that the concrete operator layer must supply. -/
def PrimeResolventConvergence (E : ℕ → ℝ) : Prop :=
  Tendsto E atTop (𝓝 0)

/-- Minimal abstract package required before the project can claim a complete
prime--resolvent argument. -/
structure PublicationGate : Prop where
  xiBridge : XiStieltjesExtensionTarget → XiOnlyRealZeros
  concreteSpectralModel : Prop
  spectralRate : Prop
  primeTailTheorem : Prop
  noCircularUseOfRH : Prop
  leanBuildGreen : Prop
  oracleReviewed : Prop

end RiemannPrimeResolvent

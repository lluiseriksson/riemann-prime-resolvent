/-
Copyright (c) 2026 Lluís Eriksson.
Released under the GNU Affero General Public License v3.0.
-/

import Mathlib.NumberTheory.LSeries.RiemannZeta

/-!
# Riemann Xi interface

Mathlib defines the entire pole-removed completed zeta as
`completedRiemannZeta₀`.  The formula below reconstructs the conventional
Riemann `ξ` function and evaluates it on the critical-line coordinate.

The equivalence between `XiOnlyRealZeros` and Mathlib's `RiemannHypothesis` is
an explicit formalization milestone; it is not asserted in this seed release.
-/

namespace RiemannPrimeResolvent

open Complex

/-- The conventional `ξ(s)` reconstructed from `completedRiemannZeta₀`. -/
noncomputable def riemannXiS (s : ℂ) : ℂ :=
  (s * (s - 1) * completedRiemannZeta₀ s + 1) / 2

/-- Critical-line coordinate `Ξ(z) = ξ(1/2 + i z)`. -/
noncomputable def riemannXi (z : ℂ) : ℂ :=
  riemannXiS ((1 / 2 : ℂ) + I * z)

/-- All zeros of `Ξ` lie on the real axis. -/
def XiOnlyRealZeros : Prop :=
  ∀ z : ℂ, riemannXi z = 0 → z.im = 0

/-- The slit plane used by the Stieltjes-extension strategy. -/
def slitPlane : Set ℂ :=
  {z | z.im ≠ 0 ∨ 0 < z.re}

/-- Abstract target of the project, deliberately separated from a theorem. -/
def XiStieltjesExtensionTarget : Prop :=
  ∃ S : ℂ → ℂ,
    DifferentiableOn ℂ S slitPlane ∧
    ∀ x : ℝ, 1 / 4 < x →
      S x =
        (1 / (2 * Real.sqrt x) : ℂ) *
          (deriv riemannXiS ((1 / 2 : ℂ) + Real.sqrt x) /
            riemannXiS ((1 / 2 : ℂ) + Real.sqrt x))

end RiemannPrimeResolvent

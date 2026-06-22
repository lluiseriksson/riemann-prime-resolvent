/-
Copyright (c) 2026 Lluís Eriksson.
Released under the GNU Affero General Public License v3.0.
-/

import Mathlib

/-!
# Finite Stieltjes and squared-resolvent models

The infinite trace-class theory is not yet formalized here.  This file provides
the finite positive model that numerical certificates will instantiate.
-/

namespace RiemannPrimeResolvent

open scoped BigOperators

variable {ι : Type*}

/-- Finite Stieltjes transform of nonnegative spectral locations `t i`. -/
noncomputable def finiteStieltjes
    (s : Finset ι) (t : ι → ℝ) (x : ℝ) : ℝ :=
  ∑ i ∈ s, (t i + x)⁻¹

/-- Finite version of `Tr (D² + x I)⁻¹`, indexed by positive ordinates. -/
noncomputable def finiteSquaredResolvent
    (s : Finset ι) (γ : ι → ℝ) (x : ℝ) : ℝ :=
  ∑ i ∈ s, (γ i ^ 2 + x)⁻¹

/-- Positivity of a finite Stieltjes transform. -/
theorem finiteStieltjes_nonneg
    (s : Finset ι) (t : ι → ℝ) (x : ℝ)
    (ht : ∀ i ∈ s, 0 ≤ t i) (hx : 0 ≤ x) :
    0 ≤ finiteStieltjes s t x := by
  unfold finiteStieltjes
  exact Finset.sum_nonneg fun i hi =>
    inv_nonneg.mpr (add_nonneg (ht i hi) hx)

/-- Positivity of the finite squared-resolvent observable. -/
theorem finiteSquaredResolvent_nonneg
    (s : Finset ι) (γ : ι → ℝ) (x : ℝ) (hx : 0 ≤ x) :
    0 ≤ finiteSquaredResolvent s γ x := by
  unfold finiteSquaredResolvent
  exact Finset.sum_nonneg fun i _ =>
    inv_nonneg.mpr (add_nonneg (sq_nonneg (γ i)) hx)

/-- A paired spectrum contributes twice the positive-ordinate sum. -/
noncomputable def finitePairedTrace
    (s : Finset ι) (γ : ι → ℝ) (x : ℝ) : ℝ :=
  2 * finiteSquaredResolvent s γ x

/-- The factor `1/2` removes double counting of a paired spectrum. -/
theorem half_finitePairedTrace
    (s : Finset ι) (γ : ι → ℝ) (x : ℝ) :
    (1 / 2 : ℝ) * finitePairedTrace s γ x = finiteSquaredResolvent s γ x := by
  unfold finitePairedTrace
  ring

end RiemannPrimeResolvent

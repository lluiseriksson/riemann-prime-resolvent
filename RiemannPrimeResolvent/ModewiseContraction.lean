import RiemannPrimeResolvent.SectorContraction
import Mathlib.Tactic

/-!
# Modewise versus uniform contraction

A contraction chosen after fixing each test mode is merely a reformulation of
pointwise dominance.  A single contraction chosen before the mode is a
strictly stronger gluing condition.  This file records the quantifier gap and
an exact two-mode counterexample.
-/

namespace RiemannPrimeResolvent

/-- Pointwise dominance is equivalent to a contraction coefficient that may
depend on the mode. -/
theorem modewiseContraction_iff_pointwiseDominance
    {ι : Type*} (S A : ι → ℝ)
    (hS : ∀ i, 0 ≤ S i) (hA : ∀ i, 0 ≤ A i) :
    (∀ i, A i ≤ S i) ↔
      ∀ i, ∃ t : ℝ, 0 ≤ t ∧ t ≤ 1 ∧ A i = t * S i := by
  constructor
  · intro h i
    exact (nonnegative_le_iff_exists_unitInterval_mul (hS i) (hA i)).mp (h i)
  · intro h i
    exact (nonnegative_le_iff_exists_unitInterval_mul (hS i) (hA i)).mpr (h i)

/-- Two nonnegative modes with pointwise dominance but incompatible optimal
contraction coefficients. -/
def twoModeSymmetricEnergy (_ : Bool) : ℝ := 1

def twoModeAntisymmetricEnergy (i : Bool) : ℝ := if i then 1 else 0

theorem twoMode_pointwiseDominance (i : Bool) :
    twoModeAntisymmetricEnergy i ≤ twoModeSymmetricEnergy i := by
  cases i <;> simp [twoModeAntisymmetricEnergy, twoModeSymmetricEnergy]

theorem twoMode_has_modewiseContractions :
    ∀ i, ∃ t : ℝ, 0 ≤ t ∧ t ≤ 1 ∧
      twoModeAntisymmetricEnergy i = t * twoModeSymmetricEnergy i := by
  apply (modewiseContraction_iff_pointwiseDominance
    twoModeSymmetricEnergy twoModeAntisymmetricEnergy
    (by intro i; simp [twoModeSymmetricEnergy])
    (by intro i; cases i <;> simp [twoModeAntisymmetricEnergy])).mp
  exact twoMode_pointwiseDominance

/-- The modewise witnesses in the preceding theorem do not glue to one
scalar contraction coefficient. -/
theorem twoMode_no_uniformScalarContraction :
    ¬∃ t : ℝ, ∀ i,
      twoModeAntisymmetricEnergy i = t * twoModeSymmetricEnergy i := by
  rintro ⟨t, ht⟩
  have hfalse := ht false
  have htrue := ht true
  simp [twoModeAntisymmetricEnergy, twoModeSymmetricEnergy] at hfalse htrue
  linarith

end RiemannPrimeResolvent

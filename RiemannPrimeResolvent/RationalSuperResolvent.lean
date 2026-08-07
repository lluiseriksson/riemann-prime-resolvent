import Mathlib.Tactic

/-!
# The elementary rational kernel as a scalar resolvent

This file formalizes the scalar algebra behind the fermionic resolvent form
of the elementary rational detector.  It contains no trace-class statement
and makes no claim about the Möbius-weighted estimate or RH.
-/

namespace RiemannPrimeResolvent

/-- The base rational profile used by the elementary detector. -/
noncomputable def rationalResolventProfile (y : ℝ) : ℝ := y / (1 + y ^ 2)

/-- Rescaling the rational profile gives the real part of a resolvent pair. -/
theorem rationalResolventProfile_div (h R : ℝ) (hR : R ≠ 0) :
    rationalResolventProfile (h / R) = R * h / (h ^ 2 + R ^ 2) := by
  unfold rationalResolventProfile
  field_simp
  ring

/-- Purely real denominator identity underlying the conjugate resolvent sum. -/
theorem conjugateResolventPair_real (h R : ℝ) (hden : h ^ 2 + R ^ 2 ≠ 0) :
    R / 2 * (1 / (h ^ 2 + R ^ 2) * (2 * h)) =
      R * h / (h ^ 2 + R ^ 2) := by
  field_simp

end RiemannPrimeResolvent

import Mathlib.Tactic

/-!
# A finite no-go theorem for an odd commuting operator

An operator commuting with a diagonal operator of simple spectrum is
diagonal.  If it is also odd for a nonvanishing parity grading, it is zero.
This is the finite algebra used in the prime-Fock supercharge audit; it makes
no spectral-convergence or RH claim.
-/

namespace RiemannPrimeResolvent

/-- Entrywise form of the simple-spectrum odd-commutant no-go theorem. -/
theorem oddCommutant_eq_zero
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (energy grading : ι → ℝ) (Q : ι → ι → ℝ)
    (henergy : Function.Injective energy)
    (hgrading : ∀ i, grading i ≠ 0)
    (hcomm : ∀ i j, (energy i - energy j) * Q i j = 0)
    (hodd : ∀ i j, (grading i + grading j) * Q i j = 0) :
    Q = 0 := by
  funext i j
  by_cases hij : i = j
  · subst j
    have htwo : grading i + grading i ≠ 0 := by
      intro h
      have : grading i = 0 := by linarith
      exact hgrading i this
    exact (mul_eq_zero.mp (hodd i i)).resolve_left htwo
  · have hne : energy i - energy j ≠ 0 := sub_ne_zero.mpr (henergy.ne hij)
    exact (mul_eq_zero.mp (hcomm i j)).resolve_left hne

end RiemannPrimeResolvent

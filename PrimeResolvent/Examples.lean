import PrimeResolvent.FiniteCertificates

/-!
# Small exact examples

These examples are kernel-checked consequences of the generic theorems.  They
are not numerical evidence for RH.
-/

set_option autoImplicit false

namespace PrimeResolvent

/-- A three-atom nonnegative toy spectrum. -/
def demoSpectrum : Fin 3 → ℝ := ![1, 4, 9]

example : ∀ i, 0 ≤ demoSpectrum i := by
  intro i
  fin_cases i <;> norm_num [demoSpectrum]

example : IsHausdorffCompletelyMonotone
    (finiteResolventMoment 1 demoSpectrum) := by
  apply finiteResolventMoment_isHausdorffCompletelyMonotone
  · norm_num
  · intro i
    fin_cases i <;> norm_num [demoSpectrum]

example (k n : ℕ) :
    0 ≤ hausdorffDiff k (finiteResolventMoment 1 demoSpectrum) n := by
  apply finiteResolventMoment_hausdorffDiff_nonneg
  · norm_num
  · intro i
    fin_cases i <;> norm_num [demoSpectrum]

end PrimeResolvent

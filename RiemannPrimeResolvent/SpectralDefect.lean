/-
Copyright (c) 2026 Lluís Eriksson.
Released under the GNU Affero General Public License v3.0.
-/

import Mathlib

/-!
# Scalar spectral-defect interfaces

These definitions isolate the exact quantities that a Galerkin or interval
certificate must control.  No claim is made here that the Connes--Consani--
Moscovici operators satisfy the required rates.
-/

namespace RiemannPrimeResolvent

/-- Rayleigh/gap plus Galerkin-tail defect proposed in the research note. -/
noncomputable def rayleighGapDefect
    (normK rayleighExcess gap tail : ℝ) : ℝ :=
  normK * Real.sqrt (2 * rayleighExcess / gap) + 2 * tail

/-- Nonnegativity of the Rayleigh/gap defect in its intended range. -/
theorem rayleighGapDefect_nonneg
    {normK rayleighExcess gap tail : ℝ}
    (hnorm : 0 ≤ normK) (hr : 0 ≤ rayleighExcess)
    (hgap : 0 < gap) (htail : 0 ≤ tail) :
    0 ≤ rayleighGapDefect normK rayleighExcess gap tail := by
  have hquot : 0 ≤ 2 * rayleighExcess / gap := by
    exact div_nonneg (mul_nonneg (by norm_num) hr) hgap.le
  unfold rayleighGapDefect
  exact add_nonneg (mul_nonneg hnorm (Real.sqrt_nonneg _))
    (mul_nonneg (by norm_num) htail)

/-- Residual/separation version suitable for certified finite matrices. -/
noncomputable def residualGapDefect
    (normK residual separation tail : ℝ) : ℝ :=
  Real.sqrt 2 * normK * residual / separation + 2 * tail

/-- Nonnegativity of the residual/separation defect. -/
theorem residualGapDefect_nonneg
    {normK residual separation tail : ℝ}
    (hnorm : 0 ≤ normK) (hres : 0 ≤ residual)
    (hsep : 0 < separation) (htail : 0 ≤ tail) :
    0 ≤ residualGapDefect normK residual separation tail := by
  unfold residualGapDefect
  have hfirst : 0 ≤ Real.sqrt 2 * normK * residual / separation := by
    exact div_nonneg
      (mul_nonneg (mul_nonneg (Real.sqrt_nonneg _) hnorm) hres)
      hsep.le
  linarith

end RiemannPrimeResolvent

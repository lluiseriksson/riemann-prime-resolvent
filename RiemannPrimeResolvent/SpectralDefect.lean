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

/-- A scalar spectral-gap estimate controls the distance between two aligned
unit vectors.  In the intended application, `ground` is the normalized finite
ground state, `trial` is the normalized projected trial vector, and
`overlap = <ground, trial>_R` after choosing the sign of `ground` so that the
overlap is nonnegative.  Finite spectral decomposition supplies
`gap * (1 - overlap^2) <= rayleighExcess`.

This is the Hilbert-space step behind the Rayleigh/gap term; it makes no claim
that a concrete operator satisfies the scalar spectral estimate. -/
theorem norm_sub_le_sqrt_rayleigh_div_gap
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {ground trial : E} {overlap rayleighExcess gap : ℝ}
    (hground : ‖ground‖ = 1) (htrial : ‖trial‖ = 1)
    (hoverlap : inner ℝ ground trial = overlap)
    (hoverlap_nonneg : 0 ≤ overlap)
    (hr : 0 ≤ rayleighExcess) (hgap : 0 < gap)
    (hspectral : gap * (1 - overlap ^ 2) ≤ rayleighExcess) :
    ‖ground - trial‖ ≤ Real.sqrt (2 * rayleighExcess / gap) := by
  have hoverlap_le_one : overlap ≤ 1 := by
    rw [← hoverlap]
    exact real_inner_le_one_of_norm_eq_one hground htrial
  have hdist_sq : ‖ground - trial‖ ^ 2 = 2 * (1 - overlap) := by
    rw [norm_sub_sq_real, hground, htrial, hoverlap]
    ring
  have hone : 1 - overlap ≤ 1 - overlap ^ 2 := by
    nlinarith
  have hquot : 1 - overlap ^ 2 ≤ rayleighExcess / gap := by
    exact (le_div_iff₀ hgap).2 (by simpa [mul_comm] using hspectral)
  have hsquare : ‖ground - trial‖ ^ 2 ≤ 2 * rayleighExcess / gap := by
    calc
      ‖ground - trial‖ ^ 2 = 2 * (1 - overlap) := hdist_sq
      _ ≤ 2 * (1 - overlap ^ 2) :=
        mul_le_mul_of_nonneg_left hone (by norm_num)
      _ ≤ 2 * (rayleighExcess / gap) :=
        mul_le_mul_of_nonneg_left hquot (by norm_num)
      _ = 2 * rayleighExcess / gap := by ring
  exact (Real.le_sqrt (norm_nonneg _) (by positivity)).2 hsquare

/-- Returning from a normalized projected trial vector to the complete trial
costs at most twice the Galerkin tail.  The first tail controls `complete -
projected`; the second is the reverse-triangle cost of replacing
`||projected||` by `||complete||` after phase/sign alignment. -/
theorem norm_scaled_ground_sub_complete_le
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {ground trial complete projected : E} {alignment tail : ℝ}
    (htrial : ‖trial‖ = 1)
    (hprojected : projected = ‖projected‖ • trial)
    (halign : ‖ground - trial‖ ≤ alignment)
    (htail : ‖complete - projected‖ ≤ tail) :
    ‖‖complete‖ • ground - complete‖ ≤
      ‖complete‖ * alignment + 2 * tail := by
  have htail' : ‖projected - complete‖ ≤ tail := by
    simpa [norm_sub_rev] using htail
  have hnorm : |‖complete‖ - ‖projected‖| ≤ tail :=
    (abs_norm_sub_norm_le complete projected).trans htail
  have hmiddle : ‖‖complete‖ • trial - projected‖ =
      |‖complete‖ - ‖projected‖| := by
    conv_lhs => rw [hprojected]
    rw [← sub_smul, norm_smul, htrial, mul_one, Real.norm_eq_abs]
  calc
    ‖‖complete‖ • ground - complete‖ =
        ‖(‖complete‖ • ground - ‖complete‖ • trial) +
          (‖complete‖ • trial - projected) + (projected - complete)‖ := by
            congr 1
            abel
    _ ≤ ‖‖complete‖ • ground - ‖complete‖ • trial‖ +
          ‖‖complete‖ • trial - projected‖ + ‖projected - complete‖ := by
            exact (norm_add_le _ _).trans
              (add_le_add (norm_add_le _ _) (le_refl _))
    _ = ‖complete‖ * ‖ground - trial‖ +
          |‖complete‖ - ‖projected‖| + ‖projected - complete‖ := by
            rw [← smul_sub, norm_smul, Real.norm_of_nonneg (norm_nonneg complete)]
            rw [hmiddle]
    _ ≤ ‖complete‖ * alignment + 2 * tail := by
      have hfirst : ‖complete‖ * ‖ground - trial‖ ≤
          ‖complete‖ * alignment :=
        mul_le_mul_of_nonneg_left halign (norm_nonneg complete)
      linarith

/-- The finite Galerkin approximation inequality in the exact scalar shape
used by `rayleighGapDefect`.  The Rayleigh/gap distance is proved above; this
theorem adds the projected-to-complete tail without renaming the concrete
operator obligation. -/
theorem norm_scaled_ground_sub_complete_le_rayleighGapDefect
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {ground trial complete projected : E}
    {overlap rayleighExcess gap tail : ℝ}
    (hground : ‖ground‖ = 1) (htrial : ‖trial‖ = 1)
    (hoverlap : inner ℝ ground trial = overlap)
    (hoverlap_nonneg : 0 ≤ overlap)
    (hr : 0 ≤ rayleighExcess) (hgap : 0 < gap)
    (hspectral : gap * (1 - overlap ^ 2) ≤ rayleighExcess)
    (hprojected : projected = ‖projected‖ • trial)
    (htail : ‖complete - projected‖ ≤ tail) :
    ‖‖complete‖ • ground - complete‖ ≤
      rayleighGapDefect ‖complete‖ rayleighExcess gap tail := by
  apply norm_scaled_ground_sub_complete_le htrial hprojected
  · exact norm_sub_le_sqrt_rayleigh_div_gap hground htrial hoverlap
      hoverlap_nonneg hr hgap hspectral
  · exact htail

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

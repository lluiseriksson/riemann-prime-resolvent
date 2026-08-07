import Mathlib.Analysis.Complex.Basic

/-!
# Prime Poisson score: finite algebraic core

This file kernel-checks two identities used in the localized Weil-form audit:

* positivity of the one-prime Poisson denominator/kernel for `0 ≤ r < 1`;
* the `(1,1)` signature of the elementary exponential boundary block.

It deliberately makes no claim about the critical Kronecker restriction
inequality, which is the RH-level analytic step.
-/

namespace RiemannPrimeResolvent

noncomputable section

/-- Denominator of the circle Poisson kernel, with `c = cos θ`. -/
def poissonDen (r c : ℝ) : ℝ := 1 - 2 * r * c + r ^ 2

/-- The Poisson denominator is strictly positive for `0 ≤ r < 1`, `c ≤ 1`. -/
theorem poissonDen_pos {r c : ℝ} (hr0 : 0 ≤ r) (hr1 : r < 1) (hc : c ≤ 1) :
    0 < poissonDen r c := by
  have hs : 0 < (1 - r) ^ 2 := sq_pos_of_pos (sub_pos.mpr hr1)
  have hrc : 0 ≤ 2 * r * (1 - c) := mul_nonneg (mul_nonneg (by positivity) hr0) (sub_nonneg.mpr hc)
  dsimp [poissonDen]
  nlinarith

/-- Positivity of the normalized one-prime Poisson kernel. -/
theorem poissonKernel_pos {r c : ℝ} (hr0 : 0 ≤ r) (hr1 : r < 1) (hc : c ≤ 1) :
    0 < (1 - r ^ 2) / poissonDen r c := by
  have hnum : 0 < 1 - r ^ 2 := by nlinarith
  exact div_pos hnum (poissonDen_pos hr0 hr1 hc)

/-- Euler prime-tower multiplier in rational closed form. -/
def primeTowerMultiplier (r c logp : ℝ) : ℝ :=
  2 * logp * (r * c - r ^ 2) / poissonDen r c

/-- Centering constant in the radial Poisson-score identity. -/
def primeTowerCenter (r logp : ℝ) : ℝ :=
  2 * logp * r ^ 2 / (1 - r ^ 2)

/-- Algebraic score after the analytic derivative has been evaluated. -/
def primePoissonScore (r c logp : ℝ) : ℝ :=
  primeTowerCenter r logp - primeTowerMultiplier r c logp

/-- The finite algebraic core of `multiplier = center - score`. -/
theorem primeTower_eq_center_sub_score (r c logp : ℝ) :
    primeTowerMultiplier r c logp =
      primeTowerCenter r logp - primePoissonScore r c logp := by
  simp [primePoissonScore]

/--
The elementary boundary kernel has signature `(1,1)` after passing from
`I₊, I₋` to the even/odd coordinates `I_c, I_s`.
-/
theorem exponentialBoundary_signature (Ic Is : ℂ) :
    star (Ic + Is) * (Ic - Is) + star (Ic - Is) * (Ic + Is) =
      2 * (star Ic * Ic - star Is * Is) := by
  rw [star_add, star_sub]
  ring

private theorem star_mul_self_eq_normSq (z : ℂ) :
    star z * z = (Complex.normSq z : ℂ) := by
  apply Complex.ext
  · simp [Complex.normSq_apply]
  · simp
    ring

/-- Nonnegativity of the real boundary pairing is exactly domination of the
odd/sine sector by the even/cosine sector. -/
theorem exponentialBoundary_re_nonnegative_iff (Ic Is : ℂ) :
    0 ≤ (star (Ic + Is) * (Ic - Is) +
      star (Ic - Is) * (Ic + Is)).re ↔
      Complex.normSq Is ≤ Complex.normSq Ic := by
  rw [exponentialBoundary_signature]
  rw [star_mul_self_eq_normSq, star_mul_self_eq_normSq]
  norm_num

/-- Strict failure of even-sector dominance produces a negative boundary
pairing. -/
theorem exponentialBoundary_re_neg_iff (Ic Is : ℂ) :
    (star (Ic + Is) * (Ic - Is) +
      star (Ic - Is) * (Ic + Is)).re < 0 ↔
      Complex.normSq Ic < Complex.normSq Is := by
  rw [exponentialBoundary_signature]
  rw [star_mul_self_eq_normSq, star_mul_self_eq_normSq]
  norm_num
  constructor <;> intro h <;> linarith

/-- Swapping the even and odd sectors reverses the real boundary sign. -/
theorem exponentialBoundary_re_swap (Ic Is : ℂ) :
    (star (Is + Ic) * (Is - Ic) +
      star (Is - Ic) * (Is + Ic)).re =
      -(star (Ic + Is) * (Ic - Is) +
        star (Ic - Is) * (Ic + Is)).re := by
  rw [exponentialBoundary_signature, exponentialBoundary_signature]
  norm_num
  ring

/-- The unrestricted boundary form is genuinely indefinite. -/
theorem exponentialBoundary_re_zero_one :
    (star ((0 : ℂ) + 1) * ((0 : ℂ) - 1) +
      star ((0 : ℂ) - 1) * ((0 : ℂ) + 1)).re = -2 := by
  norm_num

theorem not_exponentialBoundary_re_nonnegative_univ :
    ¬(∀ Ic Is : ℂ, 0 ≤
      (star (Ic + Is) * (Ic - Is) +
        star (Ic - Is) * (Ic + Is)).re) := by
  intro h
  have := h 0 1
  rw [exponentialBoundary_re_zero_one] at this
  norm_num at this

/-- If an admissible class is closed under swapping even and odd sectors,
universal nonnegativity forces the boundary form to vanish on that class. -/
theorem exponentialBoundary_zero_of_swapClosed_nonnegative
    (Admissible : ℂ → ℂ → Prop)
    (hswap : ∀ Ic Is, Admissible Ic Is → Admissible Is Ic)
    (hpos : ∀ Ic Is, Admissible Ic Is → 0 ≤
      (star (Ic + Is) * (Ic - Is) +
        star (Ic - Is) * (Ic + Is)).re)
    {Ic Is : ℂ} (hmem : Admissible Ic Is) :
    (star (Ic + Is) * (Ic - Is) +
      star (Ic - Is) * (Ic + Is)).re = 0 := by
  have h₁ := hpos Ic Is hmem
  have h₂ := hpos Is Ic (hswap Ic Is hmem)
  rw [exponentialBoundary_re_swap] at h₂
  linarith

end

end RiemannPrimeResolvent

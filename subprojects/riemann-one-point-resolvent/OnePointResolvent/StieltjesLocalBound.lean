import Mathlib

/-!
# Uniform local bounds for finite positive Stieltjes transforms

A single positive real value controls every positive finite Stieltjes sum on a
fixed complex disk.  The factor `2` is independent of the atom count, weights,
spectrum and approximant index.
-/

set_option autoImplicit false

namespace OnePointResolvent

open scoped BigOperators

/-- A finite positive Stieltjes sum at a complex argument. -/
noncomputable def finitePositiveStieltjes
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ) (z : ℂ) : ℂ :=
  ∑ i ∈ s, (weight i : ℂ) / ((spectrum i : ℂ) + z)

/-- The corresponding one-point value on the positive real axis. -/
noncomputable def finitePositiveStieltjesAt
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ) (x : ℝ) : ℝ :=
  ∑ i ∈ s, weight i / (spectrum i + x)

/-- Positive weights and spectrum give a nonnegative one-point value. -/
theorem finitePositiveStieltjesAt_nonneg
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ) (x : ℝ)
    (hweight : ∀ i ∈ s, 0 ≤ weight i)
    (hspectrum : ∀ i ∈ s, 0 ≤ spectrum i)
    (hx : 0 < x) :
    0 ≤ finitePositiveStieltjesAt s weight spectrum x := by
  unfold finitePositiveStieltjesAt
  apply Finset.sum_nonneg
  intro i hi
  exact div_nonneg (hweight i hi) (add_nonneg (hspectrum i hi) hx.le)

/-- On the disk `‖z - x₀‖ ≤ x₀ / 2`, every nonnegative spectral denominator
is at least half of its value at `x₀`. -/
theorem stieltjes_disk_denominator_bound
    {t x₀ : ℝ} {z : ℂ}
    (ht : 0 ≤ t)
    (hx₀ : 0 < x₀)
    (hz : ‖z - (x₀ : ℂ)‖ ≤ x₀ / 2) :
    t + x₀ ≤ 2 * ‖(t : ℂ) + z‖ := by
  have hzreal : x₀ - z.re ≤ x₀ / 2 := by
    calc
      x₀ - z.re ≤ ‖(x₀ : ℂ) - z‖ := by
        simpa using Complex.re_le_norm ((x₀ : ℂ) - z)
      _ = ‖z - (x₀ : ℂ)‖ := by rw [norm_sub_rev]
      _ ≤ x₀ / 2 := hz
  have hwreal : t + z.re ≤ ‖(t : ℂ) + z‖ := by
    simpa using Complex.re_le_norm ((t : ℂ) + z)
  linarith

/-- The factor-two disk bound for one positive Stieltjes atom. -/
theorem stieltjes_atom_norm_le_two
    {weight t x₀ : ℝ} {z : ℂ}
    (hweight : 0 ≤ weight)
    (ht : 0 ≤ t)
    (hx₀ : 0 < x₀)
    (hz : ‖z - (x₀ : ℂ)‖ ≤ x₀ / 2) :
    ‖(weight : ℂ) / ((t : ℂ) + z)‖ ≤ 2 * (weight / (t + x₀)) := by
  have hd : 0 < t + x₀ := add_pos_of_nonneg_of_pos ht hx₀
  have hden := stieltjes_disk_denominator_bound ht hx₀ hz
  have hnorm : 0 < ‖(t : ℂ) + z‖ := by
    by_contra h
    have hzero : ‖(t : ℂ) + z‖ = 0 :=
      le_antisymm (not_lt.mp h) (norm_nonneg _)
    rw [hzero, mul_zero] at hden
    linarith
  rw [Complex.norm_div, Complex.norm_real, Real.norm_of_nonneg hweight]
  apply (div_le_iff₀ hnorm).2
  have hmul :=
    mul_le_mul_of_nonneg_left hden (div_nonneg hweight hd.le)
  calc
    weight = (weight / (t + x₀)) * (t + x₀) := by
      rw [div_mul_cancel₀ weight (ne_of_gt hd)]
    _ ≤ (weight / (t + x₀)) * (2 * ‖(t : ℂ) + z‖) := hmul
    _ = (2 * (weight / (t + x₀))) * ‖(t : ℂ) + z‖ := by ring

/-- A positive finite Stieltjes sum on the half-radius disk is controlled by
`2` times its value at the center.  No cardinality or spectral bound occurs. -/
theorem finitePositiveStieltjes_norm_le_two
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ)
    (x₀ : ℝ) (z : ℂ)
    (hweight : ∀ i ∈ s, 0 ≤ weight i)
    (hspectrum : ∀ i ∈ s, 0 ≤ spectrum i)
    (hx₀ : 0 < x₀)
    (hz : ‖z - (x₀ : ℂ)‖ ≤ x₀ / 2) :
    ‖finitePositiveStieltjes s weight spectrum z‖ ≤
      2 * finitePositiveStieltjesAt s weight spectrum x₀ := by
  classical
  unfold finitePositiveStieltjes finitePositiveStieltjesAt
  calc
    ‖∑ i ∈ s, (weight i : ℂ) / ((spectrum i : ℂ) + z)‖
        ≤ ∑ i ∈ s, ‖(weight i : ℂ) / ((spectrum i : ℂ) + z)‖ :=
      norm_sum_le _ _
    _ ≤ ∑ i ∈ s, 2 * (weight i / (spectrum i + x₀)) := by
      apply Finset.sum_le_sum
      intro i hi
      exact stieltjes_atom_norm_le_two
        (hweight i hi) (hspectrum i hi) hx₀ hz
    _ = 2 * ∑ i ∈ s, weight i / (spectrum i + x₀) := by
      rw [Finset.mul_sum]

/-- Uniformity over a family with varying finite cutoffs, weights and spectra.
A one-point bound `M` propagates to the same disk with the universal factor `2`. -/
theorem finitePositiveStieltjes_family_norm_le_two
    {κ ι : Type*}
    (s : κ → Finset ι)
    (weight spectrum : κ → ι → ℝ)
    (x₀ M : ℝ)
    (hweight : ∀ j i, i ∈ s j → 0 ≤ weight j i)
    (hspectrum : ∀ j i, i ∈ s j → 0 ≤ spectrum j i)
    (hx₀ : 0 < x₀)
    (hone : ∀ j, finitePositiveStieltjesAt (s j) (weight j) (spectrum j) x₀ ≤ M)
    (j : κ) (z : ℂ)
    (hz : ‖z - (x₀ : ℂ)‖ ≤ x₀ / 2) :
    ‖finitePositiveStieltjes (s j) (weight j) (spectrum j) z‖ ≤ 2 * M := by
  calc
    ‖finitePositiveStieltjes (s j) (weight j) (spectrum j) z‖
        ≤ 2 * finitePositiveStieltjesAt (s j) (weight j) (spectrum j) x₀ :=
      finitePositiveStieltjes_norm_le_two
        (s j) (weight j) (spectrum j) x₀ z
        (hweight j) (hspectrum j) hx₀ hz
    _ ≤ 2 * M := mul_le_mul_of_nonneg_left (hone j) (by norm_num)

end OnePointResolvent

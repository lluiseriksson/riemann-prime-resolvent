import Mathlib

/-!
# Uniform local bounds for finite positive Stieltjes transforms

A one-point value controls a positive finite Stieltjes sum whenever the complex
denominators admit a uniform comparison with their value at that point.  The
factor-two disk theorem is a concrete instance of this producer/consumer API.
All constants are independent of the atom count, weights, spectrum and cutoff.
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

/-- Any denominator comparison produces the corresponding one-atom Stieltjes
bound.  This is the reusable consumer theorem for disk, compact and future
operator-specific geometric estimates. -/
theorem stieltjes_atom_norm_le_of_denominator
    {C weight t x₀ : ℝ} {z : ℂ}
    (hweight : 0 ≤ weight)
    (ht : 0 ≤ t)
    (hx₀ : 0 < x₀)
    (hden : t + x₀ ≤ C * ‖(t : ℂ) + z‖) :
    ‖(weight : ℂ) / ((t : ℂ) + z)‖ ≤ C * (weight / (t + x₀)) := by
  have hd : 0 < t + x₀ := add_pos_of_nonneg_of_pos ht hx₀
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
    _ ≤ (weight / (t + x₀)) * (C * ‖(t : ℂ) + z‖) := hmul
    _ = (C * (weight / (t + x₀))) * ‖(t : ℂ) + z‖ := by ring

/-- A pointwise denominator comparison propagates through every positive finite
Stieltjes sum without introducing an atom-count or spectral-size constant. -/
theorem finitePositiveStieltjes_norm_le_of_denominator
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ)
    (C x₀ : ℝ) (z : ℂ)
    (hweight : ∀ i ∈ s, 0 ≤ weight i)
    (hspectrum : ∀ i ∈ s, 0 ≤ spectrum i)
    (hx₀ : 0 < x₀)
    (hden : ∀ i ∈ s,
      spectrum i + x₀ ≤ C * ‖(spectrum i : ℂ) + z‖) :
    ‖finitePositiveStieltjes s weight spectrum z‖ ≤
      C * finitePositiveStieltjesAt s weight spectrum x₀ := by
  classical
  unfold finitePositiveStieltjes finitePositiveStieltjesAt
  calc
    ‖∑ i ∈ s, (weight i : ℂ) / ((spectrum i : ℂ) + z)‖
        ≤ ∑ i ∈ s, ‖(weight i : ℂ) / ((spectrum i : ℂ) + z)‖ :=
      norm_sum_le _ _
    _ ≤ ∑ i ∈ s, C * (weight i / (spectrum i + x₀)) := by
      apply Finset.sum_le_sum
      intro i hi
      exact stieltjes_atom_norm_le_of_denominator
        (hweight i hi) (hspectrum i hi) hx₀ (hden i hi)
    _ = C * ∑ i ∈ s, weight i / (spectrum i + x₀) := by
      rw [Finset.mul_sum]

/-- Uniformity over a family with varying cutoffs, weights and spectra follows
from a single denominator producer and a one-point bound. -/
theorem finitePositiveStieltjes_family_norm_le_of_denominator
    {κ ι : Type*}
    (s : κ → Finset ι)
    (weight spectrum : κ → ι → ℝ)
    (C x₀ M : ℝ)
    (hC : 0 ≤ C)
    (hweight : ∀ j i, i ∈ s j → 0 ≤ weight j i)
    (hspectrum : ∀ j i, i ∈ s j → 0 ≤ spectrum j i)
    (hx₀ : 0 < x₀)
    (hone : ∀ j, finitePositiveStieltjesAt (s j) (weight j) (spectrum j) x₀ ≤ M)
    (j : κ) (z : ℂ)
    (hden : ∀ i ∈ s j,
      spectrum j i + x₀ ≤ C * ‖(spectrum j i : ℂ) + z‖) :
    ‖finitePositiveStieltjes (s j) (weight j) (spectrum j) z‖ ≤ C * M := by
  calc
    ‖finitePositiveStieltjes (s j) (weight j) (spectrum j) z‖
        ≤ C * finitePositiveStieltjesAt (s j) (weight j) (spectrum j) x₀ :=
      finitePositiveStieltjes_norm_le_of_denominator
        (s j) (weight j) (spectrum j) C x₀ z
        (hweight j) (hspectrum j) hx₀ hden
    _ ≤ C * M := mul_le_mul_of_nonneg_left (hone j) hC

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
    ‖(weight : ℂ) / ((t : ℂ) + z)‖ ≤ 2 * (weight / (t + x₀)) :=
  stieltjes_atom_norm_le_of_denominator hweight ht hx₀
    (stieltjes_disk_denominator_bound ht hx₀ hz)

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
      2 * finitePositiveStieltjesAt s weight spectrum x₀ :=
  finitePositiveStieltjes_norm_le_of_denominator
    s weight spectrum 2 x₀ z hweight hspectrum hx₀ fun i hi =>
      stieltjes_disk_denominator_bound (hspectrum i hi) hx₀ hz

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
    ‖finitePositiveStieltjes (s j) (weight j) (spectrum j) z‖ ≤ 2 * M :=
  finitePositiveStieltjes_family_norm_le_of_denominator
    s weight spectrum 2 x₀ M (by norm_num) hweight hspectrum hx₀ hone j z
    fun i hi => stieltjes_disk_denominator_bound (hspectrum j i hi) hx₀ hz

end OnePointResolvent

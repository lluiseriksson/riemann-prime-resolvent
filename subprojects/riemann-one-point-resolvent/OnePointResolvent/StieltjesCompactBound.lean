import OnePointResolvent.ResolventCompactification
import OnePointResolvent.StieltjesLocalBound

/-!
# Compact-set bounds through resolvent compactification

The unbounded spectral parameter `t ≥ 0` is replaced by
`u = x₀ / (t + x₀) ∈ [0,1]`.  The identity

`u * (t + z) = x₀ + u * (z - x₀)`

turns denominator control on an arbitrary compact subset of the slit plane into
a minimum problem on the compact product `K × [0,1]`.  This is the geometric
producer consumed by the abstract Stieltjes bounds.
-/

set_option autoImplicit false

namespace OnePointResolvent

open Set

/-- The compactified denominator associated with the one-point base `x₀`. -/
noncomputable def stieltjesCompactifiedDenominator
    (x₀ : ℝ) (z : ℂ) (u : ℝ) : ℂ :=
  (x₀ : ℂ) + (u : ℂ) * (z - (x₀ : ℂ))

/-- The compactified spectral coordinate is strictly positive for a positive
base point and a nonnegative spectrum. -/
theorem compactifiedPoint_pos {x₀ t : ℝ}
    (hx₀ : 0 < x₀) (ht : 0 ≤ t) :
    0 < compactifiedPoint x₀ t := by
  unfold compactifiedPoint
  exact div_pos hx₀ (spectrum_shift_pos hx₀ ht)

/-- The compactified denominator never vanishes on the slit plane for
`u ∈ [0,1]`. -/
theorem stieltjesCompactifiedDenominator_ne_zero
    {x₀ u : ℝ} {z : ℂ}
    (hx₀ : 0 < x₀)
    (hz : z ∈ Complex.slitPlane)
    (hu : u ∈ Set.Icc (0 : ℝ) 1) :
    stieltjesCompactifiedDenominator x₀ z u ≠ 0 := by
  intro hzero
  rcases Complex.mem_slitPlane_iff.mp hz with hzre | hzim
  · have hre : x₀ + u * (z.re - x₀) = 0 := by
      simpa [stieltjesCompactifiedDenominator] using congrArg Complex.re hzero
    by_cases hu0 : u = 0
    · subst u
      simp at hre
      linarith
    · have hupos : 0 < u := lt_of_le_of_ne hu.1 (Ne.symm hu0)
      have hleft : 0 ≤ (1 - u) * x₀ :=
        mul_nonneg (sub_nonneg.mpr hu.2) hx₀.le
      have hright : 0 < u * z.re := mul_pos hupos hzre
      have hpos : 0 < (1 - u) * x₀ + u * z.re :=
        add_pos_of_nonneg_of_pos hleft hright
      have heq : x₀ + u * (z.re - x₀) = (1 - u) * x₀ + u * z.re := by
        ring
      rw [heq] at hre
      linarith
  · have him : u * z.im = 0 := by
      simpa [stieltjesCompactifiedDenominator] using congrArg Complex.im hzero
    rcases mul_eq_zero.mp him with hu0 | hzim0
    · subst u
      have hre : x₀ = 0 := by
        simpa [stieltjesCompactifiedDenominator] using congrArg Complex.re hzero
      linarith
    · exact hzim hzim0

/-- Exact algebraic bridge from the unbounded spectral parameter to its compact
coordinate. -/
theorem stieltjes_compactified_denominator_identity
    {x₀ t : ℝ} (hx₀ : 0 < x₀) (ht : 0 ≤ t) (z : ℂ) :
    (compactifiedPoint x₀ t : ℂ) * ((t : ℂ) + z) =
      stieltjesCompactifiedDenominator x₀ z (compactifiedPoint x₀ t) := by
  have h : t + x₀ ≠ 0 := ne_of_gt (spectrum_shift_pos hx₀ ht)
  have hreal :
      x₀ * (t + x₀)⁻¹ * t =
        x₀ - x₀ * (t + x₀)⁻¹ * x₀ := by
    field_simp [h]
    ring
  unfold stieltjesCompactifiedDenominator compactifiedPoint
  rw [div_eq_mul_inv]
  set u : ℂ := ((x₀ * (t + x₀)⁻¹ : ℝ) : ℂ)
  have hut : u * (t : ℂ) = (x₀ : ℂ) - u * (x₀ : ℂ) := by
    subst u
    exact_mod_cast hreal
  calc
    u * ((t : ℂ) + z) = u * (t : ℂ) + u * z := by ring
    _ = ((x₀ : ℂ) - u * (x₀ : ℂ)) + u * z := by rw [hut]
    _ = (x₀ : ℂ) + u * (z - (x₀ : ℂ)) := by ring

/-- Norm form of the compactified denominator identity. -/
theorem stieltjes_compactified_denominator_norm_identity
    {x₀ t : ℝ} (hx₀ : 0 < x₀) (ht : 0 ≤ t) (z : ℂ) :
    compactifiedPoint x₀ t * ‖(t : ℂ) + z‖ =
      ‖stieltjesCompactifiedDenominator x₀ z (compactifiedPoint x₀ t)‖ := by
  rw [← stieltjes_compactified_denominator_identity hx₀ ht z, norm_mul,
    Complex.norm_real, Real.norm_of_nonneg (compactifiedPoint_nonneg hx₀ ht)]

/-- Cross-multiplied norm identity, avoiding division by the compactified
coordinate. -/
theorem stieltjes_compactified_denominator_cross_identity
    {x₀ t : ℝ} (hx₀ : 0 < x₀) (ht : 0 ≤ t) (z : ℂ) :
    (t + x₀) *
        ‖stieltjesCompactifiedDenominator x₀ z (compactifiedPoint x₀ t)‖ =
      x₀ * ‖(t : ℂ) + z‖ := by
  rw [← stieltjes_compactified_denominator_norm_identity hx₀ ht z]
  unfold compactifiedPoint
  field_simp [ne_of_gt (spectrum_shift_pos hx₀ ht)] <;> ring

/-- A positive lower bound for the compactified denominator yields the
uncompactified denominator comparison required by the Stieltjes consumer. -/
theorem stieltjes_denominator_bound_of_compactified
    {δ x₀ t : ℝ} {z : ℂ}
    (hx₀ : 0 < x₀)
    (ht : 0 ≤ t)
    (hδ : 0 < δ)
    (hcompact : δ ≤
      ‖stieltjesCompactifiedDenominator x₀ z (compactifiedPoint x₀ t)‖) :
    t + x₀ ≤ (x₀ / δ) * ‖(t : ℂ) + z‖ := by
  rw [div_mul_eq_mul_div]
  apply (le_div_iff₀ hδ).2
  calc
    (t + x₀) * δ ≤
        (t + x₀) *
          ‖stieltjesCompactifiedDenominator x₀ z (compactifiedPoint x₀ t)‖ :=
      mul_le_mul_of_nonneg_left hcompact (add_nonneg ht hx₀.le)
    _ = x₀ * ‖(t : ℂ) + z‖ :=
      stieltjes_compactified_denominator_cross_identity hx₀ ht z

/-- On a compact subset of the slit plane, compactified denominators have
a strictly positive uniform lower bound. The empty compact is handled
vacuously by the same extreme-value lemma. -/
theorem exists_stieltjesCompactifiedDenominator_lower_bound
    {K : Set ℂ} (hK : IsCompact K)
    {x₀ : ℝ} (hx₀ : 0 < x₀)
    (hslit : K ⊆ Complex.slitPlane) :
    ∃ δ, 0 < δ ∧
      ∀ z ∈ K, ∀ u ∈ Set.Icc (0 : ℝ) 1,
        δ ≤ ‖stieltjesCompactifiedDenominator x₀ z u‖ := by
  have hQ : IsCompact (K ×ˢ Set.Icc (0 : ℝ) 1) :=
    hK.prod isCompact_Icc
  have hcontinuous : Continuous
      (fun p : ℂ × ℝ =>
        ‖stieltjesCompactifiedDenominator x₀ p.1 p.2‖) := by
    unfold stieltjesCompactifiedDenominator
    fun_prop
  have hpositive : ∀ p ∈ K ×ˢ Set.Icc (0 : ℝ) 1,
      0 < ‖stieltjesCompactifiedDenominator x₀ p.1 p.2‖ := by
    intro p hp
    exact norm_pos_iff.mpr
      (stieltjesCompactifiedDenominator_ne_zero hx₀ (hslit hp.1) hp.2)
  obtain ⟨δ, hδ, hδbound⟩ :=
    hQ.exists_forall_le' hcontinuous.continuousOn hpositive
  refine ⟨δ, hδ, ?_⟩
  intro z hz u hu
  exact hδbound (z, u) ⟨hz, hu⟩

/-- Every compact subset of the slit plane has a denominator-comparison
constant, independent of the spectral value `t ≥ 0`. -/
theorem exists_stieltjes_denominator_bound_on_compact
    {K : Set ℂ} (hK : IsCompact K)
    {x₀ : ℝ} (hx₀ : 0 < x₀)
    (hslit : K ⊆ Complex.slitPlane) :
    ∃ C, 0 ≤ C ∧
      ∀ z ∈ K, ∀ t : ℝ, 0 ≤ t →
        t + x₀ ≤ C * ‖(t : ℂ) + z‖ := by
  obtain ⟨δ, hδ, hδbound⟩ :=
    exists_stieltjesCompactifiedDenominator_lower_bound hK hx₀ hslit
  refine ⟨x₀ / δ, div_nonneg hx₀.le hδ.le, ?_⟩
  intro z hz t ht
  exact stieltjes_denominator_bound_of_compactified hx₀ ht hδ
    (hδbound z hz (compactifiedPoint x₀ t)
      ⟨compactifiedPoint_nonneg hx₀ ht, compactifiedPoint_le_one hx₀ ht⟩)

/-- A uniform one-point bound propagates to every compact subset of the slit
plane with one compact-dependent constant and no cutoff-dependent factor. -/
theorem exists_finitePositiveStieltjes_family_bound_on_compact
    {κ ι : Type*}
    (s : κ → Finset ι)
    (weight spectrum : κ → ι → ℝ)
    {K : Set ℂ} (hK : IsCompact K)
    (x₀ M : ℝ)
    (hweight : ∀ j i, i ∈ s j → 0 ≤ weight j i)
    (hspectrum : ∀ j i, i ∈ s j → 0 ≤ spectrum j i)
    (hx₀ : 0 < x₀)
    (hone : ∀ j, finitePositiveStieltjesAt (s j) (weight j) (spectrum j) x₀ ≤ M)
    (hslit : K ⊆ Complex.slitPlane) :
    ∃ C, 0 ≤ C ∧
      ∀ j z, z ∈ K →
        ‖finitePositiveStieltjes (s j) (weight j) (spectrum j) z‖ ≤ C * M := by
  obtain ⟨C, hC, hden⟩ :=
    exists_stieltjes_denominator_bound_on_compact hK hx₀ hslit
  refine ⟨C, hC, ?_⟩
  intro j z hz
  exact finitePositiveStieltjes_family_norm_le_of_denominator
    s weight spectrum C x₀ M hC hweight hspectrum hx₀ hone j z
    fun i hi => hden z hz (spectrum j i) (hspectrum j i hi)

end OnePointResolvent

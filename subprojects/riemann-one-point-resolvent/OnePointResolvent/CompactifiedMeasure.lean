import OnePointResolvent.StieltjesResolventBridge
import Mathlib.MeasureTheory.Measure.Prokhorov

/-!
# Compactified finite measures for positive Stieltjes families

The finite positive Stieltjes data are repackaged as finite measures on `ℝ`
whose support lies in the compact interval `[0,1]`.  This deliberately uses an
ambient real finite measure, rather than a proof-dependent subtype measure, so
that Mathlib's compact-support Prokhorov theorem applies directly.

For a base point `x₀ > 0` and spectral value `t ≥ 0`, set

* `u = x₀ / (t + x₀) ∈ [0,1]`,
* `a = w / (t + x₀) ≥ 0`.

The resulting measure is `Σ aᵢ δ_{uᵢ}`.  Its exact mass is the one-point value
`S(x₀)`, and a cutoff-independent one-point bound places the whole family in a
compact set of finite measures.

This module closes only the finite-measure compactness input.  It does not claim
subsequence extraction in compact-open topology, limit-kernel identification,
convergence to `S_Xi`, or RH.
-/

set_option autoImplicit false

namespace OnePointResolvent

open scoped BigOperators NNReal ENNReal
open MeasureTheory Set

/-- Compactified atomic weight `w / (t + x₀)`. -/
noncomputable def compactifiedStieltjesWeight (w t x₀ : ℝ) : ℝ :=
  w / (t + x₀)

/-- Compactified atomic weights are nonnegative for positive data. -/
theorem compactifiedStieltjesWeight_nonneg
    {w t x₀ : ℝ} (hw : 0 ≤ w) (ht : 0 ≤ t) (hx₀ : 0 < x₀) :
    0 ≤ compactifiedStieltjesWeight w t x₀ := by
  unfold compactifiedStieltjesWeight
  exact div_nonneg hw (add_nonneg ht hx₀.le)

/-- A Dirac mass bundled as a finite measure. -/
noncomputable def stieltjesDiracFiniteMeasure (x : ℝ) : FiniteMeasure ℝ :=
  ⟨Measure.dirac x, by infer_instance⟩

private theorem stieltjesDiracFiniteMeasure_mass (x : ℝ) :
    (stieltjesDiracFiniteMeasure x).mass = 1 := by
  rw [← ENNReal.coe_inj, FiniteMeasure.ennreal_mass]
  simp [stieltjesDiracFiniteMeasure]

private theorem finiteMeasure_mass_smul (c : ℝ≥0) (μ : FiniteMeasure ℝ) :
    (c • μ).mass = c * μ.mass := by
  rw [FiniteMeasure.mass, FiniteMeasure.smul_apply, FiniteMeasure.mass]
  rfl

private theorem finiteMeasure_mass_add (μ ν : FiniteMeasure ℝ) :
    (μ + ν).mass = μ.mass + ν.mass := by
  rw [FiniteMeasure.mass]
  exact congrFun (FiniteMeasure.coeFn_add μ ν) Set.univ

private theorem finiteMeasure_apply_add
    (μ ν : FiniteMeasure ℝ) (A : Set ℝ) :
    (μ + ν) A = μ A + ν A :=
  congrFun (FiniteMeasure.coeFn_add μ ν) A

private theorem stieltjesDiracFiniteMeasure_apply_compl_eq_zero
    {x : ℝ} {A : Set ℝ} (hx : x ∈ A) :
    stieltjesDiracFiniteMeasure x Aᶜ = 0 := by
  rw [← ENNReal.coe_eq_zero,
    FiniteMeasure.ennreal_coeFn_eq_coeFn_toMeasure]
  simp [stieltjesDiracFiniteMeasure, hx]

private theorem finiteMeasure_mass_sum
    {ι : Type*} (s : Finset ι) (μ : ι → FiniteMeasure ℝ) :
    (∑ i ∈ s, μ i).mass = ∑ i ∈ s, (μ i).mass := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih =>
      rw [Finset.sum_insert ha, Finset.sum_insert ha,
        finiteMeasure_mass_add, ih]

private theorem finiteMeasure_apply_sum
    {ι : Type*} (s : Finset ι) (μ : ι → FiniteMeasure ℝ) (A : Set ℝ) :
    (∑ i ∈ s, μ i) A = ∑ i ∈ s, μ i A := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih =>
      rw [Finset.sum_insert ha, Finset.sum_insert ha,
        finiteMeasure_apply_add, ih]

/-- Compactified finite atomic measure

`Σ_{i∈s} (wᵢ/(tᵢ+x₀)) δ_{x₀/(tᵢ+x₀)}`.

`Real.toNNReal` makes the definition total.  Under the positivity hypotheses of
the theorems below, no truncation occurs. -/
noncomputable def compactifiedStieltjesFiniteMeasure
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ) (x₀ : ℝ) :
    FiniteMeasure ℝ :=
  ∑ i ∈ s,
    Real.toNNReal (compactifiedStieltjesWeight (weight i) (spectrum i) x₀) •
      stieltjesDiracFiniteMeasure (compactifiedPoint x₀ (spectrum i))

/-- The mass of the compactified finite measure is exactly the one-point
Stieltjes value. -/
theorem compactifiedStieltjesFiniteMeasure_mass_eq
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ) (x₀ : ℝ)
    (hweight : ∀ i ∈ s, 0 ≤ weight i)
    (hspectrum : ∀ i ∈ s, 0 ≤ spectrum i)
    (hx₀ : 0 < x₀) :
    ((compactifiedStieltjesFiniteMeasure s weight spectrum x₀).mass : ℝ) =
      finitePositiveStieltjesAt s weight spectrum x₀ := by
  classical
  have hmass : ∀ i ∈ s,
      0 ≤ compactifiedStieltjesWeight (weight i) (spectrum i) x₀ := by
    intro i hi
    exact compactifiedStieltjesWeight_nonneg
      (hweight i hi) (hspectrum i hi) hx₀
  unfold compactifiedStieltjesFiniteMeasure
  rw [finiteMeasure_mass_sum]
  simp only [finiteMeasure_mass_smul, stieltjesDiracFiniteMeasure_mass, mul_one]
  push_cast
  unfold finitePositiveStieltjesAt compactifiedStieltjesWeight
  apply Finset.sum_congr rfl
  intro i hi
  simpa [compactifiedStieltjesWeight] using
    (Real.coe_toNNReal
      (compactifiedStieltjesWeight (weight i) (spectrum i) x₀) (hmass i hi))

/-- Every compactified atom lies in `[0,1]`, hence the finite measure gives zero
mass to the complement. -/
theorem compactifiedStieltjesFiniteMeasure_compl_Icc_eq_zero
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ) (x₀ : ℝ)
    (hspectrum : ∀ i ∈ s, 0 ≤ spectrum i)
    (hx₀ : 0 < x₀) :
    compactifiedStieltjesFiniteMeasure s weight spectrum x₀
        (Set.Icc (0 : ℝ) 1)ᶜ = 0 := by
  classical
  unfold compactifiedStieltjesFiniteMeasure
  rw [finiteMeasure_apply_sum]
  apply Finset.sum_eq_zero
  intro i hi
  have hmem : compactifiedPoint x₀ (spectrum i) ∈ Set.Icc (0 : ℝ) 1 :=
    ⟨compactifiedPoint_nonneg hx₀ (hspectrum i hi),
      compactifiedPoint_le_one hx₀ (hspectrum i hi)⟩
  rw [FiniteMeasure.smul_apply,
    stieltjesDiracFiniteMeasure_apply_compl_eq_zero hmem]
  simp

/-- Mass-controlled finite measures supported on `[0,1]`. -/
def compactifiedStieltjesMeasureFamily
    (M : ℝ≥0) : Set (FiniteMeasure ℝ) :=
  {μ | μ.mass ≤ M ∧ μ (Set.Icc (0 : ℝ) 1)ᶜ = 0}

/-- A one-point bound places a compactified Stieltjes measure in the common
mass-and-support controlled family. -/
theorem compactifiedStieltjesFiniteMeasure_mem_family
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ)
    (x₀ : ℝ) (M : ℝ≥0)
    (hweight : ∀ i ∈ s, 0 ≤ weight i)
    (hspectrum : ∀ i ∈ s, 0 ≤ spectrum i)
    (hx₀ : 0 < x₀)
    (hone : finitePositiveStieltjesAt s weight spectrum x₀ ≤ (M : ℝ)) :
    compactifiedStieltjesFiniteMeasure s weight spectrum x₀ ∈
      compactifiedStieltjesMeasureFamily M := by
  constructor
  · apply NNReal.coe_le_coe.mp
    rw [compactifiedStieltjesFiniteMeasure_mass_eq
      s weight spectrum x₀ hweight hspectrum hx₀]
    exact hone
  · exact compactifiedStieltjesFiniteMeasure_compl_Icc_eq_zero
      s weight spectrum x₀ hspectrum hx₀

/-- The common bounded-mass, `[0,1]`-supported finite-measure family is compact
in Mathlib's weak topology. -/
theorem isCompact_compactifiedStieltjesMeasureFamily
    (M : ℝ≥0) :
    IsCompact (compactifiedStieltjesMeasureFamily M) := by
  simpa [compactifiedStieltjesMeasureFamily] using
    (isCompact_setOf_finiteMeasure_le_of_isCompact
      (E := ℝ) M (K := Set.Icc (0 : ℝ) 1) isCompact_Icc)


/-- Every indexed family satisfying the common one-point bound lands inside the
same compact mass-and-support controlled set. -/
theorem range_compactifiedStieltjesFiniteMeasure_subset_family
    {κ ι : Type*}
    (s : κ → Finset ι)
    (weight spectrum : κ → ι → ℝ)
    (x₀ : ℝ) (M : ℝ≥0)
    (hweight : ∀ j i, i ∈ s j → 0 ≤ weight j i)
    (hspectrum : ∀ j i, i ∈ s j → 0 ≤ spectrum j i)
    (hx₀ : 0 < x₀)
    (hone : ∀ j,
      finitePositiveStieltjesAt (s j) (weight j) (spectrum j) x₀ ≤ (M : ℝ)) :
    Set.range (fun j =>
      compactifiedStieltjesFiniteMeasure
        (s j) (weight j) (spectrum j) x₀) ⊆
      compactifiedStieltjesMeasureFamily M := by
  rintro μ ⟨j, rfl⟩
  exact compactifiedStieltjesFiniteMeasure_mem_family
    (s j) (weight j) (spectrum j) x₀ M
    (hweight j) (hspectrum j) hx₀ (hone j)

/-- The weak closure of any uniformly one-point-bounded compactified Stieltjes
family is compact. This is the relative-compactness statement consumed by the
future limit-identification layer. -/
theorem isCompact_closure_range_compactifiedStieltjesFiniteMeasure
    {κ ι : Type*}
    (s : κ → Finset ι)
    (weight spectrum : κ → ι → ℝ)
    (x₀ : ℝ) (M : ℝ≥0)
    (hweight : ∀ j i, i ∈ s j → 0 ≤ weight j i)
    (hspectrum : ∀ j i, i ∈ s j → 0 ≤ spectrum j i)
    (hx₀ : 0 < x₀)
    (hone : ∀ j,
      finitePositiveStieltjesAt (s j) (weight j) (spectrum j) x₀ ≤ (M : ℝ)) :
    IsCompact (closure (Set.range (fun j =>
      compactifiedStieltjesFiniteMeasure
        (s j) (weight j) (spectrum j) x₀))) := by
  have hfamily := isCompact_compactifiedStieltjesMeasureFamily M
  apply hfamily.of_isClosed_subset isClosed_closure
  exact closure_minimal
    (range_compactifiedStieltjesFiniteMeasure_subset_family
      s weight spectrum x₀ M hweight hspectrum hx₀ hone)
    hfamily.isClosed

end OnePointResolvent

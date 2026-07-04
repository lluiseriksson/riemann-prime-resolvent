import OnePointResolvent.CompactifiedMeasure
import Mathlib.Topology.Order.ProjIcc

/-!
# Weak limits of compactified Stieltjes measures

The compactified Stieltjes kernel is continuous on `[0,1]`.  Composing it with
`Set.projIcc` gives a bounded continuous test function on the ambient real line,
so Mathlib's weak topology on `FiniteMeasure ℝ` can consume it directly.

This file proves three exact bridges:

* the finite compactified measure integrates the kernel to the original finite
  Stieltjes sum;
* weak convergence of finite measures implies convergence of every fixed
  slit-plane Stieltjes observable;
* hence any weak limit of the compactified approximants is a pointwise limit of
  the finite Stieltjes transforms.

The projection outside `[0,1]` is only a bounded-continuous extension device.
All compactified approximants and their weak limits remain supported on
`[0,1]`, so its off-support values carry no mathematical content.

This module does not yet upgrade pointwise convergence to compact-open
convergence, identify the limit with `S_Xi`, or prove RH.
-/

set_option autoImplicit false

namespace OnePointResolvent

open Filter MeasureTheory Set Topology
open scoped BigOperators NNReal

/-- The compactified Stieltjes kernel before bounded extension to the ambient
real line. -/
noncomputable def compactifiedStieltjesKernel
    (x₀ : ℝ) (z : ℂ) (u : ℝ) : ℂ :=
  (x₀ : ℂ) / stieltjesCompactifiedDenominator x₀ z u

/-- On `[0,1]`, the compactified kernel is continuous for every slit-plane
argument. -/
theorem continuous_compactifiedStieltjesKernel_on_Icc
    {x₀ : ℝ} (hx₀ : 0 < x₀) {z : ℂ}
    (hz : z ∈ Complex.slitPlane) :
    Continuous (fun u : Set.Icc (0 : ℝ) 1 =>
      compactifiedStieltjesKernel x₀ z u) := by
  unfold compactifiedStieltjesKernel
  apply Continuous.div continuous_const
  · unfold stieltjesCompactifiedDenominator
    fun_prop
  · intro u
    exact stieltjesCompactifiedDenominator_ne_zero hx₀ hz u.property

/-- The compactified kernel as a bounded continuous function on `[0,1]`. -/
noncomputable def compactifiedStieltjesKernelOnIccBCF
    (x₀ : ℝ) (z : ℂ) (hx₀ : 0 < x₀)
    (hz : z ∈ Complex.slitPlane) :
    BoundedContinuousFunction (Set.Icc (0 : ℝ) 1) ℂ :=
  BoundedContinuousFunction.mkOfCompact
    ⟨fun u => compactifiedStieltjesKernel x₀ z u,
      continuous_compactifiedStieltjesKernel_on_Icc hx₀ hz⟩

/-- A bounded continuous extension to `ℝ`, obtained by projecting every real
number to `[0,1]`. -/
noncomputable def compactifiedStieltjesKernelBCF
    (x₀ : ℝ) (z : ℂ) (hx₀ : 0 < x₀)
    (hz : z ∈ Complex.slitPlane) :
    BoundedContinuousFunction ℝ ℂ :=
  (compactifiedStieltjesKernelOnIccBCF x₀ z hx₀ hz).compContinuous
    ⟨Set.projIcc (0 : ℝ) 1 zero_le_one, continuous_projIcc⟩

/-- The bounded extension agrees with the original kernel on `[0,1]`. -/
theorem compactifiedStieltjesKernelBCF_apply_of_mem
    {x₀ u : ℝ} {z : ℂ} (hx₀ : 0 < x₀)
    (hz : z ∈ Complex.slitPlane) (hu : u ∈ Set.Icc (0 : ℝ) 1) :
    compactifiedStieltjesKernelBCF x₀ z hx₀ hz u =
      compactifiedStieltjesKernel x₀ z u := by
  change compactifiedStieltjesKernel x₀ z
      (Set.projIcc (0 : ℝ) 1 zero_le_one u) =
    compactifiedStieltjesKernel x₀ z u
  rw [Set.projIcc_of_mem zero_le_one hu]

/-- Integrating the bounded compactified kernel against a finite measure. -/
noncomputable def compactifiedStieltjesTransform
    (μ : FiniteMeasure ℝ) (x₀ : ℝ) (z : ℂ)
    (hx₀ : 0 < x₀) (hz : z ∈ Complex.slitPlane) : ℂ :=
  ∫ u, compactifiedStieltjesKernelBCF x₀ z hx₀ hz u ∂(μ : Measure ℝ)

/-- The compactified atom weight times the compactified kernel is exactly the
original Stieltjes atom. -/
theorem compactifiedStieltjesWeight_mul_kernel
    {w t x₀ : ℝ} (ht : 0 ≤ t) (hx₀ : 0 < x₀)
    {z : ℂ} (hz : z ∈ Complex.slitPlane) :
    (compactifiedStieltjesWeight w t x₀ : ℂ) *
        compactifiedStieltjesKernel x₀ z (compactifiedPoint x₀ t) =
      (w : ℂ) / ((t : ℂ) + z) := by
  have hshift : t + x₀ ≠ 0 := ne_of_gt (spectrum_shift_pos hx₀ ht)
  have hshiftC : (t : ℂ) + (x₀ : ℂ) ≠ 0 := by
    exact_mod_cast hshift
  have hpointC : (compactifiedPoint x₀ t : ℂ) ≠ 0 := by
    exact_mod_cast (compactifiedPoint_pos hx₀ ht).ne'
  have hmem : compactifiedPoint x₀ t ∈ Set.Icc (0 : ℝ) 1 :=
    ⟨compactifiedPoint_nonneg hx₀ ht, compactifiedPoint_le_one hx₀ ht⟩
  have hden :
      stieltjesCompactifiedDenominator x₀ z (compactifiedPoint x₀ t) ≠ 0 :=
    stieltjesCompactifiedDenominator_ne_zero hx₀ hz hmem
  have htz : (t : ℂ) + z ≠ 0 := by
    intro hzero
    apply hden
    rw [← stieltjes_compactified_denominator_identity hx₀ ht z,
      hzero, mul_zero]
  have hweight_mul :
      (compactifiedStieltjesWeight w t x₀ : ℂ) * (x₀ : ℂ) =
        (w : ℂ) * (compactifiedPoint x₀ t : ℂ) := by
    unfold compactifiedStieltjesWeight compactifiedPoint
    push_cast
    field_simp [hshiftC]
  unfold compactifiedStieltjesKernel
  calc
    (compactifiedStieltjesWeight w t x₀ : ℂ) *
        ((x₀ : ℂ) /
          stieltjesCompactifiedDenominator x₀ z (compactifiedPoint x₀ t)) =
        ((compactifiedStieltjesWeight w t x₀ : ℂ) * (x₀ : ℂ)) /
          stieltjesCompactifiedDenominator x₀ z (compactifiedPoint x₀ t) := by
      ring
    _ = ((w : ℂ) * (compactifiedPoint x₀ t : ℂ)) /
        ((compactifiedPoint x₀ t : ℂ) * ((t : ℂ) + z)) := by
      rw [hweight_mul, ← stieltjes_compactified_denominator_identity hx₀ ht z]
    _ = (w : ℂ) / ((t : ℂ) + z) := by
      field_simp [hpointC, htz]

private theorem stieltjesDiracFiniteMeasure_toMeasure (x : ℝ) :
    (stieltjesDiracFiniteMeasure x : Measure ℝ) = Measure.dirac x :=
  rfl

/-- The finite compactified measure integrates the compactified kernel to the
original finite Stieltjes sum. -/
theorem compactifiedStieltjesFiniteMeasure_transform_eq
    {ι : Type*} (s : Finset ι) (weight spectrum : ι → ℝ)
    (x₀ : ℝ) (z : ℂ)
    (hweight : ∀ i ∈ s, 0 ≤ weight i)
    (hspectrum : ∀ i ∈ s, 0 ≤ spectrum i)
    (hx₀ : 0 < x₀) (hz : z ∈ Complex.slitPlane) :
    compactifiedStieltjesTransform
        (compactifiedStieltjesFiniteMeasure s weight spectrum x₀)
        x₀ z hx₀ hz =
      finitePositiveStieltjes s weight spectrum z := by
  classical
  unfold compactifiedStieltjesTransform compactifiedStieltjesFiniteMeasure
  rw [FiniteMeasure.toMeasure_sum,
    MeasureTheory.integral_finsetSum_measure]
  · unfold finitePositiveStieltjes
    apply Finset.sum_congr rfl
    intro i hi
    rw [FiniteMeasure.toMeasure_smul,
      MeasureTheory.integral_smul_nnreal_measure,
      stieltjesDiracFiniteMeasure_toMeasure,
      MeasureTheory.integral_dirac]
    have hmem : compactifiedPoint x₀ (spectrum i) ∈ Set.Icc (0 : ℝ) 1 :=
      ⟨compactifiedPoint_nonneg hx₀ (hspectrum i hi),
        compactifiedPoint_le_one hx₀ (hspectrum i hi)⟩
    rw [compactifiedStieltjesKernelBCF_apply_of_mem hx₀ hz hmem]
    simp only [NNReal.smul_def, Complex.real_smul]
    rw [Real.coe_toNNReal _
      (compactifiedStieltjesWeight_nonneg
        (hweight i hi) (hspectrum i hi) hx₀)]
    exact compactifiedStieltjesWeight_mul_kernel
      (hspectrum i hi) hx₀ hz
  · intro i hi
    rw [FiniteMeasure.toMeasure_smul,
      stieltjesDiracFiniteMeasure_toMeasure]
    exact (MeasureTheory.integrable_dirac (by simp)).smul_measure_nnreal

/-- Weak convergence of finite measures implies convergence of every fixed
compactified slit-plane observable. -/
theorem tendsto_compactifiedStieltjesTransform_of_tendsto
    {κ : Type*} {F : Filter κ}
    {μs : κ → FiniteMeasure ℝ} {μ : FiniteMeasure ℝ}
    (hμ : Tendsto μs F (𝓝 μ))
    (x₀ : ℝ) (z : ℂ) (hx₀ : 0 < x₀)
    (hz : z ∈ Complex.slitPlane) :
    Tendsto (fun j => compactifiedStieltjesTransform (μs j) x₀ z hx₀ hz)
      F (𝓝 (compactifiedStieltjesTransform μ x₀ z hx₀ hz)) := by
  simpa [compactifiedStieltjesTransform] using
    ((FiniteMeasure.tendsto_iff_forall_integral_rclike_tendsto ℂ).1 hμ
      (compactifiedStieltjesKernelBCF x₀ z hx₀ hz))

/-- A weak limit of compactified finite approximants is a pointwise limit of
their finite Stieltjes transforms at every fixed slit-plane argument. -/
theorem tendsto_finitePositiveStieltjes_of_compactifiedMeasure_tendsto
    {κ ι : Type*} {F : Filter κ}
    (s : κ → Finset ι)
    (weight spectrum : κ → ι → ℝ)
    (x₀ : ℝ) (z : ℂ)
    (hweight : ∀ j i, i ∈ s j → 0 ≤ weight j i)
    (hspectrum : ∀ j i, i ∈ s j → 0 ≤ spectrum j i)
    (hx₀ : 0 < x₀) (hz : z ∈ Complex.slitPlane)
    {μ : FiniteMeasure ℝ}
    (hμ : Tendsto (fun j =>
      compactifiedStieltjesFiniteMeasure
        (s j) (weight j) (spectrum j) x₀) F (𝓝 μ)) :
    Tendsto (fun j =>
      finitePositiveStieltjes (s j) (weight j) (spectrum j) z)
      F (𝓝 (compactifiedStieltjesTransform μ x₀ z hx₀ hz)) := by
  have h := tendsto_compactifiedStieltjesTransform_of_tendsto
    hμ x₀ z hx₀ hz
  have hrewrite :
      (fun j => compactifiedStieltjesTransform
        (compactifiedStieltjesFiniteMeasure
          (s j) (weight j) (spectrum j) x₀)
        x₀ z hx₀ hz) =
      (fun j => finitePositiveStieltjes
        (s j) (weight j) (spectrum j) z) := by
    funext j
    exact compactifiedStieltjesFiniteMeasure_transform_eq
      (s j) (weight j) (spectrum j) x₀ z
      (hweight j) (hspectrum j) hx₀ hz
  rw [hrewrite] at h
  exact h

/-- The weak closure of a uniformly one-point-bounded family remains inside
the same mass-and-support controlled compact set. -/
theorem closure_range_compactifiedStieltjesFiniteMeasure_subset_family
    {κ ι : Type*}
    (s : κ → Finset ι)
    (weight spectrum : κ → ι → ℝ)
    (x₀ : ℝ) (M : ℝ≥0)
    (hweight : ∀ j i, i ∈ s j → 0 ≤ weight j i)
    (hspectrum : ∀ j i, i ∈ s j → 0 ≤ spectrum j i)
    (hx₀ : 0 < x₀)
    (hone : ∀ j,
      finitePositiveStieltjesAt (s j) (weight j) (spectrum j) x₀ ≤ (M : ℝ)) :
    closure (Set.range (fun j =>
      compactifiedStieltjesFiniteMeasure
        (s j) (weight j) (spectrum j) x₀)) ⊆
      compactifiedStieltjesMeasureFamily M := by
  exact closure_minimal
    (range_compactifiedStieltjesFiniteMeasure_subset_family
      s weight spectrum x₀ M hweight hspectrum hx₀ hone)
    (isCompact_compactifiedStieltjesMeasureFamily M).isClosed

end OnePointResolvent

import Mathlib.Analysis.PSeries

/-!
# Explicit deterministic tail bounds for the four-dimensional gamma model

This file formalizes the scalar p-series estimates behind the `O(K⁻¹)` mean
tail and `O(K⁻³)` variance tail in the mean-corrected gamma approximation to
Riemann Xi.  It makes no statement about zeta zeros.
-/

open Filter
open scoped BigOperators Topology

noncomputable section

namespace RiemannPrimeResolvent

/-- The elementary telescoping majorant for a quadratic tail. -/
theorem invSq_succ_le_telescope (n : ℕ) (hn : 0 < n) :
    (((n + 1 : ℕ) : ℝ)⁻¹) ^ 2 ≤
      ((n : ℝ)⁻¹ - (((n + 1 : ℕ) : ℝ)⁻¹)) := by
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  have hn1R : (0 : ℝ) < n + 1 := by positivity
  field_simp
  norm_num [Nat.cast_add] at *

/-- The elementary telescoping majorant for a quartic tail. -/
theorem invFourth_succ_le_telescope (n : ℕ) (hn : 0 < n) :
    (((n + 1 : ℕ) : ℝ)⁻¹) ^ 4 ≤
      (1 / 3 : ℝ) * (((n : ℝ)⁻¹) ^ 3 - (((n + 1 : ℕ) : ℝ)⁻¹) ^ 3) := by
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  have hn1R : (0 : ℝ) < n + 1 := by positivity
  field_simp
  norm_num [Nat.cast_add] at *
  ring_nf at *
  nlinarith [sq_nonneg (n : ℝ)]

/-- Explicit shifted quadratic p-series tail: `sum_{m≥0}(K+m+1)⁻² ≤ K⁻¹`. -/
theorem shifted_invSq_tsum_le (K : ℕ) (hK : 0 < K) :
    (∑' m : ℕ, ((((K + m + 1 : ℕ) : ℝ)⁻¹) ^ 2)) ≤ (K : ℝ)⁻¹ := by
  let r : ℕ → ℝ := fun m => (((K + m : ℕ) : ℝ)⁻¹)
  let g : ℕ → ℝ := fun m => r m - r (m + 1)
  have hr0 : Tendsto r atTop (nhds 0) := by
    have htop : Tendsto (fun m : ℕ => ((m : ℝ) + K)) atTop atTop :=
      Filter.tendsto_atTop_add_const_right atTop (K : ℝ) tendsto_natCast_atTop_atTop
    have hinv := tendsto_inv_atTop_zero.comp htop
    change Tendsto (fun m : ℕ => (((m : ℝ) + K)⁻¹)) atTop (nhds 0) at hinv
    dsimp [r]
    simpa only [Nat.cast_add, add_comm] using hinv
  have hg_nonneg : ∀ m, 0 ≤ g m := by
    intro m
    dsimp [g, r]
    have hpos : (0 : ℝ) < (K + m : ℕ) := by exact_mod_cast Nat.add_pos_left hK m
    have hpos' : (0 : ℝ) < (K + (m + 1) : ℕ) := by positivity
    apply sub_nonneg.mpr
    exact (inv_le_inv₀ hpos' hpos).2 (by exact_mod_cast Nat.le_add_right (K + m) 1)
  have hg : HasSum g (K : ℝ)⁻¹ := by
    rw [hasSum_iff_tendsto_nat_of_nonneg hg_nonneg]
    have htel : ∀ n, (∑ m ∈ Finset.range n, g m) = r 0 - r n := by
      intro n
      simpa [g] using Finset.sum_range_sub' r n
    simp_rw [htel]
    simpa [r] using
      (tendsto_const_nhds.sub hr0 :
        Tendsto (fun n => (K : ℝ)⁻¹ - r n) atTop (nhds ((K : ℝ)⁻¹ - 0)))
  have hle : ∀ m : ℕ, ((((K + m + 1 : ℕ) : ℝ)⁻¹) ^ 2) ≤ g m := by
    intro m
    exact invSq_succ_le_telescope (K + m) (Nat.add_pos_left hK m)
  have hf : Summable (fun m : ℕ => ((((K + m + 1 : ℕ) : ℝ)⁻¹) ^ 2)) :=
    hg.summable.of_nonneg_of_le (fun _ => by positivity) hle
  exact (Summable.tsum_le_tsum
    hle hf hg.summable).trans_eq hg.tsum_eq

/-- Explicit shifted quartic p-series tail: `sum_{m≥0}(K+m+1)⁻⁴ ≤ K⁻³/3`. -/
theorem shifted_invFourth_tsum_le (K : ℕ) (hK : 0 < K) :
    (∑' m : ℕ, ((((K + m + 1 : ℕ) : ℝ)⁻¹) ^ 4)) ≤
      (1 / 3 : ℝ) * ((K : ℝ)⁻¹) ^ 3 := by
  let r : ℕ → ℝ := fun m => (((K + m : ℕ) : ℝ)⁻¹) ^ 3
  let g : ℕ → ℝ := fun m => (1 / 3 : ℝ) * (r m - r (m + 1))
  have hr0 : Tendsto r atTop (nhds 0) := by
    have htop : Tendsto (fun m : ℕ => ((m : ℝ) + K)) atTop atTop :=
      Filter.tendsto_atTop_add_const_right atTop (K : ℝ) tendsto_natCast_atTop_atTop
    have hinv := tendsto_inv_atTop_zero.comp htop
    change Tendsto (fun m : ℕ => (((m : ℝ) + K)⁻¹)) atTop (nhds 0) at hinv
    dsimp [r]
    simpa only [Nat.cast_add, add_comm, zero_pow (by norm_num : 3 ≠ 0)] using hinv.pow 3
  have hg_nonneg : ∀ m, 0 ≤ g m := by
    intro m
    dsimp [g, r]
    have hpos : (0 : ℝ) < (K + m : ℕ) := by exact_mod_cast Nat.add_pos_left hK m
    have hpos' : (0 : ℝ) < (K + (m + 1) : ℕ) := by positivity
    have hbase : (((K + (m + 1) : ℕ) : ℝ)⁻¹) ≤ (((K + m : ℕ) : ℝ)⁻¹) :=
      (inv_le_inv₀ hpos' hpos).2 (by exact_mod_cast Nat.le_add_right (K + m) 1)
    have hcub : (((K + (m + 1) : ℕ) : ℝ)⁻¹) ^ 3 ≤
        (((K + m : ℕ) : ℝ)⁻¹) ^ 3 := by
      gcongr
    positivity
  have hg : HasSum g ((1 / 3 : ℝ) * ((K : ℝ)⁻¹) ^ 3) := by
    rw [hasSum_iff_tendsto_nat_of_nonneg hg_nonneg]
    have htel : ∀ n,
        (∑ m ∈ Finset.range n, g m) =
          (1 / 3 : ℝ) * (r 0 - r n) := by
      intro n
      change (∑ m ∈ Finset.range n, (1 / 3 : ℝ) * (r m - r (m + 1))) =
        (1 / 3 : ℝ) * (r 0 - r n)
      rw [← Finset.mul_sum, Finset.sum_range_sub']
    simp_rw [htel]
    simpa [r] using
      ((tendsto_const_nhds.sub hr0).const_mul (1 / 3 : ℝ))
  have hle : ∀ m : ℕ, ((((K + m + 1 : ℕ) : ℝ)⁻¹) ^ 4) ≤ g m := by
    intro m
    exact invFourth_succ_le_telescope (K + m) (Nat.add_pos_left hK m)
  have hf : Summable (fun m : ℕ => ((((K + m + 1 : ℕ) : ℝ)⁻¹) ^ 4)) :=
    hg.summable.of_nonneg_of_le (fun _ => by positivity) hle
  exact (Summable.tsum_le_tsum
    hle hf hg.summable).trans_eq hg.tsum_eq

/-- The explicit `O(K⁻¹)` deterministic bound for the gamma-tail mean. -/
theorem gammaMeanTail_le (K : ℕ) (hK : 0 < K) :
    (2 / Real.pi) * (∑' m : ℕ, ((((K + m + 1 : ℕ) : ℝ)⁻¹) ^ 2)) ≤
      (2 / Real.pi) * (K : ℝ)⁻¹ := by
  exact mul_le_mul_of_nonneg_left (shifted_invSq_tsum_le K hK) (by positivity)

/-- The explicit `O(K⁻³)` deterministic bound for the gamma-tail variance. -/
theorem gammaVarianceTail_le (K : ℕ) (hK : 0 < K) :
    (2 / Real.pi ^ 2) * (∑' m : ℕ, ((((K + m + 1 : ℕ) : ℝ)⁻¹) ^ 4)) ≤
      (2 / Real.pi ^ 2) * ((1 / 3 : ℝ) * ((K : ℝ)⁻¹) ^ 3) := by
  exact mul_le_mul_of_nonneg_left (shifted_invFourth_tsum_le K hK) (by positivity)

end RiemannPrimeResolvent

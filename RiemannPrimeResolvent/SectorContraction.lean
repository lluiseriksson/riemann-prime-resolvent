import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Sector dominance and contraction witnesses

After adding a nonnegative reserve `M`, an oriented cross term `c` can be
written as the difference between the positive candidates `M+c` and `M-c`.
This file calibrates the contraction strategy exactly: for nonnegative scalar
sectors, existence of a unit-interval contraction coefficient is equivalent to
the desired ordering, and for `M+c` and `M-c` that ordering is exactly `c >= 0`.
-/

namespace RiemannPrimeResolvent

def symmetricSectorEnergy (M c : ℝ) : ℝ := M + c
def antisymmetricSectorEnergy (M c : ℝ) : ℝ := M - c

/-- A reserve dominating `|c|` makes both reflection-sector energies
nonnegative. -/
theorem sectorEnergies_nonnegative_of_abs_le {M c : ℝ} (h : |c| ≤ M) :
    0 ≤ symmetricSectorEnergy M c ∧ 0 ≤ antisymmetricSectorEnergy M c := by
  constructor <;> simp only [symmetricSectorEnergy, antisymmetricSectorEnergy] <;>
    linarith [le_abs_self c, neg_le_abs c]

/-- For nonnegative scalar energies, dominance is equivalent to a contraction
coefficient in `[0,1]`. -/
theorem nonnegative_le_iff_exists_unitInterval_mul {S A : ℝ}
    (hS : 0 ≤ S) (hA : 0 ≤ A) :
    A ≤ S ↔ ∃ t : ℝ, 0 ≤ t ∧ t ≤ 1 ∧ A = t * S := by
  constructor
  · intro hAS
    by_cases hS0 : S = 0
    · subst S
      have hA0 : A = 0 := by linarith
      exact ⟨0, by norm_num, by norm_num, by simp [hA0]⟩
    · have hSpos : 0 < S := lt_of_le_of_ne hS (Ne.symm hS0)
      refine ⟨A / S, div_nonneg hA hS, (div_le_one hSpos).2 hAS, ?_⟩
      field_simp
  · rintro ⟨t, ht0, ht1, rfl⟩
    exact mul_le_of_le_one_left hS ht1

/-- Ordering the two reserved sectors remains exactly the sign of the
oriented cross term, independently of the reserve. -/
theorem sectorDominance_iff_cross_nonnegative (M c : ℝ) :
    antisymmetricSectorEnergy M c ≤ symmetricSectorEnergy M c ↔ 0 ≤ c := by
  simp only [symmetricSectorEnergy, antisymmetricSectorEnergy]
  constructor <;> intro h <;> linarith

/-- Even when both sectors are made nonnegative by a reserve, existence of a
contractive map from the symmetric energy to the antisymmetric energy is
equivalent to the original sign condition `c >= 0`. -/
theorem sectorContraction_exists_iff_cross_nonnegative {M c : ℝ}
    (hreserve : |c| ≤ M) :
    (∃ t : ℝ, 0 ≤ t ∧ t ≤ 1 ∧
      antisymmetricSectorEnergy M c = t * symmetricSectorEnergy M c) ↔ 0 ≤ c := by
  obtain ⟨hS, hA⟩ := sectorEnergies_nonnegative_of_abs_le hreserve
  rw [← sectorDominance_iff_cross_nonnegative M c]
  exact (nonnegative_le_iff_exists_unitInterval_mul hS hA).symm

end RiemannPrimeResolvent

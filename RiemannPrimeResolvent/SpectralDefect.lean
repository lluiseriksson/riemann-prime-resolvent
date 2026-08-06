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

/-- A strictly positive indexed gap makes the distinguished ground index the
unique index carrying its eigenvalue.  When indices enumerate an eigenbasis
with multiplicity, this is the exact combinatorial guard against a degenerate
ground eigenspace. -/
theorem groundIndex_unique_of_positive_gap
    {ι : Type*} (eigenvalue : ι → ℝ) (groundIndex : ι) (gap : ℝ)
    (hgap_pos : 0 < gap)
    (hgap : ∀ i, i ≠ groundIndex →
      eigenvalue groundIndex + gap ≤ eigenvalue i) :
    ∀ i, eigenvalue i = eigenvalue groundIndex → i = groundIndex := by
  intro i hi
  by_contra hne
  have hsep := hgap i hne
  linarith

/-- For an antitone finite eigenvalue list of length at least two, a gap
between the last (ground) entry and the penultimate entry propagates to every
other entry.  This reduces the universal indexed-gap certificate to one
adjacent inequality. -/
theorem antitone_gap_from_penultimate
    {n : ℕ} (eigenvalue : Fin (n + 2) → ℝ) (hanti : Antitone eigenvalue)
    (gap : ℝ)
    (hadjacent :
      eigenvalue (Fin.last (n + 1)) + gap ≤
        eigenvalue (Fin.castSucc (Fin.last n))) :
    ∀ i, i ≠ Fin.last (n + 1) →
      eigenvalue (Fin.last (n + 1)) + gap ≤ eigenvalue i := by
  intro i hi
  have hi_le_penultimate : i ≤ Fin.castSucc (Fin.last n) := by
    apply Fin.le_iff_val_le_val.mpr
    have hi_val_ne : i.val ≠ n + 1 := by
      intro hval
      apply hi
      apply Fin.ext
      simpa using hval
    change i.val ≤ n
    omega
  exact hadjacent.trans (hanti hi_le_penultimate)

/-- In an orthonormal eigenbasis, a gap above a distinguished ground state
forces the scalar Rayleigh/gap inequality.  This is the finite-dimensional
spectral-decomposition step that turns an eigenvalue gap into `hspectral` for
`norm_sub_le_sqrt_rayleigh_div_gap`. -/
theorem spectralGap_mul_one_sub_inner_sq_le_rayleighExcess_of_eigenbasis
    {ι E : Type*} [Fintype ι] [DecidableEq ι]
    [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (T : E →ₗ[ℝ] E) (b : OrthonormalBasis ι ℝ E) (eigenvalue : ι → ℝ)
    (heigen : ∀ i, T (b i) = eigenvalue i • b i)
    (groundIndex : ι) (trial : E) (gap : ℝ)
    (htrial : ‖trial‖ = 1)
    (hgap : ∀ i, i ≠ groundIndex →
      eigenvalue groundIndex + gap ≤ eigenvalue i) :
    gap * (1 - inner ℝ (b groundIndex) trial ^ 2) ≤
      inner ℝ (T trial) trial - eigenvalue groundIndex := by
  let coefficient : ι → ℝ := fun i => inner ℝ (b i) trial
  have hsum_sq : ∑ i, coefficient i ^ 2 = 1 := by
    simpa [coefficient, htrial] using b.sum_sq_inner_right trial
  have hrayleigh : inner ℝ (T trial) trial =
      ∑ i, eigenvalue i * coefficient i ^ 2 := by
    nth_rw 1 [← b.sum_repr' trial]
    simp only [map_sum, map_smul, sum_inner, heigen, real_inner_smul_left,
      smul_smul, coefficient]
    apply Finset.sum_congr rfl
    intro i _
    ring
  have hone_sub : 1 - coefficient groundIndex ^ 2 =
      ∑ i ∈ Finset.univ.erase groundIndex, coefficient i ^ 2 := by
    have hsplit := Finset.sum_erase_add (s := Finset.univ)
      (f := fun i => coefficient i ^ 2) (Finset.mem_univ groundIndex)
    rw [hsum_sq] at hsplit
    linarith
  have hlower :
      ∑ i ∈ Finset.univ.erase groundIndex, gap * coefficient i ^ 2 ≤
        ∑ i ∈ Finset.univ.erase groundIndex,
          (eigenvalue i - eigenvalue groundIndex) * coefficient i ^ 2 := by
    apply Finset.sum_le_sum
    intro i hi
    apply mul_le_mul_of_nonneg_right
    · linarith [hgap i (Finset.ne_of_mem_erase hi)]
    · positivity
  have hweighted :
      ∑ i, (eigenvalue i - eigenvalue groundIndex) * coefficient i ^ 2 =
        (∑ i, eigenvalue i * coefficient i ^ 2) -
          eigenvalue groundIndex * ∑ i, coefficient i ^ 2 := by
    simp_rw [sub_mul]
    rw [Finset.sum_sub_distrib, Finset.mul_sum]
  have herase :
      ∑ i, (eigenvalue i - eigenvalue groundIndex) * coefficient i ^ 2 =
        ∑ i ∈ Finset.univ.erase groundIndex,
          (eigenvalue i - eigenvalue groundIndex) * coefficient i ^ 2 := by
    calc
      ∑ i, (eigenvalue i - eigenvalue groundIndex) * coefficient i ^ 2 =
          (∑ i ∈ Finset.univ.erase groundIndex,
            (eigenvalue i - eigenvalue groundIndex) * coefficient i ^ 2) +
            (eigenvalue groundIndex - eigenvalue groundIndex) *
              coefficient groundIndex ^ 2 :=
        (Finset.sum_erase_add (s := Finset.univ)
          (f := fun i => (eigenvalue i - eigenvalue groundIndex) * coefficient i ^ 2)
          (Finset.mem_univ groundIndex)).symm
      _ = ∑ i ∈ Finset.univ.erase groundIndex,
          (eigenvalue i - eigenvalue groundIndex) * coefficient i ^ 2 := by ring
  calc
    gap * (1 - inner ℝ (b groundIndex) trial ^ 2) =
        ∑ i ∈ Finset.univ.erase groundIndex, gap * coefficient i ^ 2 := by
      rw [show inner ℝ (b groundIndex) trial = coefficient groundIndex from rfl,
        hone_sub, Finset.mul_sum]
    _ ≤ ∑ i ∈ Finset.univ.erase groundIndex,
          (eigenvalue i - eigenvalue groundIndex) * coefficient i ^ 2 := hlower
    _ = ∑ i, (eigenvalue i - eigenvalue groundIndex) * coefficient i ^ 2 :=
      herase.symm
    _ = inner ℝ (T trial) trial - eigenvalue groundIndex := by
      rw [hweighted, ← hrayleigh, hsum_sq]
      ring

/-- A finite-dimensional symmetric operator supplies the preceding diagonal
data through Mathlib's spectral theorem.  Thus the only operator-specific
input left here is the certified separation of every other eigenvalue from
the selected ground eigenvalue. -/
theorem spectralGap_mul_one_sub_inner_sq_le_rayleighExcess_of_isSymmetric
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] {n : ℕ}
    (T : E →ₗ[ℝ] E) (hT : T.IsSymmetric)
    (hn : Module.finrank ℝ E = n) (groundIndex : Fin n)
    (trial : E) (gap : ℝ) (htrial : ‖trial‖ = 1)
    (hgap : ∀ i, i ≠ groundIndex →
      hT.eigenvalues hn groundIndex + gap ≤ hT.eigenvalues hn i) :
    gap * (1 - inner ℝ (hT.eigenvectorBasis hn groundIndex) trial ^ 2) ≤
      inner ℝ (T trial) trial - hT.eigenvalues hn groundIndex := by
  exact spectralGap_mul_one_sub_inner_sq_le_rayleighExcess_of_eigenbasis
    T (hT.eigenvectorBasis hn) (hT.eigenvalues hn)
    (hT.apply_eigenvectorBasis hn) groundIndex trial gap htrial hgap

/-- For a finite-dimensional symmetric operator, the positive indexed gap
hypothesis forces the selected ground eigenspace itself to have dimension one.
This exposes, at statement level, the simplicity that the Rayleigh/gap bound
needs and rules out an orthogonal trial vector at the same eigenvalue. -/
theorem finrank_groundEigenspace_eq_one_of_positive_gap
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] {n : ℕ}
    (T : E →ₗ[ℝ] E) (hT : T.IsSymmetric)
    (hn : Module.finrank ℝ E = n) (groundIndex : Fin n) (gap : ℝ)
    (hgap_pos : 0 < gap)
    (hgap : ∀ i, i ≠ groundIndex →
      hT.eigenvalues hn groundIndex + gap ≤ hT.eigenvalues hn i) :
    Module.finrank ℝ
      (Module.End.eigenspace T (hT.eigenvalues hn groundIndex)) = 1 := by
  rw [← hT.card_filter_eigenvalues_eq hn]
  refine Finset.card_eq_one.mpr ⟨groundIndex, ?_⟩
  ext i
  simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_singleton]
  constructor
  · exact groundIndex_unique_of_positive_gap
      (hT.eigenvalues hn) groundIndex gap hgap_pos hgap i
  · intro hi
    subst i
    rfl

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

/-- Operator-level Rayleigh/gap distance bound.  For a finite-dimensional
symmetric operator, a positive certified eigenvalue gap and phase alignment
imply the distance estimate without taking the scalar inequality as a separate
hypothesis. -/
theorem norm_eigenvectorBasis_sub_trial_le_sqrt_rayleigh_div_gap
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] {n : ℕ}
    (T : E →ₗ[ℝ] E) (hT : T.IsSymmetric)
    (hn : Module.finrank ℝ E = n) (groundIndex : Fin n)
    (trial : E) (gap : ℝ) (htrial : ‖trial‖ = 1)
    (hoverlap_nonneg :
      0 ≤ inner ℝ (hT.eigenvectorBasis hn groundIndex) trial)
    (hgap_pos : 0 < gap)
    (hgap : ∀ i, i ≠ groundIndex →
      hT.eigenvalues hn groundIndex + gap ≤ hT.eigenvalues hn i) :
    ‖hT.eigenvectorBasis hn groundIndex - trial‖ ≤
      Real.sqrt (2 *
        (inner ℝ (T trial) trial - hT.eigenvalues hn groundIndex) / gap) := by
  let ground := hT.eigenvectorBasis hn groundIndex
  let overlap := inner ℝ ground trial
  let rayleighExcess := inner ℝ (T trial) trial - hT.eigenvalues hn groundIndex
  have hspectral : gap * (1 - overlap ^ 2) ≤ rayleighExcess := by
    exact spectralGap_mul_one_sub_inner_sq_le_rayleighExcess_of_isSymmetric
      T hT hn groundIndex trial gap htrial hgap
  have hground : ‖ground‖ = 1 := (hT.eigenvectorBasis hn).norm_eq_one groundIndex
  have hoverlap_le_one : overlap ≤ 1 := by
    exact real_inner_le_one_of_norm_eq_one hground htrial
  have hone_sq_nonneg : 0 ≤ 1 - overlap ^ 2 := by
    dsimp [overlap, ground] at hoverlap_nonneg ⊢
    nlinarith
  have hr : 0 ≤ rayleighExcess :=
    (mul_nonneg hgap_pos.le hone_sq_nonneg).trans hspectral
  exact norm_sub_le_sqrt_rayleigh_div_gap hground htrial rfl
    hoverlap_nonneg hr hgap_pos hspectral

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

/-- End-to-end finite Galerkin bound for a symmetric operator.  Mathlib's
finite spectral theorem discharges the former scalar `hspectral` premise;
the remaining concrete certificates are the positive eigenvalue separation,
phase alignment, projection normalization, and tail bound. -/
theorem norm_scaled_eigenvectorBasis_sub_complete_le_rayleighGapDefect
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] {n : ℕ}
    (T : E →ₗ[ℝ] E) (hT : T.IsSymmetric)
    (hn : Module.finrank ℝ E = n) (groundIndex : Fin n)
    (trial complete projected : E) (gap tail : ℝ)
    (htrial : ‖trial‖ = 1)
    (hoverlap_nonneg :
      0 ≤ inner ℝ (hT.eigenvectorBasis hn groundIndex) trial)
    (hgap_pos : 0 < gap)
    (hgap : ∀ i, i ≠ groundIndex →
      hT.eigenvalues hn groundIndex + gap ≤ hT.eigenvalues hn i)
    (hprojected : projected = ‖projected‖ • trial)
    (htail : ‖complete - projected‖ ≤ tail) :
    ‖‖complete‖ • hT.eigenvectorBasis hn groundIndex - complete‖ ≤
      rayleighGapDefect ‖complete‖
        (inner ℝ (T trial) trial - hT.eigenvalues hn groundIndex) gap tail := by
  apply norm_scaled_ground_sub_complete_le htrial hprojected
  · exact norm_eigenvectorBasis_sub_trial_le_sqrt_rayleigh_div_gap
      T hT hn groundIndex trial gap htrial hoverlap_nonneg hgap_pos hgap
  · exact htail

/-- Statement-level guarded version of the end-to-end estimate: the same
positive indexed gap simultaneously certifies that the ground eigenspace is
one-dimensional and proves the Galerkin approximation bound. -/
theorem simpleGround_and_norm_scaled_eigenvectorBasis_sub_complete_le
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] {n : ℕ}
    (T : E →ₗ[ℝ] E) (hT : T.IsSymmetric)
    (hn : Module.finrank ℝ E = n) (groundIndex : Fin n)
    (trial complete projected : E) (gap tail : ℝ)
    (htrial : ‖trial‖ = 1)
    (hoverlap_nonneg :
      0 ≤ inner ℝ (hT.eigenvectorBasis hn groundIndex) trial)
    (hgap_pos : 0 < gap)
    (hgap : ∀ i, i ≠ groundIndex →
      hT.eigenvalues hn groundIndex + gap ≤ hT.eigenvalues hn i)
    (hprojected : projected = ‖projected‖ • trial)
    (htail : ‖complete - projected‖ ≤ tail) :
    Module.finrank ℝ
        (Module.End.eigenspace T (hT.eigenvalues hn groundIndex)) = 1 ∧
      ‖‖complete‖ • hT.eigenvectorBasis hn groundIndex - complete‖ ≤
        rayleighGapDefect ‖complete‖
          (inner ℝ (T trial) trial - hT.eigenvalues hn groundIndex) gap tail := by
  constructor
  · exact finrank_groundEigenspace_eq_one_of_positive_gap
      T hT hn groundIndex gap hgap_pos hgap
  · exact norm_scaled_eigenvectorBasis_sub_complete_le_rayleighGapDefect
      T hT hn groundIndex trial complete projected gap tail htrial
      hoverlap_nonneg hgap_pos hgap hprojected htail

/-- Adjacent-gap version of the guarded end-to-end theorem.  Because Mathlib
sorts the eigenvalues of a finite symmetric operator in decreasing order, for
dimension `n + 2` it is enough to separate the last eigenvalue from the
penultimate one.  The conclusion still exposes both ground-state simplicity
and the Galerkin approximation bound. -/
theorem simpleGround_and_norm_scaled_eigenvectorBasis_sub_complete_le_of_adjacentGap
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] {n : ℕ}
    (T : E →ₗ[ℝ] E) (hT : T.IsSymmetric)
    (hn : Module.finrank ℝ E = n + 2)
    (trial complete projected : E) (gap tail : ℝ)
    (htrial : ‖trial‖ = 1)
    (hoverlap_nonneg :
      0 ≤ inner ℝ (hT.eigenvectorBasis hn (Fin.last (n + 1))) trial)
    (hgap_pos : 0 < gap)
    (hadjacent :
      hT.eigenvalues hn (Fin.last (n + 1)) + gap ≤
        hT.eigenvalues hn (Fin.castSucc (Fin.last n)))
    (hprojected : projected = ‖projected‖ • trial)
    (htail : ‖complete - projected‖ ≤ tail) :
    Module.finrank ℝ
        (Module.End.eigenspace T
          (hT.eigenvalues hn (Fin.last (n + 1)))) = 1 ∧
      ‖‖complete‖ • hT.eigenvectorBasis hn (Fin.last (n + 1)) - complete‖ ≤
        rayleighGapDefect ‖complete‖
          (inner ℝ (T trial) trial -
            hT.eigenvalues hn (Fin.last (n + 1))) gap tail := by
  have hgap : ∀ i, i ≠ Fin.last (n + 1) →
      hT.eigenvalues hn (Fin.last (n + 1)) + gap ≤ hT.eigenvalues hn i :=
    antitone_gap_from_penultimate (hT.eigenvalues hn)
      (hT.eigenvalues_antitone hn) gap hadjacent
  exact simpleGround_and_norm_scaled_eigenvectorBasis_sub_complete_le
    T hT hn (Fin.last (n + 1)) trial complete projected gap tail htrial
    hoverlap_nonneg hgap_pos hgap hprojected htail

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

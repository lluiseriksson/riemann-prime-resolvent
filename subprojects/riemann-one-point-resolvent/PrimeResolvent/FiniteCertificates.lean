import PrimeResolvent.ResolventCompactification

/-!
# Finite Gram certificates

These definitions expose the positive sum-of-squares certificates behind
finite Hankel and localizing matrix tests.  They deliberately avoid any claim
about the infinite Hausdorff moment theorem.
-/

set_option autoImplicit false

namespace PrimeResolvent

open scoped BigOperators

/-- Evaluation of a finite coefficient vector on a monomial vector. -/
def evalMonomialVector
    {ι : Type*} [Fintype ι] {N : ℕ}
    (point : ι → ℝ) (coeff : Fin N → ℝ) (a : ι) : ℝ :=
  ∑ i, coeff i * point a ^ (i : ℕ)

/-- Gram/sum-of-squares certificate for a finite atomic Hankel matrix. -/
def atomicHankelCertificate
    {ι : Type*} [Fintype ι] {N : ℕ}
    (weight point : ι → ℝ) (coeff : Fin N → ℝ) : ℝ :=
  ∑ a, weight a * (evalMonomialVector point coeff a) ^ 2

/-- Localizing sum-of-squares certificate for support in `[0,1]`. -/
def atomicLocalizingCertificate
    {ι : Type*} [Fintype ι] {N : ℕ}
    (weight point : ι → ℝ) (coeff : Fin N → ℝ) : ℝ :=
  ∑ a, weight a * (1 - point a) *
    (evalMonomialVector point coeff a) ^ 2

/-- Positive atomic weights make every finite Hankel Gram certificate
nonnegative. -/
theorem atomicHankelCertificate_nonneg
    {ι : Type*} [Fintype ι] {N : ℕ}
    (weight point : ι → ℝ) (coeff : Fin N → ℝ)
    (hweight : ∀ a, 0 ≤ weight a) :
    0 ≤ atomicHankelCertificate weight point coeff := by
  classical
  unfold atomicHankelCertificate
  apply Finset.sum_nonneg
  intro a ha
  exact mul_nonneg (hweight a) (sq_nonneg _)

/-- If all atoms lie below one, every finite localizing certificate is
nonnegative. -/
theorem atomicLocalizingCertificate_nonneg
    {ι : Type*} [Fintype ι] {N : ℕ}
    (weight point : ι → ℝ) (coeff : Fin N → ℝ)
    (hweight : ∀ a, 0 ≤ weight a)
    (hpoint1 : ∀ a, point a ≤ 1) :
    0 ≤ atomicLocalizingCertificate weight point coeff := by
  classical
  unfold atomicLocalizingCertificate
  apply Finset.sum_nonneg
  intro a ha
  exact mul_nonneg
    (mul_nonneg (hweight a) (sub_nonneg.mpr (hpoint1 a)))
    (sq_nonneg _)

/-- Resolvent compactification supplies a nonnegative finite Hankel
certificate. -/
theorem finiteResolventHankelCertificate_nonneg
    {ι : Type*} [Fintype ι] {N : ℕ}
    (x₀ : ℝ) (spectrum : ι → ℝ) (coeff : Fin N → ℝ)
    (hx₀ : 0 < x₀)
    (hspectrum : ∀ i, 0 ≤ spectrum i) :
    0 ≤ atomicHankelCertificate
      (fun i => resolventWeight x₀ (spectrum i))
      (fun i => compactifiedPoint x₀ (spectrum i)) coeff := by
  apply atomicHankelCertificate_nonneg
  intro i
  exact resolventWeight_nonneg hx₀ (hspectrum i)

/-- Resolvent compactification supplies a nonnegative localizing
certificate. -/
theorem finiteResolventLocalizingCertificate_nonneg
    {ι : Type*} [Fintype ι] {N : ℕ}
    (x₀ : ℝ) (spectrum : ι → ℝ) (coeff : Fin N → ℝ)
    (hx₀ : 0 < x₀)
    (hspectrum : ∀ i, 0 ≤ spectrum i) :
    0 ≤ atomicLocalizingCertificate
      (fun i => resolventWeight x₀ (spectrum i))
      (fun i => compactifiedPoint x₀ (spectrum i)) coeff := by
  apply atomicLocalizingCertificate_nonneg
  · intro i
    exact resolventWeight_nonneg hx₀ (hspectrum i)
  · intro i
    exact compactifiedPoint_le_one hx₀ (hspectrum i)

end PrimeResolvent

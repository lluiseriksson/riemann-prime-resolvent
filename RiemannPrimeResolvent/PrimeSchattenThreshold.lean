import Mathlib.NumberTheory.SumPrimeReciprocals

/-!
# Prime Schatten summability thresholds

The diagonal prime family with singular values `p⁻ˢ` belongs to the scalar
`q`-summability class exactly when `q * σ > 1`, where `σ` is the real part of
the spectral parameter.  This file formalizes the series-theoretic core of
the Schatten threshold; no statement about zeta zeros is used.
-/

noncomputable section

namespace RiemannPrimeResolvent

/-- The `q`-power sum of the prime singular values converges precisely beyond
the line `q * σ = 1`. -/
theorem primeSchattenSummable_iff {q σ : ℝ} :
    Summable (fun p : Nat.Primes => (p : ℝ) ^ (-(q * σ))) ↔ 1 < q * σ := by
  rw [Nat.Primes.summable_rpow]
  constructor <;> intro h <;> linarith

/-- Trace-class scalar threshold for the prime diagonal family. -/
theorem primeTraceSummable_iff {σ : ℝ} :
    Summable (fun p : Nat.Primes => (p : ℝ) ^ (-σ)) ↔ 1 < σ := by
  simpa using (primeSchattenSummable_iff (q := 1) (σ := σ))

/-- Hilbert--Schmidt scalar threshold: the critical boundary is `σ = 1/2`. -/
theorem primeHilbertSchmidtSummable_iff {σ : ℝ} :
    Summable (fun p : Nat.Primes => (p : ℝ) ^ (-(2 * σ))) ↔ (1 / 2 : ℝ) < σ := by
  rw [Nat.Primes.summable_rpow]
  constructor <;> intro h <;> linarith

end RiemannPrimeResolvent

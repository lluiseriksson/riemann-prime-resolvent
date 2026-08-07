import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Data.Nat.Totient
import Mathlib.Data.Real.Basic

/-!
# Positive feature lift for the critical GCD kernel

This file formalizes the finite algebraic core of the prime-coordinate
dimensional lift. It proves positivity of every finite weighted feature
energy and records the divisor-totient identity underlying the normalized
GCD kernel. It makes no restriction estimate and no claim about the
Riemann hypothesis.
-/

namespace RiemannPrimeResolvent

open scoped BigOperators

/-- A finite feature energy with nonnegative feature weights is nonnegative. -/
theorem finiteFeatureSquareEnergy_nonneg
    {ι κ : Type*} (features : Finset κ) (points : Finset ι)
    (weight : κ → ℝ) (feature : κ → ι → ℝ) (coefficient : ι → ℝ)
    (hweight : ∀ k ∈ features, 0 ≤ weight k) :
    0 ≤ ∑ k ∈ features,
      weight k * (∑ i ∈ points, coefficient i * feature k i) ^ 2 := by
  exact Finset.sum_nonneg fun k hk =>
    mul_nonneg (hweight k hk) (sq_nonneg _)

/-- Finite dual synthesis is just a reindexing of the feature expansion.

This is the algebraic core of reconstructing a scalar observable from a
family of divisor features. It deliberately assumes the pointwise synthesis
identity; controlling the norm of a concrete arithmetic dual family is a
separate analytic obligation. -/
theorem finiteDualSynthesis
    {ι κ : Type*} (features : Finset κ) (points : Finset ι)
    (dual : κ → ℝ) (feature : κ → ι → ℝ)
    (coefficient target : ι → ℝ)
    (hsynthesis : ∀ i ∈ points,
      target i = ∑ k ∈ features, dual k * feature k i) :
    ∑ i ∈ points, coefficient i * target i =
      ∑ k ∈ features, dual k *
        (∑ i ∈ points, coefficient i * feature k i) := by
  calc
    ∑ i ∈ points, coefficient i * target i =
        ∑ i ∈ points, ∑ k ∈ features,
          coefficient i * (dual k * feature k i) := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [hsynthesis i hi, Finset.mul_sum]
    _ = ∑ k ∈ features, ∑ i ∈ points,
          coefficient i * (dual k * feature k i) := by
      rw [Finset.sum_comm]
    _ = ∑ k ∈ features, dual k *
          (∑ i ∈ points, coefficient i * feature k i) := by
      apply Finset.sum_congr rfl
      intro k _
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i _
      ring

/-- Squared Cauchy--Schwarz bound for a finite dual-feature pairing.

Weights such as `φ(d)` can be absorbed into `dual` and `signal`; the theorem
then exposes the exact product of dual cost and feature energy. -/
theorem finiteDualPairing_sq_le
    {κ : Type*} (features : Finset κ) (dual signal : κ → ℝ) :
    (∑ k ∈ features, dual k * signal k) ^ 2 ≤
      (∑ k ∈ features, dual k ^ 2) *
        (∑ k ∈ features, signal k ^ 2) := by
  exact Finset.sum_mul_sq_le_sq_mul_sq features dual signal

/-- The common-divisor feature weights sum to the gcd. This is the
pointwise arithmetic identity behind the critical GCD Gram matrix. -/
theorem natGcd_eq_totientSum (m n : ℕ) :
    Nat.gcd m n =
      ∑ d ∈ (Nat.gcd m n).divisors, Nat.totient d :=
  (Nat.sum_totient (Nat.gcd m n)).symm

end RiemannPrimeResolvent

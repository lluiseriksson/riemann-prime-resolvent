import Mathlib.NumberTheory.Ostrowski
import Mathlib.NumberTheory.Divisors
import Mathlib.NumberTheory.NumberField.ProductFormula

/-!
# Rational numbers and their non-Archimedean coordinates

The completions of `ℚ` provide a rigorous interpretation of infinitely many
"hidden dimensions": one real place and one `p`-adic place for every prime.
This file records the finiteness restriction that is essential for arithmetic:
a fixed rational number has nonzero valuation at only finitely many places.
-/

noncomputable section

namespace RiemannPrimeResolvent

/-- Ostrowski's classification, exposed here as the precise answer to why
prime-indexed completions occur: every nontrivial real-valued absolute value
on `ℚ` is equivalent either to the ordinary absolute value or to the `p`-adic
absolute value for a unique prime `p`. -/
theorem rationalAbsoluteValue_real_or_unique_padic
    (f : AbsoluteValue ℚ ℝ) (hf : f.IsNontrivial) :
    f ≈ Rat.AbsoluteValue.real ∨
      ∃! p, ∃ (_ : Fact p.Prime), f ≈ Rat.AbsoluteValue.padic p :=
  Rat.AbsoluteValue.equiv_real_or_padic f hf

/-- A finite over-approximation to the nonzero `p`-adic coordinates of a
rational: divisors of its numerator or denominator. -/
def rationalPadicSupport (q : ℚ) : Finset ℕ :=
  q.num.natAbs.divisors ∪ q.den.divisors

/-- Outside `rationalPadicSupport q`, the `p`-adic valuation of `q` is zero.
This holds for every natural index `p`; primality is not needed for the
vanishing statement. -/
theorem padicValRat_eq_zero_of_not_mem_support (q : ℚ) (p : ℕ)
    (hp : p ∉ rationalPadicSupport q) :
    padicValRat p q = 0 := by
  by_cases hq : q = 0
  · subst q
    simp
  · have hnum0 : q.num.natAbs ≠ 0 := Int.natAbs_ne_zero.mpr (Rat.num_ne_zero.2 hq)
    have hden0 : q.den ≠ 0 := q.den_ne_zero
    have hpnum : ¬p ∣ q.num.natAbs := by
      intro hdiv
      apply hp
      simp [rationalPadicSupport, Nat.mem_divisors, hdiv, hnum0]
    have hpden : ¬p ∣ q.den := by
      intro hdiv
      apply hp
      simp [rationalPadicSupport, Nat.mem_divisors, hdiv, hden0]
    rw [padicValRat_def, padicValInt.eq_zero_of_not_dvd, padicValNat.eq_zero_of_not_dvd hpden]
    · simp
    · simpa [Int.natCast_dvd] using hpnum

/-- The set of natural indices with a nonzero valuation is finite.  In
particular, infinitely many completions do not give a rational infinitely many
independent arithmetic coordinates. -/
theorem finite_setOf_padicValRat_ne_zero (q : ℚ) :
    {p : ℕ | padicValRat p q ≠ 0}.Finite := by
  refine (rationalPadicSupport q).finite_toSet.subset ?_
  intro p hp
  by_contra hpmem
  exact hp (padicValRat_eq_zero_of_not_mem_support q p hpmem)

/-- Restricting to prime indices preserves the finite-support conclusion. -/
theorem finite_setOf_prime_and_padicValRat_ne_zero (q : ℚ) :
    {p : ℕ | p.Prime ∧ padicValRat p q ≠ 0}.Finite := by
  exact (finite_setOf_padicValRat_ne_zero q).subset (by
    intro p hp
    exact hp.2)

/-- At each genuine prime place, multiplication of nonzero rationals becomes
addition of integer coordinates.  Thus the prime valuations are arithmetic
coordinates, but by the preceding theorem each rational vector is finitely
supported. -/
theorem primeCoordinate_mul {p : ℕ} [Fact p.Prime] {q r : ℚ}
    (hq : q ≠ 0) (hr : r ≠ 0) :
    padicValRat p (q * r) = padicValRat p q + padicValRat p r :=
  padicValRat.mul hq hr

/-- The global product formula specialized to the rational number field.  It
is the exact multiplicative conservation law coupling the Archimedean place
to all finite places. -/
theorem rational_global_product_formula {q : ℚ} (hq : q ≠ 0) :
    (∏ w : NumberField.InfinitePlace ℚ, w q ^ w.mult) *
        ∏ᶠ w : NumberField.FinitePlace ℚ, w q = 1 :=
  NumberField.prod_abs_eq_one hq

/-- Additive form of the rational product formula: the logarithmic
Archimedean contribution is exactly the negative of the total finite-place
contribution. -/
theorem rational_global_log_balance {q : ℚ} (hq : q ≠ 0) :
    Real.log (∏ w : NumberField.InfinitePlace ℚ, w q ^ w.mult) =
      -Real.log (∏ᶠ w : NumberField.FinitePlace ℚ, w q) := by
  let A : ℝ := ∏ w : NumberField.InfinitePlace ℚ, w q ^ w.mult
  let B : ℝ := ∏ᶠ w : NumberField.FinitePlace ℚ, w q
  have hAB : A * B = 1 := rational_global_product_formula hq
  have hA : A ≠ 0 := by
    intro h
    simp [h] at hAB
  have hB : B ≠ 0 := by
    intro h
    simp [h] at hAB
  have hlog := congrArg Real.log hAB
  rw [Real.log_mul hA hB, Real.log_one] at hlog
  change Real.log A = -Real.log B
  linarith

/-- Squaring the global logarithmic balance yields only a null quadratic
direction.  This records why the product formula by itself supplies
cancellation but no strict positivity. -/
theorem rational_global_log_balance_sq {q : ℚ} (hq : q ≠ 0) :
    (Real.log (∏ w : NumberField.InfinitePlace ℚ, w q ^ w.mult) +
      Real.log (∏ᶠ w : NumberField.FinitePlace ℚ, w q)) ^ 2 = 0 := by
  rw [rational_global_log_balance hq]
  ring

end RiemannPrimeResolvent

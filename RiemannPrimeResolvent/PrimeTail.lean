/-
Copyright (c) 2026 Lluís Eriksson.
Released under the GNU Affero General Public License v3.0.
-/

import Mathlib.Analysis.SumIntegralComparisons
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt
import Mathlib.Topology.Algebra.InfiniteSum.Real
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Push


open Set MeasureTheory
open scoped BigOperators

/-!
# Closed-form model for the omitted-prime tail

RF-1: the actual von Mangoldt tail is summable and bounded by the closed form
for an integer cutoff `N >= 3`, `delta > 0`, and `sigma >= 1 + delta`.
The proof bounds finite partial sums using `vonMangoldt_le_log`, monotonicity,
and a finite sum-integral comparison, then deduces summability. No zero-location
or spectral premise is used. The continuous square cutoff is linked only when
it equals the last included integer; arbitrary real cutoff substitution is invalid.
-/

namespace RiemannPrimeResolvent

/-- The elementary integral majorant
`X⁻δ (log X / δ + 1 / δ²)`, written without real-power notation. -/
noncomputable def primeTailMajorant (δ X : ℝ) : ℝ :=
  Real.exp (-δ * Real.log X) *
    (Real.log X / δ + 1 / δ ^ 2)

/-- The closed-form tail majorant is nonnegative in its intended range. -/
theorem primeTailMajorant_nonneg {δ X : ℝ}
    (hδ : 0 < δ) (hX : 1 ≤ X) :
    0 ≤ primeTailMajorant δ X := by
  have hlog : 0 ≤ Real.log X := Real.log_nonneg hX
  have hδsq : 0 < δ ^ 2 := sq_pos_of_pos hδ
  unfold primeTailMajorant
  exact mul_nonneg (Real.exp_pos _).le
    (add_nonneg (div_nonneg hlog hδ.le)
      (div_nonneg zero_le_one hδsq.le))

/-- Resolvent-scaled prime tail associated with `a > 1/2` and cutoff `lam²`. -/
noncomputable def resolventPrimeTailMajorant (a lam : ℝ) : ℝ :=
  primeTailMajorant (a - 1 / 2) (lam ^ 2) / (2 * a)

/-- Nonnegativity of the scaled majorant. -/
theorem resolventPrimeTailMajorant_nonneg {a lam : ℝ}
    (ha : 1 / 2 < a) (hLam : 1 ≤ lam) :
    0 ≤ resolventPrimeTailMajorant a lam := by
  have hδ : 0 < a - 1 / 2 := by linarith
  have hLamSq : 1 ≤ lam ^ 2 := by nlinarith [sq_nonneg (lam - 1)]
  have ha0 : 0 < 2 * a := by linarith
  unfold resolventPrimeTailMajorant
  exact div_nonneg (primeTailMajorant_nonneg hδ hLamSq) ha0.le

private noncomputable def tailKernel (δ x : ℝ) : ℝ :=
  Real.log x * Real.exp (-(1 + δ) * Real.log x)

private theorem kernel_deriv (δ : ℝ) {x : ℝ} (hx : 0 < x) :
    HasDerivAt (tailKernel δ)
      (Real.exp (-(1 + δ) * Real.log x) / x * (1 - (1 + δ) * Real.log x)) x := by
  have hlog := Real.hasDerivAt_log hx.ne'
  convert! hlog.mul ((hlog.const_mul (-(1 + δ))).exp) using 1
  field_simp
  <;> ring

private theorem majorant_deriv {δ x : ℝ} (hδ : 0 < δ) (hx : 0 < x) :
    HasDerivAt (primeTailMajorant δ) (-tailKernel δ x) x := by
  have hlog := Real.hasDerivAt_log hx.ne'
  have he : Real.exp (-(1 + δ) * Real.log x) = Real.exp (-δ * Real.log x) / x := by
    rw [show -(1 + δ) * Real.log x = -δ * Real.log x + -Real.log x by ring,
      Real.exp_add, Real.exp_neg, Real.exp_log hx, div_eq_mul_inv]
  convert! ((hlog.const_mul (-δ)).exp).mul
    ((hlog.div_const δ).add_const (1 / δ ^ 2)) using 1
  simp only [tailKernel, he]
  field_simp [hδ.ne', hx.ne']
  <;> ring

private theorem kernel_antitone {δ : ℝ} (hδ : 0 < δ) :
    AntitoneOn (tailKernel δ) (Ici 3) := by
  apply antitoneOn_of_deriv_nonpos (convex_Ici 3)
  · intro x hx
    exact (kernel_deriv δ (by have := hx; change 3 ≤ x at this; linarith)).continuousAt.continuousWithinAt
  · intro x hx
    have hx3 : 3 ≤ x := interior_subset hx
    exact (kernel_deriv δ (by linarith)).differentiableAt.differentiableWithinAt
  · intro x hx
    have hx3 : 3 ≤ x := interior_subset hx
    have hx0 : 0 < x := by linarith
    rw [(kernel_deriv δ hx0).deriv]
    have hl : 1 ≤ Real.log x := by
      apply Real.exp_le_exp.mp
      rw [Real.exp_log hx0]
      exact Real.exp_one_lt_three.le.trans hx3
    apply mul_nonpos_of_nonneg_of_nonpos
    · exact div_nonneg (Real.exp_pos _).le hx0.le
    · nlinarith

private theorem majorant_nonneg {δ x : ℝ} (hδ : 0 < δ) (hx : 1 ≤ x) :
    0 ≤ primeTailMajorant δ x := by
  unfold primeTailMajorant
  exact mul_nonneg (Real.exp_pos _).le
    (add_nonneg (div_nonneg (Real.log_nonneg hx) hδ.le)
      (div_nonneg zero_le_one (sq_nonneg δ)))

private theorem kernel_sum_bound {δ : ℝ} {N : ℕ} (hδ : 0 < δ) (hN : 3 ≤ N)
    (m : ℕ) :
    (∑ i ∈ Finset.range m, tailKernel δ (N + (i + 1 : ℕ))) ≤ primeTailMajorant δ N := by
  have hN3 : (3 : ℝ) ≤ N := by exact_mod_cast hN
  have hNm : (N : ℝ) ≤ N + m := le_add_of_nonneg_right (Nat.cast_nonneg m)
  have ha : AntitoneOn (tailKernel δ) (Icc (N : ℝ) (N + m)) :=
    (kernel_antitone hδ).mono (fun x hx => le_trans hN3 hx.1)
  have hi : IntervalIntegrable (tailKernel δ) volume (N : ℝ) (N + m) :=
    (ha.mono (by rw [uIcc_of_le hNm])).intervalIntegrable
  have hd : ∀ x ∈ uIcc (N : ℝ) (N + m),
      HasDerivAt (fun y => -primeTailMajorant δ y) (tailKernel δ x) x := by
    intro x hx
    rw [uIcc_of_le hNm] at hx
    have hx0 : 0 < x := by linarith [hx.1]
    convert! (majorant_deriv hδ hx0).neg using 1 <;> simp
  have he := intervalIntegral.integral_eq_sub_of_hasDerivAt hd hi
  calc
    (∑ i ∈ Finset.range m, tailKernel δ (N + (i + 1 : ℕ)))
        ≤ ∫ x in (N : ℝ)..N + m, tailKernel δ x := ha.sum_le_integral
    _ = primeTailMajorant δ N - primeTailMajorant δ (N + m) := by rw [he]; ring
    _ ≤ primeTailMajorant δ N := sub_le_self _ (majorant_nonneg hδ (by linarith))

/-- The omitted von Mangoldt contribution, indexed from the first omitted integer. -/
noncomputable def primeTailTerm (σ : ℝ) (N k : ℕ) : ℝ :=
  ArithmeticFunction.vonMangoldt (N + (k + 1)) / ((N + (k + 1) : ℕ) : ℝ) ^ σ

private theorem primeTailTerm_nonneg (σ : ℝ) (N k : ℕ) :
    0 ≤ primeTailTerm σ N k := by
  unfold primeTailTerm
  exact div_nonneg ArithmeticFunction.vonMangoldt_nonneg (Real.rpow_nonneg (by positivity) _)

private theorem primeTailTerm_le_kernel {δ σ : ℝ} {N : ℕ}
    (hN : 3 ≤ N) (hσ : 1 + δ ≤ σ) (k : ℕ) :
    primeTailTerm σ N k ≤ tailKernel δ (N + (k + 1 : ℕ)) := by
  let n : ℕ := N + (k + 1)
  have hn : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast (show 1 ≤ n by dsimp [n]; omega)
  have hn0 : (0 : ℝ) < (n : ℝ) := by linarith
  have hlog : 0 ≤ Real.log (n : ℝ) := Real.log_nonneg hn
  have hΛ := ArithmeticFunction.vonMangoldt_le_log (n := n)
  have hpow : (n : ℝ) ^ (1 + δ) ≤ (n : ℝ) ^ σ :=
    Real.rpow_le_rpow_of_exponent_le hn hσ
  have heq : (N : ℝ) + (k + 1 : ℕ) = (n : ℝ) := by simp only [n, Nat.cast_add]
  unfold primeTailTerm tailKernel
  rw [heq]
  change ArithmeticFunction.vonMangoldt n / (n : ℝ) ^ σ ≤
    Real.log (n : ℝ) * Real.exp (-(1 + δ) * Real.log (n : ℝ))
  calc
    ArithmeticFunction.vonMangoldt n / (n : ℝ) ^ σ
      ≤ Real.log (n : ℝ) / (n : ℝ) ^ σ :=
        div_le_div_of_nonneg_right hΛ (Real.rpow_nonneg hn0.le _)
    _ ≤ Real.log (n : ℝ) / (n : ℝ) ^ (1 + δ) :=
        div_le_div_of_nonneg_left hlog (Real.rpow_pos_of_pos hn0 _) hpow
    _ = Real.log (n : ℝ) * Real.exp (-(1 + δ) * Real.log (n : ℝ)) := by
        rw [Real.rpow_def_of_pos hn0, div_eq_mul_inv, ← Real.exp_neg]
        congr 2
        ring

theorem primeTail_summable_and_le {δ σ : ℝ} {N : ℕ}
    (hN : 3 ≤ N) (hδ : 0 < δ) (hσ : 1 + δ ≤ σ) :
    Summable (primeTailTerm σ N) ∧
      (∑' k, primeTailTerm σ N k) ≤ primeTailMajorant δ N := by
  have hb : ∀ m, (∑ k ∈ Finset.range m, primeTailTerm σ N k) ≤ primeTailMajorant δ N := by
    intro m
    exact (Finset.sum_le_sum (fun k _ => primeTailTerm_le_kernel hN hσ k)).trans
      (kernel_sum_bound hδ hN m)
  exact ⟨summable_of_sum_range_le (primeTailTerm_nonneg σ N) hb,
    Real.tsum_le_of_sum_range_le (primeTailTerm_nonneg σ N) hb⟩


/-- The same integer cutoff is retained in the scaled arithmetic error. -/
theorem scaled_integer_primeTail_le {a : ℝ} {N : ℕ}
    (ha : 1 / 2 < a) (hN : 3 ≤ N) :
    (∑' k, primeTailTerm (a + 1 / 2) N k) / (2 * a)
      ≤ primeTailMajorant (a - 1 / 2) N / (2 * a) := by
  have h := primeTail_summable_and_le (δ := a - 1 / 2) (σ := a + 1 / 2)
    hN (by linarith) (by linarith)
  exact div_le_div_of_nonneg_right h.2 (by linarith)

/-- The existing continuous parameter can be used directly only with an
explicit agreement between its square and the last included integer. -/
theorem scaled_primeTail_le_of_integer_square {a lam : ℝ} {N : ℕ}
    (ha : 1 / 2 < a) (hN : 3 ≤ N) (hcut : (N : ℝ) = lam ^ 2) :
    (∑' k, primeTailTerm (a + 1 / 2) N k) / (2 * a)
      ≤ resolventPrimeTailMajorant a lam := by
  simpa only [resolventPrimeTailMajorant, ← hcut] using scaled_integer_primeTail_le ha hN


end RiemannPrimeResolvent

import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.Analysis.Calculus.ContDiff.RestrictScalars
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-!
# A first-order Taylor remainder bound

This file isolates the analytic mechanism used by the mean-corrected gamma
approximation: after subtraction of the linear term, a twice differentiable
function has a quadratic remainder.  It is independent of zeta and of any
probabilistic model.
-/

open MeasureTheory Set
open scoped Interval

noncomputable section

namespace RiemannPrimeResolvent

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- The order-one Taylor polynomial on a set, written without polynomial machinery. -/
theorem taylorWithinEval_one (f : ℝ → E) (s : Set ℝ) (a t : ℝ) :
    taylorWithinEval f 1 s a t =
      f a + (t - a) • derivWithin f s a := by
  rw [show (1 : ℕ) = 0 + 1 by norm_num, taylorWithinEval_succ]
  simp

/-- A quadratic bound after removing the linear Taylor term on an ordered interval.

The constant is the one supplied by Mathlib's general vector-valued Taylor
bound.  It is deliberately a factor two weaker than the sharp integral
remainder used on paper; the `O((t-a)^2)` mechanism is already explicit.
-/
theorem firstOrderTaylorWithin_remainder_bound
    {f : ℝ → E} {a b C t : ℝ} (hab : a ≤ b)
    (hf : ContDiffOn ℝ 2 f (Icc a b)) (ht : t ∈ Icc a b)
    (hC : ∀ y ∈ Icc a b,
      ‖iteratedDerivWithin 2 f (Icc a b) y‖ ≤ C) :
    ‖f t - f a - (t - a) • derivWithin f (Icc a b) a‖ ≤
      C * (t - a) ^ 2 := by
  have h := taylor_mean_remainder_bound (n := 1) hab hf ht hC
  rw [taylorWithinEval_one] at h
  calc
    ‖f t - f a - (t - a) • derivWithin f (Icc a b) a‖ =
        ‖f t - (f a + (t - a) • derivWithin f (Icc a b) a)‖ := by
      congr 1
      abel
    _ ≤ C * (t - a) ^ 2 / (Nat.factorial 1 : ℝ) := by simpa using h
    _ = C * (t - a) ^ 2 := by norm_num

/-- The sharp, orientation-free first-order Taylor bound obtained from the
integral remainder.  Unlike `firstOrderTaylorWithin_remainder_bound`, this
handles either order of the endpoints and includes the factor `1/2`. -/
theorem firstOrderTaylor_remainder_bound_sharp
    [CompleteSpace E] {f : ℝ → E} {x x₀ C : ℝ} (hC0 : 0 ≤ C)
    (hf : ContDiffOn ℝ 2 f (uIcc x₀ x))
    (hC : ∀ y ∈ uIcc x₀ x,
      ‖iteratedDerivWithin 2 f (uIcc x₀ x) y‖ ≤ C) :
    ‖f x - f x₀ - (x - x₀) • derivWithin f (uIcc x₀ x) x₀‖ ≤
      C * |x - x₀| ^ 2 / 2 := by
  have hTaylor := taylor_integral_remainder (n := 1) hf
  rw [taylorWithinEval_one] at hTaylor
  have hpoint : ∀ᵐ t : ℝ ∂volume.restrict (Ι x₀ x),
      ‖(((x - t) ^ 1 / (Nat.factorial 1 : ℝ)) •
        iteratedDerivWithin 2 f (uIcc x₀ x) t)‖ ≤ C * |x - t| := by
    rw [ae_restrict_iff' measurableSet_uIoc]
    filter_upwards with t
    intro ht
    simp only [pow_one, Nat.factorial_one, Nat.cast_one, div_one, norm_smul,
      Real.norm_eq_abs]
    simpa [mul_comm] using
      mul_le_mul_of_nonneg_left (hC t (uIoc_subset_uIcc ht)) (abs_nonneg (x - t))
  have hbound : IntervalIntegrable (fun t : ℝ => C * |x - t|) volume x₀ x :=
    (continuous_const.mul (continuous_const.sub continuous_id).abs).intervalIntegrable _ _
  have hnorm := intervalIntegral.norm_integral_le_abs_of_norm_le (μ := volume) hpoint hbound
  have hcalc :
      abs (∫ t : ℝ in x₀..x, C * |x - t|) = C * |x - x₀| ^ 2 / 2 := by
    rw [intervalIntegral.abs_integral_eq_abs_integral_uIoc]
    have hpow := integral_pow_abs_sub_uIoc (a := x) (b := x₀) (n := 1)
    norm_num at hpow
    rw [uIoc_comm x₀ x]
    simp_rw [abs_sub_comm x]
    rw [integral_const_mul, hpow]
    rw [abs_mul, abs_of_nonneg hC0, abs_of_nonneg (by positivity)]
    simp only [sq_abs]
    ring_nf
  calc
    ‖f x - f x₀ - (x - x₀) • derivWithin f (uIcc x₀ x) x₀‖ =
        ‖f x - (f x₀ + (x - x₀) • derivWithin f (uIcc x₀ x) x₀)‖ := by
      congr 1
      abel
    _ = ‖∫ t in x₀..x, ((x - t) ^ 1 / (Nat.factorial 1 : ℝ)) •
        iteratedDerivWithin 2 f (uIcc x₀ x) t‖ := congrArg norm hTaylor
    _ ≤ abs (∫ t : ℝ in x₀..x, C * |x - t|) := hnorm
    _ = C * |x - x₀| ^ 2 / 2 := hcalc

/-- The second-derivative kernel of a shifted complex power is controlled by
the left endpoint whenever the real part of the exponent is at most two. -/
theorem shiftedCpow_secondDerivative_norm_le
    {x u : ℝ} {p : ℂ} (hx : 0 < x) (hu : 0 ≤ u) (hp : p.re ≤ 2) :
    ‖p * (p - 1) * (((x + u : ℝ) : ℂ) ^ (p - 2))‖ ≤
      ‖p * (p - 1)‖ * x ^ (p.re - 2) := by
  rw [norm_mul, Complex.norm_cpow_eq_rpow_re_of_pos (by linarith)]
  norm_num [Complex.sub_re]
  exact mul_le_mul_of_nonneg_left
    (Real.rpow_le_rpow_of_nonpos hx (by linarith) (by linarith))
    (mul_nonneg (norm_nonneg p) (norm_nonneg (p - 1)))

/-- First derivative of a shifted complex power along the positive real axis. -/
theorem hasDerivAt_shiftedCpow {x u : ℝ} {p : ℂ}
    (hxu : 0 < x + u) (hp : p ≠ 0) :
    HasDerivAt (fun v : ℝ => (((x + v : ℝ) : ℂ) ^ p))
      (p * (((x + u : ℝ) : ℂ) ^ (p - 1))) u := by
  have hinner : HasDerivAt (fun v : ℝ => x + v) 1 u :=
    (hasDerivAt_id u).const_add x
  have hfun : (fun v : ℝ => (((x + v : ℝ) : ℂ) ^ p)) =
      (fun y : ℝ => (y : ℂ) ^ p) ∘ (fun v : ℝ => x + v) := by
    funext v
    simp [Complex.ofReal_add]
  rw [hfun]
  simpa only [one_smul] using
    (hasDerivAt_ofReal_cpow_const hxu.ne' hp).scomp u hinner

/-- Derivative of the first-derivative expression for a shifted complex power. -/
theorem hasDerivAt_shiftedCpow_deriv {x u : ℝ} {p : ℂ}
    (hxu : 0 < x + u) (hp1 : p - 1 ≠ 0) :
    HasDerivAt
      (fun v : ℝ => p * (((x + v : ℝ) : ℂ) ^ (p - 1)))
      (p * (p - 1) * (((x + u : ℝ) : ℂ) ^ (p - 2))) u := by
  have hinner : HasDerivAt (fun v : ℝ => x + v) 1 u :=
    (hasDerivAt_id u).const_add x
  have hpow0 := (hasDerivAt_ofReal_cpow_const hxu.ne' hp1).scomp u hinner
  simp only [one_smul] at hpow0
  have hcomp :
      ((fun y : ℝ => (y : ℂ) ^ (p - 1)) ∘ HAdd.hAdd x) =
        ((fun y : ℝ => (y : ℂ) ^ (p - 1)) ∘ (fun v : ℝ => x + v)) := by
    funext v
    rfl
  rw [hcomp] at hpow0
  have hpow : HasDerivAt
      ((fun y : ℝ => (y : ℂ) ^ (p - 1)) ∘ (fun v : ℝ => x + v))
      ((p - 1) * (((x + u : ℝ) : ℂ) ^ (p - 2))) u := by
    convert hpow0 using 1
    congr 2
    ring_nf
  have hfun : (fun v : ℝ => p * (((x + v : ℝ) : ℂ) ^ (p - 1))) =
      (fun v : ℝ => p *
        (((fun y : ℝ => (y : ℂ) ^ (p - 1)) ∘ (fun w : ℝ => x + w)) v)) := by
    funext v
    simp [Complex.ofReal_add]
  rw [hfun]
  simpa [mul_assoc] using hpow.const_mul p

/-- A shifted complex power is twice continuously real-differentiable on any
interval that stays in the positive half-line. -/
theorem contDiffOn_shiftedCpow {x a b : ℝ} {p : ℂ}
    (hpos : 0 < x + min a b) :
    ContDiffOn ℝ 2 (fun u : ℝ => (((x + u : ℝ) : ℂ) ^ p)) (uIcc a b) := by
  have hdiff : DifferentiableOn ℂ (fun z : ℂ => z ^ p) Complex.slitPlane :=
    differentiableOn_id.cpow_const (fun z hz => hz)
  have houterC : ContDiffOn ℂ 2 (fun z : ℂ => z ^ p) Complex.slitPlane :=
    hdiff.contDiffOn Complex.isOpen_slitPlane
  have houterR : ContDiffOn ℝ 2 (fun z : ℂ => z ^ p) Complex.slitPlane :=
    houterC.restrict_scalars ℝ
  have hinner : ContDiffOn ℝ 2 (fun u : ℝ => ((x + u : ℝ) : ℂ)) (uIcc a b) := by
    have hreal : ContDiff ℝ 2 (fun u : ℝ => x + u) := by fun_prop
    have hcomplex := Complex.ofRealCLM.contDiff.comp hreal
    convert hcomplex.contDiffOn using 1
    ext u
    rfl
  have hmap : MapsTo (fun u : ℝ => ((x + u : ℝ) : ℂ)) (uIcc a b) Complex.slitPlane := by
    intro u hu
    exact Complex.ofReal_mem_slitPlane.2 (by
      have hmin : min a b ≤ u := hu.1
      linarith)
  have hcomp := houterR.comp hinner hmap
  simpa [Function.comp_def, Complex.ofReal_add] using hcomp

/-- On a nondegenerate positive interval, the second iterated derivative
within the interval is the expected complex-power expression. -/
theorem iteratedDerivWithin_two_shiftedCpow {x a b y : ℝ} {p : ℂ}
    (hab : a ≠ b) (hpos : 0 < x + min a b) (hy : y ∈ uIcc a b)
    (hp : p ≠ 0) (hp1 : p - 1 ≠ 0) :
    iteratedDerivWithin 2 (fun u : ℝ => (((x + u : ℝ) : ℂ) ^ p))
        (uIcc a b) y =
      p * (p - 1) * (((x + y : ℝ) : ℂ) ^ (p - 2)) := by
  have hu : UniqueDiffOn ℝ (uIcc a b) := uniqueDiffOn_Icc (by grind)
  have hpositive : ∀ z ∈ uIcc a b, 0 < x + z := by
    intro z hz
    have hzmin : min a b ≤ z := hz.1
    linarith
  have hfirst : EqOn
      (derivWithin (fun u : ℝ => (((x + u : ℝ) : ℂ) ^ p)) (uIcc a b))
      (fun u : ℝ => p * (((x + u : ℝ) : ℂ) ^ (p - 1))) (uIcc a b) := by
    intro z hz
    exact (hasDerivAt_shiftedCpow (hpositive z hz) hp).hasDerivWithinAt.derivWithin
      (hu z hz)
  rw [show (2 : ℕ) = 1 + 1 by norm_num, iteratedDerivWithin_succ,
    iteratedDerivWithin_one]
  rw [derivWithin_congr hfirst (hfirst hy)]
  exact (hasDerivAt_shiftedCpow_deriv (hpositive y hy) hp1).hasDerivWithinAt.derivWithin
    (hu y hy)

/-- Sharp first-order Taylor remainder for a shifted complex power on the
positive half-line.  The explicit constant is taken at the leftmost point of
the unoriented interval. -/
theorem shiftedCpow_firstOrder_remainder_bound
    {x a b : ℝ} {p : ℂ} (hpos : 0 < x + min a b)
    (hp : p ≠ 0) (hp1 : p - 1 ≠ 0) (hpre : p.re ≤ 2) :
    ‖(((x + b : ℝ) : ℂ) ^ p) - (((x + a : ℝ) : ℂ) ^ p) -
        (b - a) • (p * (((x + a : ℝ) : ℂ) ^ (p - 1)))‖ ≤
      ‖p * (p - 1)‖ * (x + min a b) ^ (p.re - 2) * |b - a| ^ 2 / 2 := by
  by_cases hab : a = b
  · subst b
    simp
  · have hu : UniqueDiffOn ℝ (uIcc a b) := uniqueDiffOn_Icc (by grind)
    have ha : a ∈ uIcc a b := left_mem_uIcc
    have hderiv :
        derivWithin (fun u : ℝ => (((x + u : ℝ) : ℂ) ^ p)) (uIcc a b) a =
          p * (((x + a : ℝ) : ℂ) ^ (p - 1)) :=
      (hasDerivAt_shiftedCpow (by
        have hamin : min a b ≤ a := min_le_left _ _
        linarith) hp).hasDerivWithinAt.derivWithin (hu a ha)
    rw [← hderiv]
    apply firstOrderTaylor_remainder_bound_sharp (by positivity)
      (contDiffOn_shiftedCpow hpos)
    intro y hy
    rw [iteratedDerivWithin_two_shiftedCpow hab hpos hy hp hp1]
    have hymin : 0 ≤ y - min a b := sub_nonneg.mpr hy.1
    convert shiftedCpow_secondDerivative_norm_le hpos hymin hpre using 1
    ring_nf

/-- Centering kills the integrated linear Taylor term on a probability
space.  This algebraic lemma is the bridge from a pointwise quadratic
remainder to a variance estimate. -/
theorem integral_centeredTaylor_eq_remainder
    {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]
    [CompleteSpace E] {X : Ω → ℝ} {f : ℝ → E} {x₀ : ℝ} (d : E)
    (hX : Integrable X μ) (hfX : Integrable (fun ω => f (X ω)) μ)
    (hmean : ∫ ω, X ω ∂μ = x₀) :
    (∫ ω, f (X ω) ∂μ) - f x₀ =
      ∫ ω, f (X ω) - f x₀ - (X ω - x₀) • d ∂μ := by
  have hconst : Integrable (fun _ : Ω => f x₀) μ := integrable_const _
  have hcenter : Integrable (fun ω => X ω - x₀) μ := hX.sub (integrable_const _)
  have hlin : Integrable (fun ω => (X ω - x₀) • d) μ :=
    hcenter.smul_const d
  calc
    (∫ ω, f (X ω) ∂μ) - f x₀ =
        ∫ ω, f (X ω) - f x₀ ∂μ := by
      rw [integral_sub hfX hconst]
      simp
    _ = ∫ ω, (f (X ω) - f x₀ - (X ω - x₀) • d) +
        (X ω - x₀) • d ∂μ := by
      congr 1
      funext ω
      abel
    _ = (∫ ω, f (X ω) - f x₀ - (X ω - x₀) • d ∂μ) +
        ∫ ω, (X ω - x₀) • d ∂μ := by
      rw [integral_add]
      exact (hfX.sub hconst).sub hlin
      exact hlin
    _ = ∫ ω, f (X ω) - f x₀ - (X ω - x₀) • d ∂μ := by
      rw [integral_smul_const]
      have : ∫ ω, X ω - x₀ ∂μ = 0 := by
        rw [integral_sub hX (integrable_const _), hmean]
        simp
      rw [this, zero_smul, add_zero]

/-- An integrated pointwise Taylor bound: after centering, the norm of the
expectation defect is bounded by the expected quadratic remainder. -/
theorem norm_integral_centeredTaylor_le
    {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]
    [CompleteSpace E] {X : Ω → ℝ} {f : ℝ → E} {x₀ C : ℝ} (d : E)
    (hX : Integrable X μ) (hfX : Integrable (fun ω => f (X ω)) μ)
    (hmean : ∫ ω, X ω ∂μ = x₀)
    (hquad : Integrable (fun ω => C * |X ω - x₀| ^ 2 / 2) μ)
    (hpoint : ∀ᵐ ω ∂μ,
      ‖f (X ω) - f x₀ - (X ω - x₀) • d‖ ≤ C * |X ω - x₀| ^ 2 / 2) :
    ‖(∫ ω, f (X ω) ∂μ) - f x₀‖ ≤
      ∫ ω, C * |X ω - x₀| ^ 2 / 2 ∂μ := by
  rw [integral_centeredTaylor_eq_remainder d hX hfX hmean]
  exact norm_integral_le_of_norm_le hquad hpoint

end RiemannPrimeResolvent

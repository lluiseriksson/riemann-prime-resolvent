import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic

/-!
# Barrier for the automatic positive spectral compression

For the trace-zero kernel `[[a,c],[c,-a]]`, the positive spectral branch is
controlled by `sqrt (a^2+c^2)`.  This is always nonnegative, but it is even in
the signed cross term `c`.  The results below isolate the resulting
relativization barrier: data that only see `c^2` or the spectral radius cannot
characterize the sign `c >= 0`.
-/

namespace RiemannPrimeResolvent

noncomputable section

/-- Spectral radius of a real symmetric trace-zero two-sector kernel. -/
def traceZeroSpectralRadius (a c : ℝ) : ℝ :=
  Real.sqrt (a ^ 2 + c ^ 2)

theorem traceZeroSpectralRadius_nonneg (a c : ℝ) :
    0 ≤ traceZeroSpectralRadius a c :=
  Real.sqrt_nonneg _

theorem traceZeroSpectralRadius_sq (a c : ℝ) :
    traceZeroSpectralRadius a c ^ 2 = a ^ 2 + c ^ 2 := by
  rw [traceZeroSpectralRadius, Real.sq_sqrt]
  positivity

/-- Flipping the signed prime--Archimedean cross term leaves the spectral
radius unchanged. -/
theorem traceZeroSpectralRadius_neg_cross (a c : ℝ) :
    traceZeroSpectralRadius a (-c) = traceZeroSpectralRadius a c := by
  simp [traceZeroSpectralRadius]

/-- No predicate depending only on `c^2` can characterize `c >= 0` for all
real `c`: the values `1` and `-1` are indistinguishable to such a predicate. -/
theorem no_squareInvariant_predicate_characterizes_nonnegative (P : ℝ → Prop) :
    ¬(∀ c : ℝ, (0 ≤ c ↔ P (c ^ 2))) := by
  intro h
  have hP : P (1 : ℝ) := by
    have := (h 1).mp (by norm_num)
    simpa using this
  have hneg : 0 ≤ (-1 : ℝ) := by
    apply (h (-1)).mpr
    simpa using hP
  norm_num at hneg

/-- More directly, no predicate of the positive spectral radius at fixed `a`
can characterize the sign of the cross term. -/
theorem no_spectralRadius_predicate_characterizes_cross_nonnegative
    (a : ℝ) (P : ℝ → Prop) :
    ¬(∀ c : ℝ, (0 ≤ c ↔ P (traceZeroSpectralRadius a c))) := by
  intro h
  have hP : P (traceZeroSpectralRadius a 1) :=
    (h 1).mp (by norm_num)
  have hsame : traceZeroSpectralRadius a (-1) = traceZeroSpectralRadius a 1 :=
    traceZeroSpectralRadius_neg_cross a 1
  have hneg : 0 ≤ (-1 : ℝ) := by
    apply (h (-1)).mpr
    rwa [hsame]
  norm_num at hneg

end

end RiemannPrimeResolvent

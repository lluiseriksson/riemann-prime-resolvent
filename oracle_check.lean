import RiemannPrimeResolvent

#print axioms RiemannPrimeResolvent.ErrorBudget.total_nonneg
#print axioms RiemannPrimeResolvent.three_step_triangle
#print axioms RiemannPrimeResolvent.error_le_budget
#print axioms RiemannPrimeResolvent.ErrorBudget.tendsto_total_zero
#print axioms RiemannPrimeResolvent.VanishingBudget.total
#print axioms RiemannPrimeResolvent.finiteStieltjes_nonneg
#print axioms RiemannPrimeResolvent.finiteSquaredResolvent_nonneg
#print axioms RiemannPrimeResolvent.half_finitePairedTrace
#print axioms RiemannPrimeResolvent.primeTailMajorant_nonneg
#print axioms RiemannPrimeResolvent.resolventPrimeTailMajorant_nonneg
#print axioms RiemannPrimeResolvent.primeTail_summable_and_le
#print axioms RiemannPrimeResolvent.scaled_integer_primeTail_le
#print axioms RiemannPrimeResolvent.scaled_primeTail_le_of_integer_square
#print axioms RiemannPrimeResolvent.beatsHalfThreshold_witness
#print axioms RiemannPrimeResolvent.publicationGate_delivers
#print axioms RiemannPrimeResolvent.rateExponent_pos
#print axioms RiemannPrimeResolvent.rateExponent_le_two_thirds
#print axioms RiemannPrimeResolvent.rateExponent_eq_two_thirds
#print axioms RiemannPrimeResolvent.rateExponent_eq_spectral
#print axioms RiemannPrimeResolvent.rayleighGapDefect_nonneg
#print axioms RiemannPrimeResolvent.residualGapDefect_nonneg

-- Semantic regression: smallest allowed cutoff and the exact square bridge.
example : Summable (RiemannPrimeResolvent.primeTailTerm 2 3) :=
  (RiemannPrimeResolvent.primeTail_summable_and_le
    (δ := 1) (by norm_num) (by norm_num) (by norm_num)).1

example : RiemannPrimeResolvent.primeTailTerm 2 3 0 =
    ArithmeticFunction.vonMangoldt 4 / (4 : Real) ^ (2 : Real) := by rfl

example : (∑' k, RiemannPrimeResolvent.primeTailTerm (3 / 2) 4 k) / 2 ≤
    RiemannPrimeResolvent.resolventPrimeTailMajorant 1 2 := by
  simpa only [show (1 : Real) + 1 / 2 = 3 / 2 by norm_num, mul_one] using
    RiemannPrimeResolvent.scaled_primeTail_le_of_integer_square
    (a := 1) (lam := 2) (N := 4) (by norm_num) (by norm_num) (by norm_num)

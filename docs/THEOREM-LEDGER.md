# Lean theorem ledger

The rows marked `verified` are machine-checked against `oracle_check.lean` by
`scripts/check_oracle_coverage.py`. Each entry is exact, fully qualified and in
the same order as its `#print axioms` command.

| Declaration | Status | Meaning |
|---|---|---|
| `RiemannPrimeResolvent.ErrorBudget.total_nonneg` | verified | nonnegative components give nonnegative total |
| `RiemannPrimeResolvent.three_step_triangle` | verified | three-stage deterministic comparison |
| `RiemannPrimeResolvent.error_le_budget` | verified | component bounds imply a total bound |
| `RiemannPrimeResolvent.ErrorBudget.tendsto_total_zero` | verified | componentwise zero limits give total zero |
| `RiemannPrimeResolvent.finiteStieltjes_nonneg` | verified | positivity of finite Stieltjes sums |
| `RiemannPrimeResolvent.finiteSquaredResolvent_nonneg` | verified | positivity of finite squared resolvents |
| `RiemannPrimeResolvent.half_finitePairedTrace` | verified | removes paired-spectrum double counting |
| `RiemannPrimeResolvent.primeTailMajorant_nonneg` | verified | closed-form majorant is nonnegative |
| `RiemannPrimeResolvent.resolventPrimeTailMajorant_nonneg` | verified | scaled majorant is nonnegative |
| `RiemannPrimeResolvent.rateExponent_pos` | verified | positivity of the candidate rate exponent |
| `RiemannPrimeResolvent.rateExponent_le_two_thirds` | verified | universal two-thirds ceiling |
| `RiemannPrimeResolvent.rateExponent_eq_two_thirds` | verified | saturated branch formula |
| `RiemannPrimeResolvent.rateExponent_eq_spectral` | verified | spectral branch formula |
| `RiemannPrimeResolvent.rayleighGapDefect_nonneg` | verified | nonnegativity of the Rayleigh/gap scalar defect |
| `RiemannPrimeResolvent.residualGapDefect_nonneg` | verified | nonnegativity of the residual/gap scalar defect |

The full integer-cutoff prime-tail inequality, slit-plane criterion and concrete
operator convergence are not present as verified declarations.

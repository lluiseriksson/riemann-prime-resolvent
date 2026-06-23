# Lean theorem ledger

The verified rows below are synchronized one-for-one with
`OnePointResolvent/Oracle.lean` by `scripts/check_oracle_coverage.py`. They cover
only the finite certificate layer; they do not state the analytic RH criterion.

| Declaration | Status | Meaning |
|---|---|---|
| `OnePointResolvent.hausdorffDiff_atomicMoment` | verified | exact finite signed-difference formula for atomic moments |
| `OnePointResolvent.atomicMoment_isHausdorffCompletelyMonotone` | verified | finite positive atoms on `[0,1]` give complete monotonicity |
| `OnePointResolvent.finiteResolventMoment_isHausdorffCompletelyMonotone` | verified | compactified finite spectra give Hausdorff moments |
| `OnePointResolvent.finiteResolventHankelCertificate_nonneg` | verified | finite resolvent Hankel certificate is nonnegative |
| `OnePointResolvent.finiteResolventLocalizingCertificate_nonneg` | verified | finite localizing certificate is nonnegative |
| `OnePointResolvent.resolvent_errorBudget` | verified | deterministic three-stage resolvent error budget |

The infinite Hausdorff representation theorem, holomorphic slit-plane extension
and equivalence with RH remain documented analytic targets rather than
kernel-checked declarations.

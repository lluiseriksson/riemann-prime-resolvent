# Lean theorem ledger

The verified rows below are synchronized one-for-one with every public
`theorem`/`lemma` in the `OnePointResolvent` namespace and with
`OnePointResolvent/Oracle.lean` by `scripts/check_oracle_coverage.py`. The actual
Lean report must contain the same ordered declarations and may depend only on
`Classical.choice`, `Quot.sound` and `propext`. These rows cover the finite
certificate and local Stieltjes-domination layers; they do not state the
analytic RH criterion.

| Declaration | Status | Meaning |
|---|---|---|
| `OnePointResolvent.hausdorffDiff_zero` | verified | zeroth signed difference is the original sequence |
| `OnePointResolvent.hausdorffDiff_succ` | verified | recursive signed forward-difference identity |
| `OnePointResolvent.hausdorffDiff_atomicMoment` | verified | exact finite signed-difference formula for atomic moments |
| `OnePointResolvent.atomicMoment_isHausdorffCompletelyMonotone` | verified | finite positive atoms on `[0,1]` give complete monotonicity |
| `OnePointResolvent.hausdorffDiff_atomicMoment_nonneg` | verified | every finite atomic signed difference is nonnegative |
| `OnePointResolvent.spectrum_shift_pos` | verified | a nonnegative spectral value has positive shifted denominator |
| `OnePointResolvent.resolventWeight_nonneg` | verified | finite resolvent weights are nonnegative |
| `OnePointResolvent.compactifiedPoint_nonneg` | verified | compactified spectral coordinates are nonnegative |
| `OnePointResolvent.compactifiedPoint_le_one` | verified | compactified spectral coordinates are at most one |
| `OnePointResolvent.finiteResolventMoment_isHausdorffCompletelyMonotone` | verified | compactified finite spectra give Hausdorff moments |
| `OnePointResolvent.finiteResolventMoment_hausdorffDiff_nonneg` | verified | finite resolvent signed differences are nonnegative |
| `OnePointResolvent.atomicHankelCertificate_nonneg` | verified | nonnegative atoms give nonnegative Hankel certificates |
| `OnePointResolvent.atomicLocalizingCertificate_nonneg` | verified | support below one gives nonnegative localizing certificates |
| `OnePointResolvent.finiteResolventHankelCertificate_nonneg` | verified | finite resolvent Hankel certificate is nonnegative |
| `OnePointResolvent.finiteResolventLocalizingCertificate_nonneg` | verified | finite localizing certificate is nonnegative |
| `OnePointResolvent.abs_sub_le_three` | verified | deterministic three-link triangle inequality |
| `OnePointResolvent.resolvent_errorBudget` | verified | deterministic three-stage resolvent error budget |
| `OnePointResolvent.finitePositiveStieltjesAt_nonneg` | verified | positive finite Stieltjes one-point values are nonnegative |
| `OnePointResolvent.stieltjes_disk_denominator_bound` | verified | half-radius disk gives a universal factor-two denominator comparison |
| `OnePointResolvent.stieltjes_atom_norm_le_two` | verified | one positive atom is controlled by twice its center value |
| `OnePointResolvent.finitePositiveStieltjes_norm_le_two` | verified | finite positive sums inherit the factor-two disk bound |
| `OnePointResolvent.finitePositiveStieltjes_family_norm_le_two` | verified | one-point family bounds are uniform in cutoffs, weights and spectra |

The arbitrary-compact domination theorem, infinite Hausdorff representation,
holomorphic slit-plane extension and equivalence with RH remain documented
analytic targets rather than kernel-checked declarations.

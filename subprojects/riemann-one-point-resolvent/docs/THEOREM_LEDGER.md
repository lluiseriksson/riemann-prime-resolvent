# Lean theorem ledger

The verified rows below are synchronized one-for-one with every public
`theorem`/`lemma` in the `OnePointResolvent` namespace and with
`OnePointResolvent/Oracle.lean` by `scripts/check_oracle_coverage.py`. The actual
Lean report must contain the same ordered declarations and may depend only on
`Classical.choice`, `Quot.sound` and `propext`. These rows cover the finite
certificate, compact Stieltjes-domination, atomic resolvent-bridge and
compactified finite-measure layers; they do not state the analytic RH criterion.

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
| `OnePointResolvent.stieltjes_atom_norm_le_of_denominator` | verified | any denominator comparison controls one positive atom |
| `OnePointResolvent.finitePositiveStieltjes_norm_le_of_denominator` | verified | denominator comparisons propagate through finite positive sums |
| `OnePointResolvent.finitePositiveStieltjes_family_norm_le_of_denominator` | verified | one denominator producer controls varying cutoff families |
| `OnePointResolvent.stieltjes_disk_denominator_bound` | verified | half-radius disk gives a universal factor-two denominator comparison |
| `OnePointResolvent.stieltjes_atom_norm_le_two` | verified | one positive atom is controlled by twice its center value |
| `OnePointResolvent.finitePositiveStieltjes_norm_le_two` | verified | finite positive sums inherit the factor-two disk bound |
| `OnePointResolvent.finitePositiveStieltjes_family_norm_le_two` | verified | one-point family bounds are uniform in cutoffs, weights and spectra |
| `OnePointResolvent.compactifiedPoint_pos` | verified | the resolvent compactification coordinate is strictly positive |
| `OnePointResolvent.stieltjesCompactifiedDenominator_ne_zero` | verified | the compactified denominator is nonzero on the slit plane |
| `OnePointResolvent.stieltjes_compactified_denominator_identity` | verified | exact algebraic compactification of the Stieltjes denominator |
| `OnePointResolvent.stieltjes_compactified_denominator_norm_identity` | verified | norm form of the compactified denominator identity |
| `OnePointResolvent.stieltjes_compactified_denominator_cross_identity` | verified | cross-multiplied compactification identity without division |
| `OnePointResolvent.stieltjes_denominator_bound_of_compactified` | verified | a compactified lower bound yields an unbounded-spectrum comparison |
| `OnePointResolvent.exists_stieltjesCompactifiedDenominator_lower_bound` | verified | compact slit-plane sets have a positive compactified denominator minimum |
| `OnePointResolvent.exists_stieltjes_denominator_bound_on_compact` | verified | every compact slit-plane set admits a spectrum-uniform comparison constant |
| `OnePointResolvent.exists_finitePositiveStieltjes_family_bound_on_compact` | verified | one-point family bounds propagate uniformly to arbitrary compact slit-plane sets |
| `OnePointResolvent.resolventTransform_finitePositiveStieltjesMeasure` | verified | finite positive sums equal Mathlib resolvent transforms at the sign-changed argument |
| `OnePointResolvent.compactifiedStieltjesWeight_nonneg` | verified | compactified atomic weights are nonnegative for positive input data |
| `OnePointResolvent.compactifiedStieltjesFiniteMeasure_mass_eq` | verified | compactified finite-measure mass is exactly the one-point Stieltjes value |
| `OnePointResolvent.compactifiedStieltjesFiniteMeasure_compl_Icc_eq_zero` | verified | every compactified measure is supported on `[0,1]` |
| `OnePointResolvent.compactifiedStieltjesFiniteMeasure_mem_family` | verified | one-point bounds place finite measures in a common mass/support family |
| `OnePointResolvent.isCompact_compactifiedStieltjesMeasureFamily` | verified | the common bounded-mass `[0,1]`-supported family is weakly compact |
| `OnePointResolvent.range_compactifiedStieltjesFiniteMeasure_subset_family` | verified | every uniformly one-point-bounded indexed family lies in the same compact measure set |
| `OnePointResolvent.isCompact_closure_range_compactifiedStieltjesFiniteMeasure` | verified | the weak closure of every such indexed family is compact |

The finite-measure compactness and relative-compactness inputs are now
kernel-checked. Exact integration against a limiting measure, compact-open
extraction, interval uniqueness,
holomorphic slit-plane extension of the target and equivalence with RH remain
documented analytic targets rather than kernel-checked declarations.

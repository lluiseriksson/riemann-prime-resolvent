# Programme consumption digest

This digest lists the construction-side declarations and contracts that a
consumer can name without importing any unproved analytic endpoint. It is a
routing document only: it does not instantiate the concrete operator model, the
slit-plane implication, the prime-tail estimate or the final convergence
argument.

## Stable construction-side surface

| Consumer need | Exact object | Owner |
|---|---|---|
| Typed publication gate | `RiemannPrimeResolvent.PublicationGate` | `RiemannPrimeResolvent/PublicationFrontier.lean` |
| Gate-to-target delivery lemma | `RiemannPrimeResolvent.publicationGate_delivers` | `RiemannPrimeResolvent/PublicationFrontier.lean`, checked by `oracle_check.lean` |
| Xi criterion interface target | `RiemannPrimeResolvent.XiStieltjesExtensionTarget` | `RiemannPrimeResolvent/XiInterface.lean` |
| Xi real-zero conclusion type | `RiemannPrimeResolvent.XiOnlyRealZeros` | `RiemannPrimeResolvent/XiInterface.lean` |
| Component error budgets | `RiemannPrimeResolvent.ErrorBudget` and `RiemannPrimeResolvent.VanishingBudget` | `RiemannPrimeResolvent/Convergence.lean` |
| Total budget convergence | `RiemannPrimeResolvent.VanishingBudget.total` | `RiemannPrimeResolvent/Convergence.lean` |
| Spectral-rate predicate | `RiemannPrimeResolvent.BeatsHalfThreshold` | `RiemannPrimeResolvent/RateOptimization.lean` |
| Machine-readable shared contract | `docs/contracts/resolvent-interface.json` | mirrored into `subprojects/riemann-one-point-resolvent/docs/contracts/resolvent-interface.json` |

## Interface contract routing

The shared JSON contract is a vocabulary and status-policy handoff, not a proof
object. Consumers can read these exact top-level fields when wiring another
artifact to this repository:

| Field | Current role | Safe consumer use |
|---|---|---|
| `contract_version` | interface version, currently `0.3.0` | pin a downstream parser or audit to this contract shape |
| `canonical_target` | names the documented `S_Xi` target formula and domain | quote the target convention before supplying a separate criterion proof |
| `construction_repository` | lists construction-side obligations owned by this repo | route spectral-model, positivity, trace/resolvent and prime-tail work to the root project |
| `criterion_repository` | lists criterion-layer input requirements and the subproject path | route slit-plane/Stieltjes consumption to `subprojects/riemann-one-point-resolvent` |
| `status_policy` | defines `verified`, `documented`, `open` and `numerical` meanings | reject downstream wording that upgrades documentation or regressions into theorem claims |

Release tooling requires the root contract and the criterion-subproject mirror to
be byte-identical. A consumer should therefore treat either copy as the same
contract, but should edit only the root copy and regenerate the mirror through
the release workflow when the interface actually changes.

## Criterion subproject surface

The imported criterion layer exposes these exact names for downstream routing.
They are finite/compactness APIs only; they do not assert the open analytic
endpoint.

| Consumer need | Exact object | Owner |
|---|---|---|
| Hausdorff complete-monotonicity predicate | `OnePointResolvent.IsHausdorffCompletelyMonotone` | `subprojects/riemann-one-point-resolvent/OnePointResolvent/Basic.lean` |
| Finite resolvent moment complete monotonicity | `OnePointResolvent.finiteResolventMoment_isHausdorffCompletelyMonotone` | `subprojects/riemann-one-point-resolvent/OnePointResolvent/ResolventCompactification.lean` |
| One-point disk bound for finite Stieltjes families | `OnePointResolvent.finitePositiveStieltjes_family_norm_le_two` | `subprojects/riemann-one-point-resolvent/OnePointResolvent/StieltjesLocalBound.lean` |
| Compact slit-plane Stieltjes family bound | `OnePointResolvent.exists_finitePositiveStieltjes_family_bound_on_compact` | `subprojects/riemann-one-point-resolvent/OnePointResolvent/StieltjesCompactBound.lean` |
| Mathlib resolvent-transform bridge | `OnePointResolvent.resolventTransform_finitePositiveStieltjesMeasure` | `subprojects/riemann-one-point-resolvent/OnePointResolvent/StieltjesResolventBridge.lean` |
| Compactified finite-measure mass identity | `OnePointResolvent.compactifiedStieltjesFiniteMeasure_mass_eq` | `subprojects/riemann-one-point-resolvent/OnePointResolvent/CompactifiedMeasure.lean` |
| Compactified transform recovery | `OnePointResolvent.compactifiedStieltjesFiniteMeasure_transform_eq` | `subprojects/riemann-one-point-resolvent/OnePointResolvent/CompactifiedKernelLimit.lean` |
| Pointwise weak-limit passage | `OnePointResolvent.tendsto_finitePositiveStieltjes_of_compactifiedMeasure_tendsto` | `subprojects/riemann-one-point-resolvent/OnePointResolvent/CompactifiedKernelLimit.lean` |

## Hypotheses still required

A downstream construction has to supply all of the following before the gate is
usable as a real programme endpoint:

1. a concrete source for `XiStieltjesExtensionTarget`, separate from the
   construction of any spectral model;
2. a model-derived `defect : Nat -> Real` and proof of
   `BeatsHalfThreshold defect`;
3. a model-derived `budget : Nat -> ErrorBudget` and proof of
   `VanishingBudget budget`;
4. an operator-side account of domains, self-adjointness, multiplicities,
   trace normalization and finite approximation;
5. a no-placeholder Lean audit through `scripts/verify_lean.sh` and
   `scripts/verify_static.sh`.
6. for criterion-layer consumption, compact-open uniformization, interval
   uniqueness, holomorphic target identification and the connection from the
   resulting criterion statement to the target function; these remain documented
   obligations rather than kernel-checked declarations.

## Safe consumption pattern

Consumers should import declarations from the Lean files above and cite
`docs/THEOREM-LEDGER.md` for the checked inventory. The safe integration point is
the `PublicationGate` record: future work should fill its fields with certified
construction data rather than restating the criterion or introducing standalone
frontier propositions.

## Handoff matrix

| Item | Consume now? | Required evidence before stronger use |
|---|---:|---|
| `PublicationGate.xiBridge` | yes, as a field to supply | an independent proof of `XiStieltjesExtensionTarget -> XiOnlyRealZeros` |
| `PublicationGate.defect` | yes, as a named input slot | a model-derived `defect : Nat -> Real`, not the witness sequence |
| `PublicationGate.spectralRate` | yes, as a rate obligation | a proof of `BeatsHalfThreshold defect` for the model-derived sequence |
| `PublicationGate.budget` | yes, as a named input slot | a model-derived `budget : Nat -> ErrorBudget` |
| `PublicationGate.budgetVanishes` | yes, as a convergence obligation | a proof of `VanishingBudget budget` tied to the same budget sequence |
| `publicationGate_delivers` | yes, as an eliminator | an explicit `XiStieltjesExtensionTarget` argument |

The current `beatsHalfThreshold_witness` is only an existence check for the
rate predicate. It is useful for API sanity, but it is not evidence that any
future operator model satisfies the rate requirement.

The unresolved work remains the four research-frontier items in
`docs/RESEARCH-FRONTIER.md`. Those items are not release blockers and are not
claims of completion.

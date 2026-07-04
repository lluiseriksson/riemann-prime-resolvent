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

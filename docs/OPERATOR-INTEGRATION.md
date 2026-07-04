# Operator integration obligations

A concrete construction must specify the Hilbert space, domains, self-adjointness, finite truncations, spectral pairing, multiplicities and trace normalization. It must then prove a one-point resolvent bound and convergence on a nonempty interval.

Finite residual or Rayleigh certificates are useful only with independently proved gap/separation and truncation bounds. Source model convergence cannot be transferred to the true lowest state by notation alone.

The final theorem should consume the shared interface rather than restating the companion criterion.

## Consumption map

| Operator-layer input | Existing owner | Consumption point |
|---|---|---|
| Slit-plane target implication | `XiStieltjesExtensionTarget → XiOnlyRealZeros` in `RiemannPrimeResolvent/XiInterface.lean` | `PublicationGate.xiBridge` in `RiemannPrimeResolvent/PublicationFrontier.lean` |
| Concrete scalar defect sequence | future model-derived `defect : ℕ → ℝ` | `PublicationGate.defect` and `PublicationGate.spectralRate` |
| Quantified rate above the half threshold | `BeatsHalfThreshold defect` | `PublicationGate.spectralRate`; the current `beatsHalfThreshold_witness` is only a satisfiability witness |
| Component error budgets | `budget : ℕ → ErrorBudget` with `VanishingBudget budget` | `PublicationGate.budget`, `PublicationGate.budgetVanishes` and `VanishingBudget.total` |
| Interface vocabulary | `docs/contracts/resolvent-interface.json` | shared construction/criterion contract mirrored into the criterion subproject |

This map is only a routing aid for future construction work. It does not
instantiate the concrete operator model, the slit-plane implication or the
prime-resolvent convergence endpoint.

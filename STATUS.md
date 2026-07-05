# Status

- **Verified in Lean:** finite/scalar bookkeeping listed in the theorem ledger.
- **Documented, not yet fully formalized:** the abstract slit-plane/Stieltjes implication, owned by the criterion subproject.
- **Open:** concrete prime-built one-point bounds and interval convergence, operator domains, trace-class control, alignment, multiplicity and normalization.
- **Numerical:** regression and convention checks only.

The strongest honest headline is: *a reproducible construction-side research programme with a kernel-checked finite substrate and explicit convergence frontier.*

## Closeout state

Engineering status: complete for `v0.3.0-docs-integrated`. Research status: RF-1 through
RF-4 remain open. Archive status: not recommended while those records need to
remain writable. See `MAINTENANCE.md`.

## Maintenance heartbeat 2026-07-05 18:18 UTC

Default branch `main` is at
`cfb50a9db40b20d70c4fae950017e3aba8c24c24`. The latest default-branch
`CI` run `28748985808` completed successfully on that commit, including both
`lean` and `static` jobs. The latest default-branch `Documentation` run
`28746945208` completed successfully on
`61de51df156f5020bc8494be57d2eedb8a1e88a2`. The latest default-branch
`Container` run `28745207243` completed successfully on
`6344b351bb04fed0f23ebe09698f545a5ea2aa2a`.

There is no open Codex-authored PR waiting for merge. The remaining open PRs
are older Dependabot maintenance branches: `#5`, `#6`, `#7`, `#8`, `#10`,
`#12`, `#14` and `#15`. Each is currently `UNSTABLE` because at least one
required check failed on the dependency branch, so they need separate failure
triage before they are consumable.

No open issue currently has the `agent-task`, `blocked` or `interface-change`
label. The next safe maintenance step is to triage one old red dependency PR
without mixing it with research-frontier edits.

## Programme consumption digest

Current reusable root Lean declarations for the construction side are:

- `RiemannPrimeResolvent.PublicationGate` in `RiemannPrimeResolvent/PublicationFrontier.lean`, a typed package of the future bridge, defect sequence, error budgets, spectral-rate witness and vanishing-budget witness.
- `RiemannPrimeResolvent.publicationGate_delivers`, checked by `oracle_check.lean`, which consumes an explicit `XiStieltjesExtensionTarget` through the gate's `xiBridge`.
- `RiemannPrimeResolvent.VanishingBudget.total` and `RiemannPrimeResolvent.ErrorBudget.tendsto_total_zero`, which turn componentwise budget convergence into total convergence.
- `RiemannPrimeResolvent.beatsHalfThreshold_witness`, which records a nonempty scalar rate predicate without instantiating the concrete operator model.

The exact remaining inputs before this can become a consumed programme gate are:

- a concrete `XiStieltjesExtensionTarget` source, owned by `RiemannPrimeResolvent/XiInterface.lean` and the criterion subproject documentation;
- a model-derived `defect : Nat -> Real` satisfying `BeatsHalfThreshold`;
- a model-derived `budget : Nat -> ErrorBudget` satisfying `VanishingBudget`;
- no new project axioms, placeholders or untracked theorem claims, as enforced by `scripts/verify_lean.sh` and `scripts/verify_static.sh`.

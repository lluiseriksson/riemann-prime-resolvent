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

## Maintenance heartbeat 2026-07-04 18:28 UTC

Default branch `main` is at
`369f34b1fdfbad7b8988e2610a4825ed1e96ebfe`. The latest default-branch
`CI` run `28712686131` and `Documentation` run `28712686130` both completed
successfully on that commit.

There is no open Codex-authored PR waiting for merge. The remaining open PRs
are Dependabot maintenance branches: `#13`, `#26` and `#27` are green but need
conflict resolution against `main`; older dependency PRs `#5`-`#12`, `#14`,
`#15` and `#17` still need separate failure triage before they are consumable.

No open issue currently has the `agent-task`, `blocked` or `interface-change`
label. The next safe maintenance step is to resolve one Dependabot branch at a
time, starting with a green-but-conflicted GitHub Actions PR, without mixing it
with research-frontier edits.

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

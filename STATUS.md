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

## Maintenance heartbeat 2026-07-06 12:20 UTC

Default branch `main` is at
`7693022a5b8791799ce0583c9696ab058de38ba2`. The latest default-branch `CI`
run `28780298611` completed successfully on that commit, including both `lean`
and `static` jobs. The latest default-branch `Documentation` run `28765846942`
completed successfully on `91a18d0ab936595e5450395570e2ca24c39ce9d8`. The
latest default-branch `Container` run `28765846917` completed successfully on
that same dependency-alignment commit.

There is no open Codex-authored PR waiting for merge. The currently green
Dependabot PRs are root dependency updates `#5`, `#7` and `#8`, plus
subproject dependency update `#14`; they are ready for human review/merge
subject to the usual dependency policy. The remaining red Dependabot PRs are
subproject dependency updates `#10` and `#12`.
Their observed blockers are exact dependency-resolution conflicts in the shared
CI/container install environment:

- `#10`: `mpmath==1.4.1` conflicts with `sympy==1.14.0`, which requires
  `mpmath<1.4`.
- `#12`: subproject `matplotlib==3.11.0` conflicts with root
  `matplotlib==3.10.8`; merging or otherwise incorporating the green root
  `matplotlib` update `#5` is the prerequisite before this branch is
  consumable.

No open issue currently has the `agent-task`, `blocked` or `interface-change`
label. The next safe maintenance step is to merge/review the green root
dependency PRs first, then rebase or rerun `#12`; `#10` should stay blocked
unless `sympy` also allows the newer `mpmath` range.

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

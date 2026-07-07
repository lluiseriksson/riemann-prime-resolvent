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

## Maintenance heartbeat 2026-07-07 01:17 UTC

Default branch `main` is at
`0530f920c5a77cc81332c203e6adb2a40d30bbb3`, which merged contract-consumption
routing PR `#49`. The latest default-branch `CI` run `28833592636` completed
successfully on that commit, including both `lean` and `static` jobs. The
latest default-branch `Documentation` run `28833592638` also completed
successfully on that commit. The latest default-branch `Container` run
`28765846917` remains green on `91a18d0ab936595e5450395570e2ca24c39ce9d8`; no
container inputs changed in the contract-routing merge.

The previous Codex-authored routing PR `#49` is merged and no Codex-authored PR
remains open. The current mother-facing consumption route is
`docs/PROGRAMME-CONSUMPTION-DIGEST.md`, which names the construction-side
`PublicationGate`, `publicationGate_delivers`, `XiStieltjesExtensionTarget`,
`ErrorBudget`, `VanishingBudget` and `BeatsHalfThreshold` surfaces, plus the
criterion-layer finite/compactness APIs imported from the subproject.

The currently green Dependabot PRs are root dependency updates `#5`, `#7` and
`#8`, plus subproject dependency update `#14`; they are ready for human
review/merge subject to the usual dependency policy. The remaining red
Dependabot PRs are subproject dependency updates `#10` and `#12`. Their observed
blockers are exact dependency-resolution conflicts in the shared CI/container
install environment:

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

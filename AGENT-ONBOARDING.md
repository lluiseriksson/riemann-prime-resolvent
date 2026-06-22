# Agent onboarding

You are working on a long-horizon formalized research programme.  Accuracy and
epistemic labels are more important than speed.

## One-command bootstrap

```bash
chmod +x scripts/*.sh
./scripts/bootstrap.sh
./scripts/verify.sh
```

The bootstrap script installs no system packages.  It expects `git`, `elan`,
`lake`, `lean`, Python 3, and network access.  On a clean Linux host, install
Elan first:

```bash
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf   | sh -s -- -y
source "$HOME/.elan/env"
```

## First-session checklist

1. Run `git status --short`; the tree must be clean.
2. Record `lean --version`, `lake --version`, and `git rev-parse HEAD`.
3. Run `lake update` only if `lake-manifest.json` is absent or intentionally
   being regenerated.  The Mathlib SHA is pinned in `lakefile.lean`.
4. Run `lake exe cache get`.
5. Run `lake build`.
6. Run `lake env lean oracle_check.lean`.
7. Run `python3 scripts/check_consistency.py`.
8. Commit `verification/latest.log` only at named checkpoints.

## Research discipline

Every mathematical item has one of four statuses:

- `LEAN-VERIFIED`: compiled theorem, no placeholders;
- `PAPER-PROVED`: conventional proof reviewed but not yet formalized;
- `CANDIDATE`: plausible derivation requiring source audit or checking;
- `OPEN`: missing mathematical result.

Never upgrade a status without evidence.  In particular, do not turn an open
operator convergence statement into an `axiom` merely to make downstream code
compile.  Instead define it as a `Prop`, a structure field, or an explicit
hypothesis of a conditional theorem.

## Preferred workflow

Work in small commits:

```text
feat(xi): define conventional xi and prove functional symmetry
feat(slit): prove -z^2 maps the upper half-plane to the slit plane
feat(zeros): prove the abstract slit-plane extension criterion
feat(stieltjes): formalize finite-measure compactness interface
feat(primes): prove the explicit von Mangoldt tail bound
```

Every commit should:

- build the touched target;
- update `docs/THEOREM-LEDGER.md`;
- add its `#print axioms` line to `oracle_check.lean`;
- append a short entry to `verification/LEDGER.md`.

## Do not start with the concrete operator

The concrete operator layer needs substantial unbounded-operator and trace-class
infrastructure.  First close the abstract analytic chain and the elementary
prime tail.  This produces useful Mathlib-scale contributions even if the
spectral alignment problem remains open.

## Source policy

Use primary sources for technical claims.  The initial source map is in
`docs/SOURCE-CLAIM-AUDIT.md`.  Record theorem/section/page numbers before using
a published estimate.  The candidate prolate-strip calculation in the research
note must be checked against the exact Fourier/Mellin conventions of the source
paper before being promoted.

## End-of-session handoff

Update:

- `RESEARCH-STATUS.md`;
- `docs/THEOREM-LEDGER.md`;
- `verification/LEDGER.md`;
- `HANDOFF-PROMPT.md` if the frontier changed.

Then run `./scripts/verify.sh` and leave the repository clean.

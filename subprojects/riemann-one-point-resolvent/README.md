# One-Point Resolvent–Hausdorff Programme

[![License: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-green.svg)](LICENSE)

> **Status:** abstract criterion programme and verified finite certificate layer. This repository does not prove the Riemann hypothesis.

This is the **criterion layer** of the broader Riemann prime–resolvent programme. It is maintained as a subproject inside [`lluiseriksson/riemann-prime-resolvent`](https://github.com/lluiseriksson/riemann-prime-resolvent), after preserving the former `riemann-one-point-resolvent` Git history in the monorepo. The canonical rendered criterion documentation is [`https://lluiseriksson.github.io/riemann-prime-resolvent/criterion/`](https://lluiseriksson.github.io/riemann-prime-resolvent/criterion/).

It studies the target

\[
\mathcal S_\Xi(x)=\frac{1}{2\sqrt{x}}
\frac{\xi'}{\xi}\!\left(\frac12+\sqrt{x}\right),
\qquad x>\frac14,
\]

and the one-point derivative sequence

\[
b_n(x_0)=x_0^n\frac{(-1)^n}{n!}\mathcal S_\Xi^{(n)}(x_0).
\]

The documentation gives a conventional argument that RH is equivalent to this sequence being a Hausdorff moment sequence on `[0,1]`, subject to the explicitly listed analytic background and convention bridge. The Lean source currently checks the finite atomic algebra, compactification and positive Gram/localizing certificates—not the complete RH equivalence.

## Documentation is the manuscript

There is no standalone `paper/` directory and no committed manuscript PDF. The full exposition is under [`docs/manuscript/`](docs/manuscript/index.md), versioned with the Lean source and published by the canonical monorepo Pages workflow.

## Relationship to the prime repository

The repository root owns the construction problem: produce concrete positive spectral observables satisfying this subproject's abstract one-point bound and interval-convergence interface. See [`docs/PROGRAMME_RELATION.md`](docs/PROGRAMME_RELATION.md).

## Quick start

```bash
lake exe cache get
./scripts/verify_lean.sh
python3 -m pip install -r requirements.txt -r requirements-docs.txt
./scripts/verify_static.sh
make audit
```

The audit is read-only and checks release metadata, workflow policy, portable source inventory and deterministic packaging. Run `make manifest` only after deliberately reviewing changed source or generated files.

## Repository map

| Path | Purpose |
|---|---|
| `OnePointResolvent/` | canonical Lean namespace and finite verified core |
| `docs/manuscript/` | integrated mathematical exposition |
| `docs/contracts/` | shared machine-readable interface |
| `scripts/` | certificates, figures, static checks, metadata, manifests and release tooling |
| `tests/` | exact and regression checks |
| `.github/workflows/` | preserved Lean/static CI, documentation and source-release definitions |

Begin with [`docs/index.md`](docs/index.md) and [`docs/MATHEMATICAL_STATUS.md`](docs/MATHEMATICAL_STATUS.md).

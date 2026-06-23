# Riemann Prime–Resolvent Programme

[![Lean and static CI](https://github.com/lluiseriksson/riemann-prime-resolvent/actions/workflows/ci.yml/badge.svg)](https://github.com/lluiseriksson/riemann-prime-resolvent/actions/workflows/ci.yml)
[![Documentation](https://github.com/lluiseriksson/riemann-prime-resolvent/actions/workflows/docs.yml/badge.svg)](https://github.com/lluiseriksson/riemann-prime-resolvent/actions/workflows/docs.yml)
[![Container](https://github.com/lluiseriksson/riemann-prime-resolvent/actions/workflows/container.yml/badge.svg)](https://github.com/lluiseriksson/riemann-prime-resolvent/actions/workflows/container.yml)

> **Status:** research programme and verified finite bookkeeping. This repository does not prove the Riemann hypothesis.

This is the **single public repository** for the Riemann resolvent programme. The root project owns the construction and convergence layer: prime-built spectral side, explicit error budgets, finite resolvent models, rate bookkeeping and the non-circular convergence obligations needed by the abstract criterion.

The former companion repository now lives inside this monorepo at [`subprojects/riemann-one-point-resolvent`](subprojects/riemann-one-point-resolvent). That subproject owns the criterion layer: slit-plane continuation, one-point Hausdorff reconstruction and finite moment certificates. Its documentation is published beneath the canonical site at [`/criterion/`](https://lluiseriksson.github.io/riemann-prime-resolvent/criterion/).

## Canonical dependency

\[
\text{concrete prime-built }S_j
\xrightarrow{\text{one-point bound + interval convergence}}
\mathcal S_\Xi
\xrightarrow{\text{companion criterion}}
\mathrm{RH}.
\]

The difficult first arrow is open. It is split into separately reviewable spectral, model and prime-tail terms rather than hidden inside a global convergence assumption.

## Documentation is the manuscript

There is no separate `paper/` tree and no committed manuscript PDF. The full scholarly narrative lives under [`docs/programme/`](docs/programme/index.md) and is rendered as a versioned MkDocs site. Figures use web-native SVG/PNG sources.

## Verified Lean layer

The current modules prove elementary, unconditional results about:

- three-part error bookkeeping and componentwise convergence;
- finite Stieltjes and squared-resolvent positivity;
- paired-spectrum normalization;
- sign properties of the closed-form prime-tail majorant;
- finite Rayleigh/gap and residual/separation defects;
- the scalar candidate rate exponent.

Run:

```bash
lake exe cache get
./scripts/verify_lean.sh
```

The exact inventory is in [`docs/THEOREM-LEDGER.md`](docs/THEOREM-LEDGER.md).

## Static, metadata and release checks

Install both Python dependency roots, then run the integrated audit:

```bash
python3 -m pip install \
  -r requirements.txt \
  -r requirements-docs.txt \
  -r subprojects/riemann-one-point-resolvent/requirements.txt \
  -r subprojects/riemann-one-point-resolvent/requirements-docs.txt
./scripts/verify_static.sh
make audit
```

`make audit` is read-only. It checks metadata/version coherence, SHA-pinned workflows, portable manifest paths, mirrored contracts/tooling and the exact source inventory. Deliberately regenerate manifests only after reviewing all source and generated changes with `make manifest`.

## Reproducible container

```bash
docker build -t riemann-prime-resolvent .
docker run --rm -it riemann-prime-resolvent ./scripts/verify_static.sh
```

The image installs a versioned Elan release and both monorepo Python dependency sets. The dedicated Container workflow builds and smoke-tests it whenever its inputs change.

## Repository map

| Path | Purpose |
|---|---|
| `RiemannPrimeResolvent/` | Lean source for the verified construction-side substrate |
| `docs/` | integrated manuscript, claim ledger, roadmap, source audit and interface contract |
| `figures/` | DOT/CSV sources plus generated SVG/PNG graphics |
| `experiments/` | exact certificate schema and examples |
| `scripts/` | deterministic verification, metadata, manifest and release tooling |
| `subprojects/riemann-one-point-resolvent/` | imported criterion layer, including its preserved Git history |
| `.github/workflows/` | Lean/static CI, composite Pages documentation, container validation and source releases |

Start with [`docs/index.md`](docs/index.md) and [`docs/PROGRAMME_RELATION.md`](docs/PROGRAMME_RELATION.md).

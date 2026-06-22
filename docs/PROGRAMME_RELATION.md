# Relationship to `riemann-one-point-resolvent`

The two repositories are layers of one programme.

## This repository owns

- concrete prime-built spectral models;
- Galerkin and alignment errors;
- trace/resolvent estimates;
- the arithmetic cutoff and normalization audit;
- rate optimization and exact finite certificates;
- the proof that a concrete family satisfies the shared interface.

## The companion repository owns

- the target \(\mathcal S_\Xi\) as an abstract criterion;
- slit-plane continuation and the logarithmic-derivative pole argument;
- the one-point Hausdorff moment formulation;
- finite moment and positive-semidefinite certificate algebra;
- the abstract normal-family implication.

## Shared contract

The machine-readable contract is [`contracts/resolvent-interface.json`](contracts/resolvent-interface.json). A release check compares its digest with the expected cross-repository digest supplied by the delivery package.

No theorem should be copied between repositories merely to make either repository appear self-contained. Documentation may summarize the other layer, but canonical definitions have one owner.

# Monorepo programme relation

The programme used to be split across `riemann-prime-resolvent` and
`riemann-one-point-resolvent`. It now lives in this single repository. The
construction layer remains at the repository root; the criterion layer is
preserved under `subprojects/riemann-one-point-resolvent/`.

## This repository owns

- concrete prime-built spectral models;
- Galerkin and alignment errors;
- trace/resolvent estimates;
- the arithmetic cutoff and normalization audit;
- rate optimization and exact finite certificates;
- the proof that a concrete family satisfies the shared interface.

## The criterion subproject owns

- the target \(\mathcal S_\Xi\) as an abstract criterion;
- slit-plane continuation and the logarithmic-derivative pole argument;
- the one-point Hausdorff moment formulation;
- finite moment and positive-semidefinite certificate algebra;
- the abstract normal-family implication.

## Shared contract

The machine-readable contract is [`contracts/resolvent-interface.json`](contracts/resolvent-interface.json). The same contract is mirrored in the criterion subproject so both layers keep one vocabulary inside the monorepo.

No theorem should be duplicated merely to make either layer appear complete. Documentation may summarize the other layer, but canonical definitions have one owner.

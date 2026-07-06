# Relationship to the monorepo root

## This repository is the criterion layer

The criterion layer now lives at
`subprojects/riemann-one-point-resolvent` inside the public monorepo. It owns
the abstract route

\[
\text{positive Stieltjes extension agreeing with }\mathcal S_\Xi
\Longrightarrow
\text{all zeros of }\Xi\text{ are real}
\Longrightarrow \mathrm{RH},
\]

and the equivalent one-point Hausdorff formulation.

## The monorepo root is the construction layer

The root project must construct a concrete family of self-adjoint prime-built
observables and prove:

- positivity/Stieltjes structure;
- a uniform bound at one positive point;
- convergence to \(\mathcal S_\Xi\) on a nonempty interval;
- domains, traces, multiplicities and normalizations;
- non-circularity.

## Shared contract

The byte-identical shared contract is kept at the monorepo-root path
`docs/contracts/resolvent-interface.json` and mirrored here as
[`contracts/resolvent-interface.json`](contracts/resolvent-interface.json).
A shared definition is changed only by synchronized edits to both copies.

Criterion work and construction work remain different review surfaces inside
the monorepo. Documentation may summarize the other layer, but canonical
definitions have one owner.

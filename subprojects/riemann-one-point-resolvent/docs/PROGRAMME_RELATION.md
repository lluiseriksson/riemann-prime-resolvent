# Relationship to `riemann-prime-resolvent`

## This repository is the criterion layer

It owns the abstract route

\[
\text{positive Stieltjes extension agreeing with }\mathcal S_\Xi
\Longrightarrow
\text{all zeros of }\Xi\text{ are real}
\Longrightarrow \mathrm{RH},
\]

and the equivalent one-point Hausdorff formulation.

## The companion is the construction layer

`riemann-prime-resolvent` must construct a concrete family of self-adjoint prime-built observables and prove:

- positivity/Stieltjes structure;
- a uniform bound at one positive point;
- convergence to \(\mathcal S_\Xi\) on a nonempty interval;
- domains, traces, multiplicities and normalizations;
- non-circularity.

## Shared contract

Both repositories contain the byte-identical file [`contracts/resolvent-interface.json`](contracts/resolvent-interface.json). A shared definition is changed only by synchronized pull requests.

The repositories should remain separate on GitHub: criterion work and construction work have different review surfaces and progress independently.

# Numerical certification plan

The numerical layer must produce certificates, not trusted conclusions.

## Finite matrix certificate

For each `(lambda,N)` export:

- exact rational or interval enclosure of every matrix entry;
- proof/certificate of Hermitian symmetry;
- normalized trial vector enclosure;
- Rayleigh quotient enclosure;
- residual norm upper bound;
- lower bound on separation from the next spectral cluster;
- Galerkin-tail upper bound;
- interval enclosures for the squared-resolvent trace on a grid.

## Uniform interval control

For a finite Hermitian matrix `D`,

\[
S_D(x)=\tfrac12\operatorname{Tr}(D^2+xI)^{-1}.
\]

Use interval linear algebra to enclose `S_D(x_j)` on a grid.  A derivative or
resolvent-identity bound then controls the gaps between grid points.  Every
constant and grid endpoint must be exported in a machine-readable JSON file.

## Certificate schema

See `experiments/schema/certificate.schema.json`.  The first checker may be
Python-based, but the final publication path should translate the certificate
to rational inequalities verified by Lean.

## Prohibited shortcuts

- accepting NumPy eigenvalues as exact;
- inferring a global gap from plotted eigenvalues;
- verifying only the first few spectral points;
- using an RH-based zero list as an input to the proof layer;
- omitting high-energy tail control.

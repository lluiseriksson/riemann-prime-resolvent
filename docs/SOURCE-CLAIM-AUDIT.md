# Source–claim audit

Only primary sources should support technical claims.

| Claim | Source | Status in this repo |
|---|---|---|
| Self-adjoint spectral approximants are built from rank-one perturbations on `[lambda^-1,lambda]` and involve primes `p <= lambda^2` | Connes–Consani–Moscovici, *Zeta Spectral Triples*, arXiv:2511.22755, abstract | SOURCE-VERIFIED |
| Numerical spectra approximate low Riemann zeros; rigorous convergence would establish RH | Same source, abstract | SOURCE-VERIFIED |
| Regularized determinants are proposed as normalized approximants to `Xi` | Same source, abstract | SOURCE-VERIFIED |
| Lower-bounded self-adjoint operator + simple isolated lowest eigenvalue + even eigenfunction gives Fourier transform with only real zeros | Connes–van Suijlekom, *Quadratic Forms, Real Zeros and Echoes of the Spectral Action*, arXiv:2511.23257, abstract | SOURCE-VERIFIED |
| Mathlib defines `RiemannHypothesis`, completed zeta, and functional equation | Mathlib pinned source `Mathlib/NumberTheory/LSeries/RiemannZeta.lean` | SOURCE-VERIFIED |
| Slit-plane extension criterion | Derivation in this repo | PAPER-PROVED; external review pending |
| One-point Stieltjes control yields a normal family | Classical analysis; exact citation still required | PAPER-PROVED; citation pending |
| Explicit von Mangoldt tail majorant | Elementary integral comparison | PAPER-PROVED; Lean pending |
| Candidate extension of a prolate/model estimate to a larger strip | Prior exploratory derivation | CANDIDATE; do not cite as theorem |
| Threshold `q>1/2` and optimized rate `rho(q)` apply to the concrete operator | Prior exploratory derivation | CANDIDATE; depends on unverified model estimate |
| Concrete lowest-state alignment rate | No source/proof | OPEN |

## Required audit before paper submission

1. Add exact theorem/section/page references from arXiv:2511.22755.
2. Check all Mellin/Fourier signs and support conventions.
3. Verify determinant normalizations and whether exponential factors survive the
   log-derivative/squared-resolvent symmetrization.
4. Obtain a specialist review of the slit-plane criterion.
5. Search the literature for equivalent Stieltjes/Pick/Nevanlinna criteria to
   assess novelty honestly.

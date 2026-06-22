# Lean 4 roadmap

## Phase 0 — seed verification (days)

- Make the supplied modules compile on the pinned toolchain.
- Preserve zero placeholders and project axioms.
- Record the first full build/oracle log.

## Phase 1 — Xi bridge (1–3 months)

Deliverables:

- conventional `xi` formula from `completedRiemannZeta₀`;
- functional equation and evenness of `Xi`;
- nonvanishing on the imaginary segment corresponding to `sigma>1`;
- equivalence between `XiOnlyRealZeros` and Mathlib `RiemannHypothesis`.

This phase should produce reusable Mathlib contributions.

## Phase 2 — slit-plane criterion (2–5 months)

Deliverables:

- upper-half-plane/square-map geometry;
- analytic order/local factorization API;
- log-derivative pole theorem;
- identity-theorem argument and exclusion of nonreal zeros.

The global connectedness step may require new topology/complex-analysis lemmas.

## Phase 3 — prime tail (1–3 months)

Deliverables:

- von Mangoldt definition/API;
- Euler-product logarithmic derivative on `Re(s)>1`;
- decreasing integral comparison;
- explicit uniform tail bound with all constants.

## Phase 4 — finite spectral certificates (2–6 months)

Deliverables:

- Hermitian finite model;
- Rayleigh/gap and residual/separation alignment;
- rational/interval certificate schema;
- executable checker independent of floating-point trust.

## Phase 5 — Stieltjes compactness (4–10 months)

Deliverables:

- positive finite measures and Stieltjes transforms;
- local boundedness on the slit plane;
- suitable normal-family/Montel theorem;
- interval-limit criterion.

## Phase 6 — concrete operator layer (2–4+ years)

Deliverables:

- semilocal quadratic form and domains;
- lower-bounded self-adjoint operator;
- compact resolvent;
- lowest-state simplicity/parity;
- trace-class squared resolvent;
- convergence estimates.

The mathematical discovery time for the final alignment/convergence theorem is
not predictable and may dominate the formalization.

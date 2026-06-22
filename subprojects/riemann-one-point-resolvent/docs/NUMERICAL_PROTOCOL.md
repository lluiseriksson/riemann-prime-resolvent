# Numerical protocol

## Purpose

The numerical script is an interface test for formulas, signs, normalizations, file formats, and plots. It is not a proof strategy by itself.

## Default calculation

- domain: `x in [1,25]`;
- target precision: 50 decimal digits in mpmath;
- prime-power cutoff: 20,000;
- critical-line zeros: first 40 returned by mpmath;
- output grid: 70 points.

## Interpretation

- The prime truncation approaches the target rapidly when `sigma = 1/2 + sqrt(x)` is well inside the Euler-product half-plane.
- The finite-zero curve lies below the target because the positive spectral tail is omitted.
- Floating-point agreement is not evidence that a concrete operator family converges.

## Certification rule

Any future numerical claim used in a theorem must export exact rational or interval certificates. Lean should check the certificate and a theorem must connect the finite object to the infinite operator. Screenshots and decimal tables are insufficient.

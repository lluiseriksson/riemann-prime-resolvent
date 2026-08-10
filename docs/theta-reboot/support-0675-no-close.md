# Registered non-closure at support 0.675

## Scope

This is a diagnostic of one rigorous lower-bound architecture.  It is not a
negative eigenvalue certificate for the Weil--Suzuki operator, is not evidence
against RH, and does not retract the certified frontier at \(a=0.65\).

## Registered attempt

The attempted certificate used

\[
 a=0.675,\quad d=16,\quad 16\le n<640,\quad
 640\le n<4096,
\]

smooth order 39, tail balance 1, residual balance 0.01, the directional
self-tail Gram, and 512-bit Arb arithmetic.  The smooth Taylor remainder was

\[
 2.199785681906283\cdot10^{-14}.
\]

The even Schur lower matrix returned the exact inertia outcome

```text
negative=3, positive=53, unresolved=0
```

before the odd sector was adjudicated.  Thus the pre-registered success
condition failed cleanly.  No tolerance was relaxed and no conclusion about
the true operator was drawn.

## Diagnosis and next gate

At \(a=0.65\), extracting the self tail removed the dominant isotropic loss.
At \(a=0.675\), three directions remain negative after the separate Grams for
endpoint flux, adjacent singularity and self regularization are combined by
Young inequalities.  The next accepted improvement must therefore do one of:

1. recombine more of those exact rows before taking outer products;
2. retain their cross Gram explicitly;
3. prove a smaller correction on the three-dimensional dangerous subspace.

Increasing the smooth order again cannot address this failure, and increasing
the local degree count without a directional mechanism has already failed at
\(a=0.625\) with much greater computational cost.

The smooth-image completeness bug found during this audit was repaired
separately: target degrees now extend through \(p+k+1\), and the full
\(a=0.65\) frontier certificate was rerun successfully after the correction.

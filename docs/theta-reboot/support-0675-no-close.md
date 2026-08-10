# Historical non-closure and its resolution at support 0.675

## Scope

This records the failure of one rigorous lower-bound architecture and the
later certificate that repaired it.  The failed run was not a negative
eigenvalue certificate for the Weil--Suzuki operator and was never evidence
against RH.

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

## Diagnosis

At \(a=0.65\), extracting the self tail removed the dominant isotropic loss.
At \(a=0.675\), three directions remained negative after the separate Grams for
endpoint flux, adjacent singularity and self regularization are combined by
Young inequalities.  A complete scalar-balance sweep showed that no choice of
the Young parameter could repair this common-denominator estimate.  The
accepted improvement therefore had to do one of:

1. recombine more of those exact rows before taking outer products;
2. retain their cross Gram explicitly;
3. prove a smaller correction on the three-dimensional dangerous subspace.

Increasing the smooth order again cannot address this failure, and increasing
the local degree count without a directional mechanism has already failed at
\(a=0.625\) with much greater computational cost.

The smooth-image completeness bug found during this audit was repaired
separately: target degrees now extend through \(p+k+1\), and the full
\(a=0.65\) frontier certificate was rerun successfully after the correction.

## Resolution

The obstruction was not the exact self tail.  It was the estimate that kept
the prime-two comparison but subtracted the entire prime-three norm.  The
seven cut intervals fiber pointwise into a four-vertex path, a two-vertex
edge and an isolated vertex.  Bounding boundary potential and both active
prime translations together gives the rigorous common complement floor

\[
 D\succeq0.6936865091909813I.
\]

With the registered tail balance `0.05`, the corrected smooth targets and the
directional self-tail Gram, the even and odd Schur matrices have inertia
`(negative=0, positive=56, unresolved=0)`.  Exact Arb interval arithmetic
then proves

\[
 \boxed{A_{0.675}\succeq
 1.5531308365921327\cdot10^{-13}I>0}.
\]

Domain monotonicity consequently gives \(\lambda_a>0\) for every
\(0<a\le0.675\).  The pointwise graph proof and complete numbers are recorded
in [the joint two-prime floor note](joint-two-prime-floor.md).  The next gate
is the new prime-power-four translation at \(a=\log2\), not another balance
adjustment inside the two-prime partition.

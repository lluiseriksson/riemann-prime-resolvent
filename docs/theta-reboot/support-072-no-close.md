# Registered non-closure at support 0.72

## Claim boundary

This note records the failure of one rigorous Schur architecture.  It is not a
negative-vector certificate for Suzuki's operator and is not evidence against
RH.  The unconditional full-operator frontier remains \(a=0.7\).

## Fixed run

The run used the same parameters as the support-0.7 certificate:

```text
a=0.72, local degrees=12, tail start=176, explicit end=8192,
smooth order=47, self remainder end=32768, precision=512 bits,
pointwise subdivisions=1024, tail balance=0.2, residual balance=0.0001.
```

The support-independent self-tail Gram was reused from its separately checked
cache.  All support-dependent components were regenerated in Arb.  The final
component cache has SHA-256

```text
c5cff9fba1684a5822e1544a2a96f91aa843d9b0074e239df6e81a51875ecad4
```

and reruns the adjudication in seconds.

## Mechanical verdict

With the common denominator for the whole near band \(12\le n<176\), the
even Schur matrix has

```text
negative=5, positive=72, unresolved=1.
```

A fixed grid

```text
tail balance     0.01, 0.03, 0.1, 0.2, 0.3, 1, 3
residual balance 1e-6, 1e-5, 1e-4, 1e-3, 1e-2
```

returned the same count in all 35 cases.  Scalar Young rebalancing therefore
does not repair this instance.

## Diagnosis

The exact finite source remains positive.  Its lowest midpoint eigenvalues
are approximately

\[
 7.63\cdot10^{-14}\quad\text{(even)},\qquad
 4.40\cdot10^{-11}\quad\text{(odd)}.
\]

The failure appears only after subtracting the near-band Gram against the
single global denominator

\[
 d_{12}=0.2209732158977950.
\]

The five lowest even midpoint eigenvalues then become approximately

\[
 -1.9590,\ -1.2692,\ -0.7803,\ -0.6803,\ -0.0800.
\]

The remote directional correction is much smaller and does not cause the
failure.  Thus this is a coarse inverse bound on a wide band, not a measured
negative direction of the operator.

## Multiscale repair target

For orthogonal degree bands \(P_j\) beginning at \(m_j\), the same form
inequality used at support 0.7 gives

\[
 D\succeq\sum_j d_{m_j}P_j,
 \qquad
 D^{-1}\preceq\sum_j d_{m_j}^{-1}P_j,
\]

with \(d_{m_j}=H_{m_j}+B\).  Consequently the rigorous replacement is

\[
 BD^{-1}B^*\preceq
 \sum_j d_{m_j}^{-1}(BP_j)(BP_j)^*.
\]

`arb_third_window_near_tail_gram.py` can now accumulate several registered
bands in one pass and a regression test proves that their sum encloses the
original aggregate Gram.  The proposed cuts are

\[
 12,16,24,48,96,176.
\]

The first production attempt was stopped as `INCONCLUSIVE-COST` before an
artifact was written; therefore no sign claim is made for the multiscale
matrix.  A source-row checkpoint or cached Legendre-Q map is required before
another production run.

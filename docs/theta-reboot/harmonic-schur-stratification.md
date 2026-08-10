# Uniform harmonic stratification of the Schur correction

## The support-independent statement

Let \(P_n\) be mutually orthogonal degree projections and suppose the high
block of a localized Weil operator obeys the form inequality

\[
 D\succeq\sum_{n\ge N}d_nP_n,
 \qquad d_n=H_n+c>0,
\]

where \(H_n=\sum_{k=1}^n1/k\). No invariance of \(P_n\) under \(D\) is
required. Inverse antitonicity gives

\[
 D^{-1}\preceq\sum_{n\ge N}d_n^{-1}P_n.
\]

For the source-to-complement map \(B\), put

\[
 G_n=(BP_n)(BP_n)^*\succeq0,
 \qquad
 R_*=\sum_{n\ge N}\frac{G_n}{d_n}.
\]

Then \(BD^{-1}B^*\preceq R_*\). This is the fully degree-resolved Schur
majorant.

## Near-optimal band theorem

Partition the degrees into consecutive bands \(I_j=[m_j,m_{j+1})\), and set

\[
 R_{\mathcal P}=\sum_j\frac{1}{d_{m_j}}
                  \sum_{n\in I_j}G_n.
\]

If, for some \(\varepsilon>0\),

\[
 d_n\le(1+\varepsilon)d_{m_j}
 \qquad(n\in I_j),
\]

then coefficientwise positivity proves the two-sided Loewner estimate

\[
 \boxed{R_*\preceq R_{\mathcal P}
              \preceq(1+\varepsilon)R_*}. \tag{HS}
\]

Indeed, monotonicity of \(d_n\) gives \(d_{m_j}^{-1}\ge d_n^{-1}\), while
the displayed ratio condition gives
\(d_{m_j}^{-1}\le(1+\varepsilon)d_n^{-1}\). Multiplication by each
\(G_n\succeq0\) and summation proves (HS).

This is stronger than merely saying that refinement helps: it supplies a
registered relative error for the entire matrix-valued Schur correction.

## Number of bands

Choose every next boundary greedily at the first degree where

\[
 d_n>(1+\varepsilon)d_{m_j}.
\]

The denominator at successive band starts grows geometrically. Therefore the
number of bands needed through degree \(M\) is at most

\[
 1+\left\lceil
 \frac{\log(d_{M-1}/d_N)}{\log(1+\varepsilon)}
 \right\rceil.
\]

Since \(d_M=H_M+c\sim\log M\), this is

\[
 O_\varepsilon(\log\log M).
\]

Thus degreewise sharpness does not require one stored Gram per degree. A
doubly logarithmic number of bands controls the relative overcharge uniformly
as the explicit tail cutoff grows.

For the support-0.72 denominator \(d_{12}=0.220973215897795\), an overhead
target of 25% through degree 8191 produces 14 bands:

```text
12, 13, 15, 17, 20, 25, 32, 44, 65, 105, 190, 398, 1001, 3166, 8192
```

The executable constructor and its regression test are
`harmonic_schur_stratification.py` and
`test_harmonic_schur_stratification.py`.

## What this does and does not solve

The theorem is independent of the support partition and survives the entry
of new prime powers. It gives a uniform, near-optimal way to estimate the
high-complement inverse and explains why the two-band repair at support 0.72
worked.

It does **not** prove the remaining finite Schur matrix positive for every
support. That source-side sign still contains the prime--archimedean
cancellation equivalent to the global Weil criterion. Consequently (HS) is a
genuine scalable component of a possible RH proof, not RH itself.

# The thirteen-block prime-power-four window

## Exact window and graph

For

\[
 \log2<a<\frac12\log\frac92,
\]

the endpoint orbit under the active displacements

\[
 h_2=\frac{\log2}{a},\qquad
 h_3=\frac{\log3}{a},\qquad
 h_4=\frac{\log4}{a}=2h_2
\]

closes into thirteen intervals.  At \(a=0.7\), the exact translation graph
has seven prime-two edges, three prime-three edges and one prime-power-four
edge.  The last edge has weight

\[
 -\frac{\Lambda(4)}{\sqrt4}=-\frac{\log2}{2},
\]

not \(-\log4/2\).  The code now validates prime powers and uses their von
Mangoldt weight in the global Legendre, jet and tail routines as well as in
the cut graph.

The thirteen vertices split into three pointwise components:

\[
 \{0,2,4,6,8,10,12\},\qquad
 \{1,5,7,11\},\qquad
 \{3,9\}.
\]

All intervals within one component have equal length, so the translations
are exact identity blocks in normalized local Legendre coordinates.

## Rigorous high-complement floor

Subdividing the common local coordinate into 1024 cells and applying Arb/Rump
eigenvalue isolation to the three graph fibers gives

| component size | graph lower |
|---:|---:|
| 7 | `-0.5192203929849014` |
| 4 | `-0.5655672739981310` |
| 2 | `-0.3495724171563144` |

After adding the scalar term, subtracting the order-47 smooth loss and adding
\(H_{16}\),

\[
 \boxed{D_{\ge16}\succeq0.6043415694704174I>0}.
\]

This was the first rigorous component of the programme beyond
\(a=\log2\).  The directional infinite-tail Schur correction described below
has now closed the full operator at \(a=0.7\).

## Exact finite source

`arb_third_window_source.py` now assembles the thirteen-block dominant
logarithmic form, scalar, order-controlled smooth kernel and exact
prime-power graph entry by entry in Arb.  Reflection pairs the blocks

\[
 (0,12),(1,11),(2,10),(3,9),(4,8),(5,7)
\]

and leaves block 6 as the centre; the two parity spectra reconstruct the full
finite spectrum in an independent regression test.  A degree-four,
order-23 diagnostic has smallest finite-source Ritz values approximately
`4.0063e-7` (even) and `1.3232e-5` (odd), with smooth remainder
`1.9916e-8`.  These are design data, not lower bounds for the infinite
operator.

## Global-basis diagnostic

As an independent check, the corrected global Legendre source with 32 modes,
the same complement denominator, prime powers `(2, 3, 4)` and smooth order 47
has positive finite Schur margins in both parity sectors (about
`3.4e-13` and `2.4e-10` after an entrywise Weyl budget).  Its old scalar
omitted-tail estimate is of order `1e-1`, so it cannot certify the operator.
The failed comparison identifies the next required mechanism: retain the
endpoint, adjacent-singular and self-tail directions in the thirteen-block
basis, as was necessary in the seven-block window.

Executable components are `third_prime_partition`,
`build_third_window_prime_matrix` and
`certify_third_window_pointwise_floor`; the finite source is
`build_arb_third_window_source`.

## Full directional Schur closure

The source uses 12 local Legendre modes in each of the thirteen intervals.
The complement is split orthogonally into the near band
\(12\le n<176\) and the remote tail \(n\ge176\).  If \(P\) and \(Q\)
denote those projections, the harmonic diagonal and the common pointwise
floor give the form inequality

\[
 D\succeq d_{\rm near}P+d_{\rm tail}Q,
 \qquad
 d_{\rm near}=0.3268232544521020,
 \quad d_{\rm tail}=2.974150455025881.
\]

The inverse is operator antitone on positive operators.  Therefore

\[
 D^{-1}\preceq d_{\rm near}^{-1}P+d_{\rm tail}^{-1}Q.
\]

This step is valid even though the complement mixes Legendre degrees.  It is
the reason the much smaller remote-tail coupling need not be charged against
the weakest near-band denominator.  Exact Arb Grams retain the endpoint flux,
adjacent singular and self-tail directions through degree 8191; the remaining
scalar losses are bounded by

\[
 \varepsilon_{\rm smooth}\le2.266540766067023\cdot10^{-16},
 \qquad
 \varepsilon_{\rm other}\le2.3664536098916882\cdot10^{-14}.
\]

At 512-bit precision the even and odd Schur matrices both have 78 certified
positive eigenvalues and no negative or unresolved eigenvalues.  Their lower
spectral endpoints are respectively

\[
 1.5700644483114687\cdot10^{-13},\qquad
 2.5162073334751495\cdot10^{-10}.
\]

The block reconstruction then proves

\[
 \boxed{A_{0.7}\succeq
 1.0783783252951832\cdot10^{-15}I>0}.
\]

The complete claim boundary and reproduction data are in
[the support-0.7 certificate](support-070-certificate.md).

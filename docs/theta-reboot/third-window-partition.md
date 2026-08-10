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

This is the first rigorous component of the programme beyond
\(a=\log2\).  It is not a proof that \(A_{0.7}>0\): the directional
infinite-tail Schur correction remains open.

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

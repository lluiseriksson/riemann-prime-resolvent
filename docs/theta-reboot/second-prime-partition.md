# The seven-block partition in the second prime window

## Window and cuts

For

\[
 \frac{\log3}{2}<a<\log2,
\]

the only active prime powers are $2$ and $3$. Put

\[
 h_2=\frac{\log2}{a},\qquad h_3=\frac{\log3}{a}.
\]

Both lie in $(1,2)$. Inserting only the four obvious cuts
$\pm(1-h_2),\pm(1-h_3)$ is insufficient: translating the $h_3$ cut by
$h_2$ creates the additional pair $\pm(1-h_3+h_2)$. The ordered closure is

\[
\begin{aligned}
-1<&\ 1-h_3< h_3-h_2-1<1-h_2\\
  <&\ h_2-1<1-h_3+h_2<h_3-1<1.
\end{aligned}
\]

All inequalities are strict throughout the displayed window. The seven
interval lengths are

\[
 (e,b,e,c,e,b,e),
\]

where

\[
 e=2-h_3,qquad b=2h_3-h_2-2,qquad c=2(h_2-1).
\]

This is the precise higher-dimensional version of the first-window
edge/centre/edge picture: a new prime adds cuts, and closure under the old
translation adds the extra pair needed for an invariant block geometry.

## Exact translation graph

Number the intervals from left to right by $0,\ldots,6$. Translation by
$h_2$ maps whole intervals

\[
 0\longrightarrow4,qquad1\longrightarrow5,qquad2\longrightarrow6,
\]

and translation by $h_3$ maps

\[
 0\longrightarrow6.
\]

Corresponding source and target intervals have equal length. Therefore, in
their normalized local Legendre bases, the finite-prime part is the weighted
adjacency operator with edges

\[
 -\frac{\log2}{\sqrt2}I
 \quad\text{and}\quad
 -\frac{\log3}{\sqrt3}I.
\]

No quadrature and no translation tail enter this block. The executable
geometry is `second_prime_partition`; `build_second_window_prime_matrix`
assembles the exact finite graph.

## Boundary and next obligation

At $a=\log3/2$ the prime-three edge has zero length and the first-window
architecture applies. At $a=\log2$ the central prime-two interval collapses
and the prime power $4$ enters, so a new closure is required.

The seven-block arithmetic term is now exact. The remaining work in this
window is analytic: construct the dominant logarithmic and smooth blocks on
the three length classes, derive their endpoint fluxes, and reproduce the
Schur--Kato source-and-tail certificate without replacing cross blocks by
absolute whole-operator norms.

# Retaining the self-regularized tail Gram

## The lost direction

In the second-window Schur certificate, the residual tail above degree 639
was formerly bounded by

\[
 \eta_{m other}<6.497746183024722\cdot10^{-6}.
\]

Inspection of the seven-by-seven comparison matrix shows that this number is
entirely the self-regularized block on each of the seven local intervals.  All
remaining adjacent-analytic and separated entries are below
`1.5e-323` in the registered geometry.  Replacing the self block by
\(\eta_{m other}^2I\) therefore discards essentially all useful direction.

## Exact coefficient and Gram

After both endpoint fluxes are removed, the coefficient from local Legendre
degree \(k\) to high degree \(n\) is

\[
 c_{nk}=
 \frac{\sqrt{(2n+1)(2k+1)}\,k(k+1)}
 {[n(n+1)-k(k+1)]\,n(n+1)}
\]

when \(n-k\) is even, and zero otherwise.  The new certificate accumulates

\[
 G_{\rm self}=\sum_{640\le n<4096}c_n^*c_n
\]

in Arb before squaring, separately in the even and odd seven-block bases.
The tail from 4096 onward is bounded by the existing exact numerator estimate
divided by \(4096\cdot4097\), giving norm

\[
 \eta_{\ge4096}<2.5702355963954028\cdot10^{-8}.
\]

After this scalar remainder is added to the diagonal of the Gram, its largest
map norm is below `2.8203617359694905e-6`; more importantly, the full matrix
retains how the small ground-state direction sees it.

## Two-stage Young majorant

Let \(U_0\) denote endpoint flux plus adjacent singular tail, \(T\) the self
tail and \(E\) the remaining residual.  The proof uses

\[
 (U_0+T)(U_0+T)^*
 \preceq(1+\delta)G_{U_0}+(1+\delta^{-1})G_{\rm self}
\]

and then

\[
 (U_0+T+E)(U_0+T+E)^*
 \preceq(1+\varepsilon)G_{U_0+T}
 +(1+\varepsilon^{-1})\|E\|^2I.
\]

The registered values are \(\delta=1\), \(\varepsilon=0.01\).  No tail term
is deleted; only the stage at which its direction is forgotten changes.

## Certified consequence

At \(a=0.65\), with smooth order 31 and all other main cutoffs unchanged, the
interval Schur inertias are

| sector | negative | positive | unresolved | Schur lower | coercive lower |
|---|---:|---:|---:|---:|---:|
| even | 0 | 56 | 0 | `3.4679675703228396e-11` | `4.3679506990184653e-13` |
| odd | 0 | 56 | 0 | `1.8058523028626904e-8` | `2.2654067763727258e-10` |

Thus

\[
 A_{0.65}\succeq4.3679506990184653\cdot10^{-13}I>0.
\]

Domain monotonicity then proves \(\lambda_a>0\) for every
\(0<a\le0.65\).  This remains a bounded-support theorem and does not prove
RH.  The executable components are `arb_second_window_self_gram.py` and
`support_065_certificate.py`.

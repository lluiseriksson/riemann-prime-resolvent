# Certified localized positivity at support one half

## Theorem

Let $A_a$ be Suzuki's Friedrichs operator for the localized Weil quadratic
form in the normalization fixed throughout this directory.  Then

\[
 A_{1/2}\succeq
 6.34161294362643\cdot10^{-7} I>0.
\]

The statement is unconditional.  It does not assume RH and does not infer
RH: it proves positivity at one support radius, whereas Weil positivity at
every compact support is equivalent to RH.

## Second spectral points

The basis is split at the exact translate by $2\log2$.  The prime-two block
is then exact and degree preserving.  Source-level Arb matrices use local
degree 16, an explicit dominant coupling through degree 127, and the common
complement floor

\[
 Q_{16}A_{1/2}Q_{16}\succeq1.4381589390415481 Q_{16}.
\]

Endpoint fluxes are summed explicitly through degree 4095 and bounded by a
telescopic PSD remainder.  The remaining Green tail obeys

\[
 \|Q_{128}D\mathcal LP_{16}\|<1000.706853,
 \qquad
 \left\|\frac{Q_{128}D\mathcal LP_{16}}{128\cdot129}\right\|
 <0.060604824.
\]

The conservative inequality

\[
 (L+R)(L+R)^*\preceq2LL^*+2RR^*
\]

keeps the flux--remainder cross term.  Interval eigendecomposition of the
resulting Schur lower matrices gives:

| parity | shift | negative | positive | unresolved | first positive lower |
|---|---:|---:|---:|---:|---:|
| even | 0.01 | 1 | 23 | 0 | 0.002846228699609642 |
| odd | 0.3 | 1 | 23 | 0 | 0.056246584614408346 |

The maximum entry radii are respectively $1.405\cdot10^{-15}$ and
$1.423\cdot10^{-15}$.  Hence the second spectral points are at least $0.01$
and $0.3$ in the even and odd sectors.

## Kato--Temple discharge

The independently constructed degree-256 trial vectors, with residual action
through degree 8191 and source-level Arb tails, give

| parity | Rayleigh upper | residual upper | second floor | Temple lower |
|---|---:|---:|---:|---:|
| even | $9.3341890542\cdot10^{-7}$ | $5.4701242847\cdot10^{-5}$ | 0.01 | $6.3416129436\cdot10^{-7}$ |
| odd | $1.9372906447\cdot10^{-4}$ | $8.2424307999\cdot10^{-4}$ | 0.3 | $1.9146300520\cdot10^{-4}$ |

The smaller even lower bound proves the displayed theorem.

## Reproduction and scope

`support_05_endpoint_certificate.py` is the interval second-eigenvalue
certificate; `arb_regularized_map_bound.py` proves its last analytic tail;
`support_05_certificate.py` composes those results with the Kato--Temple
certificates.  A full run takes about twenty minutes on the registered
Windows workstation, dominated by the 3072-bit degree-128 cross block.

The same architecture has now been extended to the strictly larger support
$a=0.51$; see `support-051-certificate.md`.  The remaining part of the first
prime window requires sharper spectral-gap control before the prime-three
translation enters at $a=\log3/2$.

# Certified localized positivity at support 0.51

## Theorem

Let $A_a$ be Suzuki's Friedrichs operator for the localized Weil quadratic
form, with the normalization used throughout this directory.  Then

\[
 A_{0.51}\succeq 2.3382546887665845\cdot10^{-7}I>0.
\]

This is unconditional.  It proves positivity at the single support radius
$a=0.51$; it neither proves positivity on an interval nor proves RH.

## Extension of the exact architecture

The three-interval prime-two partition is valid throughout

\[
 \frac{\log2}{2}<a\le\frac{\log3}{2}.
\]

The earlier restriction $a\le1/2$ in the smooth Taylor remainder was also
artificial.  Its Bernoulli majorant has ratio $2a/3$, so the same rational
Schur bound is valid for every $0<a<3/2$.  At $a=0.51$ the comparison data are

\[
 m_{\partial,2}>-0.180369861,\qquad
 Q_{16}A_{0.51}Q_{16}\succeq1.3973642675997522Q_{16}.
\]

The regularized degree-128 tail remains below $0.060604824$.

## Certified spectral gaps

The degree-16/128 common-floor Schur certificate, evaluated with Arb at 1024
bits, gives:

| parity | shift | negative | positive | unresolved | first positive lower |
|---|---:|---:|---:|---:|---:|
| even | 0.003 | 1 | 23 | 0 | 0.0031409736711534237 |
| odd | 0.1 | 1 | 23 | 0 | 0.19290435015651805 |

Thus the second spectral points are at least $0.003$ and $0.1$ in the even
and odd sectors.

## Kato--Temple discharge

| parity | Rayleigh upper | residual upper | second floor | Temple lower |
|---|---:|---:|---:|---:|
| even | $5.6278801913\cdot10^{-7}$ | $3.1411261015\cdot10^{-5}$ | 0.003 | $2.3382546888\cdot10^{-7}$ |
| odd | $1.0837789405\cdot10^{-4}$ | $6.0020332748\cdot10^{-4}$ | 0.1 | $1.0477153348\cdot10^{-4}$ |

The even certificate uses a degree-256 trial vector and explicit residual
through degree 16383.  The odd certificate needs only degree 8191.

## Boundary of the present method

At $a=0.54$ the finite lowest eigenvalue is still positive, about
$1.06\cdot10^{-7}$, but the common-floor Schur bound is too lossy: after a
shift of $0.0011$ it has two negative directions.  This is not evidence of a
negative eigenvalue.  It identifies the next proof obligation: a nested Schur
estimate which uses the substantially larger floor on $Q_{128}$ while keeping
the coupling between the degree bands.

The top-level reproducer is `support_051_certificate.py`.

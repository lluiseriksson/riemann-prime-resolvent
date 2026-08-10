# A certified support interval about 0.54

## Statement

Put

\[
 N=1\,037\,278\,868\,969\,346\,048.
\]

For every real $a$ satisfying

\[
 |a-0.54|\le 10^{-N},
\]

the localized Weil--Suzuki operator obeys

\[
 A_a\succeq1.4266759182629438\cdot10^{-9}I>0.
\]

This is an unconditional open-neighbourhood consequence of the point
certificate at $a_0=0.54$. The radius is deliberately written by its decimal
exponent because its floating-point value underflows. It is not an estimate of
the true positive interval and it does not prove RH.

## Relative-form estimate

Write

\[
 A_a=\mathcal L+B_a,
\]

where $\mathcal L=A_2-\frac12\log(1-x^2)$ is Suzuki's nonnegative
scale-free logarithmic form. Its regional part $A_2$ is Legendre diagonal;
$\mathcal L$ itself also contains the positive boundary potential. At the
certified centre,

\[
 A_{a_0}\succeq mI,qquad
 m=7.13337959131472\cdot10^{-9}.
\]

The scalar, prime-two and smooth terms give the elementary norm bound

\[
 \|B_{a_0}\|\le M=5.059189678269552,
 \qquad \mathcal L\le A_{a_0}+MI.
\]

For $h(a)=\log(2)/a$, let $\delta=|h(a)-h(a_0)|$ and
$L=\log(1+\delta^{-2})$. The Fourier multiplier inequality already checked in
`support_continuity_modulus.py` gives

\[
 |\Delta P[f]|
 \le4p\|f\|\sqrt{\frac{2\mathcal L[f]+C\|f\|^2}{L}},
\]

where

\[
 p=\frac{\log2}{\sqrt2},\qquad
 C=\frac4\pi-2\gamma+\log2.
\]

Young's inequality therefore yields, for every $\eta>0$,

\[
 |\Delta P[f]|
 \le\eta\mathcal L[f]
 +\left(\frac{8p^2}{\eta L}
 +\frac{4p\sqrt C}{\sqrt L}\right)\|f\|^2.
\tag{1}
\]

Choose

\[
 \eta=\frac{m}{5(m+M)}.
\]

The relative loss $\eta(m+M)$ then consumes at most $m/5$. Requiring

\[
 L\ge\max\left\{
 \frac{40p^2}{\eta m},
 \left(\frac{20p\sqrt C}{m}\right)^2
 \right\}
\]

allocates at most another $m/5$ to each of the two scalar terms in (1).
The Arb upper bound for the right-hand side is
$4.77684572193308\cdot10^{18}$.

## Ordinary parameter terms

On the registered neighbourhood $0.53\le a\le0.545$, the exact rational
Taylor coefficients and their Bernoulli/cosh tail majorants prove

\[
 \sup_{0\le t\le1.09}|r''(t)|
 <2.1111342064017986,
\]

\[
 \sup_{0\le t\le1.09}|r''(t)+tr'''(t)|
 <2.8200587436319813.
\]

Consequently the scalar and smooth changes are at most

\[
 \left(\frac1{0.53}+2\cdot2.8200587436319813\right)|a-a_0|.
\]

The registered radius is much smaller than the $1.8954\cdot10^{-10}$ needed
to charge this term another $m/5$. Thus four losses consume at most $4m/5$
and the remaining lower bound is $m/5$.

Finally,

\[
 |h(a)-h(a_0)|
 \le\frac{\log2}{0.53\cdot0.54}|a-a_0|.
\]

The displayed integer $N$ is the outward-rounded ceiling that simultaneously
enforces the translation resolution, the ordinary radius and containment in
the first-prime neighbourhood. The executable certificate is
`support_interval_certificate.py`.

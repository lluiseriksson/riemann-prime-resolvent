# An explicit unconditional small-support bound

## Statement

Let \(Q_W^a\) be the localized Weil quadratic form in the normalization of
Suzuki, and let \(0<a\le 1/16\). Then, unconditionally,

\[
\boxed{
  Q_W^a(v)\ge
  \bigl[-\log a-\log(2\pi)-\gamma-4a\bigr]\lVert v\rVert_2^2
}
\]

on the form domain. In particular,

\[
  Q_W^a(v)>0\qquad(0\ne v,\;0<a\le1/16),
\]

because the coefficient at the right endpoint is

\[
  \log16-\log(2\pi)-\gamma-\frac14
  =0.1074959909\ldots>0.
\]

This makes the phrase “positive for sufficiently small \(a\)” effective. It is
not a proof of RH and it does not yet reach the first prime threshold
\(a=\tfrac12\log2\).

## Derivation

For \(2a<\log2\), the prime sum in Suzuki's equation (205) is empty and

\[
Q_W^a(v)=\mathcal L_a(v)-(2A+1)\lVert v\rVert_2^2
-\iint r''(x-y)v(y)\overline{v(x)}\,dx\,dy,
\]

where

\[
  2A+1=\log(2\pi)+\gamma.
\]

The Beurling--Deny part immediately gives

\[
\begin{aligned}
\mathcal L_a(v)
&=\frac14\iint\frac{|v(x)-v(y)|^2}{|x-y|}\,dx\,dy
-\frac12\int\log(a^2-x^2)|v(x)|^2\,dx\\
&\ge -\log a\,\lVert v\rVert_2^2.
\end{aligned}
\]

For \(t>0\) below the first prime, differentiating the exact archimedean
formula and subtracting the second derivative of
\(\tfrac12t\log t+At\) gives

\[
r''(t)=
-e^{t/2}-e^{-t/2}
+\frac{e^{-t/2}}{1-e^{-2t}}
-\frac1{2t},
\qquad r''(0)=-\frac74.
\]

On \(0\le t\le1/8\), elementary exponential bounds give

\[
  -2\le r''(t)\le0.
\]

Write

\[
h(t)=\frac{e^{-t/2}}{1-e^{-2t}}-\frac1{2t}.
\]

For the lower estimate use

\[
\frac1{1-e^{-2t}}\ge\frac1{2t}+\frac12,
\qquad e^{-t/2}\ge1-\frac t2,
\]

to obtain \(h(t)\ge-1/4+(1-t/2)/2\ge7/32\). Moreover,
\(e^x\le(1-x)^{-1}\) for \(0\le x<1\), hence

\[
e^{t/2}+e^{-t/2}\le2e^{1/16}\le\frac{32}{15}.
\]

Thus \(r''(t)\ge7/32-32/15=-919/480>-2\). For the upper
estimate, \(1/(1-e^{-2t})\le1/(2t)+1\) gives \(h(t)\le1\), so
\(r''(t)\le-2\cosh(t/2)+1\le-1\). No floating-point statement enters
the proof.

For fixed \(x\in(-a,a)\), the \(y\)-interval has length \(2a\), and
\(|x-y|\le2a\le1/8\). Schur's test therefore yields

\[
  \left|\iint r''(x-y)v(y)\overline{v(x)}\,dx\,dy\right|
  \le4a\lVert v\rVert_2^2.
\]

Combining the three estimates proves the displayed bound first on
\(H_0^1(-a,a)\), hence on the closed form domain by density and lower
semicontinuity. The coefficient is decreasing in \(a\), so checking \(a=1/16\)
proves strict positivity throughout the registered interval.

## Why this matters and where it stops

This is a genuine infinite-dimensional lower bound derived from the
prime--archimedean formula, not a positive Galerkin eigenvalue. Its limitation
is equally exact: the estimate treats the smooth remainder by absolute value
and contains no mechanism for the cancellations that become decisive near the
first prime threshold. Crossing that threshold requires incorporating the
translation at \(\log2\) jointly with the archimedean operator; bounding it by
its norm loses the sign and cannot scale to RH.

# An explicit unconditional small-support bound

## Statement

Let \(Q_W^a\) be the localized Weil quadratic form in the normalization of
Suzuki, and let \(0<a\le 1/14\). Then, unconditionally,

\[
\boxed{
  Q_W^a(v)\ge
  \left[-\log a-\log(2\pi)-\gamma+
  \frac{5-\sqrt{19}}6-4a\right]\lVert v\rVert_2^2
}
\]

on the form domain. In particular,

\[
  Q_W^a(v)>0\qquad(0\ne v,\;0<a\le1/14),
\]

because the coefficient at the right endpoint is

\[
  \log14-\log(2\pi)-\gamma+\frac{5-\sqrt{19}}6-\frac27
  =0.0451004886\ldots>0.
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
&\ge \left(-\log a+\frac{5-\sqrt{19}}6\right)
\lVert v\rVert_2^2.
\end{aligned}
\]

Here is an elementary proof of the positive constant. On \((-1,1)\), write
\(w=me_0+q\), where \(e_0=1/\sqrt2\), \(q\perp e_0\), and
\(|m|^2+\lVert q\rVert^2=1\). The regional logarithmic Laplacian

\[
  A_2w(x)=\frac12\int_{-1}^1\frac{w(x)-w(y)}{|x-y|}\,dy
\]

diagonalizes in the Legendre basis with eigenvalues \(H_n\). Consequently its
quadratic form is at least \(\lVert q\rVert^2\). Also
\(-\tfrac12\log(1-x^2)\ge x^2/2\), and the reverse triangle inequality gives

\[
\mathcal L(w)\ge r^2+
\frac12\max\!\left(\frac{\sqrt{1-r^2}}{\sqrt3}-r,0\right)^2,
\qquad r=\lVert q\rVert.
\]

If the maximum vanishes, \(r^2\ge1/4\). Otherwise the smallest eigenvalue of

\[
\begin{pmatrix}
1/6&-1/(2\sqrt3)\\
-1/(2\sqrt3)&3/2
\end{pmatrix}
\]

is \((5-\sqrt{19})/6\). This proves the claimed lower bound for
\(\mathcal L\).

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

On \(0\le t\le1/7\), elementary exponential bounds give

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

to obtain \(h(t)\ge-1/4+(1-t/2)/2\ge3/14\). Moreover,
\(e^x\le(1-x)^{-1}\) for \(0\le x<1\), hence

\[
e^{t/2}+e^{-t/2}\le2e^{1/14}\le\frac{28}{13}.
\]

Thus \(r''(t)\ge3/14-28/13=-353/182>-2\). For the upper
estimate, \(1/(1-e^{-2t})\le1/(2t)+1\) gives \(h(t)\le1\), so
\(r''(t)\le-2\cosh(t/2)+1\le-1\). No floating-point statement enters
the proof.

For fixed \(x\in(-a,a)\), the \(y\)-interval has length \(2a\), and
\(|x-y|\le2a\le1/7\). Schur's test therefore yields

\[
  \left|\iint r''(x-y)v(y)\overline{v(x)}\,dx\,dy\right|
  \le4a\lVert v\rVert_2^2.
\]

Combining the three estimates proves the displayed bound first on
\(H_0^1(-a,a)\), hence on the closed form domain by density and lower
semicontinuity. The coefficient is decreasing in \(a\), so checking \(a=1/14\)
proves strict positivity throughout the registered interval.

The endpoint sign can be certified with rational bounds only:
\(\pi<22/7\), \(\gamma<289/500\),
\(\sqrt{19}<4359/1000\), and
\(e^{4/5}<2.226<49/22\). They imply

\[
\log(7/\pi)-\gamma+\frac{5-\sqrt{19}}6-\frac27
>\frac45-\frac{289}{500}+\frac{641}{6000}-\frac27
=\frac{1811}{42000}>0.
\]

## Why this matters and where it stops

This is a genuine infinite-dimensional lower bound derived from the
prime--archimedean formula, not a positive Galerkin eigenvalue. Its limitation
is equally exact: the estimate treats the smooth remainder by absolute value
and contains no mechanism for the cancellations that become decisive near the
first prime threshold. Crossing that threshold requires incorporating the
translation at \(\log2\) jointly with the archimedean operator; bounding it by
its norm loses the sign and cannot scale to RH.

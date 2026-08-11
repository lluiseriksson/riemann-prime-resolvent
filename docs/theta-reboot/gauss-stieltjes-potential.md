# Gauss--Stieltjes lower potentials

## Exact lower hierarchy

Put \(y=x^2\).  The boundary potential has the Stieltjes representation

\[
 V(x)=-\frac12\log(1-x^2)
 =\frac12\int_0^1\frac{y}{1-ty}\,dt.
\]

Let \((t_j,w_j)_{j=1}^m\) be the Gauss--Legendre rule on \([0,1]\), and set

\[
 R_m(x)=\frac12\sum_{j=1}^m w_j\frac{x^2}{1-t_jx^2}.
\]

For \(f_y(t)=y/(1-ty)\), every derivative of even order is nonnegative:

\[
 f_y^{(2m)}(t)=\frac{(2m)!y^{2m+1}}{(1-ty)^{2m+1}}\ge0.
\]

The signed Gauss remainder therefore proves

\[
 0\le R_m(x)\le V(x)\qquad(|x|<1).
\]

If \(p_m(t)=P_m(2t-1)\), Gaussian exactness applied to
\((1-p_m(t))/(1-t)\) gives

\[
 \sum_j\frac{w_j}{1-t_j}
 =\int_{-1}^1\frac{1-P_m(s)}{1-s}\,ds=2H_m,
\]

and hence \(R_m(1)=H_m\).  This is a lower comparison for the
archimedean potential and contains no prime or zeta zero.

## Certified banded truncation

For \(0<t<1\), define

\[
 q(t)=\frac{1-\sqrt{1-t}}{1+\sqrt{1-t}}.
\]

The Poisson-kernel expansion gives

\[
 \frac{x^2}{1-tx^2}
 =\frac1t\left[
 \frac1{\sqrt{1-t}}
 \left(1+2\sum_{k\ge1}q(t)^kT_{2k}(x)\right)-1\right].
\]

Writing \(R_{m,J}\) for the partial sum through \(T_{2J}\), one has

\[
 \|R_m-R_{m,J}\|_\infty\le
 \varepsilon_{m,J}:=
 \sum_{j=1}^m
 \frac{w_j}{t_j\sqrt{1-t_j}}
 \frac{q(t_j)^{J+1}}{1-q(t_j)}.
\]

Consequently

\[
 \underline R_{m,J}:=R_{m,J}-\varepsilon_{m,J}\le V,
 \qquad \underline R_{m,J}\ge-2\varepsilon_{m,J}.
\]

Multiplication by \(T_{2J}\) has Legendre bandwidth \(2J\).  Thus the
comparison operator obtained by replacing \(V\) with
\(\underline R_{m,J}\) has no logarithmic potential tail.

For \((m,J)=(8,256)\), the descriptive value is

\[
 \varepsilon_{8,256}=3.2071\cdot10^{-32}.
\]

## Exact prime-translation floor

For displacement \(h_n=\log n/a\), residue fibers are path graphs of
essential maximum length

\[
 q_n=\left\lceil\frac{2a}{\log n}\right\rceil.
\]

The path spectrum therefore proves

\[
 T_{n,a}\succeq-
 \frac{2\Lambda(n)}{\sqrt n}
 \cos\frac{\pi}{q_n+1}\,I.
\]

At \(a=1\), the active prime powers \(2,3,4,5,7\) give total loss
\(3.1292522911\).  With the registered smooth loss and \(N=256\),

\[
 H_{256}-\log(2\pi)-\gamma-C_{\rm smooth}(1)
 -3.1292522911-2\varepsilon_{8,256}>0.1385.
\]

This proves positivity of the high Legendre complement for the lower
comparison.  It does not prove positivity of the remaining finite Schur
matrix and therefore does not prove RH.

## Exact Markov remainder: no positivity need be discarded

The Gauss comparison has a stronger exact form.  Let

\[
 p_m(t)=P_m(2t-1),\qquad
 F(z)=\int_0^1\frac{dt}{z-t},
\]

and let \(Q_mF(z)=\sum_jw_j/(z-t_j)\) be its \(m\)-node Gaussian
approximant.  The polynomial

\[
 \frac{p_m(z)^2-p_m(t)^2}{z-t}
\]

has degree \(2m-1\) in \(t\).  Gaussian exactness and
\(p_m(t_j)=0\) therefore give

\[
 p_m(z)^2\bigl(F(z)-Q_mF(z)\bigr)
 =\int_0^1\frac{p_m(t)^2}{z-t}\,dt.                 \tag{GS1}
\]

Putting \(z=x^{-2}\) proves the exact positive remainder formula

\[
 \boxed{
 V(x)-R_m(x)=
 \frac1{2p_m(x^{-2})^2}
 \int_0^1\frac{p_m(t)^2}{x^{-2}-t}\,dt>0
 }
 \qquad(0<|x|<1).                                   \tag{GS2}
\]

If \(q_m(y)=y^mp_m(1/y)\), this becomes the continuous square

\[
 \boxed{
 V(x)-R_m(x)=\frac12\int_0^1
 \left(
  \frac{x^{2m+1}p_m(t)}
       {q_m(x^2)\sqrt{1-tx^2}}
 \right)^2dt.}                                      \tag{GS3}
\]

The finite Gaussian part is itself a sum of squares,

\[
 R_m(x)=\frac12\sum_{j=1}^mw_j
 \left(\frac{x}{\sqrt{1-t_jx^2}}\right)^2.          \tag{GS4}
\]

Thus (GS3)--(GS4) give an exact finite-plus-continuous Gram realization of
the whole boundary potential.  This is stronger than the lower comparison:
the endpoint coercivity in \(V-R_m\) can be retained instead of thrown away.

The order at the origin is also exact.  Expanding in \(y=x^2\), Gaussian
exactness matches the moments \(\int_0^1t^kdt\) for
\(0\le k\le2m-1\), so

\[
 V(x)-R_m(x)=O(x^{4m+2}).                            \tag{GS5}
\]

At the other endpoint, \(R_m(1)=H_m\) stays finite while the remainder in
(GS2) carries the logarithmic divergence.  This explains why a modest
Gaussian order is almost exact on low polynomial modes although convergence
is not uniform up to \(|x|=1\).

## Root plus added node: an exact nested resolvent

Let \(J_m\) be the \(m\)-by-\(m\) Jacobi matrix of multiplication by \(t\)
in the orthonormal shifted-Legendre basis.  Its diagonal entries are \(1/2\)
and its links are

\[
 a_k=\frac{k}{2\sqrt{(2k-1)(2k+1)}}\qquad(1\le k<m).
\]

The spectral theorem for Gaussian quadrature gives

\[
 \boxed{
 R_m(x)=\frac{x^2}{2}\,
 e_0^T(I-x^2J_m)^{-1}e_0.}                           \tag{GS6}
\]

Moreover, \(J_m\) is the leading principal block of \(J_{m+1}\).  Put

\[
 A_m=I-x^2J_m,qquad
 s_m=1-\frac{x^2}{2}
 -x^4a_m^2e_{m-1}^TA_m^{-1}e_{m-1}.
\]

Because the spectrum of every \(J_m\) lies in \((0,1)\), both \(A_m\) and
its Schur complement \(s_m\) are positive for \(|x|<1\).  Block inversion
then gives the exact increment

\[
 \boxed{
 R_{m+1}(x)-R_m(x)=
 \frac{x^6a_m^2}{2s_m}
 \left(e_{m-1}^TA_m^{-1}e_0\right)^2>0.}             \tag{GS7}
\]

Thus

\[
 0<R_1(x)<R_2(x)<\cdots<V(x)
\]

and every added Jacobi dimension is literally a positive square.  Formula
(GS7) is the rigorous ``root plus added node'' reading: the black root is the
current finite resolvent and the added red node enters through one Schur
square.  The factor \(e_{m-1}^TA_m^{-1}e_0=O(x^{2m-2})\) also recovers the
order \(x^{4m+2}\) in (GS5).

This hierarchy suggests a finite target at support \(a=1\).  If one proves
that the localized operator with \(V\) replaced by some \(R_m\) is positive,
then the exact operator is positive by (GS2), with no RH assumption.  The
double-precision audit below makes \(m=12\) the first candidate requiring an
interval source-and-tail calculation.  Failure for one \(m\) would not close
the hierarchy because (GS7) raises the operator monotonically.

## The single-floor Schur shortcut fails

The multiplication compression was implemented in two independent ways:
an enlarged Legendre Jacobi recurrence and a polynomial-exact Gauss rule.
For size 32, \((m,J)=(8,64)\), their largest entry discrepancy is
\(1.55\cdot10^{-13}\) in double precision.  The degree-exact Gauss route
makes much larger polynomial degrees cheap.

A descriptive size-64 audit, using smooth order 95 with analytic omitted
norm below \(4.99\cdot10^{-17}\), gives

\[
\begin{array}{c|c|c|c}
m&J&\varepsilon_{m,J}&
 (\lambda_{\min}^{\rm even},\lambda_{\min}^{\rm odd})\\ \hline
8&128&1.89\cdot10^{-16}&(-9.08\cdot10^{-8},-9.03\cdot10^{-9})\\
12&384&8.76\cdot10^{-33}&(-6.63\cdot10^{-16},-5.80\cdot10^{-15})\\
16&512&4.42\cdot10^{-33}&(-2.04\cdot10^{-15},-7.79\cdot10^{-15})
\end{array}
\]

The last two rows are at the double-precision sign floor and are not sign
certificates.  They do show that the rational deficit, not the Chebyshev
truncation, has already disappeared at this resolution.

More importantly, using the proved common complement floor \(\beta=0.1385\)
as a *single* Schur denominator is structurally too crude.  For the first 16
global Legendre modes, charging only the explicitly computed columns
16--127 at \(\beta^{-1}\) produces smallest Schur eigenvalues approximately

\[
 -11.78\quad\text{(even)},\qquad -15.15\quad\text{(odd)}. \tag{GS8}
\]

These are diagnostics, not interval claims, but their scale identifies the
correct architecture: the high-complement theorem is useful only after an
explicit multiband elimination.  Replacing the exact potential globally by
a strict lower polynomial, or charging every high mode at one denominator,
cannot be the final step.

The next non-circular target is therefore to keep (GS3) as an auxiliary Gram
block and combine it with the signed prime translations inside the same
multiband Schur calculation.  A threshold-uniform factorization of that
combined block would be a genuine route beyond the isolated certificates at
support 0.70 and 0.72.  Merely asserting its positivity would again rename
the localized Weil criterion and hence RH.

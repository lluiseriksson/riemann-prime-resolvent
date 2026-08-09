# Legendre tail coercivity and a finite reduction

## Exact diagonal part

On the fixed interval \((-1,1)\), Suzuki's form contains

\[
\mathcal L(w)=
\frac14\iint\frac{|w(x)-w(y)|^2}{|x-y|}\,dx\,dy
-\frac12\int\log(1-x^2)|w(x)|^2\,dx.
\]

The first term is the quadratic form of

\[
 A_2w(x)=\frac12\int_{-1}^1\frac{w(x)-w(y)}{|x-y|}\,dy.
\]

This operator has the exact Legendre spectrum

\[
  A_2P_n=H_nP_n,\qquad
  H_n=\sum_{k=1}^n\frac1k.
\]

The identity is recorded in Rosenzweig--Stanfill,
[*On the fundamental solutions of two nonlocal parabolic equations related to
logarithmic Laplacians*](https://arxiv.org/abs/2606.04225), equation (1.10).
Since the remaining multiplication potential is nonnegative, the min--max
principle gives

\[
  \mu_n(\mathcal L)\ge H_n.
\]

This is the quantitative version of the \(H^{\log}\) compactness used in
Suzuki's continuity proof.

## Bounded arithmetic perturbation

Write the scaled localized operator as

\[
  A_a=\mathcal L+K_a.
\]

For \(0<a\le1/2\), elementary operator bounds give

\[
\lVert K_a\rVert\le
\left|-\log a-\log(2\pi)-\gamma\right|
+2\sum_{\log n<2a}\frac{\Lambda(n)}{\sqrt n}
+6a.
\tag{T}
\]

The three terms are respectively the scalar shift, the norm-two bound for
each truncated translation plus its adjoint, and Schur's test applied to the
smooth remainder. The last estimate uses \(|r''(t)|\le3\) for
\(|t|\le1\). Indeed, the estimates in the small-support note give
\(h(t)\ge1/4-t/4\ge0\), while
\(e^{t/2}+e^{-t/2}\le e^{1/2}+1<8/3\); the opposite sign follows from
\(h(t)\le1\).

Let \(P_N\) be the spectral projection of \(\mathcal L\) onto its first
\(N\) eigenfunctions. On the complementary space,

\[
  (1-P_N)A_a(1-P_N)
  \ge\bigl(H_N-\lVert K_a\rVert\bigr)(1-P_N).
\]

Thus every possible nonpositive direction lies in a finite block plus its
bounded coupling to a strictly positive tail as soon as
\(H_N>\lVert K_a\rVert\).

## Registered dimensions

The deliberately crude but rigorous rule (T) gives:

| \(a\) | active prime powers | \(\lVert K_a\rVert\) bound | first \(N\) | tail margin |
|---:|:---|---:|---:|---:|
| 0.3000 | none | 3.01112 | 11 | 0.00876 |
| 0.3465 | none | 3.43422 | 17 | 0.00533 |
| 0.4000 | \(2\) | 4.87906 | 74 | 0.00896 |
| 0.4500 | \(2\) | 5.29684 | 112 | 0.00333 |
| 0.5000 | \(2\) | 5.70220 | 168 | 0.00195 |

This does **not** certify the low block. A valid lower-eigenvalue proof must
also enclose the finite block and its off-diagonal coupling, for example by an
interval Schur complement in an independently certified approximation to the
\(\mathcal L\)-eigenbasis. A positive Ritz value alone is an upper bound and
cannot fill this role.

## Scaling warning

For large \(a\),

\[
  \sum_{\log n<2a}\frac{\Lambda(n)}{\sqrt n}\sim2e^a.
\]

Since \(H_N\sim\log N+\gamma\), the crude dimension required by (T) grows like
\(\exp(Ce^a)\). The reduction is finite for every fixed support, but not
uniformly economical. Beating this double-exponential budget requires signed
prime--archimedean cancellation in the tail; absolute-value estimates cannot
prove RH.

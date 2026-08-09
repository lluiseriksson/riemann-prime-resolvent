# The continuous Weil--Suzuki operator

## Why this replaces the first-window matrix as the main target

The first-window matrix is a useful falsifier, but it only samples one compact
test space. Suzuki's continuous realization packages the full localized Weil
quadratic form into a self-adjoint operator (A_a) on (L^2(-a,a)). Its
lowest eigenvalue is

\[
  \lambda_a=\inf_{0\ne v\in\mathcal D(Q_W^a)}
  \frac{Q_W^a(v)}{\lVert v\rVert_2^2}.
\]

The source proves unconditionally that (a\mapsto\lambda_a) is continuous,
that it is positive for sufficiently small (a), and that RH fails exactly
when (lambda_a<0) for some (a). Thus the operative target is a coercive
estimate preventing this eigenvalue branch from reaching zero.

Primary source: M. Suzuki, [*Weil's quadratic form via the screw
function*](https://arxiv.org/abs/2606.09096), especially equations (103)--(108)
and Theorems 1, 3, and 4.

## A structural lemma: domain monotonicity

### Proposition

If (0<a<b), then

\[
  \boxed{\lambda_b\leq\lambda_a.}
\]

### Proof

Extend every (v\in C_c^\infty(-a,a)) by zero to ((-b,b)). Its norm and
the cutoff-free Weil value (Q_W(v)) do not change. Hence the Rayleigh
quotients used for (a) form a subset of those used for (b). Taking the
infimum and using Suzuki's identification of (lambda_a) with the infimum on
(C_c^\infty(-a,a)) gives the claim. No zero of zeta and no instance of RH is
used. ∎

Together with Suzuki's continuity theorem this gives a precise crossing
picture. If RH is false, the set

\[
  \{a>0:\lambda_a<0\}
\]

is an upper interval, and its left endpoint is preceded by positive values and
has value zero (a zero plateau is not excluded). This improves the geometry of
the target but does not prove its sign.

## Source-normalized discretization

`experiments/theta_pencil/screw_weil_operator.py` implements the defining Weil
functional directly. For (f=v*\widetilde v),

\[
\begin{aligned}
Q_W(v)={}&
\left|\int v(x)e^{x/2}\,dx\right|^2+
\left|\int v(x)e^{-x/2}\,dx\right|^2\\
&-(\log 4\pi+\gamma)\lVert v\rVert_2^2\\
&-\int_0^\infty
\frac{e^{-t/2}(f(t)+f(-t))-2e^{-t}f(0)}{1-e^{-2t}}\,dt\\
&-\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}
\bigl(f(\log n)+f(-\log n)\bigr).
\end{aligned}
\]

The tail beyond (2a) is integrated exactly as
(-2\operatorname{atanh}(e^{-2a})f(0)). Omitting this term creates a false
sign, so it is part of the registered judge. The basis consists of exact
orthonormal Dirichlet modes

\[
  a^{-1/2}\sin\!\left(\frac{n\pi(x+a)}{2a}\right),\qquad n\ge1.
\]

This eliminates the (10^8)-scale Gram conditioning seen in a raw
polynomial-times-bump basis.

## Reproducible audit

With 8193 grid points the following lowest Ritz values are obtained:

| (a) | dimension | prime powers | Gram condition | lowest Ritz value |
|---:|---:|:---|---:|---:|
| 0.3000 | 16 | none | 1.000000000000006 | (9.05724\times10^{-3}) |
| 0.3465 | 16 | none | 1.000000000000006 | (1.51147\times10^{-3}) |
| 0.4000 | 24 | (2) | 1.000000000000010 | (2.14778\times10^{-4}) |
| 0.5000 | 24 | (2) | 1.000000000000008 | (1.07955\times10^{-6}) |
| 0.5500 | 32 | (2,3) | 1.000000000000011 | (5.95049\times10^{-8}) |

At (a=0.55), dimension 32, the values at 4097, 8193, and 16385 grid
points are respectively (6.26670\times10^{-8}),
(5.95049\times10^{-8}), and (5.90549\times10^{-8}). The last
eigenvector has the component balance

\[
  1.303465683-1.285758527-0.017707097
  =5.90549\times10^{-8},
\]

where the terms are polar, archimedean, and prime contributions.

As an independent conditional cross-check, summing
(2|\widehat v(\gamma_j)|^2) over the first 100 tabulated critical-line zeros
gives (5.80626\times10^{-8}), or 98.32% of the explicit-formula value. This
uses known critical-line zeros only to validate the implementation; it is not
part of any proof.

## Interpretation and next theorem

The tiny positive value is real numerical structure, not evidence that RH is
nearly proved. The minimizing vector suppresses the first two zero samples and
uses time--frequency concentration to make the remaining samples small. This
is consistent with the superexponential decay reported independently in a 2026
finite-element study of the same operator.

The next acceptable advance is an analytic, source-side lower bound

\[
  Q_W^a(v)\ge c(a)\lVert v\rVert_2^2,
  \qquad c(a)\ge0,
\]

derived from the archimedean kernel and the finite translation operators, with
no zero data and no assumed Weil positivity. A finite positive Ritz value does
not supply this bound because Rayleigh--Ritz controls eigenvalues from above.

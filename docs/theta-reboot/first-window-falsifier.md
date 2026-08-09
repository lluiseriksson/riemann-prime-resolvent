# First arithmetic window: exact quadratic form and falsifier

## Claim boundary

This note constructs and tests a finite-dimensional compression of the Weil
form in the first source-faithful support window. It is not a proof of the
infinite-dimensional inequality and is not evidence for RH beyond the tested
subspaces.

Primary formula source: Connes--Consani, *Weil positivity and Trace formula,
the archimedean place*, [arXiv:2006.13771](https://arxiv.org/abs/2006.13771),
Appendix A, equations (A.4)--(A.6). The audited TeX had SHA-256
`b01d353b0423b6fedee373c3c33fe3678eea733f62049810750f6c64ef20f3fc`.

## Logarithmic form

Let $H(t)=h_1(e^t)$ and

\[
 h(t)=\int_{\mathbb R}H(u)\overline{H(u-t)}\,du.
\]

The two constraints on the convolution root are

\[
 \int H(t)e^{t/2}\,dt=0,
 \qquad
 \int H(t)e^{-t/2}\,dt=0.
\tag{C}
\]

They are imposed without a numerical projection by writing

\[
 H=Q\phi,\qquad Q=-\frac{d^2}{dt^2}+\frac14,
\]

for a smooth compactly supported $\phi$. Integration by parts proves (C)
exactly.

If the convolution support is contained in $[-a,a]$, the archimedean term in
the sign convention of the global explicit formula is

\[
 W_{\mathbb R}(H)=
 (\log(4\pi)+\gamma)h(0)
 +\int_0^a
 \frac{e^{-t/2}(h(t)+h(-t))-2e^{-t}h(0)}{1-e^{-2t}}\,dt
 -2\operatorname{artanh}(e^{-a})h(0).
\tag{A}
\]

The final term is the exact tail of the principal-value subtraction. Omitting
it reverses the numerical verdict and is therefore a mandatory normalization
test.

For $4<q\le5$ and $a<\frac12\log q$, only the first power of $2$ can lie in
the support. The finite-prime contribution is exactly

\[
 W_2(H)=\frac{2\log2}{\sqrt2}\operatorname{Re}h(\log2).
\tag{P2}
\]

The registered finite-dimensional judge is the largest generalized
eigenvalue of $W_{\mathbb R}+W_2$ relative to the $L^2$ Gram matrix. The
required sign is nonpositive.

## Independent Fourier representation

Writing

\[
 \theta'(s)=\frac12\operatorname{Re}\psi\!\left(\frac14+\frac{is}{2}\right)
 -\frac12\log\pi,
\]

the same quadratic form is

\[
 W_{\mathbb R}(H)+W_2(H)
 =\frac1\pi\int_{\mathbb R}
 \left[-\theta'(s)+\frac{\log2}{\sqrt2}\cos(s\log2)\right]
 |\widehat H(s)|^2\,ds.
\tag{F}
\]

Thus the first-window problem is a support-restricted Toeplitz inequality with
an explicit symbol. Formula (F) is evaluated independently of (A), using the
digamma function and Fourier quadrature.

## Numerical audit

Three convergence grids, 2049/4097/8193 points, agree in the extremal
eigenvalue to better than $3\times10^{-7}$ in the registered eight-dimensional
pilot. The two representations (A) and (F) agree in generalized operator norm
to $7\times10^{-7}$ for the independent three-vector audit.

At the upper support edge $q=5$, support margin $0.999$:

| basis | dimension | Gram condition | largest eigenvalue |
|---|---:|---:|---:|
| Legendre times flat bump, then $Q$ | 12 | $7.9\times10^2$ | $-0.32749$ |
| Legendre times flat bump, then $Q$ | 16 | $1.5\times10^4$ | $-0.31440$ |
| Legendre times flat bump, then $Q$ | 20 | $2.4\times10^5$ | $-0.30840$ |
| translated flat bumps, then $Q$ | 32 | $2.24$ | $-3.46819$ |

No wrong-sign vector was found. The global bases are more adversarial than the
localized bases and suggest an extremal value near $-0.3$ for this particular
family. This observation is not extrapolated to the full Paley--Wiener space.

## Analytic target exposed by the experiment

For $a\le\frac12\log5$, prove that

\[
 \int_{\mathbb R}
 \left[-\theta'(s)+\frac{\log2}{\sqrt2}\cos(s\log2)\right]
 |\widehat H(s)|^2\,ds\le0
\]

for every $H\in C_c^\infty([-a/2,a/2])$ satisfying (C). A proof must be
uniform up to the support boundary and may not invoke the zero set of zeta.

This is now the exact W2 obligation. The next analytic attempt will seek a
factorization or a sharp Paley--Wiener/Toeplitz bound for this symbol.

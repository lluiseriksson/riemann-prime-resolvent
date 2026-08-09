# Scaling Hamiltonian: equation-level extraction

## Provenance and scope

Primary source: A. Connes and C. Consani, *The Scaling Hamiltonian*,
[arXiv:1910.14368](https://arxiv.org/abs/1910.14368), especially equations
(2.27)--(2.30), (3.1), (4.1), and Conjecture 4.1.

The source TeX used for this audit had SHA-256
`4230cef7af5cdaefdd0924e6b8154ab0e6b6cebf076fd7bf7542df518b8db390`.
The source archive is not vendored in this repository.

This page separates three levels:

- **source identity**: transcribed from the paper;
- **derived target**: an equivalent reformulation within the stated domain;
- **open claim**: not proved here or in the cited source.

## Semilocal setting

For a finite set of places (S\ni\infty), the source uses

\[
 X_S=\mathbb A_S/\mathbb Q_S^*,
\]

with the unitary scaling representation on (L^2(X_S)). If (P_\Lambda)
is the infrared cutoff and

\[
 \widehat P_\Lambda=\mathcal F_S P_\Lambda\mathcal F_S^{-1},
 \qquad R_\Lambda=\widehat P_\Lambda P_\Lambda,
\]

then the semilocal trace formula is

\[
 \operatorname{Tr}(\vartheta(f)R_\Lambda)
 =2f(1)\log\Lambda+
 \sum_{v\in S}\int_{\mathbb Q_v^*}'
 \frac{f(w^{-1})}{|1-w|}\,d^*w+o(1).
\]

The prime on the integral is essential: its normalization is tied to the
choice of basic additive character and the global Poisson formula. It is not
permitted to replace it by an independently normalized local principal value.

## Symmetric test-function convention

Set (h_1(x)=x^{1/2}g(x)),

\[
 h_2(x)=h_1^*(x):=\overline{h_1(x^{-1})},
 \qquad h=h_1\star h_2.
\]

The two Weil constraints become

\[
 \int_0^\infty h_1(x)x^{1/2}\,d^*x=0,
 \qquad
 \int_0^\infty h_1(x)x^{-1/2}\,d^*x=0.
\]

With the source's sign convention, the desired inequality is

\[
 \mathcal W_S(h_1):=
 \sum_{v\in S}\int_{\mathbb Q_v^*}'
 \frac{|w|^{1/2}}{|1-w|}h(w)\,d^*w\le 0.
\tag{W-S}
\]

## Exact operator identity

Let (F=2P-1), (\mathrm d u=[F,u]), and let (u) be the product of the
ratios of the local factors on the critical line. The source proves

\[
 \mathcal W_S(h_1)=
 \operatorname{Tr}\!\left(
 \widehat h_1\widehat h_1^*
 \frac12u^{-1}[F,u]\right).
\tag{O-S}
\]

Here (\widehat h_1\widehat h_1^*\) is positive. It does **not** follow that
the trace has the desired sign, because the second factor has no global sign.

## Exact failure of the naive compression

The tempting factorization

\[
 Pu^*(1-P)uP=-\frac12u^{-1}[F,u]
\]

holds if and only if (Pu=PuP); equivalently, (u^*) is inner in the
relevant Hardy space. This condition fails at both kinds of places:

\[
 u_p(s)=\frac{1-p^{-(1-z)}}{1-p^{-z}},\qquad z=\frac12+is,
\]

has poles in one half-plane and is unbounded in the other, while the
archimedean ratio is likewise unbounded. Moreover, the source shows that the
archimedean logarithmic derivative alone does not have constant sign.

Consequently, W1 is **not** a search for positivity of each local logarithmic
derivative and is **not** a repetition of the failed inner-function argument.

## Support-restricted target

Conjecture 4.1 of the source states that, for

\[
 S_q=\{\infty\}\cup\{p:p<q\},
\]

the semilocal framework should suffice for tests supported in
\((q^{-1/2},q^{1/2})\). There is a subtle but decisive threshold issue.
For \(2<q\le3\), one has \(S_q=\{\infty,2\}\), but
\(q^{1/2}<2\). Since the finite-place term only samples nonzero powers of
the prime, the \(p=2\) distribution is then inactive. The first window in
which a finite-prime value can occur has \(q>4\), and consequently

\[
 4<q\le5,\qquad S_q=\{\infty,2,3\}.
\]

The concrete research target is therefore:

> Prove (W-S), or an exactly equivalent compression inequality, on the
> support-restricted test space for \(4<q\le5\), after imposing both Weil
> constraints.

This is a restricted quadratic-form problem. A pointwise sign for
(u^{-1}[F,u]) is neither required nor expected. Extending the result from one
support window to all compact supports remains a separate, open induction over
finite sets of places.

## Claim boundary

The source proves the trace identities and diagnoses the failed direct
positivity argument. It does not prove Conjecture 4.1. This repository has not
proved (W-S) in the first source-faithful arithmetic window
\(S=\{\infty,2,3\}\). Studying \(S=\{\infty,2\}\) with support reaching (2)
would be a stronger auxiliary conjecture, not Conjecture 4.1 itself.

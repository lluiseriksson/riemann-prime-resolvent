# The first-crossing real-rooted witness

## Claim boundary

This note does **not** prove the Riemann hypothesis. It combines two
unconditional operator results to sharpen what a counterexample to RH would
have to produce at the first loss of localized Weil positivity.

Primary sources:

- A. Connes and W. D. van Suijlekom,
  [*Quadratic Forms, Real Zeros and Echoes of the Spectral Action*](https://arxiv.org/abs/2511.23257),
  especially Theorem 6.1 and its proof;
- M. Suzuki,
  [*Weil's quadratic form via the screw function*](https://arxiv.org/abs/2606.09096),
  especially Theorems 1.1--1.4 and the proof of Lemma 3.1.

Let \(Q_W^a\) be the closed localized Weil form on \(L^2(-a,a)\), let
\(A_a\) be its associated self-adjoint operator, and put

\[
 \lambda_a=\min\operatorname{spec}(A_a).
\]

Suzuki proves unconditionally that \(A_a\) is lower bounded with discrete
spectrum, that \(a\mapsto\lambda_a\) is continuous, and that the span

\[
 E_a=\operatorname{span}\{e^{i\pi n x/a}:n\in\mathbb Z\}
\]

is a core for the quadratic form \(Q_W^a\). The form and the operator commute
with reflection \(Jf(x)=f(-x)\).

## 1. Removing the evenness restriction

Connes--van Suijlekom prove their finite real-zero theorem when the
one-dimensional kernel is even. Their commutator identity also yields the odd
case after a resolvent change of variable.

### Proposition 1 (finite odd-kernel theorem)

Let \(Q\) be a real positive semidefinite matrix indexed by
\(\{-N,\ldots,N\}\), with

\[
 q_{ii}=a_i,\qquad q_{ij}=\frac{b_i-b_j}{i-j}\quad(i\ne j),
 \qquad a_{-i}=a_i,\quad b_{-i}=-b_i.
\]

If \(\ker Q=\mathbb R\xi\) and \(\xi_{-j}=-\xi_j\), then every zero of

\[
 R(t):=\sum_{j=-N}^{N}\frac{\xi_j}{t-j}
\]

away from its removable poles is real. Consequently the Fourier transform of
the zero-extended trigonometric polynomial represented by \(\xi\) has only
real zeros.

### Proof

Let \(D e_j=j e_j\), \(\eta=\sum_j e_j\), and
\(\beta=\sum_j b_j e_j\). The exact commutator identity is

\[
 DQ-QD=|\beta\rangle\langle\eta|-|\eta\rangle\langle\beta|.     \tag{C}
\]

Choose a real \(r\notin\{-N,\ldots,N\}\) such that \(R(r)\ne0\), and set

\[
 X=(D-rI)^{-1},\quad p=X\beta,\quad q=X\eta,\quad
 c=\langle q,\xi\rangle=-R(r)\ne0.
\]

Multiplication of (C) on both sides by \(X\) gives

\[
 QX-XQ=|p\rangle\langle q|-|q\rangle\langle p|=:C.
\]

Put \(u=QX\xi=C\xi\) and \(\ell=q/c\). Since
\(u=cp-\langle p,\xi\rangle q\), direct expansion gives

\[
 C=|u\rangle\langle\ell|-|\ell\rangle\langle u|,
 \qquad \langle\ell,\xi\rangle=1.
\]

Therefore

\[
 X':=X-|X\xi\rangle\langle\ell|
\]

satisfies \(X'\xi=0\) and

\[
 QX'-(X')^*Q=0.                                                \tag{SA}
\]

It induces a self-adjoint operator on the separated Euclidean quotient by
\(\ker Q\). As in Connes--van Suijlekom Lemma 5.3, a basis formed by \(\xi\)
and lifts of quotient eigenvectors makes \(X'\) triangular with real
diagonal. Hence every zero of \(\det(X'-sI)\) is real.

Write \(x_j=(j-r)^{-1}\). The matrix determinant lemma and oddness
\(\sum_j\xi_j=0\) give, away from the poles,

\[
\begin{aligned}
\frac{\det(X'-sI)}{\det(X-sI)}
 &=1-\frac1c\sum_j\frac{x_j^2\xi_j}{x_j-s}\\
 &=-\frac{s^2}{c}\sum_j\frac{\xi_j}{x_j-s}.
\end{aligned}                                                   \tag{D}
\]

Under the real Möbius substitution \(t=r+1/s\),

\[
 \sum_j\frac{\xi_j}{x_j-s}=\frac{R(t)}{s^2}.                    \tag{M}
\]

Thus a non-real zero \(t\) of \(R\) would give the non-real eigenvalue
\(s=(t-r)^{-1}\) of \(X'\), contradicting (SA). Zeros at sampling nodes arise
only when the corresponding residue vanishes and are already real. The
Shannon formula used in Connes--van Suijlekom Proposition 5.5 writes the
Fourier transform as a sine factor times \(R\), so all its zeros are real.
\(\square\)

The proof is algebraic and uses neither zeta nor RH. As a falsification check,
a deterministic random search constructed positive even and odd parity
blocks with a one-dimensional odd kernel. After enforcing the kernel equation
at matrix level, 12,744 feasible matrices were found across
\(N=3,4,5,6\); the reduced polynomial \(P(s)=sR_0(s^2)\) was real-rooted in
every case. This check is not used in the proof.

## 2. The form-core version of the infinite theorem

The precise statement of Connes--van Suijlekom Theorem 6.1 assumes that the
form on trigonometric polynomials defines a lower-bounded essentially
self-adjoint operator. Inspection of its proof gives the following slightly
more flexible formulation.

### Lemma 2 (parity-free form-core real-zero theorem)

Let \(q\) be a lower-bounded closed real convolution form on an interval of
length \(L\), obtained from a real one-sided distribution as in equation (6)
of Connes--van Suijlekom. Assume:

1. the trigonometric polynomials form a core for \(q\);
2. the associated self-adjoint operator \(A\) has a simple isolated lowest
   eigenvalue with eigenfunction \(\xi\);
3. the form commutes with reflection about the midpoint of the interval.

Then the zero extension of \(\xi\) has an entire Fourier transform and every
zero of that Fourier transform is real.

### Proof

Shift \(q\) by its lowest eigenvalue, which leaves the eigenfunction unchanged
and makes the form positive with \(\xi\) in its radical. Simplicity and
reflection invariance force \(\xi\) to have definite parity. Because the
trigonometric polynomials are a **form** core, there are normalized
trigonometric polynomials \(\eta_N\) of that same parity converging to
\(\xi\) in \(L^2\) with
\(q(\eta_N)\to q(\xi)\). Restrict \(q\) to the finite Fourier space
\(E_N=\operatorname{span}\{e_k:|k|\le N\}\).

The spectral gap above the simple isolated ground state and the min--max
principle imply that, for large \(N\), the finite restriction has a simple
lowest eigenvalue and its normalized ground vector \(\xi_N\) converges to
\(\xi\) in \(L^2\). Subtracting the finite lowest eigenvalue from that
restriction makes its matrix positive with one-dimensional kernel and does
not change \(\xi_N\). Each finite restriction commutes with reflection. Hence
its simple ground vector has definite parity; it must have the parity of
\(\xi\) for large \(N\), because normalized vectors of opposite parity are at
distance \(\sqrt2\).

If that parity is even, the finite-dimensional theorem of
Connes--van Suijlekom applies. If it is odd, Proposition 1 applies. Thus
\(\widehat{\xi_N}\) has only real zeros in either case. Compact support and
\(\xi_N\to\xi\) in \(L^2\) give locally uniform convergence
\(\widehat{\xi_N}\to\widehat\xi\) on \(\mathbb C\). Hurwitz's theorem then
puts every zero of \(\widehat\xi\) on the real axis. These are exactly the
steps of their Theorem 6.1; no operator-core approximation is used after the
form-core approximation is available. \(\square\)

### Corollary 3 (application to the localized Weil operator)

For every \(a>0\), if the lowest eigenvalue of \(A_a\) is simple, then the
Fourier transform of its full infinite-dimensional ground state has only real
zeros, regardless of its parity.

Indeed Suzuki supplies the missing form-core statement explicitly: \(E_a\)
is a core for \(Q_W^a\). Lower boundedness, closedness, discreteness and
reflection invariance are also unconditional source theorems. This corollary
closes the gap between the finite restrictions discussed in Suzuki's
introduction and the full ground state, but it does not identify that Fourier
transform with the Riemann \(\xi\)-function.

## 3. First-crossing dichotomy

The already certified endpoint bound is

\[
 A_{0.72}\succeq 9.86850102990163\cdot10^{-17}I.
\]

Domain monotonicity makes \(a\mapsto\lambda_a\) nonincreasing. Suppose RH is
false and define

\[
 a_*:=\inf\{a>0:\lambda_a<0\}.
\]

Suzuki's equivalence, continuity and the strict endpoint certificate give

\[
 \boxed{a_*>0.72,\qquad \lambda_{a_*}=0,\qquad A_{a_*}\succeq0.}       \tag{FC}
\]

Since \(A_{a_*}\) has discrete spectrum, zero is an eigenvalue. Reflection
invariance now gives an exhaustive alternative.

### Theorem 4 (counterexample witness)

If RH is false, there is an \(a_*>0.72\) for which at least one of the
following holds:

1. **degenerate crossing:** \(\dim\ker A_{a_*}\ge2\);
2. **real-rooted simple crossing:** \(\ker A_{a_*}=\mathbb C v_*\) and
   every zero of \(\widehat v_*\) is real.

### Proof

Equation (FC) gives a nonzero ground-state kernel. If its dimension is at
least two, case 1 holds. Otherwise reflection acts on the one-dimensional
kernel by \(+1\) or \(-1\), and Corollary 3 gives case 2 in either parity.
\(\square\)

This is a genuine reduction, but not yet a proof of RH. A proof must exclude
both witnesses from the explicit prime--archimedean structure of \(Q_W^a\).
Simplicity alone now has a concrete consequence, but assuming it would still
discard the degenerate counterexample mechanism.

## 4. Exact parity-gap identity

The degenerate branch of the dichotomy makes parity collision a concrete
analytic target. Let \(K\) denote the
real even distributional kernel of a reflection-invariant convolution form on
\((-a,a)\). For a smooth \(f\) on \((0,a)\), use normalized even and odd
extensions

\[
 (E f)(x)=2^{-1/2}f(|x|),\qquad
 (O f)(x)=2^{-1/2}\operatorname{sgn}(x)f(|x|).
\]

Splitting the quadratic form into the four quadrants gives, exactly,

\[
 q(Ef)=S_a(f)+H_a(f),\qquad q(Of)=S_a(f)-H_a(f),                 \tag{PG}
\]

where, with distributional pairing understood,

\[
\begin{aligned}
 S_a(f)&=\int_0^a\!\int_0^a K(x-y)f(y)\overline{f(x)}\,dy\,dx,\\
 H_a(f)&=\operatorname{Re}\int_0^a\!\int_0^a
             K(x+y)f(y)\overline{f(x)}\,dy\,dx .
\end{aligned}
\]

Thus

\[
 \boxed{q(Ef)-q(Of)=2H_a(f).}                                  \tag{HG}
\]

As a factor check, on a reflection-symmetric finite grid the unnormalized
extensions satisfy \(q(e)-q(o)=4H\). Exact rational arithmetic verified this
identity for seven independently sized grids; division by the two extension
norms gives (HG).

For the prime part of the Weil distribution this Hankel form is

\[
 H_{a,P}(f)=
 -\sum_{2\le n\le e^{2a}}\frac{\Lambda(n)}{\sqrt n}
 \operatorname{Re}\!\int_{\max(0,\log n-a)}^{\min(a,\log n)}
 f(y)\overline{f(\log n-y)}\,dy .                              \tag{HP}
\]

Formula (HP) preserves the signed prime contribution instead of taking
absolute values. It also explains why a termwise parity proof is unavailable:
reflection \(f(y)\mapsto f(\log n-y)\) has both \(+1\) and \(-1\)
directions on its overlap interval. The next viable target is therefore not
a global sign for \(H_a\), but a sign or overlap estimate on the **actual
ground-state branch**, together with a quantitative exclusion of a parity
collision. Such an exclusion would remove the most natural route to a
multiple first-crossing kernel.

## 5. Updated proof obligation

The first-crossing route now has two explicit gates:

1. prove that the lowest eigenspace cannot become multiple;
2. rule out a simple null ground state whose compactly supported Fourier
   transform is real-rooted.

The exact identity (HG) is one entry point for gate 1. Gate 2 must use the
explicit prime--archimedean formula; real-rootedness alone is not a
contradiction. No one of these gates is declared solved here.

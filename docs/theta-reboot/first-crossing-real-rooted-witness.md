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

## 1. Removing the parity restriction

Connes--van Suijlekom prove their finite real-zero theorem when the
one-dimensional kernel is even. In fact their rank-two commutator, after a
resolvent change of variable, removes not only evenness but every parity and
node-symmetry hypothesis.

### Proposition 1 (finite parity-free Loewner theorem)

Let \(d_1,\ldots,d_m\) be distinct real numbers and let \(Q\) be a real
positive semidefinite matrix with

\[
 q_{ii}=a_i,\qquad
 q_{ij}=\frac{b_i-b_j}{d_i-d_j}\quad(i\ne j),
 \qquad a_i,b_i\in\mathbb R.
\]

If \(\ker Q=\mathbb R\xi\), then every zero of

\[
 R(t):=\sum_{j=1}^{m}\frac{\xi_j}{t-d_j}
\]

away from its removable poles is real. In particular, for an arithmetic
lattice \(d_j=j\), the Fourier transform of the zero-extended trigonometric
polynomial represented by \(\xi\) has only real zeros. No parity of \(\xi\)
is required.

### Proof

Let \(D e_j=d_j e_j\), \(\eta=\sum_j e_j\), and
\(\beta=\sum_j b_j e_j\). The exact commutator identity is

\[
 DQ-QD=|\beta\rangle\langle\eta|-|\eta\rangle\langle\beta|.     \tag{C}
\]

Choose a real \(r\notin\{d_1,\ldots,d_m\}\) such that \(R(r)\ne0\), and set

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
\(\ker Q\). A basis formed by \(\xi\) and lifts of quotient eigenvectors
makes \(X'\) triangular with real diagonal. Hence every zero of
\(\det(X'-sI)\) is real.

Write \(x_j=(d_j-r)^{-1}\) and \(A=\sum_j\xi_j\). The matrix determinant
lemma gives, away from the poles,

\[
\begin{aligned}
\frac{\det(X'-sI)}{\det(X-sI)}
 &=1-\frac1c\sum_j\frac{x_j^2\xi_j}{x_j-s}\\
 &=-\frac{s}{c}\left(A+s\sum_j\frac{\xi_j}{x_j-s}\right).
\end{aligned}                                                   \tag{D}
\]

Under the real Möbius substitution \(t=r+1/s\),

\[
 \sum_j\frac{\xi_j}{x_j-s}=\frac{R(t)}{s^2}-\frac{A}{s}.       \tag{M}
\]

Substitution in (D) yields the exact identity

\[
 \boxed{\frac{\det(X'-sI)}{\det(X-sI)}=-\frac{R(r+1/s)}{c}.}     \tag{DR}
\]

Thus a non-real zero \(t\) of \(R\) would give the non-real eigenvalue
\(s=(t-r)^{-1}\) of \(X'\), contradicting (SA). Zeros at sampling nodes arise
only when the corresponding residue vanishes and are already real. For an
arithmetic lattice, the Shannon formula used in Connes--van Suijlekom
Proposition 5.5 writes the Fourier transform as a sine factor times \(R\), so
all its zeros are real. \(\square\)

The proof is algebraic and uses neither zeta nor RH. It strictly contains the
previous odd-kernel argument: when \(A=0\), (D) reduces to its earlier form,
but the cancellation in (M) shows that \(A=0\) was never needed. The earlier
12,744-matrix parity search remains a falsification check only and is not used
in the proof.

### Lemma 1.1 (exact Loewner--Cauchy interpolation identity)

Let \(\phi\) be entire and real on \(\mathbb R\), and let

\[
 L_\phi(d)_{ij}=
 \begin{cases}
  \dfrac{\phi(d_i)-\phi(d_j)}{d_i-d_j},&i\ne j,\\[4pt]
  \phi'(d_i),&i=j.
 \end{cases}
\]

If \(L_\phi(d)\xi=0\), define

\[
 R(z)=\sum_j\frac{\xi_j}{z-d_j},\qquad
 T(z)=\sum_j\frac{\phi(d_j)\xi_j}{z-d_j},\qquad
 H(z)=\phi(z)R(z)-T(z).                                      \tag{LC}
\]

Then all apparent poles of \(H\) are removable and

\[
 \boxed{H(d_i)=(L_\phi(d)\xi)_i=0.}                           \tag{LI}
\]

Consequently

\[
 H(z)=\prod_j(z-d_j)\,C(z)                                  \tag{AD}
\]

for an entire function \(C\). At every node for which \(\xi_i\ne0\), the
rational function \(r=T/R\) has the Hermite contact

\[
 r(d_i)=\phi(d_i),\qquad r'(d_i)=\phi'(d_i).                  \tag{HC}
\]

Indeed, cancellation of the principal part in (LC) gives

\[
 H(d_i)=\phi'(d_i)\xi_i+
 \sum_{j\ne i}\frac{\phi(d_i)-\phi(d_j)}{d_i-d_j}\xi_j.
\]

If \(\xi_i\ne0\), then \(R\) has a simple pole at \(d_i\), while (LI)
says that \(H\) has a zero there. Hence
\(\phi-r=H/R=O((z-d_i)^2)\), proving (HC).

For the integer lattice, subtracting a scalar \(\lambda I\) from the Loewner
matrix is still an exact Loewner matrix: put

\[
 \phi_\lambda(z)=\phi(z)-\lambda\frac{\sin(2\pi z)}{2\pi}.
\]

The correction vanishes at every integer and has derivative one there, so
\(L_{\phi_\lambda}(\mathbb Z)=L_\phi(\mathbb Z)-\lambda I\).
This accounts exactly for the finite ground-state shift in the form-core
argument; it is not an asymptotic replacement.

Identity (AD) is also a warning. Integer Hermite data do not determine an
entire function of critical exponential type: the nonzero aliasing defect
\(C\) is allowed. Any attempted passage from finite positivity to the claim
that \(\phi=T/R\) must control \(C\); setting it to zero would be an
unjustified uniqueness assumption.

### Lemma 1.2 (the full shifted Fourier pencil)

Normalize the interval to \([0,1]\), let \(\mathcal D\) be the real
one-sided distribution defining the form, and for \(\theta\in\mathbb R\) use
the orthonormal basis

\[
 U_n^\theta(x)=e^{2\pi i(n+\theta)x},\qquad n\in\mathbb Z.
\]

Put

\[
 b(z)=-\frac1\pi\mathcal D_y\!\left(\sin(2\pi zy)\right),\qquad
 c(z)=\mathcal D_y\!\left(\cos(2\pi zy)\right),                 \tag{BC}
\]

and

\[
 \phi_\theta(z)=b(z)+
 \frac{\sin(2\pi(z-\theta))}{\pi}\,c(z).                       \tag{SP}
\]

Then the matrix of the form in the shifted basis is exactly

\[
 q(U_m^\theta,U_n^\theta)=
 \begin{cases}
  \dfrac{\phi_\theta(m+\theta)-\phi_\theta(n+\theta)}{m-n},
       &m\ne n,\\[6pt]
  \phi_\theta'(n+\theta),&m=n.
 \end{cases}                                                   \tag{SL}
\]

For the off-diagonal entry, the difference of the two frequencies is the
integer \(m-n\), so the endpoint phase cancels in the convolution calculation
and gives

\[
 \frac{\sin(2\pi(m+\theta)y)-\sin(2\pi(n+\theta)y)}
      {\pi(n-m)}.
\]

At a node \(z=n+\theta\), the correction term in (SP) vanishes, while

\[
 b'(z)=-2\mathcal D_y(y\cos(2\pi zy)),\qquad
 \phi_\theta'(z)=b'(z)+2c(z)
 =2\mathcal D_y((1-y)\cos(2\pi zy)),
\]

which is the diagonal convolution entry. This proves (SL). Subtracting a
scalar \(\lambda I\) is again exact after replacing \(\phi_\theta\) by

\[
 \phi_{\theta,\lambda}(z)=\phi_\theta(z)
 -\lambda\frac{\sin(2\pi(z-\theta))}{2\pi}.                    \tag{SS}
\]

Thus Proposition 1 and Lemma 1.1 are available on every translated Fourier
lattice, not just on \(\mathbb Z\). This supplies a continuum of exact
finite-dimensional tests. It does **not** by itself glue to a single global
Herglotz function: the interpolated entire function changes with \(\theta\)
by the explicit aliasing term in (SP). In particular, replacing all
\(\phi_\theta\) by \(b\) would silently discard the endpoint contribution
\(c\), and is invalid.

### 1.3. Why sampling and generic spectral synthesis do not close the gate

There are two exact obstructions to a quick infinite-dimensional conclusion.

First, the type in (AD) is critical. The nonzero entire function

\[
 z\longmapsto\sin^2(\pi(z-\theta))                             \tag{CT}
\]

has exponential type \(2\pi\) and a double zero at every point of
\(\theta+\mathbb Z\). Hence even all value-and-derivative data on one shifted
lattice fail to determine an entire function at the type naturally supplied
by a distribution on the whole interval. Formula (CT) is an exact
counterexample to setting the aliasing defect in (AD) to zero.

Second, generic spectral synthesis is not strong enough. Baranov--Belov--
Borichev prove that a complete minimal exponential system on an interval is
hereditarily complete only up to a possible one-dimensional defect, and they
construct examples where that defect occurs. Lemma 2.1 reduces the witness
here to exactly one null direction, so that theorem does not exclude it. Burnol's
minimality and completeness theorems for zeta evaluators live instead in
extended Sonine spaces, where a function and its cosine transform satisfy
simultaneous support conditions. No bounded intertwiner from that space to
the fixed-support Suzuki form domain is presently available.

A nonzero Paley--Wiener function of fixed type has only \(O(T)\) zeros up to
height \(T\): its exponential-type bound gives
\(\log M(r)=O(r)\), and Jensen's formula, applied between \(r\) and \(2r\),
gives \(n(r)\log2=O(r)\). The zeta multiset instead has order
\(T\log T\). Thus the null
state cannot vanish at every zeta evaluator. But the weak Euler--Lagrange
equation gives a **summed** spectral cancellation, not coefficientwise
vanishing. Passing from the former to the latter would require exactly the
missing synthesis/intertwining theorem. The zero-count observation cannot be
used until that theorem is proved.

## 2. The form-core version of the infinite theorem

The precise statement of Connes--van Suijlekom Theorem 6.1 assumes that the
form on trigonometric polynomials defines a lower-bounded essentially
self-adjoint operator. Inspection of its proof gives the following slightly
more flexible formulation.

### Lemma 2 (form-core real-zero theorem for Loewner forms)

Let \(q\) be a lower-bounded closed Hermitian form on an interval of length
\(L\). Assume:

1. the trigonometric polynomials form a core for \(q\);
2. in the standard Fourier basis, every finite principal matrix is real
   symmetric and has the form

   \[
    q_{ii}=a_i,\qquad q_{ij}=\frac{b_i-b_j}{i-j}\quad(i\ne j),
    \qquad a_i,b_i\in\mathbb R;
   \]

3. the associated self-adjoint operator \(A\) has a simple isolated lowest
   eigenvalue with eigenfunction \(\xi\).

Then the zero extension of \(\xi\) has an entire Fourier transform and every
zero of that Fourier transform is real.

### Proof

Shift \(q\) by its lowest eigenvalue, which leaves the eigenfunction unchanged
and makes the form positive with \(\xi\) in its radical. Because the
trigonometric polynomials are a **form** core, there are normalized
trigonometric polynomials \(\eta_N\) converging to \(\xi\) in \(L^2\) with
\(q(\eta_N)\to q(\xi)\). Restrict \(q\) to the finite Fourier space
\(E_N=\operatorname{span}\{e_k:|k|\le N\}\).

The spectral gap above the simple isolated ground state and the min--max
principle imply that, for large \(N\), the finite restriction has a simple
lowest eigenvalue and its normalized ground vector \(\xi_N\) converges to
\(\xi\) in \(L^2\). Subtracting the finite lowest eigenvalue from that
restriction makes its matrix positive with one-dimensional kernel and does
not change \(\xi_N\). The diagonal shift changes none of the
divided-difference off-diagonal entries, so Proposition 1 applies directly.
Thus \(\widehat{\xi_N}\) has only real zeros. Compact support and
\(\xi_N\to\xi\) in \(L^2\) give locally uniform convergence
\(\widehat{\xi_N}\to\widehat\xi\) on \(\mathbb C\). Hurwitz's theorem then
puts every zero of \(\widehat\xi\) on the real axis. These are exactly the
steps of their Theorem 6.1; no operator-core approximation is used after the
form-core approximation is available. \(\square\)

The form obtained from a real one-sided distribution by equation (6) of
Connes--van Suijlekom satisfies assumption 2 by their Proposition 4.1. The
abstract formulation is useful because it is stable under the positive
Fourier-evaluation perturbations below.

### Lemma 2.1 (positive evaluation reduction of a multiple kernel)

Let \(q\succeq0\) satisfy assumptions 1 and 2 of Lemma 2, let its associated
operator have discrete spectrum, and put \(K=\ker A\ne\{0\}\). Then there is
a nonzero \(v\in K\) whose zero-extended Fourier transform has only real
zeros.

### Proof

The zero eigenspace \(K\) is finite-dimensional; write \(r=\dim K\). For
real \(t\), let

\[
 L_t(f)=\int_0^L f(x)e^{-itx}\,dx.
\]

The restrictions \(L_t|_K\), \(t\in\mathbb R\), span \(K^*\). Otherwise a
nonzero \(f\in K\) would satisfy \(L_t(f)=0\) for every real \(t\); its entire
Fourier transform would vanish on \(\mathbb R\), hence identically, forcing
\(f=0\). Choose real points \(t_1,\ldots,t_{r-1}\), none in
\((2\pi/L)\mathbb Z\), so that these restrictions are linearly independent,
and define the bounded positive form

\[
 p(f)=\sum_{j=1}^{r-1}|L_{t_j}(f)|^2.                          \tag{ER}
\]

Then \(K\cap\ker p\) is one-dimensional. Since both forms are positive,

\[
 \operatorname{rad}(q+p)=\operatorname{rad}q\cap\operatorname{rad}p
 =K\cap\ker p.                                                \tag{RI}
\]

The perturbation is bounded and finite-rank, so \(q+p\) is closed, has the
same form core, and its associated operator still has discrete spectrum. Its
lowest eigenvalue is zero, simple and isolated.

It remains to check that no matrix structure was lost. For
\(U_n(x)=L^{-1/2}e^{2\pi i n x/L}\),

\[
 L_t(U_n)=\frac{C_t}{n-tL/(2\pi)},                             \tag{EV}
\]

where \(C_t\) is independent of \(n\). Thus the matrix of
\(|L_t|^2\) is a positive multiple of

\[
 \frac1{(m-s)(n-s)},\qquad s=\frac{tL}{2\pi},                 \tag{C1}
\]

which is the Loewner matrix generated at the integer nodes by
\(b(x)=-\kappa/(x-s)\): its off-diagonal divided difference is (C1), and its
diagonal is \(\kappa/(n-s)^2\). Hence \(q+p\) still satisfies assumption 2
of Lemma 2. Applying that lemma to its unique null vector gives a vector
\(v\in K\cap\ker p\subset K\) with real-rooted Fourier transform.
\(\square\)

### Corollary 3 (application to the localized Weil operator)

For every \(a>0\), if the lowest eigenvalue of \(A_a\) is simple, then the
Fourier transform of its full infinite-dimensional ground state has only real
zeros. Reflection and parity are not needed for this conclusion.

Indeed Suzuki supplies the missing form-core statement explicitly: \(E_a\)
is a core for \(Q_W^a\). Lower boundedness, closedness and discreteness are
also unconditional source theorems. This corollary
closes the gap between the finite restrictions discussed in Suzuki's
introduction and the full ground state, but it does not identify that Fourier
transform with the Riemann \(\xi\)-function.

## 3. The first-crossing witness

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

Since \(A_{a_*}\) has discrete spectrum, zero is an eigenvalue.

### Theorem 4 (counterexample witness)

If RH is false, there are \(a_*>0.72\) and
\(0\ne v_*\in\ker A_{a_*}\) such that every zero of
\(\widehat v_*\) is real.

### Proof

Equation (FC) gives a nonzero finite-dimensional ground-state kernel. If it is
one-dimensional, Corollary 3 applies. If it is multiple, apply Lemma 2.1 to
the positive form \(Q_W^{a_*}\). In both cases one obtains a nonzero original
null vector \(v_*\in\ker A_{a_*}\), not merely a vector for a perturbed
operator, whose Fourier transform is real-rooted.
\(\square\)

This is a genuine reduction, but not yet a proof of RH. The positive
evaluation perturbation removes the multiplicity alternative without assuming
simplicity of the original Weil ground state. A proof must now exclude the
single witness in Theorem 4 from the explicit prime--archimedean structure of
\(Q_W^a\).

## 4. Exact parity-gap identity

Although multiplicity is no longer a separate logical branch, parity
collision remains a concrete diagnostic target. Let \(K\) denote the
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
collision. Such an exclusion would explain the multiplicity geometry, but
Lemma 2.1 shows that it is no longer required for the logical reduction to a
real-rooted null witness.

## 5. Updated proof obligation

The first-crossing route now has one explicit gate:

\[
 \boxed{\text{rule out a nonzero }v\in\ker A_a\text{ whose compactly
 supported Fourier transform is real-rooted.}}                 \tag{GATE}
\]

No simplicity assumption remains in (GATE). The exact identity (HG) remains
an entry point for understanding parity collisions. The separate
[cone no-go](ground-simplicity-cone-no-go.md) proves that ordinary
Beurling--Deny/Perron--Frobenius theory cannot supply simplicity once
\(a>1/2\): the off-diagonal form has a positive open band near separation
one. The remaining gate must use the explicit prime--archimedean formula;
real-rootedness alone is not a contradiction. It is not declared solved here.

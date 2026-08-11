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

### Proposition 4.1 (support saturation and Cartwright rigidity)

The witness in Theorem 4 may be chosen so that, after multiplication by a
constant phase, its Fourier transform is real on the real axis. Moreover its
essential support has convex hull exactly \([-a_*,a_*]\), and, if
\(N_{v_*}(R)\) counts the zeros of \(\widehat v_*\) in \(|z|\le R\), with
multiplicity, then

\[
 \boxed{N_{v_*}(R)=\frac{2a_*}{\pi}R+o(R).}                  \tag{ZD}
\]

In particular the remaining witness is not merely real-rooted: its real zeros
have the maximal Cartwright density allowed by its exact support length.

### Proof

First note that the Weil form is invariant under translation. Indeed,
simultaneously translating a function and its reflected conjugate leaves
\(v*\widetilde v\), and therefore \(W(v*\widetilde v)\), unchanged. Suppose
that the convex hull of the essential support of \(v_*\) had length \(2b<2a_*\).
After a translation, \(v_*\) would belong to the localized form domain on
\((-b',b')\) for some \(b<b'<a_*\), with the same zero quadratic value.
But the definition of the first crossing gives \(\lambda_{b'}>0\), a
contradiction. Hence the convex hull is exactly \([-a_*,a_*]\).

Put \(F=\widehat v_*\) and \(F^\#(z)=\overline{F(\bar z)}\). Both are
Cartwright entire functions of order at most one. Since every zero of \(F\)
is real, \(F\) and \(F^\#\) have the same zero divisor. The Cartwright
product theorem for a Paley--Wiener function with smallest inverse-transform
support interval (equivalently, Theorem 5 of Al-Hammali--Faridani) therefore
gives

\[
 F^\#(z)=e^{i(cz+d)}F(z),\qquad c,d\in\mathbb R.             \tag{PT1}
\]

Multiplication by \(e^{icz}\) translates the inverse Fourier support by
\(c\). The support indicator of each side of (PT1) is the same reflected
interval \([-a_*,a_*]\), so \(c=0\). Replacing \(F\) by
\(e^{id/2}F\) then gives \(F^\#=F\). Equivalently, after that constant phase,

\[
 v_*(-x)=\overline{v_*(x)}                                  \tag{PT2}
\]

almost everywhere.

Finally, the Paley--Wiener indicator diagram of \(F\) has vertical width
equal to the length of the convex hull of the essential support, namely
\(2a_*\). The Cartwright zero-density theorem gives total zero density equal
to that width divided by \(\pi\). All zeros are real, so no angular sector is
lost, and (ZD) follows. \(\square\)

Two cautions are essential. First, (PT2) is a conjugate-reflection symmetry,
not an assertion that the witness is even: its real and imaginary parts may
occupy the even and odd null sectors simultaneously. Second, critical density
does not make the zero set a uniqueness set for the same Paley--Wiener space;
\(F\) itself is the counterexample. Thus (ZD) sharpens the exterior synthesis
problem but does not solve it by a density count alone.

### Proposition 4.1a (pure parity or a genuine parity collision)

The witness in Proposition 4.1 may be written

\[
 v_*=e_*+i o_*,                                           \tag{PD1}
\]

where \(e_*\) is real and even, \(o_*\) is real and odd, and

\[
 e_*,o_*\in\ker A_{a_*}.                                  \tag{PD2}
\]

Consequently exactly one of the following alternatives holds:

1. one component in (PD1) vanishes, so the real-rooted witness has pure
   parity and its Fourier transform is respectively even or odd;
2. both components are nonzero, and the lowest even and odd spectral levels
   collide at zero at the same first-crossing support.

### Proof

After the constant phase in Proposition 4.1, equation (PT2) says
\(v_*(-x)=\overline{v_*(x)}\). Taking real and imaginary parts gives a real
even function \(e_*\) and a real odd function \(o_*\), proving (PD1). The
localized Weil operator commutes with conjugation and with reflection. Hence
it annihilates the real and imaginary parts of \(v_*\) and their parity
projections. Since \(A_{a_*}v_*=0\), this proves (PD2). If both components
are nonzero, zero belongs to both parity restrictions. Because
\(A_{a_*}\succeq0\), it is their lowest spectral value. If one component
vanishes, the Fourier transform of the surviving real-even function is even
and real on the real axis, while the transform of \(i\) times a real-odd
function is odd and real there. Its real-rootedness is the one already proved
for \(v_*\). \(\square\)

Thus a mixed real-rooted witness is not a third symmetry class: it is an exact
certificate of a parity collision. Excluding such a collision would reduce
the first-crossing gate to the pure even/odd real-rooted branches, but no such
exclusion is asserted here.

### Proposition 4.2 (finite rational localization of an off-line quartet)

Let \(F\) be the constant-phase real entire transform supplied by Proposition
4.1 and let \(\Lambda\subset\mathbb R\) be its zero multiset. Let
\(\Gamma\) be the zero multiset in Suzuki's spectral coordinate, so that

\[
 Q_W(g,h)=\sum_{\gamma\in\Gamma}m_\gamma
 \widehat g(\gamma)\overline{\widehat h(\bar\gamma)}.          \tag{EF}
\]

Fix a non-real orbit
\(\mathcal O=\{\gamma_0,\bar\gamma_0,-\gamma_0,-\bar\gamma_0\}\)
and a finite conjugation-invariant set
\(Z\subset\Gamma\setminus\mathcal O\). For every integer \(d\ge1\) there is
a finite set \(S\subset\Lambda\) of distinct zeros and a real polynomial
\(P\), with

\[
 G(z)=F(z)\frac{P(z)}{Q_S(z)},\qquad
 Q_S(z)=\prod_{\lambda\in S}(z-\lambda),                     \tag{RL1}
\]

such that

\[
 G(\gamma_0)=G(-\bar\gamma_0)=i,qquad
 G(\bar\gamma_0)=G(-\gamma_0)=-i,qquad
 \operatorname{ord}_\gamma G\ge m_\gamma\quad(\gamma\in Z), \tag{RL2}
\]

and \(P/Q_S=O(|z|^{-d})\) at infinity. All apparent poles in (RL1)
are removable, \(G\) belongs to the same Paley--Wiener space as \(F\), and,
for \(d\) sufficiently large, the series (EF) for \(Q_W(G)\) is absolutely
convergent.

### Proof

All zeros of \(F\) are real, so \(F\) is nonzero at every member of
\(\mathcal O\). For \(\gamma\in Z\), put

\[
 r_\gamma=\max\{0,m_\gamma-\operatorname{ord}_\gamma F\}.
\]

Choose as many distinct members of \(\Lambda\setminus Z\) as needed and form
\(Q_S\). On \(\mathcal O\), prescribe

\[
 P(\gamma)=c_\gamma\frac{Q_S(\gamma)}{F(\gamma)},             \tag{RL3}
\]

where \(c_\gamma\) is the value in (RL2), and at every \(\gamma\in Z\)
prescribe a zero jet of order \(r_\gamma\) for \(P\). These Hermite data are
invariant under conjugation. Hence Hermite interpolation gives a polynomial
\(P\) with real coefficients and degree smaller than

\[
 M=4+\sum_{\gamma\in Z}r_\gamma.
\]

Because \(S\cap Z=\varnothing\), multiplication by \(P/Q_S\) raises the zero
order of \(F\) at \(\gamma\) by at least \(r_\gamma\), proving (RL2). Taking
\(|S|\ge M+d\) gives the stated decay.

Every factor in \(Q_S\) divides \(F\), so (RL1) is entire. Division by a
finite polynomial and multiplication by \(P\) do not enlarge the
Paley--Wiener indicator; the extra decay makes the real-axis \(L^2\) and
logarithmic form-domain conditions immediate. Finally, the standard unit-strip
zero count \(O(\log(2+|T|))\) for \(\xi\), together with the local
Paley--Wiener evaluation bound in the fixed strip
\(|\operatorname{Im}z|\le1/2\), makes (EF) absolutely convergent once \(d\)
is chosen large enough. \(\square\)

The four prescribed terms in (EF) contribute

\[
 -\sum_{\gamma\in\mathcal O}m_\gamma<0.                     \tag{NEG}
\]

Thus finite interpolation is not the obstruction. An unconditional closure
would follow from the following precise tail statement: the sets \(Z\) can be
exhausted while choosing the interpolants above so that

\[
 \sum_{\gamma\in\Gamma\setminus(\mathcal O\cup Z)}
 m_\gamma |G(\gamma)|^2=o(1).                               \tag{RTL}
\]

Indeed (NEG), (RTL), and the absolute convergence would eventually give
\(Q_W(G)<0\), contradicting \(Q_W^{a_*}\succeq0\). This would exclude every
non-real \(\gamma_0\) and prove RH. Statement (RTL) is **not** proved here.
It is a weighted rational-localization problem at critical Paley--Wiener
density. Pointwise interpolation on each finite set, even with arbitrarily
large algebraic decay, does not control the growth of its interpolation
constants, so a diagonal "cancel more zeros" argument is invalid without a
uniform estimate. This is the exact remaining synthesis cost exposed by the
real-rooted witness.

### Proposition 4.3 (Jensen cost of exhaustive spectral cancellation)

Fix the off-line orbit \(\mathcal O\) and its member \(\gamma_0\). Suppose
that, for every sufficiently large \(H\), a function
\(G_H\in PW_{a_*}\) satisfies

\[
 G_H(\gamma_0)=i,
 \qquad
 \operatorname{ord}_\gamma G_H\ge m_\gamma
 \quad
 \left(\gamma\in\Gamma\setminus\mathcal O, |\gamma|\le H\right).
                                                               \tag{JC1}
\]

If \(g_H\in L^2[-a_*,a_*]\) is the inverse Fourier transform of \(G_H\),
then

\[
 \boxed{
 \log\|g_H\|_2\ge
 \frac{\log 2}{\pi}H\log\frac{H}{2\pi}
 -\left(\frac{\log 2}{\pi}+2a_*\right)H-O(\log H).}
                                                               \tag{JC2}
\]

In particular, an exhaustion in (RTL) cannot be obtained from interpolants
whose Paley--Wiener norms remain bounded, or even grow merely
exponentially in \(H\).

### Proof

Apply Jensen's formula to \(z\mapsto G_H(z+\gamma_0)\) on the circle of
radius \(2H\). Every cancelled spectral point with \(|\gamma|\le H\) lies
at distance at most \(H+O(1)\) from \(\gamma_0\), and therefore contributes

\[
 \log\frac{2H}{|\gamma-\gamma_0|}
 \ge \log 2-O(H^{-1})
\]

for each unit of its multiplicity. The Riemann--von Mangoldt formula, counted
in both spectral directions, gives

\[
 \sum_{\substack{\gamma\in\Gamma\\|\gamma|\le H}}m_\gamma
 =\frac{H}{\pi}\log\frac{H}{2\pi}-\frac{H}{\pi}+O(\log H).     \tag{JC3}
\]

Deleting the fixed orbit \(\mathcal O\) changes this only by \(O(1)\).
Since \(|G_H(\gamma_0)|=1\), Jensen's formula and (JC3) imply

\[
 \max_{|z-\gamma_0|=2H}\log|G_H(z)|
 \ge (\log 2)\left(
 \frac{H}{\pi}\log\frac{H}{2\pi}-\frac{H}{\pi}
 \right)-O(\log H).                                          \tag{JC4}
\]

The Paley--Wiener evaluation estimate on the same circle gives

\[
 |G_H(z)|\le C_{a_*,\gamma_0}e^{2a_*H}\|g_H\|_2.
                                                               \tag{JC5}
\]

Combining (JC4) and (JC5) proves (JC2). \(\square\)

Proposition 4.3 is a barrier, not a contradiction to (RTL). A sequence may
have enormous ambient Paley--Wiener norm while its sampled tail is small.
Thus (JC2) rules out every uniformly controlled interpolation argument, but
the remaining possibility is precisely a highly ill-conditioned construction
whose norm escapes between the spectral evaluation functionals. Any proof of
(RTL) must quantify that exceptional concentration rather than hide it in a
diagonal limit.

### Proposition 4.4 (low-type sampling obstruction to RTL)

Let \(A_0=0.10076\), and let \(\alpha_{\mathrm O}\) be the positive root of
\(e^x=2x+1\). Define

\[
 a_{\mathrm K}:=
 \frac{\sqrt{3\alpha_{\mathrm O}/8}}
 {\sqrt{(2\pi A_0)^2+1/4}}
 =0.8508610646\ldots .                                        \tag{KS1}
\]

For every \(0<a<a_{\mathrm K}\), there are a constant \(C_a>0\) and a
finite family \(E_a\) of spectral derivative evaluations, supported on
\(\Gamma\setminus\mathcal O\), such that every \(G=\widehat g\in PW_a\)
with square-summable spectral samples satisfies

\[
 \|g\|_2^2\le C_a\left(
 \sum_{\gamma\in\Gamma\setminus\mathcal O}m_\gamma|G(\gamma)|^2
 +\sum_{(\eta,j)\in E_a}|G^{(j)}(\eta)|^2
 \right).                                                     \tag{KS2}
\]

Consequently, no sequence satisfying (JC1), the corresponding finite
Hermite cancellations, and (RTL) exists in \(PW_a\) when
\(a<a_{\mathrm K}\). In particular, the rational-localization route of
Proposition 4.2 cannot close RH if its hypothetical first crossing lies in

\[
 0.72<a_*<0.8508610646\ldots .                                \tag{KS3}
\]

### Proof

The explicit zero-counting estimate of Bellotti--Wong is

\[
 \left|N(T)-\frac{T}{2\pi}\log\frac{T}{2\pi e}\right|
 \le A_0\log T+0.24460\log\log T+8.08292.                    \tag{KS4}
\]

Hence, for every fixed \(L>4\pi A_0\), every interval of length \(L\) at
sufficiently large positive height contains a zeta zero: subtracting (KS4)
at the two endpoints leaves the positive leading coefficient
\(L/(2\pi)-2A_0\). The same holds at negative height by symmetry.

Put \(D=\pi/a\). In every sufficiently remote interval
\([nD-L/2,nD+L/2]\), choose one spectral point \(\gamma_n\). Since the
spectral coordinate of a nontrivial zero lies in
\(|\operatorname{Im}\gamma|<1/2\),

\[
 |\gamma_n-nD|\le\delta_L,
 \qquad
 \delta_L:=\sqrt{L^2/4+1/4}.                                  \tag{KS5}
\]

The complex Kadec theorem of Avantaggiati--Loreti--Vellucci says that
\(\{e^{i\lambda_nt}\}_{n\in\mathbb Z}\) is a Riesz basis of
\(L^2[-\pi,\pi]\) whenever

\[
 \sup_n|\lambda_n-n|<
 \frac1\pi\sqrt{\frac{3\alpha_{\mathrm O}}8}.               \tag{KS6}
\]

After scaling from \([-\pi,\pi]\) to \([-a,a]\), (KS5)--(KS6) apply
provided

\[
 a\delta_L<\sqrt{3\alpha_{\mathrm O}/8}.                     \tag{KS7}
\]

The definition (KS1) is exactly the limiting condition obtained by letting
\(L\downarrow4\pi A_0\). Thus, for \(a<a_{\mathrm K}\), choose \(L\)
so that (KS7) holds and fill the finitely many central indices with their
unperturbed lattice frequencies. Complex Kadec then shows that the remote
spectral evaluation kernels form a Riesz basis for a closed subspace of
finite codimension in \(L^2[-a,a]\).

It remains only to fill that finite defect. The complete family of spectral
derivative kernels

\[
 \left\{G\mapsto G^{(j)}(\gamma):
 \gamma\in\Gamma\setminus\mathcal O, 0\le j<m_\gamma\right\} \tag{KS8}
\]

has trivial common kernel. Indeed, a nonzero \(PW_a\) function has only
\(O(R)\) zeros in \(|z|\le R\), counted with multiplicity, whereas a common
kernel vector in (KS8) would have
\(R\log R/\pi+O(R)\) zeros there by Riemann--von Mangoldt. Since the Kadec
tail has finite codimension, finitely many members of (KS8) span its missing
orthogonal complement. Call that finite family \(E_a\). The Riesz lower
bound for the tail plus this finite-dimensional completion gives (KS2).

Now let the Hermite cancellation set exhaust \(\Gamma\setminus\mathcal O\).
For all sufficiently large stages the evaluations in \(E_a\) vanish exactly,
while (RTL) makes the remaining value-sample sum tend to zero. Equation (KS2)
would force \(\|g_H\|_2\to0\). Paley--Wiener evaluation at the fixed point
\(\gamma_0\) would then give \(G_H(\gamma_0)\to0\), contradicting
\(G_H(\gamma_0)=i\). \(\square\)

The two numerical constants used here come from
[the explicit Riemann--von Mangoldt bound](https://arxiv.org/abs/2412.15470)
and
[the complex Kadec theorem](https://arxiv.org/abs/1603.08762).
Proposition 4.4 does not exclude (RTL) when \(a\ge a_{\mathrm K}\), and no
upper bound \(a_*<a_{\mathrm K}\) for a hypothetical first crossing is known.
It therefore closes a genuine parameter range of the proposed mechanism, not
the Riemann hypothesis.

### Proposition 4.5 (conjugate-pair improvement)

Let \(L_0=4\pi A_0\), and put

\[
 q_a=1-\cos(aL_0/2)+\sin(aL_0/2),
 \qquad
 \varepsilon_a=\cosh(a/2)-1.                                 \tag{KP1}
\]

Let \(a_{\mathrm P}=0.9908731338\ldots\) be the first positive solution of

\[
 (1-q_a)-(1+q_a)\varepsilon_a=0.                              \tag{KP2}
\]

Then the sampling inequality (KS2), with a possibly different finite defect
family, and hence the impossibility of (RTL), hold for every

\[
 \boxed{0<a<a_{\mathrm P}.}                                  \tag{KP3}
\]

### Proof

Choose \(L>L_0\) sufficiently close to \(L_0\). As in Proposition 4.4,
select a spectral point
\(\gamma_n=x_n+iy_n\) above each sufficiently remote lattice site
\(n\pi/a\), now recording separately that

\[
 |x_n-n\pi/a|\le L/2,
 \qquad |y_n|<1/2.                                           \tag{KP4}
\]

The real Kadec proof gives the synthesis operator

\[
 T_xc=\sum_n c_ne^{ix_nt}
\]

the normalized bounds

\[
 (1-q_{a,L})\|c\|_{\ell^2}\le\|T_xc\|_2
 \le(1+q_{a,L})\|c\|_{\ell^2},
 \quad
 q_{a,L}=1-\cos(aL/2)+\sin(aL/2),                            \tag{KP5}
\]

provided \(aL/(2\pi)<1/4\). Instead of treating the vertical displacement
as an arbitrary complex perturbation, pair the two spectral points forced by
the functional equation:

\[
 \frac{e^{i(x_n+iy_n)t}+e^{i(x_n-iy_n)t}}2
 =e^{ix_nt}\cosh(y_nt).                                      \tag{KP6}
\]

The linear imaginary perturbation has disappeared. Expanding the remaining
factor and applying the upper bound in (KP5) at each even order gives

\[
\begin{aligned}
 \left\|\sum_n c_ne^{ix_nt}(\cosh(y_nt)-1)\right\|_2
 &\le(1+q_{a,L})
   \sum_{k\ge1}\frac{(a/2)^{2k}}{(2k)!}\|c\|_{\ell^2}\\
 &=(1+q_{a,L})(\cosh(a/2)-1)\|c\|_{\ell^2}.                 \tag{KP7}
\end{aligned}
\]

Therefore the paired family in (KP6) is a Riesz basis whenever

\[
 (1-q_{a,L})-(1+q_{a,L})\varepsilon_a>0.                     \tag{KP8}
\]

For \(L\downarrow L_0\), condition (KP8) is precisely \(a<a_{\mathrm P}\).
It also implies the real Kadec condition at this first root. The remote paired
family consequently spans a finite-codimensional subspace. Complete it by
finitely many spectral derivative kernels exactly as in Proposition 4.4.
Finally,

\[
 \left|\frac{G(x_n+iy_n)+G(x_n-iy_n)}2\right|^2
 \le\frac{|G(x_n+iy_n)|^2+|G(x_n-iy_n)|^2}{2},               \tag{KP9}
\]

so the resulting lower frame bound is controlled by the same value-sample
tail appearing in (RTL). Exhaustive Hermite cancellation would again force
\(\|g_H\|_2\to0\), contradicting \(G_H(\gamma_0)=i\). \(\square\)

The improvement from \(a_{\mathrm K}\) to \(a_{\mathrm P}\) uses the full
quartet symmetry rather than treating the imaginary displacement as noise.
The comparison with the constant multiplier in (KP7) is not optimal, however.

### Proposition 4.6 (centered conjugate-pair improvement)

Let \(L_0=4\pi A_0\), let \(q_a\) be as in (KP1), and let
\(a_{\mathrm C}=1.0839780274\ldots\) be the first positive solution of

\[
 (1-q_a)-\frac{1+q_a}{2}\bigl(\cosh(a/2)-1\bigr)=0.          \tag{KC1}
\]

Then the sampling inequality (KS2), with a finite defect family, and hence
the impossibility of the exhaustive Hermite version of (RTL), hold for every

\[
 \boxed{0<a<a_{\mathrm C}.}                                  \tag{KC2}
\]

#### Proof

Retain the conjugate-pair synthesis family in (KP6). For every \(k\ge1\),

\[
 0\le y_n^{2k}\le 2^{-2k}.
\]

Instead of comparing all these coefficients with zero, subtract the midpoint
\(2^{-2k-1}\). The resulting common multiplier is

\[
 h_0(t)=1+\frac12\sum_{k\ge1}\frac{(t/2)^{2k}}{(2k)!}
       =\frac{1+\cosh(t/2)}2\ge1.                            \tag{KC3}
\]

Consequently the centered reference synthesis operator
\(c\mapsto h_0T_xc\) has lower bound \(1-q_{a,L}\). At every even order the
centered coefficient error has modulus at most \(2^{-2k-1}\). The same
Kadec upper bound used in (KP7), now applied to those centered coefficient
sequences, gives

\[
 \left\|\sum_n c_ne^{ix_nt}\bigl(\cosh(y_nt)-h_0(t)\bigr)\right\|_2
 \le\frac{1+q_{a,L}}2\bigl(\cosh(a/2)-1\bigr)\|c\|_{\ell^2}. \tag{KC4}
\]

Thus the paired family has a positive lower Riesz bound whenever the
left-hand side of (KC1), with \(L\) in place of \(L_0\), is positive. The
first root remains below the real-Kadec ceiling
\(\pi/(2L_0)=1.2405716554\ldots\), so the real-frequency basis estimate used
above is valid. Letting \(L\downarrow L_0\) yields (KC1)--(KC2), and the
finite-dimensional completion and contradiction with (RTL) are exactly as
in Propositions 4.4--4.5. \(\square\)

Coefficientwise midpoint centering is optimal within this perturbative proof:
for an interval \([0,2^{-2k}]\), no other scalar center has smaller worst-case
deviation. The calculation is audited by
`experiments/theta_pencil/kadec_sampling_threshold.py` and performs no zero
search.

### Proposition 4.7 (max-gap frame improvement)

Let \(L_0=4\pi A_0\), and let \(a_{\mathrm G}=1.8868645429\ldots\) be the
first positive solution of

\[
 \left(1-\left(\frac{aL_0}{\pi}\right)^2\right)
 -\frac12\left(1+\frac{aL_0}{\pi}\right)
  \bigl(\cosh(a/2)-1\bigr)=0.                              \tag{KG1}
\]

Then the sampling inequality (KS2), with a finite defect family and harmless
bounded positive sample weights, and hence the impossibility of the exhaustive
Hermite version of (RTL), hold for every

\[
 \boxed{0<a<a_{\mathrm G}.}                                \tag{KG2}
\]

#### Proof

We first record a self-contained max-gap sampling estimate. Let
\(X=\{x_n\}_{n\in\mathbb Z}\subset\mathbb R\) be increasing with
\(x_{n+1}-x_n\le L\). Divide the real line into the Voronoi cells of the
\(x_n\), write \(w_n\le L\) for the length of the cell of \(x_n\), and let
\(Q_XG\) equal \(G(x_n)\) on that cell. On each half-cell the function
\(G-G(x_n)\) vanishes at one endpoint. The sharp one-endpoint
Poincare--Wirtinger inequality and the Bernstein inequality for \(PW_a\) give

\[
 \|G-Q_XG\|_2\le\frac{L}{\pi}\|G'\|_2
 \le\frac{aL}{\pi}\|G\|_2.                                \tag{KG3}
\]

The same construction supplies the upper sample bound. For the lower bound,
let \(I_XG\) be the piecewise-linear interpolant through consecutive samples.
On \([x_n,x_{n+1}]\), the error \(E=G-I_XG\) has two zero endpoints, its
derivative has mean zero, and \(E''=G''\). The Dirichlet and mean-zero
Poincare inequalities, followed by Bernstein, give

\[
 \|G-I_XG\|_2\le\left(\frac L\pi\right)^2\|G''\|_2
 \le\left(\frac{aL}\pi\right)^2\|G\|_2.                    \tag{KG3a}
\]

Moreover, convexity of the squared modulus on each linear segment gives
\(\|I_XG\|_2^2\le\sum_nw_n|G(x_n)|^2\). Combining this with (KG3), and writing
\(\|Q_XG\|_2^2=\sum_nw_n|G(x_n)|^2\), yields

\[
 \left(1-\left(\frac{aL}{\pi}\right)^2\right)\|G\|_2
 \le\left(\sum_nw_n|G(x_n)|^2\right)^{1/2}
 \le\left(1+\frac{aL}{\pi}\right)\|G\|_2,                 \tag{KG4}
\]

whenever \(aL<\pi\).

By (KS4), for every \(L>L_0\) every sufficiently remote real interval of
length \(L\) contains the ordinate of a zeta zero. Select conjugate spectral
points \(x_n\pm iy_n\), \(|y_n|<1/2\), so that their real parts have gaps at
most \(L\) on both remote half-lines, and insert finitely many artificial real
nodes across the central interval. Apply (KG4) to this augmented real
sequence.

For \(G=\widehat g\), replace the real samples by the paired spectral samples

\[
 P_nG=\frac{G(x_n+iy_n)+G(x_n-iy_n)}2
     =\int_{-a}^a g(t)e^{ix_nt}\cosh(y_nt)\,dt.              \tag{KG5}
\]

Use the centered multiplier \(h_0\) from (KC3), with the common Plancherel
normalization understood. The lower bound in (KG4)
applied to the inverse transform \(h_0g\), together with \(h_0\ge1\), is
\((1-(aL/\pi)^2)\|g\|_2\). For the difference between (KG5) and this centered
reference, expand in even powers. At order \(2k\), the diagonal coefficient
has modulus at most \(2^{-2k-1}\); applying the upper bound in (KG4) to
\(t^{2k}g\) and summing gives

\[
 \left(\sum_nw_n
  |P_nG-\widehat{h_0g}(x_n)|^2\right)^{1/2}
 \le\frac12\left(1+\frac{aL}{\pi}\right)
       \bigl(\cosh(a/2)-1\bigr)\|g\|_2.                    \tag{KG6}
\]

The difference of the two sides of (KG1), with \(L\) in place of \(L_0\),
is therefore a lower frame bound for the paired samples. The first root in
(KG1) lies below the max-gap ceiling
\(\pi/L_0=2.4811433108\ldots\). Letting \(L\downarrow L_0\) proves the bound
for every \(a<a_{\mathrm G}\).

Removing the finitely many artificial central nodes leaves a closed analysis
operator with only a finite-dimensional defect. As in Proposition 4.4, finitely
many genuine spectral derivative evaluations fill that defect, and exhaustive
Hermite cancellation eventually kills them. Finally \(w_n\le L\), and (KP9)
shows

\[
 \sum_n w_n|P_nG|^2
 \le \frac L2\sum_n\bigl(|G(x_n+iy_n)|^2+|G(x_n-iy_n)|^2\bigr), \tag{KG7}
\]

so (RTL) drives the paired weighted tail to zero. This contradicts the lower
frame bound and the fixed normalization \(G(\gamma_0)=i\), exactly as before.
\(\square\)

Unlike Proposition 4.6, this argument does not require a Riesz basis or a
frequency-by-frequency perturbation of a lattice. It uses only the eventual
maximum-gap consequence of the explicit zero count. The scalar constants in
(KG1) are audited by `kadec_sampling_threshold.py`; the theorem itself is the
direct estimate (KG3)--(KG7).

It still leaves \(a_*\ge a_{\mathrm G}\) open. Extending the argument by
packing several value samples into each lattice cell would require uniform
control of distinct, separated spectral points. Riemann--von Mangoldt counts
multiplicity, while (RTL) controls values rather than derivative samples;
known average estimates for high multiplicities do not provide that uniform
local separation.

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
an entry point for understanding parity collisions. Proposition 4.1a shows
that this is precisely the only mixed-parity branch; otherwise the witness is
pure even or pure odd. The separate
[cone no-go](ground-simplicity-cone-no-go.md) proves that ordinary
Beurling--Deny/Perron--Frobenius theory cannot supply simplicity once
\(a>1/2\): the off-diagonal form has a positive open band near separation
one. The remaining gate must use the explicit prime--archimedean formula;
real-rootedness alone is not a contradiction. Proposition 4.2 gives one
fully explicit route into that gate: prove the uniform tail localization
(RTL) for the rational division family. The finite interpolation and every
algebraic cancellation required by that route are already unconditional.
Proposition 4.3 forces superexponential norm growth for any exhaustive
cancellation. Proposition 4.4 gives the first sampling obstruction,
Proposition 4.5 uses conjugate pairs, and the centered refinement in
Proposition 4.6 improves their lattice perturbation. The direct max-gap frame
in Proposition 4.7 rules out the exhaustive Hermite version of (RTL) below
\(a=1.8868645429\ldots\). For larger support the moving infinite tail remains
uncontrolled. Neither that surviving case nor an alternative exclusion is
declared solved here.

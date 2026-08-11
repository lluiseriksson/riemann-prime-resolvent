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

There is also a completeness statement at each *fixed* support.  Write

\[
 L_{a,m}=A_2+R_m+B_a,\qquad L_a=A_2+V+B_a,            \tag{GS8}
\]

where \(B_a\) is the bounded scalar, smooth, and finite prime-translation
part.  Equations (GS2) and (GS7) show that the closed forms of \(L_{a,m}\)
increase to the form of \(L_a\).  The diagonal operator
\(A_2e_n=H_ne_n\), together with the standard bounded-perturbation estimate,
gives compact resolvent.  Monotone convergence of closed forms and the
min--max principle therefore imply

\[
 \boxed{\lambda_k(L_{a,m})\nearrow\lambda_k(L_a)
 \quad(m\to\infty)\qquad(k\ge1).}                   \tag{GS9}
\]

Consequently

\[
 \boxed{L_a\succ0\quad\Longleftrightarrow\quad
 \text{there exists }m\text{ with }L_{a,m}\succ0.}  \tag{GS10}
\]

The reverse implication is the pointwise order; the forward implication
uses \(\lambda_1(L_a)>0\) in (GS9).  Thus the nested resolvents form a
complete terminating certificate hierarchy whenever the fixed-support
operator has a positive gap.  They do not settle a merely semidefinite
zero-ground case, and they do not make the choice of \(m\) uniform as
\(a\to\infty\).  Those two qualifications are precisely why (GS10) is not
RH.

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
 -11.78\quad\text{(even)},\qquad -15.15\quad\text{(odd)}. \tag{GS11}
\]

These are diagnostics, not interval claims, but their scale identifies the
correct architecture: the high-complement theorem is useful only after an
explicit multiband elimination.  Replacing the exact potential globally by
a strict lower polynomial, or charging every high mode at one denominator,
cannot be the final step.

The low spectrum at support one is a cluster rather than a single ground
state.  The appropriate a posteriori test is therefore the following block
Temple lemma.  Let \(V:\mathbb C^k\to\mathcal H\) be an isometry,
\(P=VV^*\), and \(Q=I-P\).  Put

\[
 A=V^*TV,\qquad R=QTV.
\]

If \(QTQ\succeq\beta Q\) with \(\beta>0\), completing the square gives

\[
 \boxed{A-\beta^{-1}R^*R\succ0\quad\Longrightarrow\quad T\succ0.} \tag{GS12}
\]

This treats all small eigenvalues simultaneously and reduces to the usual
one-vector Temple estimate when \(k=1\).  A first diagnostic using the four
lowest vectors of the degree-64 section inside degree 128 gives residual
norms \(1.36\cdot10^{-6}\) (even) and \(1.18\cdot10^{-5}\) (odd).  These are
too large for the observed next-cluster floors.  Extending to degree 256
reduces them only to \(4.12\cdot10^{-7}\) and \(4.61\cdot10^{-6}\).

The slow decay is the known endpoint-jump tail of the prime translations.
Thus an interval pass that merely raises the global Legendre cutoff is not
accepted.  It must retain the endpoint jets explicitly, form their *block*
residual Gram, and bound only the regular remainder.  The generic finite
matrix calculation is implemented in `block_temple.py`; the existing Arb
jet routines already supply the coordinate Gram.  What remains is its
congruence to the trial cluster and the regular non-jet residuals.

No floating orthonormalization is needed in the interval version.  For an
arbitrary injective trial map \(W\), put

\[
 G=W^*W,\qquad A=W^*TW,\qquad K=W^*T^2W.
\]

Projection onto the orthogonal complement of \(\operatorname{ran}W\) gives
the exact residual Gram

\[
 W^*T(I-WG^{-1}W^*)TW=K-AG^{-1}A.                  \tag{GS13}
\]

Therefore (GS12) is equivalently the finite generalized test

\[
 \boxed{A-\beta^{-1}(K-AG^{-1}A)\succ0.}           \tag{GS14}
\]

All entries in (GS14) can be enclosed directly for dyadic trial vectors.
The already implemented combined-prime jet correction is a Gram before any
triangle inequality, so congruencing it by the same trial matrix retains the
interference between different prime powers and different endpoint jets.

The next non-circular target is therefore to keep (GS3) as an auxiliary Gram
block and combine it with the signed prime translations inside the same
multiband Schur calculation.  A threshold-uniform factorization of that
combined block would be a genuine route beyond the isolated certificates at
support 0.70 and 0.72.  Merely asserting its positivity would again rename
the localized Weil criterion and hence RH.

## Allocating the exact potential lowers the support-one tail to degree 99

The first such combination already improves the common complement
substantially.  Split the exact boundary potential using the rational weights

\[
 \theta_5=\frac{173}{500},\qquad
 \theta_7=\frac{327}{500},\qquad \theta_5+\theta_7=1. \tag{GS15}
\]

For \(n=5,7\), the displacement \(h_n=\log n\) is larger than one, so every
nontrivial residue fiber has two vertices.  If the left vertex is \(x\), then

\[
 x\in[-1,1-h_n],\qquad |x|,|x+h_n|\ge h_n-1.
\]

Since \(V\) increases with \(|x|\), the two-vertex matrix obeys

\[
 \begin{pmatrix}
 \theta_nV(x)&-\Lambda(n)/\sqrt n\\
 -\Lambda(n)/\sqrt n&\theta_nV(x+h_n)
 \end{pmatrix}
 \succeq
 \left(\theta_nV(h_n-1)-\frac{\Lambda(n)}{\sqrt n}\right)I. \tag{GS16}
\]

One-vertex fibers contribute a nonnegative diagonal.  Therefore the global
floor is the minimum of zero and the scalar in (GS16).  At the registered
weights,

\[
 \theta_5V(\log5-1)-\frac{\log5}{\sqrt5}
 =-0.6394414991\ldots,
\]

whereas

\[
 \theta_7V(\log7-1)-\frac{\log7}{\sqrt7}
 =+0.0007159957\ldots.                              \tag{GS17}
\]

Thus the prime-seven translation costs no negative floor.  Leaving zero
potential for \(2,3,4\), their exact path spectra give respectively

\[
 -\log2,\qquad-\frac{\log3}{\sqrt3},\qquad
 -\frac{\log2}{2}.                                  \tag{GS18}
\]

With smooth order 95, the analytic smooth loss is
\(0.4414940136\), and the bounded-part floor becomes

\[
 B_1\succeq-5.1700331154\,I.                        \tag{GS19}
\]

Since \(H_{99}=5.1773775176\ldots\), this yields the design margin

\[
 \boxed{Q_{99}L_1Q_{99}\succeq0.0073444022\,Q_{99}.} \tag{GS20}
\]

The derivation (GS15)--(GS20) is analytic and uses no zero data.  The decimal
closure is wired to the existing source-level Arb chain verifier by
`support_one_allocated_floor.py`; that interval run remains required before
the displayed decimal is promoted from a design margin to a deposited
certificate.  Even at design level, the reduction from tail degree 256 to 99
is robust and changes the cost of the finite source and endpoint jets by a
large factor.

## The commensurate dyadic block lowers the tail further to degree 85

The preceding estimate still paid the prime powers 2 and 4 separately.  This
throws away the exact relation between their displacements,

\[
 h_4=\log4=2\log2=2h_2.                              \tag{GS21}
\]

Fiber both translations over residues modulo \(h_2\).  Since
\(2<3h_2\), every fiber inside \([-1,1]\) has two or three vertices.  On a
three-vertex fiber the joint prime matrix is

\[
 \begin{pmatrix}
 0&-a&-b\\ -a&0&-a\\ -b&-a&0
 \end{pmatrix},\qquad
 a=\frac{\log2}{\sqrt2},\quad b=\frac{\log2}{2}.     \tag{GS22}
\]

The antisymmetric eigenvalue is \(b\).  On the symmetric subspace the matrix
is

\[
 \begin{pmatrix}-b&-\sqrt2a\\-\sqrt2a&0\end{pmatrix},
\]

so its least eigenvalue is

\[
 \lambda_-=-\frac{b+\sqrt{b^2+8a^2}}2
 =-\frac{\log2}{4}(1+\sqrt{17}).                    \tag{GS23}
\]

The two-vertex fibers have least eigenvalue \(-a\), which is larger than
\(\lambda_-\).  Thus (GS23) is the exact global joint floor.  Compared with
the former sum \(-\log2-\log2/2\), it gains

\[
 \frac{\log2}{4}(5-\sqrt{17})
 =0.1519542158\ldots.                               \tag{GS24}
\]

Keeping the allocations (GS15) for 5 and 7, the bounded-part floor improves
to

\[
 B_1\succeq-5.0180788996\,I.                        \tag{GS25}
\]

Now \(H_{84}+B_1<0\), whereas

\[
 \boxed{Q_{85}L_1Q_{85}\succeq
 0.0076588408\,Q_{85}.}                             \tag{GS26}
\]

This second reduction, from 99 to 85, is not a numerical optimization: it is
an exact diagonalization of the commensurate residue graph.  The registered
Arb entry point now combines this exact dyadic block with the source-level
chain certificates for 3, 5, and 7.  As before, the interval run is required
before the displayed decimal is called a deposited certificate.

## A joint 5--7 path gives a rational tail at degree 58

The allocation (GS15) is still separable and therefore pays incompatible
worst fibers for the translations 5 and 7.  At support one, however, both
displacements exceed one.  Put

\[
 h_5=\log5,\qquad h_7=\log7,\qquad \delta=h_7-h_5. \tag{GS27}
\]

For a left vertex \(x\in[-1,1-h_7]\), the whole connected component is the
four-vertex path

\[
 x+h_5\;\xleftrightarrow{c_5}\;x
 \;\xleftrightarrow{c_7}\;x+h_7
 \;\xleftrightarrow{c_5}\;x+\delta,
 \qquad c_n=\frac{\log n}{\sqrt n}.                 \tag{GS28}
\]

The remaining nontrivial components are prime-5 edges parameterized by

\[
 x\in[1-h_7,\delta-1],                              \tag{GS29}
\]

and every other point is isolated.  Thus the incommensurability of
\(h_5,h_7\) causes no infinite fiber here: the large displacements and the
finite support force components of size at most four.

Adding the full boundary potential to the diagonal of (GS28), an initial
double-precision scan placed the least value at the symmetric parameter
\(x=-h_7/2\):

\[
 \lambda_{5,7}^{(4)}=-0.2624003509\ldots.           \tag{GS30}
\]

The two-path family has its observed minimum at \(x=-h_5/2\), equal to
\(-0.1983071999\ldots\).  These values only selected the pre-registered
judge

\[
 \boxed{V+T_5+T_7\succeq-0.267\,I.}               \tag{GS31}
\]

The judge has now closed without interval-library dependencies.  Use the
positive rational expansions

\[
 \log n=2\sum_{k\ge0}\frac{y_n^{2k+1}}{2k+1},
 \quad y_n=\frac{n-1}{n+1},
 \qquad
 V(z)=\frac12\sum_{k\ge1}\frac{z^{2k}}k.           \tag{GS31a}
\]

For each logarithm, 96 terms and the geometric tail give rational lower and
upper bounds.  Divide the two parameter intervals into 64 cells, use 80
positive terms of the second series for every diagonal lower bound, and
round the edge weights upward using integer lower bounds for
\(\sqrt5,\sqrt7\).  After adding \(267/1000\) to the diagonal, the exact
rational leading-minor lower bounds are

\[
\begin{array}{c|rrrr}
\text{four-path}&0.4991416659&0.2564815762&0.3377131466&0.0015294320\\
\text{two-path}&0.5571495667&0.0957605698&&
\end{array}                                        \tag{GS31b}
\]

and are all strictly positive.  These are symmetric Z-matrices.  If an
actual edge is smaller or an actual diagonal larger than the rational worst
matrix, its ground-state Rayleigh quotient on a nonnegative Perron vector
can only increase.  Sylvester's criterion applied to (GS31b) therefore
proves (GS31).  The executable proof is
`rational_joint_five_seven_certificate.py`; its integer fixed-point series
and final `Fraction` determinants contain no sampled or floating value.  The
Arb implementation in `joint_five_seven_floor.py` remains as an independent
cross-check, not as a logical dependency.

The remaining constants can be enclosed rationally as well.  The Machin
formula and alternating arctangent series enclose \(\pi\); (GS31a) encloses
\(\log(2\pi)\); and the elementary inequality

\[
 \frac1{2n+1}<H_n-\log n-\gamma
\]

at \(n=100\) gives a rational upper bound for Euler's constant.  The
Bernoulli-polynomial majorant already used for the smooth kernel is rational,
as are `isqrt` enclosures of \(\sqrt3\) and \(\sqrt{17}\).  Combining these
with (GS23), the prime-3 edge, and (GS31) yields

\[
 B_1\succeq-4.6456539428\,I,
 \qquad
 \boxed{Q_{58}L_1Q_{58}\succeq
 0.0006006509\,Q_{58}.}                            \tag{GS32}
\]

The same exact calculation gives the degree-57 margin
\(-0.0166407283\ldots<0\), so degree 58 is the first cut closed by this
certificate.  Equation (GS32) is unconditional, uses no zeta-zero data, and
turns support-one positivity into a finite 58-mode source obligation.  It is
not RH: it closes only the infinite complement at one fixed support; the
finite source and support-uniform continuation remain separate obligations.

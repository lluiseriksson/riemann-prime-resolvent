# A cut-adapted basis for the first prime window

## The obstruction it removes

At \(a=1/2\), the global Legendre Schur certificate has the correct finite
inertia, but its endpoint-jet tail fails.  If \(d\) low modes are retained
and the jet expansion starts at \(N\), its conditioning is governed by
roughly \(d^2/N\).  The required coercive cutoff is already \(d\simeq512\),
while the existing exact block ends at \(N=4096\); hence \(d^2/N\simeq64\),
far outside the asymptotic regime.  Raising the jet order magnifies rather
than repairs the error.

The moving prime cut should therefore be represented exactly, not estimated
as a tail.

## Exact decomposition

Throughout the first prime window

\[
 \frac{\log2}{2}<a\le\frac12,
 \qquad h=\frac{\log2}{a}\in[2\log2,2),
\]

only the prime power 2 is active.  Put \(c=1-h<0\) and split

\[
 [-1,1]=I_-\cup I_0\cup I_+,
 \quad I_-=[-1,c],\quad I_0=[c,-c],\quad I_+=[-c,1].
\]

Translation by \(h\) maps \(I_-\) bijectively and isometrically onto
\(I_+\).  Choose equally normalized Legendre bases
\(e_m^-\) and \(e_m^+\) in the two edge intervals, using the same affine
coordinate, and any orthonormal basis in \(I_0\).  Then

\[
 \langle e_m^+(\cdot+h),e_n^-\rangle=\delta_{mn}.
\]

Consequently the symmetrized prime translation and its contribution to the
Weil--Suzuki operator are exactly

\[
 T_h=\begin{pmatrix}0&0&I\\0&0&0\\I&0&0\end{pmatrix},
 \qquad
 P_2=-\frac{\log2}{\sqrt2}T_h.
\]

In the edge-symmetric and edge-antisymmetric combinations

\[
 e_m^{\pm}=\frac{e_m^-\pm e_m^+}{\sqrt2},
\]

this is diagonal, with eigenvalues respectively
\(-\log2/\sqrt2\) and \(+\log2/\sqrt2\); the center block has eigenvalue
zero.  There is no endpoint series, no prime tail, and no Gibbs correction.

Piecewise polynomials belong to \(H^{\log}(-1,1)\): their Fourier transforms
decay as \(O(|\xi|^{-1})\), so the logarithmically weighted square remains
integrable.  The basis is therefore inside the closed form domain even though
individual vectors may jump at the internal cuts.

## What moves to the next column

The price is that the scale-free logarithmic operator \(\mathcal L\) is no
longer diagonal.  The next finite-source calculation must evaluate its three
by three interval block matrix and prove a tail bound in local polynomial
degree.  This is preferable to the old architecture: the only discontinuous
arithmetic block is now exact, while the remaining cross-interval kernel
\(|x-y|^{-1}\) is source-independent and has fixed sign.

The executable module
`experiments/theta_pencil/cut_adapted_prime_basis.py` constructs the exact
prime block and its orthogonal diagonalizing transform.  It is the active
architecture for extending the localized theorem to \(a=1/2\).

The source calculation is no longer quadrature based.  The module
`arb_cut_dominant.py` evaluates every diagonal interval block from the closed
Legendre matrix and every off-diagonal block from the exact moments

\[
 \int_0^A\!\int_0^B\frac{u^p v^q}{D+u+v}\,du\,dv.
\]

The companion `arb_cut_smooth.py` evaluates each retained power
\(|x-y|^p\) by beta and multinomial identities.  Finally,
`arb_cut_source.py` assembles the scalar and exact prime block and performs
the reflection-parity reduction inside Arb.  No floating endpoint is fed
back into the proof: all three interval lengths are reconstructed as Arb
expressions in \(\log2/a\).

## Certified Temple half of the endpoint calculation

The improved smooth action was evaluated in Arb by retaining all polynomial
output modes through degree 280 and bounding only the analytic series
remainder.  Conditional on parity second-eigenvalue floors \(0.3\) (odd) and
\(0.01\) (even), the resulting Kato--Temple lower bounds at \(a=1/2\) are

\[
 \lambda_1^{\rm odd}\ge1.907386565208246\cdot10^{-4},
 \qquad
 \lambda_1^{\rm even}\ge5.524591896323604\cdot10^{-7}.
\]

These are certified conditional implications, not yet a positivity theorem
at \(a=1/2\).  The cut-adapted Schur calculation must still prove the two
displayed second-eigenvalue floors.

## Endpoint comparison and cut-basis Schur reduction

At \(a=1/2\), pair the two translated edge points and put

\[
 V(x)=-\tfrac12\log(1-x^2),\qquad
 m=V(\log2)-\frac{\log2}{\sqrt2}=-0.162730057875794\ldots .
\]

An interval proof verifies

\[
 \begin{pmatrix}V(x)&-\log2/\sqrt2\\
 -\log2/\sqrt2&V(x+2\log2)\end{pmatrix}\succeq mI
\]

throughout the translated edge.  The shifted determinant is even about the
midpoint.  Its second derivative is at least \(1.8035\) on
\([0,3/10]\), while monotonicity supplies a determinant margin \(0.3221\)
on the remaining endpoint interval.  This is implemented in
`support_05_comparison.py`.

The same module proves the smooth-kernel lower bound

\[
 S_{1/2}\succeq-0.057894445561 I.
\]

Here the constant power is positive semidefinite, the power-two kernel has
least eigenvalue \(-4/3\), and the remaining powers use their exact Schur
integrals.  Combining these estimates with the global Legendre spectrum
of \(A_2\) gives unconditional third-eigenvalue floors

\[
 \lambda^{\rm even}_3\ge0.140763279145,
 \qquad
 \lambda^{\rm odd}_3\ge0.340763279145.
\]

Arb finite sections of local degree \(8,12,16,20\) have exactly one eigenvalue below
the desired shifts \(0.01\) (even) and \(0.3\) (odd), with no unresolved
interval eigenvalues.  More importantly, the complement of the local
degree-16 space is orthogonal to every *global* Legendre polynomial of degree
below 16.  The comparison above therefore gives the genuine complement
floor

\[
 Q_{16}A_{1/2}Q_{16}\succeq1.438158939041\,Q_{16}.
\]

This makes the correct object a full finite-dimensional Schur complement,
not a heuristic two-vector inclusion.  Eliminating degrees 16--39 with that
floor and degrees 40--63 with their stronger harmonic floor leaves exactly
one negative direction.  The first positive Schur values are approximately
$0.0079936$ (even) and $0.0627477$ (odd).

Above degree 64 the leading term is explicit and low rank.  If
$g=\mathcal Lf$ on a local interval and

\[
 F_\pm=\lim_{t\to\pm1}(1-t^2)g'(t),
\]

then integration by parts gives

\[
 \widehat g_n=
 \frac{\sqrt{(2n+1)/2}}{n(n+1)}
 \bigl(F_+-(-1)^nF_-\bigr)
 +\frac{\widehat{Dg}_n}{n(n+1)}.
\]

The six fluxes are just endpoint values and jumps of the degree-16 trial
space.  Adding their infinite Gram matrix still leaves one negative
direction, with positive margins $0.0079925$ and $0.0627366$.  This is
not yet the endpoint theorem: the remaining regularized tail
\(\widehat{Dg}_n/[n(n+1)]\) must be bounded.  The current Schur margins allow
operator-norm bounds about $0.149$ (even) and $0.396$ (odd) on that final
tail.  The rectangular Arb source in `arb_cut_dominant_cross.py` isolates
precisely this universal obligation.  Prime, scalar and the retained smooth
series contribute no modes beyond local degree 40.

The rectangular source through degree 128 was independently evaluated at
3072-bit precision; all exported radii were below floating-point underflow.
This does **not** by itself permit the degree-128 harmonic floor in the final
Schur denominator: local degree bands are not reducing subspaces for the
global operator $A_2$.  Without a separately proved nested Schur estimate,
the common complement floor remains $1.4381589$.  Reserving an even Schur
margin $0.007$, Green's identity therefore requires

\[
 \|f\mapsto D(\mathcal Lf)\|<1650.97.
\]

The diagnostic partial norms through degree 128 are $206.1$ and $216.9$,
respectively, but those figures are not substituted for the missing global
upper bound.  The gate calculation is implemented in
`regularized_tail_gate.py`.

## A first regularized-tail bound

The common bound can in fact be proved without quadrature.  On one local
interval, write $D=-\partial_t(1-t^2)\partial_t$.  For polynomials of degree
below 16, Arb certifies

\[
 \|D A_2\|<797,\qquad
 \|V D\|_{\rm HS}<506,qquad
 \|-2t\partial_t-I\|_{\rm HS}<246.
\]

The middle estimate uses the exact beta-derivative moments

\[
 \int_{-1}^1t^{2k}\log^2(1-t^2)\,dt
 =\left.\partial_b^2B(k+\tfrac12,b)\right|_{b=1};
\]

thus the cancellation between the two endpoint logarithms is retained.
Since

\[
 D(Vf)=V(Df)-2tf'-f,
\]

the diagonal interval block is bounded by 1549.

For touching intervals of lengths $A,B$, put
$r=[A(1-t)+B(1+s)]/2$.  Direct differentiation gives

\[
 (D_t-D_s)r^{-1}
 =-4(A+B)\,\partial_v\frac{v}{(Au+Bv)^2},
 \quad u=1-t,\ v=1+s.
\]

After integration by parts, the first term is the source Legendre operator,
the shared-endpoint term is exactly the flux already retained, and the
regular commutator has Mellin norm at most
$(A+B)\pi/(2B)$.  Arb certifies
$\|\partial_t\|<87$, the remaining endpoint trace costs less than 10, and
the entire adjacent block is below $695.084<697$.  The separated edge
block has Hilbert--Schmidt norm below $0.441<1$.

The scalar three-interval comparison matrix therefore yields

\[
 \|f\mapsto D(\mathcal Lf)\|
 <1549+\sqrt2\,697+1
 <2535.707<2577.355.
\]

For the final Green remainder, however, the required map is
$Q_{128}D\mathcal LP_{16}$ rather than the full $D\mathcal LP_{16}$.  After
subtracting the endpoint fluxes, the self-interval coefficients are exactly

\[
 d_{nm}=\sqrt{(2n+1)(2m+1)}
 \frac{m(m+1)}{n(n+1)-m(m+1)},
 \qquad n>m,\quad n\equiv m\pmod2.
\]

An explicit Arb sum through degree 4095 followed by an elementary
$n^{-3}$ square-tail bound gives

\[
 \|Q_{128}D\mathcal L_{\rm self}P_{16}\|<13.093<14.
\]

Keeping the deliberately unsharpened adjacent and separated estimates then
yields

\[
 \|Q_{128}D\mathcal LP_{16}\|
 <14+\sqrt2\,697+1
 <1000.707<1650.962.
\]

Thus `arb_regularized_map_bound.py` now closes the corrected common-floor
regularized-tail gate.  No nested-band denominator is used.  What remains
before claiming positivity at $a=1/2$ is to assemble the degree-128 finite
source, the infinite flux Gram and this tail correction in one interval
inertia computation.

## Beyond one half: the second Green gate

The same cut architecture and analytic remainder are now valid throughout
the prime-two-only window.  They prove $A_{0.51}>0$, but the common-floor
certificate becomes too lossy near $a=0.54$.  A 1024-bit component diagnostic
at that point gives, in the even sector,

| component | effect relevant to the low Schur matrix |
|---|---:|
| raw second finite eigenvalue | $0.002192746$ |
| explicit degrees 16--127 plus endpoint flux | leaves about $0.002187$ |
| regularized scalar correction | $0.00568798 I$ |

Thus the finite middle band is not the obstruction.  The loss comes from
using the norm of the *whole* touching-interval map to control only
$Q_{128}D\mathcal LP_{16}$.  With the common floor $1.285048$, a target shift
$0.0011$ requires the regularized map bound to fall from the present value
about $998.3$ to below roughly $435$.

The first explicit coefficients after subtracting the six Green fluxes are
small and decay numerically like $n^{-3/2}$: for one edge block their row
norms are $2.176$ at $n=128$, $1.560$ at $n=160$, and $1.118$ at $n=200$.
These are diagnostics, not interval bounds.  Past degree 200 the direct
moment recurrence loses cancellation at 1024 bits and its midpoints must not
be used.

The next analytic obligation is therefore precise: apply Green once more to
the regularized adjacent-block image, retain its endpoint trace as another
finite-rank flux Gram, and bound the twice-regular remainder.  This targets
the measured loss directly and avoids treating local degree bands as reducing
subspaces.

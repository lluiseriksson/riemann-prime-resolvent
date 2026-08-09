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

## Endpoint comparison and two-vector cluster reduction

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

Thus only a two-vector cluster remains in either parity sector.  Arb finite
sections of local degree \(8,12,16,20\) have exactly one eigenvalue below
the desired shifts \(0.01\) (even) and \(0.3\) (odd), with no unresolved
interval eigenvalues.  For the degree-16 two-vector Ritz spaces, the
partial residual through local degree 64 gives corrected positive margins
approximately \(0.00778\) and \(0.05654\), respectively.

This last statement is deliberately not yet a certificate: the norm of the
dominant residual above degree 64 remains to be bounded.  The rectangular
Arb source in `arb_cut_dominant_cross.py` isolates precisely that universal
tail.  Prime, scalar and the retained smooth series contribute no modes
beyond local degree 40.

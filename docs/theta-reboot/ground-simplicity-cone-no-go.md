# Why ordinary Perron--Frobenius does not prove ground-state simplicity

## Claim boundary

This note closes one tempting way of eliminating the multiple first-crossing
branch. It does not show that the localized Weil ground state is multiple, and
it does not rule out a different proof of simplicity.

Let \(Q_W^a\) be Suzuki's closed localized Weil form. If RH were false, the
certified first-crossing reduction gives \(a_*>0.72\),
\(Q_W^{a_*}\succeq0\), and \(0\in\operatorname{spec}(A_{a_*})\). A standard
route to simplicity would be to prove that the semigroup of a scalar shift of
\(A_a\) is positivity improving and then apply Perron--Frobenius. The required
positivity-preserving property already fails for every \(a>1/2\).

## Proposition

For every \(a>1/2\), there are nonzero, nonnegative, smooth functions
\(f,g\in C_c^\infty(-a,a)\) with disjoint supports such that

\[
 Q_W^a(f,g)>0.                                                \tag{PF1}
\]

Consequently no scalar shift of \(Q_W^a\) satisfies the first
Beurling--Deny criterion in the ordinary cone of \(L^2(-a,a)\), and its
semigroup is not positivity preserving.

## Proof

Away from the prime-translation diagonals, the off-diagonal kernel in the
explicit Suzuki decomposition is

\[
 k(t)=-\frac1{2|t|}-r''(|t|),                                 \tag{PF2}
\]

where

\[
 r''(t)=-e^{t/2}-e^{-t/2}
 +\frac{e^{-t/2}}{1-e^{-2t}}-\frac1{2t}.                      \tag{PF3}
\]

At \(t=1\), the two singular terms cancel and

\[
 k(1)=e^{1/2}+e^{-1/2}-\frac{e^{-1/2}}{1-e^{-2}}
 =\frac{1-e^{-2}-e^{-3}}{e^{-1/2}(1-e^{-2})}>0.               \tag{PF4}
\]

The last sign is elementary: \(e>2\) gives
\(e^{-2}+e^{-3}<1/4+1/8<1\). By continuity, \(k(t)>0\) on a
small open interval \(I\) about \(1\). Shrink \(I\), if necessary, so that
it contains no \(\log n\) with \(n\ge2\); this is possible because the set of
active prime-power translations is discrete and
\(1\notin\{\log n:n\in\mathbb N\}\).

Choose nonnegative bumps \(f,g\) concentrated respectively near
\(-1/2\) and \(1/2\), with every difference between their supports in
\(I\). These supports lie in \((-a,a)\). The scalar and boundary-potential
terms have zero mixed pairing because the supports are disjoint. Every prime
translation also has zero mixed pairing by the choice of \(I\). The regional
logarithmic form and the smooth convolution combine exactly into (PF2), so

\[
 Q_W^a(f,g)=\iint k(x-y)f(y)g(x)\,dy\,dx>0,
\]

proving (PF1).

For a lower-bounded closed real symmetric form, positivity preservation of
the shifted semigroup requires
\(q(f,g)\le0\) whenever \(f,g\ge0\) have disjoint supports. A scalar shift
does not change such a mixed pairing, so (PF1) violates the criterion for
every shift. \(\square\)

## No diagonal sign-gauge repair

The obstruction cannot be removed by multiplying functions by a pointwise
real sign. Since \(r''(0)=-7/4\), (PF2) is strictly negative for all
sufficiently small \(t>0\). If a sign \(\sigma(x)\in\{\pm1\}\) made
\(\sigma(x)\sigma(y)k(x-y)\le0\) almost everywhere, these short negative
edges would force \(\sigma\) to be locally constant and hence constant on the
connected interval. The positive edge near distance one would then remain
positive. The same local argument rules out a diagonal complex phase gauge:
short edges force the phase to be constant.

## Consequence for the RH programme

At the hypothetical first crossing \(a_*>0.72\), ordinary cone
irreducibility cannot be invoked to prove that \(\ker A_{a_*}\) is
one-dimensional. A surviving simplicity proof must use oscillation,
extension theory, parity comparison, or an operator-specific nodal theorem;
it cannot be a generic positivity-improving-semigroup argument.

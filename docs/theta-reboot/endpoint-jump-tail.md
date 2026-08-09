# Endpoint-jump decomposition and a Temple route

## The prime tail is rank two at leading order

At \(a=0.4\), only the prime power \(2\) is active. Put

\[
 h=\frac{\log2}{a},\qquad b=1-h,\qquad c=\frac{\log2}{\sqrt2}.
\]

For a polynomial \(f\), the prime translation applied on \((-1,1)\) is

\[
 (T_pf)(x)=-c\left(
  1_{[-1,b]}(x)f(x+h)+1_{[-b,1]}(x)f(x-h)
 \right).
\]

Its only discontinuities have sizes \(c f(1)\) at \(b\) and
\(-c f(-1)\) at \(-b\). Hence it splits canonically as

\[
 T_pf=J_f+R_f,
\]

where

\[
 J_f=-cf(1)1_{[-1,b]}-cf(-1)1_{[-b,1]}
\]

contains both jumps and \(R_f\) is continuous and piecewise polynomial. As a
map from the finite low space, \(f\mapsto J_f\) has rank at most two. Bounding
the whole prime tail by its norm obscures exactly this fact.

The normalized Legendre coefficient of a left step is explicit:

\[
 \left\langle1_{[-1,b]},e_n\right\rangle
 =\sqrt{\frac{2n+1}{2}}
 \frac{P_{n+1}(b)-P_{n-1}(b)}{2n+1}.
\]

Wang's sharp Bernstein inequality

\[
 (1-x^2)^{1/4}|P_n(x)|
 <\sqrt{\frac2\pi}\,(n+1/2)^{-1/2}
\]

therefore gives, for jumps of total absolute size \(J\) at cuts satisfying
\((1-c_j^2)^{1/4}\ge w\),

\[
 \left(\sum_{n\ge N}|\widehat J_n|^2\right)^{1/2}
 \le \sqrt{\frac8{3\pi}}\frac{J}{w\sqrt{N-1}}.
\tag{J}
\]

This slow \(N^{-1/2}\) tail is not discarded: its two coefficient vectors can
be accumulated explicitly in the Schur complement. Formula (J) bounds only
the final uncomputed remainder.

## The continuous remainder gains a full power

After removal of the steps, \(R_f\) is absolutely continuous and \(R_f'\) is
of bounded variation. The \(m=1\) case of Wang's theorem, converted from the
usual Legendre coefficient to the orthonormal coefficient, is

\[
 |\langle R_f,e_n\rangle|
 \le
 \sqrt{\frac2{2n+1}}
 \frac{2V_1(R_f)}{\sqrt{\pi(2n-3)}(n-1/2)}.
\]

The elementary square-sum consequence used by the checker is

\[
 \left(\sum_{n\ge N}|\langle R_f,e_n\rangle|^2\right)^{1/2}
 \le\frac{4V_1(R_f)}{\sqrt{3\pi}(N-1)^{3/2}}.
\tag{R}
\]

Thus the non-summable-looking translation tail is exactly a rank-two step
tail plus an \(N^{-3/2}\) norm remainder.

The split iterates. Subtract at each internal cut the first \(r+1\) Taylor
jets of the translated polynomial. The retained part is a sum of truncated
monomials and, as a map from the low space, has rank at most \(2(r+1)\). The
remainder and its first \(r\) derivatives match across the cuts. Applying
Wang's theorem with \(m=r+1\) gives

\[
 \left(\sum_{n\ge N}|\widehat R_n|^2\right)^{1/2}
 \le
 \frac{2^{m+1}V_m(R)}
 {\sqrt{\pi(2m+1)}(N-1)^{m+1/2}},
 \qquad N\ge2m+1.
\tag{RJ}
\]

Thus any fixed finite low block admits an arbitrarily high algebraic tail
rate while only finitely many endpoint-jet directions are added explicitly.
This is the mechanism needed to certify the second-eigenvalue floor; it is not
available to a scalar operator-norm estimate.

## The boundary potential has signed endpoint moments

For a polynomial \(f=\sum_{m<D}u_me_m\), the exact matrix from the preceding
note gives, for \(n\ge D\),

\[
 \langle Vf,e_n\rangle
 =\sqrt{2n+1}\sum_{m<D\atop m+n\text{ even}}
 \frac{u_m\sqrt{2m+1}}{n(n+1)-m(m+1)}.
\]

Expanding the denominator in powers of \(m(m+1)/[n(n+1)]\) preserves the
signed moments. The first one is

\[
 \sum_{m<D}u_m\sqrt{2m+1}=\sqrt2 f(1)
\]

in the even block (and the analogous pair of endpoint traces without a parity
restriction). This explains why the actual potential tail is small for the
computed ground vector even though an absolute coefficient bound is useless.

## A posteriori positivity budget

For a normalized trial vector \(\phi\), let

\[
 \mu=\langle A_a\phi,\phi\rangle,\qquad
 \varepsilon=\|(A_a-\mu)\phi\|.
\]

If an independent inertia certificate proves that the second spectral point
is at least \(\beta>\mu\), Kato--Temple gives

\[
 \lambda_1(A_a)\ge\mu-\frac{\varepsilon^2}{\beta-\mu}.
\tag{KT}
\]

At \(a=0.4\), a 512-mode diagnostic gives

\[
 \mu=1.8126574\cdot10^{-4},\qquad
 \lambda_2^{\rm Ritz}=1.4705371\cdot10^{-2}.
\]

The directly accumulated residual from modes \(512\) through \(8191\), before
interval inflation, is \(2.1421\cdot10^{-4}\). The two analytic tail tools are
deliberately conservative:

- the prime continuous-remainder variation is \(V_1\approx196.76\), giving
  \(3.46\cdot10^{-4}\) from (R) beyond mode 8191;
- the two jumps give about \(1.4\cdot10^{-4}\) from (J);
- the exact signed-moment bound for the logarithmic potential contributes
  only \(2.45\cdot10^{-6}\).

The smooth convolution has no comparable tail problem. The cusp in the even
kernel gives, distributionally,

\[
 (K_a\phi)''(x)=\frac{a^2}{24}\phi(x)
 -a^3\int_{-1}^1r''''(a|x-y|)\phi(y)\,dy.
\]

The required derivative estimate is elementary and unconditional. Write

\[
 r''(t)=-2\cosh(t/2)+h(t),\qquad
 h(t)=\frac{e^{t/2}}{2\sinh t}-\frac1{2t}.
\]

The Bernoulli-polynomial generating function gives

\[
 h(t)=\sum_{n\ge1}\frac{B_n(3/4)2^{n-1}}{n!}t^{n-1}.
\]

For \(n\ge2\), the Fourier series of \(B_n\) and
\(\zeta(n)\le\zeta(2)<2\) imply
\[
 |B_n(3/4)|\le\frac{4n!}{(2\pi)^n}.
\]
Consequently, for \(0\le t\le4/5\),
\[
 |h''(t)|
 \le\frac4{\pi^3(1-t/\pi)^3}
 <\frac4{27(11/15)^3}<0.376.
\]
Also \(\cosh(2/5)<11/10\), directly from
\(e^{2/5}<3/2\) and \(e^{-2/5}<7/10\). Therefore
\[
 \boxed{|r''''(t)|<0.926<1\qquad(0\le t\le4/5).}
\]

It follows that for a unit vector and \(a=0.4\), the smooth image has
weighted variation \(V_1(K_a\phi)<0.23\); formula (R) makes its tail beyond
mode 8191 less than \(4.1\cdot10^{-7}\). Direct high-precision evaluation,
used only as a check, gives the much tighter range
\(0.5623<|r''''(t)|<0.5790\).

Even the triangle sum of these deliberately inflated terms remains below the
Kato--Temple positivity budget

\[
 \sqrt{\mu(0.005-\mu)}\approx9.35\cdot10^{-4}.
\]

This is not yet a theorem: \(\beta=0.005\) must be a certified lower bound for
the second eigenvalue and all finite quantities must be outward-rounded. It is
nevertheless a viable
certificate design with a factor-of-order-one margin. The previous uniform
Schur estimate had the wrong structure and a margin of the wrong sign.

## Parity-resolved inertia budget

The operator commutes with reflection. Numerically, its ground state is even
and its second state is odd. For the shifted operator \(A_{0.4}-0.005I\), it
therefore suffices to prove:

1. the odd block is positive;
2. the even block has at most one negative direction.

The diagonal tail majorant was recomputed with 88 low Legendre modes, all
potential and prime coefficients through mode 4095, the smooth coefficients
through mode 511, and six endpoint jets through mode \(10^6\). The remaining
tails use only the proved Wang, potential-moment, and smooth-kernel bounds.

| parity | first three Schur eigenvalues after explicit jets | omitted-tail correction | safe floating margin |
|:---:|:---|---:|---:|
| even | \(-0.00481952,\ 0.30131077,\ 0.90142760\) | \(0.00686116\) | \(0.2944496\) on the second eigenvalue |
| odd | \(0.00966744,\ 0.89305309,\ 1.30022835\) | \(0.00722599\) | **\(0.00244145\)** on the first eigenvalue |

The omitted-tail correction already includes cross terms. If \(J\) is the
explicit jet tail and \(E\) is the sum of all remaining weighted tails, then

\[
 \|(J+E)(J+E)^*-JJ^*\|
 \le2\|J\|\,\|E\|+\|E\|^2.
\]

For the odd block, the explicit jet correction has norm \(0.01008323\), while
the combined omitted weighted norm is \(0.03114922\). These figures produce
the displayed \(0.00722599\) inflation.

Thus every *analytic* infinite-tail obligation needed for
\(\lambda_2(A_{0.4})\ge0.005\) now fits inside a positive margin. What remains
is finite and mechanical but indispensable: recompute the 44-by-44 parity
matrices, the polynomial Gauss rules, and the six-jet recurrence with outward
rounding, then verify the two matrix inertias by interval \(LDL^*\).
Until that calculation is deposited, \(0.00244145\) is a design margin, not a
certified eigenvalue bound.

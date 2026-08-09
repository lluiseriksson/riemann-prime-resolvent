# Endpoint-jump decomposition and a Temple route

## The prime tail is rank two at leading order

At (a=0.4), only the prime power (2) is active. Put

\[
 h=\frac{\log2}{a},\qquad b=1-h,qquad c=\frac{\log2}{\sqrt2}.
\]

For a polynomial (f), the prime translation applied on ((-1,1)) is

\[
 (T_pf)(x)=-c\left(
  1_{[-1,b]}(x)f(x+h)+1_{[-b,1]}(x)f(x-h)
 \right).
\]

Its only discontinuities have sizes (c f(1)) at (b) and
(-c f(-1)) at (-b). Hence it splits canonically as

\[
 T_pf=J_f+R_f,
\]

where

\[
 J_f=-cf(1)1_{[-1,b]}-cf(-1)1_{[-b,1]}
\]

contains both jumps and (R_f) is continuous and piecewise polynomial. As a
map from the finite low space, (f\mapsto J_f) has rank at most two. Bounding
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

therefore gives, for jumps of total absolute size (J) at cuts satisfying
((1-c_j^2)^{1/4}\ge w),

\[
 \left(\sum_{n\ge N}|\widehat J_n|^2\right)^{1/2}
 \le \sqrt{\frac8{3\pi}}\frac{J}{w\sqrt{N-1}}.
\tag{J}
\]

This slow (N^{-1/2}) tail is not discarded: its two coefficient vectors can
be accumulated explicitly in the Schur complement. Formula (J) bounds only
the final uncomputed remainder.

## The continuous remainder gains a full power

After removal of the steps, (R_f) is absolutely continuous and (R_f') is
of bounded variation. The (m=1) case of Wang's theorem, converted from the
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
tail plus an (N^{-3/2}) norm remainder.

## The boundary potential has signed endpoint moments

For a polynomial (f=\sum_{m<D}u_me_m), the exact matrix from the preceding
note gives, for (n\ge D),

\[
 \langle Vf,e_n\rangle
 =\sqrt{2n+1}\sum_{m<D\atop m+n\text{ even}}
 \frac{u_m\sqrt{2m+1}}{n(n+1)-m(m+1)}.
\]

Expanding the denominator in powers of (m(m+1)/[n(n+1)]) preserves the
signed moments. The first one is

\[
 \sum_{m<D}u_m\sqrt{2m+1}=\sqrt2 f(1)
\]

in the even block (and the analogous pair of endpoint traces without a parity
restriction). This explains why the actual potential tail is small for the
computed ground vector even though an absolute coefficient bound is useless.

## A posteriori positivity budget

For a normalized trial vector (phi), let

\[
 \mu=\langle A_a\phi,\phi\rangle,qquad
 \varepsilon=\|(A_a-\mu)\phi\|.
\]

If an independent inertia certificate proves that the second spectral point
is at least (eta>mu), Kato--Temple gives

\[
 \lambda_1(A_a)\ge\mu-\frac{\varepsilon^2}{\beta-\mu}.
\tag{KT}
\]

At (a=0.4), a 512-mode diagnostic gives

\[
 \mu=1.8126574\cdot10^{-4},\qquad
 \lambda_2^{\rm Ritz}=1.4705371\cdot10^{-2}.
\]

The directly accumulated residual from modes (512) through (8191), before
interval inflation, is (2.1421\cdot10^{-4}). The two analytic tail tools are
deliberately conservative:

- the prime continuous-remainder variation is (V_1\approx196.76), giving
  (3.46\cdot10^{-4}) from (R) beyond mode 8191;
- the two jumps give about (1.4\cdot10^{-4}) from (J);
- the exact signed-moment bound for the logarithmic potential contributes
  only (2.45\cdot10^{-6}).

Even their triangle sum remains below the Kato--Temple positivity budget

\[
 \sqrt{\mu(0.005-\mu)}\approx9.35\cdot10^{-4}.
\]

This is not yet a theorem: (eta=0.005) must be a certified lower bound for
the second eigenvalue, the smooth-kernel tail must receive the same interval
treatment, and all finite quantities must be outward-rounded. It is, however,
a viable certificate design with a factor-of-order-one margin. The previous
uniform Schur estimate had the wrong structure and a margin of the wrong sign.


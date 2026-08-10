# A certified two-prime support interval about 0.551

## Statement

Put

\[
 N=203\,320\,634\,217\,923\,870\,720.
\]

For every real \(a\) satisfying

\[
 |a-0.551|\le10^{-N},
\]

the localized Weil--Suzuki operator obeys

\[
 \boxed{A_a\succeq
 2.6326642462625437\cdot10^{-10}I>0.}
\]

The neighbourhood used in the proof is \(0.55\le a\le0.56\).  It lies
strictly above \(\log3/2\) and below \(\log4/2=\log2\), so exactly the prime
translations attached to 2 and 3 are active.  This is an unconditional open
interval, not a proof of positivity for all supports and therefore not a
proof of RH.

## Point margin

The full block reconstruction in `second-window-schur.md` proves

\[
 A_{0.551}\succeq mI,
 \qquad m=1.3163321231312722\cdot10^{-9}.
\]

This is the coercive lower bound of the infinite operator, not the larger
first eigenvalue of its finite Schur complement.

## Two-prime continuity budget

Let

\[
 p_2=\frac{\log2}{\sqrt2},\qquad
 p_3=\frac{\log3}{\sqrt3},\qquad
 p=p_2+p_3<1.1244131723318378.
\]

For \(h_n(a)=\log(n)/a\), put
\(\delta_n=|h_n(a)-h_n(0.551)|\) and
\(L=\min_{n=2,3}\log(1+\delta_n^{-2})\).  Summing the two
\(H^{\log}\) translation estimates before applying Young's inequality gives

\[
 |\Delta P[f]|
 \le \eta\mathcal L[f]
 +\left(\frac{8p^2}{\eta L}
 +\frac{4p\sqrt C}{\sqrt L}\right)\|f\|^2,
\]

where

\[
 C=\frac4\pi-2\gamma+\log2
 <0.8119553954920424.
\]

The scalar, two prime terms and smooth kernel at the centre give
\(\|B_{0.551}\|<6.416175794136991\), hence
\(\mathcal L\le A_{0.551}+6.416175794136991I\).  Taking

\[
 \eta=4.103167260672816\cdot10^{-11}
\]

and allocating one fifth of \(m\) to each loss requires

\[
 L\ge9.36326122896573\cdot10^{20}.
\]

## Regular terms and conversion to a radius

Exact Taylor coefficients with the same Bernoulli/cosh tail majorants prove,
on \(0\le t\le1.12\),

\[
 |r''(t)|<2.1309230381049535,
\qquad
 |r''(t)+tr'''(t)|<2.8800768010560462.
\]

The scalar and smooth variation alone allow radius
`3.473934710269714e-11`; the logarithmic translation modulus is vastly more
restrictive.  Since

\[
 \delta_n\le
 \frac{\log3}{0.55\cdot0.551}|a-0.551|
 \qquad(n=2,3),
\]

the displayed integer \(N\) is the outward-rounded decimal exponent that
enforces the required value of \(L\).  Four losses consume at most \(4m/5\),
leaving the stated lower bound \(m/5\).

The executable proof is
`experiments/theta_pencil/support_0551_interval_certificate.py`.

## Interpretation

The theorem establishes that localized positivity genuinely survives after
prime three enters; the point certificate is not an isolated numerical
accident.  Its radius also quantifies the remaining obstruction: bare
\(H^{\log}\) continuity is far too weak for an interval-covering proof of RH.
Any scalable continuation must exploit additional regularity of the ground
state or a monotonicity/positivity principle, rather than repeat this modulus
at successive support values.

For the sign question alone, the domain-monotonicity proposition is much
stronger: the later endpoint certificate at \(a=0.60\) proves positivity for
every smaller support, including this whole neighbourhood.  The present
continuity estimate remains useful only as a quantitative comparison of
operators on the rescaled common space.

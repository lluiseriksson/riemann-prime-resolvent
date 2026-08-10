# An Euler-axis Pick criterion

## The data use only the Euler half-plane

Let

\[
 M_\Xi(z)=\frac{\Xi(z)}{\Xi'(z)},\qquad
 F_\Xi(z)=\frac{M_\Xi(z)}{c_\Xi},\qquad F_\Xi(i)=i,
\]

with the positive normalization constant \(c_\Xi=M_\Xi(i)/i\). For
\(\eta>1/2\), put \(s=1/2+\eta>1\) and

\[
 F_\Xi(i\eta)=i f_\Xi(\eta),\qquad
 f_\Xi(\eta)=\frac1{c_\Xi}
 \frac{\xi(s)}{\xi'(s)}.
\]

These values lie wholly in the absolutely convergent Euler-product region.
Writing \(L(\eta)=\xi'(1/2+\eta)/\xi(1/2+\eta)\), one has

\[
 L(\eta)=\frac1s+\frac1{s-1}-\frac12\log\pi
 +\frac12\psi\!\left(\frac s2\right)
 -\sum_{n\ge2}\frac{\Lambda(n)}{n^s}.                 \tag{E1}
\]

No zero locations occur in (E1).

## Countable Nevanlinna--Pick equivalence

Let \(E\subset(1/2,\infty)\) be countable, contain \(1\), and have an
accumulation point in the interval. For every finite list
\(\eta_1,\ldots,\eta_N\in E\), define

\[
 \boxed{
 K^{(N)}_{jk}=
 \frac{f_\Xi(\eta_j)+f_\Xi(\eta_k)}{\eta_j+\eta_k}.}   \tag{EP}
\]

Then

\[
 \boxed{
 \mathrm{RH}\quad\Longleftrightarrow\quad
 K^{(N)}\succeq0\ 
 \text{ for every finite list from }E.}                \tag{EC}
\]

For the forward direction, RH is equivalent to \(F_\Xi\) being Herglotz, and
(EP) is its Pick kernel restricted to the imaginary axis. Conversely, finite
Pick positivity supplies a Herglotz interpolant for each initial finite set.
The node \(\eta=1\) fixes the normalization, hence the interpolants form a
normal family. A diagonal subsequence interpolates every point of \(E\).
The identity theorem identifies its limit with \(F_\Xi\) first in the Euler
region and then by analytic continuation. Thus \(F_\Xi\) is Herglotz, which is
equivalent to RH.

The criterion is useful only if positivity is proved directly from (E1).
Introducing (EP) as a hypothesis merely renames RH.

## Linearization by diagonal congruence

The reciprocal in \(f_\Xi=1/(c_\Xi L)\) does not obstruct an additive
prime--archimedean analysis. Let \(D_L=\operatorname{diag}(L(\eta_j))\) and
define

\[
 H^{(N)}_{jk}=\frac{L(\eta_j)+L(\eta_k)}
 {\eta_j+\eta_k}.                                      \tag{E4}
\]

Then the exact identity

\[
 \boxed{K^{(N)}=\frac1{c_\Xi}D_L^{-1}H^{(N)}D_L^{-1}}  \tag{E5}
\]

shows that \(K^{(N)}\) and \(H^{(N)}\) have the same inertia, because
\(c_\Xi>0\) and \(L(\eta_j)>0\) in the Euler region. In particular, (E1)
splits \(H^{(N)}\) *linearly* into pole, gamma, and prime-power matrices. A
successful proof may therefore seek direct domination or a Gram
factorization of this signed matrix sum; no nonlinear reciprocal estimate is
needed.

## The first finite gate

For two heights \(x,y>0\), write \(a=f_\Xi(x)\) and \(b=f_\Xi(y)\). Direct
factorization gives

\[
 \boxed{
 \det K^{(2)}=
 \frac{(xa-yb)(xb-ya)}{xy(x+y)^2}.}                    \tag{E2}
\]

If \(x<y\) and \(f_\Xi\) is positive and decreasing, the second factor is
negative. In that regime the two-point condition is equivalent to
\(x f_\Xi(x)\le y f_\Xi(y)\). Since \(f_\Xi=1/(c_\Xi L)\), the coalescing-node
gate is

\[
 \boxed{L(\eta)-\eta L'(\eta)\ge0.}                    \tag{E3}
\]

Equivalently, \(L(\eta)/\eta\) must be nonincreasing. This is only the first
Pick minor. Even a proof of (E3) for every \(\eta>1/2\) would not prove RH;
the full matrix hierarchy in (EC) remains.

## Order two is unconditionally positive

In fact, (E3) and every two-node matrix can be closed without RH. Set

\[
 A(\eta)=\xi(1/2+\eta),\qquad L(\eta)=\frac{A'(\eta)}{A(\eta)}.
\]

The centered function \(A\) is even. Its genus-zero product in the variable
\(\eta^2\), grouped over the classes \(a\sim-a\) of centered zeros
\(a=\rho-1/2\), gives an absolutely locally uniformly convergent expansion

\[
 L(\eta)=\sum_{[a]}\frac{2\eta}{\eta^2-a^2}.            \tag{E6}
\]

For one summand,

\[
 \left(1-\eta\frac d{d\eta}\right)
 \frac{2\eta}{\eta^2-a^2}
 =\frac{4\eta^3}{(\eta^2-a^2)^2}.                      \tag{E7}
\]

An on-line class \(a=i\gamma\) contributes positively. For an off-line
orbit, pair \(a=\alpha+i\gamma\) with \(\bar a\). Writing

\[
 X=\eta^2-\alpha^2+\gamma^2,\qquad Y=2\alpha\gamma,
\]

its contribution is

\[
 8\eta^3\operatorname{Re}\frac1{(X-iY)^2}
 =8\eta^3\frac{X^2-Y^2}{(X^2+Y^2)^2}.                 \tag{E8}
\]

For a nontrivial zeta zero, \(|\alpha|<1/2\). Rigorous verification of RH up
to height \(3\cdot10^{12}\) implies that any hypothetical off-line zero has
\(|\gamma|>1\). Hence, for \(\eta>1/2\),

\[
 X=\underbrace{\eta^2-\alpha^2}_{>0}+\gamma^2
 >2|\alpha\gamma|=|Y|,
\]

so every grouped term in (E7)--(E8) is strictly positive. Therefore

\[
 \boxed{L(\eta)-\eta L'(\eta)>0\qquad(\eta>1/2).}      \tag{E9}
\]

The complementary monotonicity is also unconditional. Riemann's positive
kernel represents \(A(\eta)\) as the moment-generating function of a
nondegenerate even positive measure. Consequently

\[
 L'(\eta)=(\log A)''(\eta)
 =\operatorname{Var}_{\eta}(T)>0.                       \tag{E10}
\]

The corresponding tilted mean is \(L(\eta)>0\) for \(\eta>0\).

Thus \(\eta L(\eta)\) is increasing while \(L(\eta)/\eta\) is decreasing.
For \(1/2<x<y\), the two factors in the determinant formula applied to
\(H^{(2)}\),

\[
 (xL(x)-yL(y))(xL(y)-yL(x)),
\]

are both negative. Equations (E5) and (E2) now prove

\[
 \boxed{K^{(2)}(x,y)\succ0\quad\text{for every }1/2<x<y.} \tag{E11}
\]

This is an unconditional order-two theorem, not RH. The first unresolved
Pick obstruction is order three. The only external numerical input in the
sign proof is the rigorous zero verification of Platt and Trudgian,
[arXiv:2004.09765](https://arxiv.org/abs/2004.09765); its enormous height is
used only through the weak consequence \(|\gamma|>1\).

## Hyperbolic form of the order-three gate

Normalize \(H^{(N)}\) to unit diagonal and introduce

\[
 t_j=\frac12\log\eta_j,\qquad v_j=\frac12\log L(\eta_j).
\]

An exact cancellation gives the correlation kernel

\[
 \boxed{
 R_{jk}=\frac{H_{jk}}{\sqrt{H_{jj}H_{kk}}}
 =\frac{\cosh(v_j-v_k)}{\cosh(t_j-t_k)}.}              \tag{E12}
\]

The order-two theorem says precisely that \(t\mapsto v(t)\) is an increasing
contraction. In differential form,

\[
 0<p(t):=v'(t)=\frac{\eta L'(\eta)}{L(\eta)}<1.         \tag{E13}
\]

This metric contraction is not sufficient at order three. For example, the
piecewise-linear increasing contraction through

\[
 (t_1,t_2,t_3)=(1.37291657,1.70725522,2.21284712),
\]

\[
 (v_1,v_2,v_3)=(0.80805853,1.07720414,1.10966327)
\]

has \(\det R\approx-0.0033452\). Thus no argument using only the
one-Lipschitz property can close the next level.

There is, however, a sharp local obstruction. Put three symmetric nodes at
\(t-h,t,t+h\), write \(p=v'(t)\) and \(q=v''(t)\), and expand (E12). Direct
Taylor algebra gives

\[
 \boxed{
 \det R=\left(4(1-p^2)^2-q^2\right)h^6+O(h^8).}        \tag{E14}
\]

Consequently order-three positivity requires

\[
 \boxed{|v''(t)|\le2(1-v'(t)^2),}                      \tag{E15}
\]

or, equivalently, \(\operatorname{artanh}(v')\) must be \(2\)-Lipschitz.
In terms of the Euler-axis log derivative,

\[
 v'(t)=\frac{\eta L'}L,
\qquad
 v''(t)=2\eta\frac d{d\eta}\left(\frac{\eta L'}L\right). \tag{E16}
\]

Proving (E15) for the Riemann target would be a genuine order-three local
theorem, but still not global \(3\times3\) positivity. The next audit must
therefore separate the local curvature gate from the remaining three-point
geometry.

### Exact zero-orbit defect and variance compensation

The local gate does not hold term by term for an off-line zero, but its failure
has a closed form. For \(a=\alpha+i\gamma\), group the conjugate orbit and put

\[
 A=\eta^2-\alpha^2+\gamma^2,\qquad
 B^2=4\alpha^2\gamma^2,qquad
 T_{\alpha,\gamma}(\eta)=\frac{4\eta A}{A^2+B^2}.       \tag{E17}
\]

The on-line case has the same logarithmic derivatives, with the orbit mass
halved to avoid double-counting the class \(a\sim-a\). Define

\[
 p_{\alpha,\gamma}=\eta\frac{T'_{\alpha,\gamma}}
 {T_{\alpha,\gamma}},qquad
 q_{\alpha,\gamma}=2\eta\,p'_{\alpha,\gamma}.
\]

Direct rational differentiation and cancellation give

\[
 \boxed{
 q_{\alpha,\gamma}+2(1-p_{\alpha,\gamma}^2)
 =-\delta_{\alpha,\gamma}(\eta),}                      \tag{E18}
\]

where

\[
 \boxed{
 \delta_{\alpha,\gamma}(\eta)=
 \frac{64\eta^4\alpha^2\gamma^2}
 {A^2(A^2+4\alpha^2\gamma^2)}\ge0.}                   \tag{E19}
\]

Thus on-line orbits saturate the lower curvature boundary, while off-line
orbits miss it by an explicitly quadratic penalty in \(\alpha\).

There is also an exact compensation law for positive sums. If
\(L=\sum_j T_j\), let \(w_j=T_j/L\), \(p_j=\eta T'_j/T_j\), and let
\(p=\sum_jw_jp_j\). Differentiating the weights in the logarithmic coordinate
gives

\[
 q=2\operatorname{Var}_w(p_j)+\sum_jw_jq_j.
\]

Combining this identity with (E18) yields

\[
 \boxed{
 q+2(1-p^2)=
 4\operatorname{Var}_w(p_j)
 -\sum_{j\,\mathrm{off}}w_j\delta_j.}                 \tag{E20}
\]

Therefore the lower half of the local order-three gate is reduced to the
quantitative and non-circular inequality

\[
 \boxed{
 4\operatorname{Var}_w(p_j)
 \ge\sum_{j\,\mathrm{off}}w_j\delta_j.}                \tag{E21}
\]

This is sharper than assuming RH: the right side vanishes under RH, but (E21)
could in principle hold even with off-line zeros. Platt--Trudgian forces every
such penalty to begin above height \(T=3\cdot10^{12}\). This also gives a
uniform numerical ceiling. Indeed, writing \(r=\eta^2\),
\(a=\alpha^2\le1/4\), \(g=\gamma^2\), and \(c=g-a\), one has

\[
 \delta_{\alpha,\gamma}(\eta)
 \le \frac{16r^2g}{(r+c)^4}
 \le \frac{g}{c^2}.
\]

The second inequality uses
\(\max_{r>0}r^2/(r+c)^4=1/(16c^2)\). Since
\(g/(g-1/4)^2\) decreases for \(g>1/4\), every hypothetical off-line orbit
satisfies

\[
 \boxed{
 0\le\delta_{\alpha,\gamma}(\eta)
 \le \varepsilon_T:=
 \frac{T^2}{(T^2-1/4)^2}
 <1.12\cdot10^{-25}.}                                \tag{E22}
\]

Because the \(w_j\) sum to one, (E21) therefore follows from the still-open
but zero-free sufficient bound

\[
 \boxed{
 \operatorname{Var}_w(p_j)\ge\frac{\varepsilon_T}{4}
 <2.8\cdot10^{-26}.}                                  \tag{E23}
\]

The tiny constant is not itself a proof: a uniform positive lower bound for
this variance has not been established, and replacing it by numerical
evidence would be circular. A sharper route may compare its decay directly
with the \(\eta\)-dependent off-line penalty using unconditional zero-counting
bounds.

The module `euler_axis_pick.py` implements (EP)--(E23) as floating-point
algebra for falsification and cross-checking. Rigorous claims require interval
evaluation of (E1) and all relevant principal minors.

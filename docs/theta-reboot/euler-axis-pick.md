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

The tiny constant is not itself a proof; it only identifies the remaining
task. The next argument supplies a much larger analytic variance floor from
two zero-height bands.

### The local order-three gate is unconditional

In fact the missing variance bound can be obtained very coarsely. First, the
upper curvature inequality is automatic. For one orbit, direct algebra gives
\(-1<p_j<1\): the inequality \(p_j>-1\) has numerator

\[
 cA^2+4\alpha^2\gamma^2(2\eta^2+c)>0,
 \qquad c=\gamma^2-\alpha^2,
\]

and \(p_j<1\) is equivalent to
\(A^2>4\alpha^2\gamma^2\). The latter is immediate on the line and, off the
line, follows with enormous room from \(|\alpha|<1/2\) and
\(|\gamma|>3\cdot10^{12}\). Using (E18) in the mixture identity yields

\[
 \boxed{
 2(1-p^2)-q=
 4\sum_jw_j(1-p_j^2)+
 \sum_{j\,\mathrm{off}}w_j\delta_j>0.}                \tag{E24}
\]

For the lower inequality, use

\[
 \operatorname{Var}_w(p_j)=
 \frac12\sum_{i,j}w_iw_j(p_i-p_j)^2.                 \tag{E25}
\]

When \(1/2<\eta\le100\), take the certified on-line zeros in
\(14<\gamma_1<15\) and \(21<\gamma_2<22\). The positive-kernel argument gives
\(L'(\eta)>0\). For \(\eta\le1\), therefore, \(L(\eta)\le L(1)\). For
\(1\le\eta\le100\), (E1), \(\psi(x)<\log x\), and the negative sign of the
prime sum give

\[
 L(\eta)\le
 \frac1s+\frac1{s-1}-\frac12\log\pi+
 \frac12\log\frac{s}{2}<2,
 \qquad s=\eta+\frac12.
\]

Writing \(r=\eta^2\), the two selected weights and slopes in (E25) then give
the entirely rational bound

\[
 \operatorname{Var}_w(p_j)
 \ge
 \frac{432^2r^3}{(r+225)^3(r+484)^3}
 >2.24\cdot10^{-12}.                                 \tag{E26}
\]

The last minimum on \(1/4<r\le10^4\) occurs at an endpoint; the smaller
endpoint value is \(2.2469\ldots\cdot10^{-12}\).

For \(\eta\ge100\), no individual zero table is needed. The explicit
Riemann--von Mangoldt error bound following from
[Trudgian's bound on \(S(T)\)](https://arxiv.org/abs/1208.5846) gives, by
direct differentiation,

\[
 \begin{aligned}
 N(3\eta/4)-N(\eta/2)&\ge10^{-3}\eta\log\eta,\\
 N(2\eta)-N(3\eta/2)&\ge2\cdot10^{-2}\eta\log\eta.
 \end{aligned}                                      \tag{E27}
\]

For completeness, these inequalities remain valid after replacing the exact
zero-counting error in
\(N(T)-\frac{T}{2\pi}\log\frac{T}{2\pi e}\) by the envelope

\[
 0.112\log T+0.278\log\log T+3.385+0.2/T.
\]

Both margins are positive at \(\eta=100\), by more than \(0.16\) and
\(8.39\), respectively. Their first derivatives there exceed \(0.12\) and
\(0.22\). A second differentiation gives the elementary lower bound

\[
 F''_{a,b,k}(\eta)\ge
 \frac{(b-a)/(2\pi)-k}{\eta}
 -\frac{0.4(a^{-1}+b^{-1})}{\eta^3}>0,
\]

for \((a,b,k)=(1/2,3/4,10^{-3})\) and
\((3/2,2,2\cdot10^{-2})\), proving both inequalities for every
\(\eta\ge100\).

Count each positive-height zero with multiplicity. In the first band, its
orbit mass per counted zero is at least \(512/(769\eta)\); in the second it is
at least \(6/(29\eta)\). Also (E1) gives
\(L(\eta)\le\tfrac12\log\eta\). In the dimensionless variables
\(u=\gamma/\eta\), \(e=\alpha^2/\eta^2\), the orbit slope is

\[
 p(u,e)=1+\frac2{1+u^2-e}
 -\frac{4(1+u^2-e)}{(1+u^2-e)^2+4eu^2}.
\]

Here \(0\le e\le2.5\cdot10^{-5}\). Elementary denominator bounds give
\(p<-0.279\) in \(1/2\le u\le3/4\) and \(p>0.383\) in
\(3/2\le u\le2\). Thus the two bands are separated by more than \(0.6\),
their total weights satisfy

\[
 w_1\ge\frac{1024}{769000},\qquad
 w_2\ge\frac{0.24}{29},
\]

and (E25) gives

\[
 \operatorname{Var}_w(p_j)
 \ge0.6^2w_1w_2
 >3.96\cdot10^{-6}.                                  \tag{E28}
\]

Combining (E22), (E24), (E26), and (E28) proves

\[
 \boxed{|v''(t)|<2(1-v'(t)^2)\quad(t>\tfrac12\log(1/2))} \tag{E29}
\]

unconditionally. The two external inputs are the rigorous verification to
height \(3\cdot10^{12}\) and the explicit zero-counting error bound. This is
initially only the *coalescing-node* order-three condition. The next argument
shows that, in this particular hyperbolic kernel, it integrates globally.

### From local curvature to every separated triple

Let \(t_1<t_2<t_3\), put

\[
 x=t_2-t_1,\quad y=t_3-t_2,\quad
 u=v(t_2)-v(t_1),\quad z=v(t_3)-v(t_2),
\]

and normalize the \(3\times3\) kernel to correlations. Its three off-diagonal
entries are

\[
 a=\frac{\cosh u}{\cosh x},\qquad
 b=\frac{\cosh z}{\cosh y},\qquad
 c=\frac{\cosh(u+z)}{\cosh(x+y)}.
\]

Since \(0<v'<1\), define the interval rapidity

\[
 \mathcal A(x,u)=
 \operatorname{artanh}\!\left(\frac{\tanh u}{\tanh x}\right)
 =\frac12\log\frac{\sinh(x+u)}{\sinh(x-u)}.           \tag{E30}
\]

The correlation determinant factors exactly as

\[
 \det R=(1-a^2)(1-b^2)-(c-ab)^2.
\]

Writing \(X=\tanh x\), \(Y=\tanh y\), \(U=\tanh u\), and
\(Z=\tanh z\), division by the positive factor
\(\cosh^2u\cosh^2zX^2Y^2\) shows

\[
 \boxed{
 \det R\ge0\quad\Longleftrightarrow\quad
 |\mathcal A(x,u)-\mathcal A(y,z)|\le x+y.}           \tag{E31}
\]

Indeed,

\[
 \frac{1-(U/X)(Z/Y)}
 {\sqrt{(1-(U/X)^2)(1-(Z/Y)^2)}}
 =\cosh\bigl(\mathcal A(x,u)-\mathcal A(y,z)\bigr).
\]

It remains to integrate (E29), and here the constant \(2\) is exact. Put
\(g(t)=\operatorname{artanh}v'(t)\). Then (E29) says \(|g'|<2\).
For an interval of length \(h\) ending at \(t_0\), monotonicity of \(\tanh\)
gives

\[
 \int_0^h\tanh(g(t_0)-2r)\,dr
 \le v(t_0)-v(t_0-h)
 \le\int_0^h\tanh(g(t_0)+2r)\,dr.                    \tag{E32}
\]

The map \(u\mapsto\mathcal A(h,u)\) is increasing, and direct integration
gives the sharp endpoint identity

\[
 \mathcal A\!\left(
 h,\int_0^h\tanh(g_0\mathbin\pm2r)\,dr\right)
 =g_0\mathbin\pm h.                                  \tag{E33}
\]

Consequently the rapidity of either interval adjacent to \(t_0\) lies in
\([g(t_0)-h,g(t_0)+h]\). Applying this to the left interval of length \(x\)
and the right interval of length \(y\) proves

\[
 |\mathcal A(x,u)-\mathcal A(y,z)|\le x+y.            \tag{E34}
\]

By (E31), every \(3\times3\) principal Pick matrix on the Euler axis is
therefore positive semidefinite, unconditionally. This closes order three,
not RH: matrices of order four and higher remain uncontrolled.

### The first genuinely new gate is order four

The rapidity argument cannot be iterated without new information. A clean
counterexample already exists inside its hypotheses. Take four equally spaced
nodes with spacing \(h=0.6\), let \(g=\operatorname{artanh}v'\) be linear on
each interval, and prescribe

\[
 (g_0,g_1,g_2,g_3)=(0.7,0.01,1.1,2.2).
\]

The three slopes are \(-1.15\), \(1.8166\ldots\), and
\(1.8333\ldots\), so \(|g'|<2\) and hence every triple obeys (E34). The image
increments are available without quadrature:

\[
 u_j=\frac{\log\cosh g_{j+1}-\log\cosh g_j}
 {(g_{j+1}-g_j)/h}
 =(0.1975828\ldots,0.2817722\ldots,0.5493378\ldots).
\]

Nevertheless the normalized \(4\times4\) determinant is

\[
 \det R=-1.6277632\ldots\cdot10^{-4},
\]

while its four principal \(3\times3\) determinants are positive. The exact
new scalar obstruction can be written as an endpoint partial correlation.
With \(B=R_{\{2,3\},\{2,3\}}\), \(a=R_{1,\{2,3\}}\), and
\(b=R_{\{2,3\},4}\), put

\[
 \kappa_{14\mid23}=
 \frac{R_{14}-aB^{-1}b}
 {\sqrt{(1-aB^{-1}a^T)(1-b^TB^{-1}b)}}.              \tag{E35}
\]

Schur complementation gives

\[
 \boxed{R\succeq0\quad\Longleftrightarrow\quad
 |\kappa_{14\mid23}|\le1}                            \tag{E36}
\]

once the order-three minors are known. In the displayed counterexample,
\(\kappa_{14\mid23}=1.23385\ldots\). Thus the next proof obligation is not
another bound on \(g'\); it is a genuinely third-order conditional-correlation
constraint. For the Riemann kernel this must be derived from the zero-orbit
mixture or directly from the Euler formula.

### A full-rank verified Gram floor at order four

There is a concrete way to calibrate the required domination. An on-line zero
of height \(\gamma\) contributes to the congruent kernel (E4)

\[
 G_\gamma(x,y)=
 \frac{2(xy+\gamma^2)}{(x^2+\gamma^2)(y^2+\gamma^2)}. \tag{E37}
\]

This is the rank-two Gram kernel of the features

\[
 \frac{\sqrt2\gamma}{x^2+\gamma^2},\qquad
 \frac{\sqrt2x}{x^2+\gamma^2}.
\]

Two distinct verified heights \(\gamma_1,\gamma_2\) therefore give a
full-rank floor on four distinct nodes \(x_1<\cdots<x_4\). If
\(g_j=\gamma_j^2\), direct Cauchy--Vandermonde elimination gives

\[
 \boxed{
 \det(G_{\gamma_1}+G_{\gamma_2})=
 \left[
 \frac{4\gamma_1\gamma_2(g_2-g_1)^2
 \prod_{i<j}(x_j-x_i)}
 {\prod_i(x_i^2+g_1)(x_i^2+g_2)}
 \right]^2>0.}                                      \tag{E38}
\]

To expose exactly what remains, replace every positive-height zero by an
on-line surrogate at the same height, counted with multiplicity, and call the
resulting positive matrix \(H_0\). For an off-line pair
\(\alpha\mathbin\pm i\gamma\), write \(a=\alpha^2\), \(g=\gamma^2\),
\(C=x^2+g\), and

\[
 D=(C-a)^2+4ag.
\]

The difference between its true logarithmic-derivative mass and its two
on-line surrogates is exactly

\[
 e_{a,g}(x)=
 \frac{4x}{C}\frac{a(x^2-3g-a)}{D}.                 \tag{E39}
\]

Hence the complete perturbation is the convergent symmetric kernel

\[
 E_{ij}=\sum_{\mathrm{off}}
 \frac{e_{a,g}(x_i)+e_{a,g}(x_j)}{x_i+x_j},qquad
 H=H_0+E.                                             \tag{E40}
\]

Let \(H_{12}=G_{\gamma_1}+G_{\gamma_2}\) for the first two certified
heights. Since \(H_0\succeq H_{12}>0\), the explicit, non-circular sufficient
order-four gate is

\[
 \boxed{
 \left\|H_{12}^{-1/2}EH_{12}^{-1/2}\right\|_{\mathrm{op}}\le1.} \tag{E41}
\]

Indeed, (E41) gives \(H_{12}+E\succeq0\), and adding
\(H_0-H_{12}\succeq0\) yields \(H\succeq0\). The gate is deliberately
stronger than necessary, but every term is explicit and the off-line sum
starts only above \(3\cdot10^{12}\). The unresolved issue is uniformity in
the node geometry: \(H_{12}^{-1}\) becomes ill-conditioned as nodes
coalesce or escape, while the perturbation has matching divided-difference
cancellation that a crude entrywise norm would lose.

That cancellation is visible before taking norms. For a real vector
\(c=(c_i)_{i=1}^4\), define

\[
 F_c(w)=\sum_i\frac{c_ix_i}{x_i^2+w^2},\qquad
 G_c(w)=\sum_i\frac{c_i}{x_i^2+w^2},\qquad
 Q_c(w)=F_c(w)^2+w^2G_c(w)^2.                        \tag{E42}
\]

The quadratic form of one on-line height is \(2Q_c(\gamma)\). For an
off-line conjugate pair, put \(w=\gamma-i\alpha\). Its grouped quadratic form
is exactly \(4\operatorname{Re}Q_c(\gamma-i\alpha)\), whereas its two
on-line surrogates contribute \(4Q_c(\gamma)\). Since \(Q_c\) is real on the
real axis, Taylor's formula along the vertical segment gives

\[
 \boxed{
 \operatorname{Re}Q_c(\gamma-i\alpha)-Q_c(\gamma)
 =-\alpha^2\int_0^1(1-t)
 \operatorname{Re}Q_c''(\gamma-it\alpha)\,dt.}       \tag{E43}
\]

Thus the node-uniform order-four problem is reduced to a rational Bernstein
inequality. A sufficient form, with zero multiplicities understood, is

\[
 \boxed{
 2\sum_{\mathrm{off}}\alpha^2\int_0^1(1-t)
 |Q_c''(\gamma-it\alpha)|\,dt
 \le \sum_{\gamma>0} Q_c(\gamma)
 \quad\text{for every }c\in\mathbb R^4.}             \tag{E44}
\]

Unlike an entrywise estimate, (E44) remains meaningful when nodes coalesce:
both sides see the same rational cancellations. It is not yet proved. Its
finite-dimensional feature is important: after a common denominator,
\(F_c\) and \(G_c\) have numerator degree bounded by the four nodes. Extending
the same inequality uniformly to arbitrary dimension would recover the full
RH difficulty; the present target is only the first open dimension.

More explicitly, set \(z=w^2\) and

\[
 \begin{aligned}
 P(z)&=\prod_{i=1}^4(z+x_i^2),\\
 A_c(z)&=\sum_i c_i\prod_{j\ne i}(z+x_j^2),\\
 B_c(z)&=\sum_i c_ix_i\prod_{j\ne i}(z+x_j^2).
 \end{aligned}
\]

Then

\[
 \boxed{
 Q_c(w)=\frac{S_c(w^2)}{P(w^2)^2},\qquad
 S_c(z)=B_c(z)^2+zA_c(z)^2\ge0\quad(z\ge0),}         \tag{E45}
\]

with \(\deg S_c\le7\). Thus order four no longer asks for an estimate on an
arbitrary analytic function: it asks for a sampling/derivative inequality for
a nonnegative degree-seven numerator divided by four positive quadratic
scales. A zero of \(Q_c\) on the positive axis forces both \(A_c\) and
\(B_c\) to vanish, so this family cannot track more than finitely many of the
densely spaced zeta heights. The next quantitative target is an explicit
degree-seven Remez--Bernstein sampling lemma on dyadic height bands, combined
with the unconditional Riemann--von Mangoldt count.

### Closing the order-four sampling lemma

The required constants are much weaker than standard polynomial inequalities
provide. Partition \([T,\infty)\), \(T=3\cdot10^{12}\), into dyadic bands
\(I_Y=[Y,2Y]\). On each band take the fifteen roots of the degree-fifteen
Chebyshev polynomial, affinely transported to \(I_Y\). Around each root use a
radius

\[
 \delta Y,qquad \delta=\frac1{24\cdot14^2}.
\]

The explicit zero-counting envelope used in (E27) shows that every one of
these disjoint intervals contains a zeta zero. At the smallest band the worst
lower count is already \(5.45\cdot10^9\), and direct differentiation shows it
increases with \(Y\). Choose one positive zero height \(\lambda_k\) from each
interval.

Let \(R(w)=S_c(w^2)\), so \(\deg R\le14\), and let
\(D(w)=P(w^2)^2\). The Chebyshev Lebesgue constant is less than \(3\).
Markov's inequality and the choice of \(\delta\) give

\[
 \|R\|_{I_Y}
 \le3\left(\max_k|R(\lambda_k)|+\frac1{12}\|R\|_{I_Y}\right),
\]

hence

\[
 \|R\|_{I_Y}\le4\max_k|R(\lambda_k)|.               \tag{E46}
\]

Across \(I_Y\), each factor \(w^2+x_i^2\) varies by at most a factor \(4\),
so \(\max D/\min D\le4^8\). On the real interval,

\[
 \|R'\|\le\frac{2\cdot14^2}{Y}\|R\|,
 \qquad
 \|R''\|\le\frac{4\cdot14^4}{Y^2}\|R\|,
\]

while \(|D'/D|\le16/Y\) and
\(|(D'/D)'|\le16/Y^2\). Differentiating \(Q=R/D\), inserting (E46), and
then using Taylor's formula through the strip \(|\operatorname{Im}w|\le1/2\)
gives the deliberately rounded bound

\[
 \boxed{
 \sup_{\substack{Y\le\operatorname{Re}w\le2Y\\
                  |\operatorname{Im}w|\le1/2}}
 |Q_c''(w)|
 \le\frac{C_*}{Y^2}\max_{1\le k\le15}Q_c(\lambda_k),
 \qquad C_*=2\cdot10^{11}.}                          \tag{E47}
\]

For reference, the real-axis bookkeeping before the harmless vertical-strip
rounding is

\[
 4\cdot4^8
 \left(4\cdot14^4+64\cdot14^2+16^2+16\right)
 <4.37\cdot10^{10};
\]

the factor allowed in (E47) is more than four times larger. Since the strip
width relative to \(Y\) is below \(1.7\cdot10^{-13}\), the stated rounding
also follows directly by expanding the degree-sixteen numerator and
denominator derivatives along the vertical segment.

There are fewer than \(Y\log Y\) positive zeros in \(I_Y\). Therefore the
left side of (E44), restricted to one band, is at most

\[
 \frac14\,Y\log Y\,\frac{C_*}{Y^2}
 \max_kQ_c(\lambda_k)
 \le0.479\max_kQ_c(\lambda_k).                       \tag{E48}
\]

Here \(1/4\) comes from
\(2\alpha^2\int_0^1(1-t)dt\le1/4\). The function \(\log Y/Y\) decreases
for \(Y\ge T\), so the displayed decimal is its worst value. The fifteen
chosen zeros are disjoint between bands, and their positive values occur in
the right side of (E44). Summing (E48) over all dyadic bands proves (E44).

Consequently every \(4\times4\) Euler-axis Pick matrix is positive
semidefinite, unconditionally. This closes the first gate not implied by the
rapidity curvature argument. It still does not prove RH: the polynomial
degree and the Markov/sampling constant grow with matrix order, and no
uniform-in-order estimate has been established.

### The same proof closes every order up to forty

The dyadic choice above was made for readability, not efficiency. For a real
vector on \(n\) nodes, the construction (E42)--(E45) gives

\[
 \deg_z S_c\le2n-1,\qquad \deg_w S_c(w^2)\le d_n:=4n-2.
\]

Use multiplicative bands \([Y,(1+q_n)Y]\) with

\[
 q_n=\frac1{4n-1}=\frac1{d_n+1},
\]

and \(d_n+1\) Chebyshev roots. Take sampling radius
\(q_nY/(100d_n^2)\). The standard bound

\[
 \Lambda_{d_n}\le1+\frac2\pi\log(d_n+1)
\]

and the perturbed-node Markov estimate replace the interpolation factor \(4\)
in (E46) by

\[
 I_n=
 \frac{\Lambda_{d_n}}{1-0.02\Lambda_{d_n}}.           \tag{E49}
\]

The real derivative bookkeeping on a band of length \(q_nY\) is

\[
 B_n=
 \frac{4d_n^4}{q_n^2}
 +\frac{16nd_n^2}{q_n}
 +(4n)^2+4n.                                         \tag{E50}
\]

For \(n\le40\), iterated Markov bounds along
\(|\operatorname{Im}w|\le1/2\) enlarge the real estimate by less than
\(1.01\): indeed \(d_n^2/(q_nT)<1.4\cdot10^{-6}\), and every denominator
factor changes by less than \(10^{-12}\). Thus a valid sampling constant is

\[
 C_n=1.01I_n(1+q_n)^{4n}B_n.                         \tag{E51}
\]

The explicit count gives fewer than
\(0.161q_nY\log Y\) positive zeros per band. Every off-line orbit accounts
for two of them, so the number of off-line pairs is at most half this value.
Hence the analogue of (E48) closes whenever

\[
 \boxed{
 \Theta_n:=\frac{0.161C_nq_n\log T}{8T}<1.}          \tag{E52}
\]

All sampling intervals contain zeros; even in the worst case
\(n=40,Y=T\), the smallest lower count exceeds \(6.46\cdot10^4\). Direct
evaluation of the explicit constants gives

\[
 \Theta_{39}=0.8512\ldots,\qquad
 \Theta_{40}=0.9715\ldots,\qquad
 \Theta_{41}=1.1051\ldots.                           \tag{E53}
\]

Therefore

\[
 \boxed{K^{(n)}\succeq0\quad\text{for every }n\le40} \tag{E54}
\]

unconditionally. The cutoff \(40\) is a limitation of these deliberately
coarse constants, not evidence of a failure at order \(41\). More
importantly, proving every fixed order separately is not RH: (EC) requires a
single argument valid for unbounded \(n\). The next mathematical target is to
replace the Markov growth in (E50) by a sampling inequality whose constant is
uniform, or grows slowly enough to be absorbed without a finite verification
height.

The obstruction has a precise scale. In the range where the perturbed
Chebyshev factor (E49) is used,

\[
 d_n\sim4n,\qquad q_n\sim\frac1{4n},\qquad
 B_n\sim16384n^6,
\]

and therefore

\[
 \boxed{
 \Theta_n\sim226.314\ldots\,I_n n^5\frac{\log T}{T}.} \tag{E55}
\]

### An \(L^1\) column-sum refinement: every order through 233

The maximum in (E46) throws away the fact that all sampled numerator values
are nonnegative.  Keeping them separately removes two powers of the degree.
The argument is given with explicit constants because an asymptotic
Marcinkiewicz--Zygmund slogan would not suffice at the endpoint.

Put

\[
 m=4n-1,\qquad d=m-1,\qquad q=\frac1m,
 \qquad I_Y=[Y,(1+q)Y],\qquad L=\frac Ym.
\]

Let \(\tau_1,\ldots,\tau_m\) be the transported roots of \(T_m\).  The
Riemann--von Mangoldt envelope already used above gives, for every \(u\ge T\),

\[
 \begin{aligned}
 &N(u+2)-N(u-2)\\
 &\quad\ge M(u+2)-M(u-2)-E(u+2)-E(u-2)>0,
 \end{aligned}                                      \tag{E56}
\]

where the lower bound at \(T\) is \(2.04669\ldots\).  Its derivative is
positive: use
\(\log((u+2)/(u-2))\ge4/u\) and the displayed formula for \(E'\).
Thus one may choose a positive zero height \(\lambda_k\) with
\(|\lambda_k-\tau_k|\le2\).  For \(n\le233\) these intervals are disjoint
and remain inside their bands.  Even at order 234 their first-band endpoint
clearance is \(2263.94\ldots\), and their minimum separation is
\(18111.53\ldots\).

Every interval \([a,b]\subset[T,\infty)\) of length at most one contains at
most

\[
 \begin{aligned}
 N(b)-N(a)
 &\le \frac1{2\pi}\log\frac b{2\pi}+2E(b)\\
 &<0.69\log b                                      \tag{E57}
 \end{aligned}
\]

positive zeros, counted with multiplicity.  Indeed the coefficient obtained
after division by \(\log b\) is at most

\[
 \frac1{2\pi}+0.224
 +0.556\frac{\log\log T}{\log T}
 +\frac{6.77}{\log T}+\frac{0.4}{T\log T}
 =0.6837857\ldots,
\]

and every nonconstant quotient here decreases for \(b\ge T\).

Let \(\ell_k\) be the cardinal polynomial at the exact Chebyshev roots on
\([-1,1]\).  Its expansion is

\[
 \ell_k(x)=\frac1m+\frac2m\sum_{r=1}^{m-1}
 \cos(r\theta_k)T_r(x),\qquad
 \theta_k=\frac{(2k+1)\pi}{2m}.                    \tag{E58}
\]

The following elementary column bounds are the key improvement:

\[
 \boxed{
 \begin{aligned}
 U_2(m)&:=\max_k\int_{-1}^1|\ell_k''(x)|\,dx
 \le\frac23m^2\left(2\log(2m)+\frac73\right),\\
 U_3(m)&:=\max_k\int_{-1}^1|\ell_k'''(x)|\,dx
 \le\frac{56}{5}m^4.                              \tag{E59}
 \end{aligned}}
\]

For completeness, write \(x=\cos\theta\).  Since

\[
 T_r'(\cos\theta)=r\frac{\sin(r\theta)}{\sin\theta},
\]

splitting at \(\theta=1/r\), using the endpoint Markov value
\(T_r''(1)=r^2(r^2-1)/3\), and integrating \(\csc\theta\) and
\(\csc^2\theta\) gives

\[
 \int_{-1}^1|T_r''(x)|\,dx
 \le r^2\left(2\log(2r)+\frac73\right).            \tag{E60}
\]

Also

\[
 \frac d{d\theta}T_r''(\cos\theta)
 =\frac{r(r^2-1)\sin(r\theta)}{\sin^2\theta}
 -\frac{3r(\sin(r\theta)\cos\theta-r\cos(r\theta)\sin\theta)
          \cos\theta}{\sin^4\theta}.
\]

The same split, with
\(\int_{1/r}^{\pi/2}\csc^j\theta\,d\theta\) bounded by
\((\pi/2)^j\int_{1/r}^{\infty}\theta^{-j}\,d\theta\), gives
\(\int|T_r'''|\le28r^4\).  Inserting these two estimates in (E58) and using
\(\sum_{r<m}r^2<m^3/3\), \(\sum_{r<m}r^4<m^5/5\) proves (E59).
The companion sup-norm bounds used below are

\[
 M_1\le\frac23m^2,\quad M_2\le\frac2{15}m^4,
 \quad M_3\le\frac2{105}m^6,
 \quad M_4\le\frac2{945}m^8,                       \tag{E61}
\]

obtained from the endpoint values of \(T_r^{(j)}\) and (E58).

Return now to the physical band.  Markov's inequality gives

\[
 \varepsilon=\frac{4d^2}{L},\qquad
 I=\frac{\Lambda_d}{1-\Lambda_d\varepsilon},
 \qquad J=1+m\varepsilon I.                        \tag{E62}
\]

Consequently

\[
 \|R\|\le I\max_k R(\lambda_k),\qquad
 \sum_kR(\tau_k)\le J\sum_kR(\lambda_k).          \tag{E63}
\]

This is where nonnegativity of \(R=S_c(w^2)\) is essential.  In contrast,
the maximum-based proof paid the number of zeros in the whole band.

Set \(\mu=d^2/L\).  Repeated Markov followed by Taylor gives, for every
degree-\(d\) polynomial \(p\),

\[
 \sup_{\substack{-1\le x\le1\\|v|\le1/L}}|p(x+iv)|
 \le e^\mu\|p\|_{[-1,1]}.                          \tag{E64}
\]

Using the vertical fundamental theorem of calculus with (E59)--(E61), define

\[
 \begin{aligned}
 a_0&=LI+e^\mu M_1J,\\
 a_1&=J\left(2m+\frac{2e^\mu M_2}{L}\right),\\
 a_2&=J\left(\frac{2U_2}{L}+\frac{4e^\mu M_3}{L^2}\right),\\
 a_3&=J\left(\frac{4U_3}{L^2}+\frac{8e^\mu M_4}{L^3}\right).             \tag{E65}
 \end{aligned}
\]

Then \(a_j\sum_kR(\lambda_k)\) bounds
\(\int_{I_Y}\sup_{|v|\le1/2}|R^{(j)}(u+iv)|\,du\) for \(j=0,1,2,3\).

Let \(D(w)=P(w^2)^2\), \(h=D'/D\), and put

\[
 \begin{gathered}
 \kappa=\left(1-\frac1{4T^2}\right)^{-1},\\
 \kappa_0=\left(1+\frac1{2T}\right)\kappa,
 \quad
 \kappa_1=\left(1+\frac1T+\frac1{4T^2}\right)\kappa^2,\\
 \kappa_2=\left(1+\frac1{2T}\right)
 \left(1+\frac1T+\frac1{4T^2}\right)\kappa^3,\\
 H_0=\frac{4\kappa_0n}{Y},\qquad
 H_1=\frac{4\kappa_1n}{Y^2},\qquad
 H_2=\frac{24\kappa_2n}{Y^3},\\
 A_n=\kappa^{2n}\left(1+\frac1m\right)^{4n}.       \tag{E66}
 \end{gathered}
\]

Direct differentiation of
\(h(w)=4w\sum_i(w^2+x_i^2)^{-1}\) gives the bounds \(H_0,H_1,H_2\).
Since

\[
 \begin{aligned}
 Q''&=D^{-1}\{R''-2hR'+(h^2-h')R\},\\
 Q'''&=D^{-1}\{R'''-3hR''+3(h^2-h')R'
                 +(-h^3+3hh'-h'')R\},
 \end{aligned}
\]

we obtain

\[
 \begin{aligned}
 C_2&=A_n\{a_2+2H_0a_1+(H_0^2+H_1)a_0\},\\
 C_3&=A_n\{a_3+3H_0a_2+3(H_0^2+H_1)a_1
 +(H_0^3+3H_0H_1+H_2)a_0\}.                       \tag{E67}
 \end{aligned}
\]

Thus \(C_j\sum_kQ_c(\lambda_k)\) bounds the corresponding integrated
strip supremum of \(Q_c^{(j)}\).

Finally partition \(I_Y\) into \(\lceil L\rceil\) equal intervals.  Their
lengths lie between \(1/2\) and \(1\).  For a nonnegative absolutely
continuous function \(H\) on such an interval,

\[
 \sup H\le2\int H+\int|H'|.                        \tag{E68}
\]

Apply this to
\(H(u)=\sup_{|v|\le1/2}|Q_c''(u+iv)|\).  Each off-line pair accounts for two
positive zeros and \(2\alpha^2\int_0^1(1-t)dt\le1/4\).  Equations
(E57), (E67), and (E68) therefore bound the contribution of one band to the
left side of (E44) by

\[
 \boxed{
 \Omega_n(Y)\sum_{k=1}^mQ_c(\lambda_k),\qquad
 \Omega_n(Y)=\frac{0.69\log((1+1/m)Y)}8(2C_2+C_3).} \tag{E69}
\]

Every factor after multiplication by the logarithm decreases with
\(Y\ge T\), so the first band is worst.  A deliberately rounded rational
certificate, uniform for \(4\le n\le233\), uses

\[
 \begin{gathered}
 m\le931,\quad \Lambda_d<5.356,\quad I<5.39,\quad J<6.39,\\
 e^\mu<1.0011,\quad A_n<2.820003,\quad
 0.69\log(16T/15)<19.872.
 \end{gathered}
\]

Substitution in (E59)--(E69), using \(T/15\) only for the harmless \(a_0\)
term and \(T/931\) for all derivative terms, gives exactly

\[
 \boxed{\Omega_n(T)<0.986931<1\qquad(4\le n\le233).} \tag{E70}
\]

The arithmetic in (E70) is performed with rational numbers in
`l1_column_sampling_budget.py`; floating point is printed only as a readable
decimal.  Summing the disjoint sampled zeros over all bands proves

\[
 \boxed{K^{(n)}\succeq0\quad\text{for every }n\le233.} \tag{E71}
\]

This supersedes (E54), but it is still not RH.  The unrounded scalar formula
is below one at order 234, but no claim is made from that floating diagnostic.
More importantly, in the regime where the fixed-radius perturbation is small,

\[
 \Omega_n(T)=O\!\left(n^3\log n\frac{\log T}{T}\right),                \tag{E72}
\]

and the perturbation factor \(J\) eventually grows as well.  Hence every
finite verified height still produces only a finite-order theorem.

### The exact signed prime-side target

The absolute-value proof can now be connected directly to the Euler product.
Set

\[
 d_i=\sum_j\frac{c_j}{x_i+x_j},\qquad
 a_i=c_id_i,\qquad
 \phi_c(t)=\sum_i a_i e^{-x_it}.                    \tag{E73}
\]

For real \(w\),

\[
 H_c(w):=\sum_i\frac{c_i}{x_i-iw}=F_c(w)+iwG_c(w),
 \qquad Q_c(w)=|H_c(w)|^2.
\]

Partial fractions give the exact cosine representation

\[
 \boxed{
 Q_c(w)=2\int_0^\infty\phi_c(t)\cos(wt)\,dt,
 \qquad \widehat Q_c(t)=2\pi\phi_c(|t|).}           \tag{E74}
\]

In particular, for one hypothetical off-line orbit,

\[
 \boxed{
 \operatorname{Re}Q_c(\gamma-i\alpha)-Q_c(\gamma)
 =2\int_0^\infty\phi_c(t)\cos(\gamma t)
   (\cosh(\alpha t)-1)\,dt.}                       \tag{E75}
\]

This is the signed version of (E43).  Taking absolute values before summing
destroys both oscillatory factors in (E75), exactly explaining the finite
barrier above.

There is also an exact prime identity with no reference to zeros.  Write

\[
 \begin{aligned}
 \mathcal A(x)={}&\frac1{x+1/2}+\frac1{x-1/2}
 -\frac12\log\pi+\frac12\psi_0\left(\frac x2+\frac14\right),\\
 p(x)={}&\sum_{r\ge2}\frac{\Lambda(r)}{r^{x+1/2}}.
 \end{aligned}
\]

The Euler product in \(s=1/2+x>1\) says \(L(x)=\mathcal A(x)-p(x)\).
Therefore

\[
 \boxed{
 c^THc
 =2\sum_i a_i\mathcal A(x_i)
  -2\sum_{r\ge2}\frac{\Lambda(r)}{\sqrt r}\,
    \phi_c(\log r).}                               \tag{E76}
\]

Thus the Fourier test generated by the Cauchy resolvent is not merely
analogous to the prime block: it is exactly that block.

Here \(\psi_0=\Gamma'/\Gamma\).  The PNT main term can be removed without an
estimate.  Let \(R(u)=\Psi(u)-u\), where
\(\Psi(u)=\sum_{r\le u}\Lambda(r)\), and set
\(f_c(u)=u^{-1/2}\phi_c(\log u)\).  Stieltjes integration by parts on
\([1,\infty)\) is legitimate because \(x_i>1/2\) and the elementary
Chebyshev bound gives \(R(u)=O(u)\).  Since \(R(1)=-1\),

\[
 \begin{aligned}
 2\int_1^\infty f_c(u)\,d\Psi(u)
 ={}&2\sum_i\frac{a_i}{x_i-1/2}+2\phi_c(0)\\
 &-2\int_1^\infty R(u)u^{-3/2}
 \left(\phi_c'(\log u)-\frac12\phi_c(\log u)\right)du.               \tag{E77}
 \end{aligned}
\]

Combining (E76) and (E77) yields the fully centered identity

\[
 \boxed{
 \frac12c^THc
 =\sum_i a_i\mathcal G(x_i)
 +\int_1^\infty R(u)u^{-3/2}
 \left(\phi_c'(\log u)-\frac12\phi_c(\log u)\right)du,}              \tag{E78}
\]

where

\[
 \mathcal G(x)=\frac1{x+1/2}-1-\frac12\log\pi
 +\frac12\psi_0\left(\frac x2+\frac14\right).
\]

This is the surviving signed target.  Its test is still finite-dimensional:

\[
 \phi_c'(t)-\frac12\phi_c(t)
 =-\sum_i(x_i+1/2)a_i e^{-x_it}.                    \tag{E79}
\]

For distinct nodes the Wronskian of the functions \(e^{-x_it}\) is a
nonzero Vandermonde times \(e^{-(\sum_i x_i)t}\).  Hence (E79), unless
identically zero, has at most \(n-1\) real zeros counted with multiplicity.
The arithmetic obstruction has therefore been reduced to a signed
PNT-remainder pairing over at most \(n\) sign intervals.  This is stronger
structural information than an unrestricted test function, but it is not yet
uniform in \(n\); replacing the integral by \(|R|\) or total variation again
loses the cancellation and does not prove (EC).

The test in (E78) has an exact mass:

\[
 \boxed{
 \int_1^\infty u^{-3/2}
 \left(\phi_c'(\log u)-\frac12\phi_c(\log u)\right)du
 =-\phi_c(0).}                                      \tag{E80}
\]

Indeed each exponential in (E79) contributes
\(-(x_i+1/2)a_i\int_1^\infty u^{-x_i-3/2}du=-a_i\).
Moreover

\[
 \phi_c(0)=\sum_i a_i
 =\sum_{i,j}\frac{c_ic_j}{x_i+x_j}>0               \tag{E81}
\]

for \(c\ne0\), because the Cauchy matrix is the Gram matrix of the functions
\(e^{-x_it}\) on \([0,\infty)\).  Define the canonical centering constant

\[
 C_c=\frac{\sum_i a_i\mathcal G(x_i)}{\phi_c(0)}.
\]

Equations (E78)--(E81) collapse the entire quadratic form to

\[
 \boxed{
 \frac12c^THc
 =\int_1^\infty (R(u)-C_c)u^{-3/2}
 \left(\phi_c'(\log u)-\frac12\phi_c(\log u)\right)du.}              \tag{E82}
\]

Thus the missing uniform theorem is no longer an unspecified appeal to
"prime cancellation": it is the sign of the single centered pairing (E82)
for the Cauchy-generated exponential tests (E79).  Proving that sign for all
finite node sets would prove the Euler-axis Pick criterion and hence RH; it
is not asserted here.  The advantage of (E82) is diagnostic: any proposed
Yang--Mills, Ward, transfer-matrix, or involution mechanism must reproduce
this precise centering constant and this precise signed test, rather than a
positive majorant of them.

There is a useful operator form of the same gate.  Define

\[
 g_c(s)=\sum_i c_i e^{-x_is}\quad(s\ge0),
 \qquad (S_tg)(s)=g(s+t).
\]

Fubini and the Cauchy integral immediately give

\[
 \boxed{
 \phi_c(t)=\int_0^\infty g_c(s)g_c(s+t)\,ds
 =\langle g_c,S_tg_c\rangle,qquad
 \phi_c(0)=\|g_c\|_2^2.}                            \tag{E83}
\]

Consequently the prime block in (E76) is exactly the weighted shift form

\[
 2\sum_{r\ge2}\frac{\Lambda(r)}{\sqrt r}
 \langle g_c,S_{\log r}g_c\rangle.                 \tag{E84}
\]

After the change of variables \(u=e^t\), put

\[
 k_c(t)=(R(e^t)-C_c)e^{-t/2},\qquad
 (V_{k_c}g)(u)=\int_0^u k_c(u-s)g(s)\,ds.
\]

Because
\(\phi_c'(t)-\phi_c(t)/2
 =\int_0^\infty g_c(s)(g_c'(s+t)-g_c(s+t)/2)\,ds\),
equation (E82) becomes

\[
 \boxed{
 \frac12c^THc
 =\left\langle
 \left(\frac d{ds}-\frac12\right)g_c,
 V_{k_c}g_c\right\rangle_{L^2(0,\infty)}.}          \tag{E85}
\]

The span of the exponentials \(e^{-xs}\), \(x>1/2\), is the precise trial
space.  Thus an OS/transfer-matrix route would have to prove accretivity of
(E85), with the nonlinear Rayleigh centering \(C_c\), on all of these finite
spans.  Positivity of an unrelated transfer kernel does not imply this
statement.  Conversely, accretivity here for every finite span is already
the Pick criterion, so it may not be imported as an assumption.

### What the positive theta kernel does, and does not, supply

Up to an irrelevant positive normalization, Riemann's Fourier formula gives
an even positive measure \(\mu\) such that

\[
 A(x)=\xi(1/2+x)=\int_{\mathbb R}e^{xt}\,d\mu(t),
 \qquad
 L(x)=\frac{A'(x)}{A(x)}.                            \tag{E86}
\]

If \(\mu_x=A(x)^{-1}e^{xt}\mu\), then

\[
 L(x)=\mathbb E_{\mu_x}T,\qquad
 L'(x)=\operatorname{Var}_{\mu_x}(T)>0.             \tag{E87}
\]

These identities are unconditional and explain the first covariance layer.
They do not imply positivity of
\((L(x)+L(y))/(x+y)\).  This failure is already visible for a two-frequency
positive measure.  Take

\[
 A_{1/10}(x)=\cosh x+\frac1{10}\cosh(2x).
\]

It is the bilateral Laplace transform of a positive even four-atom measure.
Writing \(z=\cosh x\), its zeros satisfy

\[
 2z^2+10z-1=0,\qquad
 z_-=\frac{-5-3\sqrt3}{2}<-1.
\]

Hence it has zeros

\[
 x=\pm\operatorname{arcosh}\left(\frac{5+3\sqrt3}{2}\right)
   +(2k+1)i\pi,\qquad k\in\mathbb Z,                \tag{E88}
\]

off the imaginary axis.  Positivity of the underlying measure, moment
convexity, and the variance identity (E87) therefore stop strictly before the
Pick property.

There is also a source-specific obstruction to strengthening this route to
total positivity.  Micha\l{}owski (2026) gives an interval-arithmetic
certificate that the classical de Bruijn--Newman kernel \(\Phi(|u|)\) is not
PF\(_5\), via a negative \(5\times5\) Toeplitz minor.  That external
certificate has not been independently rerun in this repository, so it is a
literature gate rather than evidence for (E71).  Together with (E88), it
rules out using generic positive-kernel or PF\(_\infty\) machinery as the
missing sign theorem.  Any successful theta argument must exploit a weaker,
source-specific property that acts directly on (E82) or (E85).

### A single arithmetic uniqueness sequence

The accumulation-set formulation (EC) is not the smallest exact data set.
There is a useful discrete replacement which keeps every sample in the Euler
half-plane.  Put

\[
 \eta_n=n+\frac12,\qquad n=1,2,\ldots,
\]

and let \(\mathsf H_N\) be the leading \(N\times N\) matrix

\[
 \boxed{(\mathsf H_N)_{ij}
   =\frac{L(i+\frac12)+L(j+\frac12)}{i+j+1},
   \qquad 1\le i,j\le N.}                            \tag{E89}
\]

Then

\[
 \boxed{\mathrm{RH}\quad\Longleftrightarrow\quad
        \mathsf H_N\succeq0\quad\hbox{for every }N\ge1.}           \tag{E90}
\]

Here is the point that makes the sparse sequence complete.  Positivity of
all leading matrices is equivalent, by (E5), to positivity of every finite
Pick matrix for the data
\(F_\Xi(i\eta_n)\).  Nevanlinna--Pick compactness therefore gives a
Herglotz function \(h\) which interpolates the whole sequence.  Restrict to
the half-plane \(\mathbb H_1=\{\operatorname{Im}z>1\}\).  Both \(h\) and
\(F_\Xi\) are of bounded type there: for the latter this follows after the
functional equation from

\[
 F_\Xi(z)=\frac{i}{c_\Xi}
 \left(\frac{\xi'}{\xi}\!\left(\frac12-iz\right)\right)^{-1}
\]

and the bounded-type property of \(\xi'/\xi\) in every half-plane
\(\operatorname{Re}s>1+\delta\).  But the shifted nodes violate the
Blaschke condition, since

\[
 \sum_{n\ge1}
 \frac{\eta_n-1}{1+(\eta_n-1)^2}
 =\sum_{n\ge1}\frac{n-\frac12}{1+(n-\frac12)^2}=\infty.             \tag{E91}
\]

Consequently the bounded-type meromorphic function \(h-F_\Xi\), which
vanishes at every node, is identically zero.  Analytic continuation makes
\(F_\Xi\) Herglotz on \(\mathbb C_+\), and hence gives RH.  This is the
non-Blaschke uniqueness mechanism developed by Hinkkanen (1997); it replaces
an interior accumulation point by an arithmetic uniqueness set at infinity.
It does not prove the required matrix positivity.

The benefit of the half-integer choice is algebraic.  Set

\[
 \ell_n=L\!\left(n+\frac12\right)=a_n-m_n,
\]

where

\[
 a_n=\frac1n+\frac1{n+1}-\frac12\log\pi
      +\frac12\psi\!\left(\frac{n+1}{2}\right),
 \qquad
 m_n=\sum_{r\ge2}\frac{\Lambda(r)}{r^{n+1}}.                       \tag{E92}
\]

Thus \((m_n)_{n\ge1}\) is an ordinary Hausdorff moment sequence after an
index shift.  Indeed the positive measure

\[
 d\mu(u)=\sum_{r\ge2}\frac{\Lambda(r)}{r^2}\,\delta_{1/r}(du),
 \qquad m_n=\int_{(0,1/2]}u^{n-1}\,d\mu(u)                       \tag{E93}
\]

is finite, with total mass \(m_1=-\zeta'(2)/\zeta(2)\).

Let \(C_{ij}=1/(i+j+1)\), the shifted Hilbert moment matrix, and let
\(D_\ell=\operatorname{diag}(\ell_1,\ell_2,\ldots)\).  Equation (E89)
is the exact anticommutator

\[
 \mathsf H=D_\ell C+CD_\ell.                                     \tag{E94}
\]

Equivalently, on \(t\mathbb R[t]\subset L^2(0,1)\), define the diagonal
Euler multiplier

\[
 \mathcal L(t^n)=\ell_n t^n,
 \qquad
 \mathcal A(t^n)=a_n t^n,
 \qquad
 (\mathcal D_u p)(t)=p(ut).
\]

For \(p(t)=\sum_{n=1}^N c_nt^n\), direct integration gives

\[
 c^T\mathsf H_Nc=2\langle p,\mathcal Lp\rangle_{L^2(0,1)},
 \qquad
 \mathcal L=\mathcal A-
   \sum_{r\ge2}\frac{\Lambda(r)}r\mathcal D_{1/r}.                \tag{E95}
\]

Therefore (E90) is the single explicit accretivity statement

\[
 \boxed{
 \langle p,\mathcal A p\rangle
 \ge \sum_{r\ge2}\frac{\Lambda(r)}r
        \langle p,\mathcal D_{1/r}p\rangle
 \quad\text{for every }p\in t\mathbb R[t].}                       \tag{E96}
\]

This form connects the Euler product to the transfer-matrix language without
introducing zero data.  Indeed the unitary map

\[
 (Up)(v)=e^{-v/2}p(e^{-v}):L^2(0,1)\longrightarrow L^2(0,\infty)
\]

satisfies

\[
 U\mathcal D_{1/r}U^{-1}=\sqrt r\,S_{\log r},
 \qquad U(t\partial_t)U^{-1}=-\partial_v-\frac12.                 \tag{E97}
\]

Thus (E96) is the lattice-exponential restriction of the translation gate
(E84)--(E85).  The non-Blaschke argument proves that this restricted trial
space is already complete for RH; it does not make its accretivity automatic.

There is also an exact warning against treating the prime moments as a
positive block.  For

\[
 P_{ij}=\frac{m_i+m_j}{i+j+1},\qquad i,j\in\{1,2\},
\]

write \(q=m_2/m_1\).  Since the support in (E93) lies in \((0,1/2]\),
one has \(0<q\le1/2\), while

\[
 \boxed{\det P
 =m_1^2\frac{-15q^2+34q-15}{240}<0.}                       \tag{E98}
\]

The polynomial in (E98) is increasing on \([0,1/2]\) and is still
\(-7/4\) at \(q=1/2\).  Hence the positive Hausdorff measure of the prime
powers produces an *indefinite* symmetrized dilation block already in size
two.  Positivity of the weights, Catalan closure, or a generic moment theorem
cannot prove (E96) termwise.  Any successful proof must couple the
archimedean multiplier to the prime dilations and recover their signed
cancellation.

The complementary shortcut fails just as early: the archimedean block is
not positive by itself.  At the first two Euler nodes,

\[
 a_1=\frac32-\frac{\gamma+\log\pi}{2},\qquad
 a_2=\frac{11}{6}-\frac{\gamma+\log\pi}{2}-\log2.
\]

Hence its leading determinant is

\[
 \boxed{
 \det\left[\frac{a_i+a_j}{i+j+1}\right]_{i,j=1}^2
 =\frac{4a_1a_2}{15}-\frac{(a_1+a_2)^2}{16}<0.}   \tag{E98a}
\]

For a fully elementary enclosure, the standard decimal bounds on
\(\gamma,\log2,\log\pi\) give
\(0.6390<a_1<0.6391\) and \(0.2792<a_2<0.2793\).  Therefore the displayed
determinant is less than

\[
 \frac{4(0.6391)(0.2793)}{15}
 -\frac{(0.6390+0.2792)^2}{16}
 <-0.00509.
\]

Thus neither summand in (E95) supplies a positive background form.  The
successful low-order matrices already rely on signed archimedean--prime
cancellation; a relative-bound proof cannot begin by discarding that
cancellation on either side.

### Jacobi coordinates close the first infinite band

The Hilbert form in (E95) has a canonical orthogonal basis.  Let \(p_n\) be
the monic degree-\(n\) polynomial obtained from the shifted Jacobi polynomial

\[
 p_n(t)=\frac{tP_{n-1}^{(0,2)}(2t-1)}{\binom{2n}{n-1}},
 \qquad n\ge1.
\]

It is orthogonal to \(t,t^2,\ldots,t^{n-1}\) in \(L^2(0,1)\), and direct
Jacobi algebra gives

\[
 [t^{n-1}]p_n=-\frac{n^2-1}{2n},
 \qquad
 h_n:=\|p_n\|_2^2
 =\frac1{(2n+1)\binom{2n}{n-1}^2}.                 \tag{E99}
\]

Put \(e_n=p_n/\sqrt{h_n}\), and write the symmetric matrix of the real part
of \(\mathcal L\) in this basis as

\[
 B_{mn}=\langle e_m,\mathcal Le_n\rangle
       +\langle\mathcal Le_m,e_n\rangle.
\]

Since \(\mathcal L\) preserves degree and is diagonal on monomials, its
matrix in the \(p_n\) basis is triangular.  Equations (E92) and (E99) then
give the exact first band

\[
 \boxed{B_{nn}=2\ell_n,\qquad
 B_{n-1,n}=\sqrt{4n^2-1}\,(\ell_n-\ell_{n-1}).}     \tag{E100}
\]

Consequently every adjacent principal block is positive semidefinite exactly
when

\[
 \boxed{
 4\ell_{n-1}\ell_n
 -(4n^2-1)(\ell_n-\ell_{n-1})^2\ge0.}              \tag{E101}
\]

This whole infinite family can be closed unconditionally.  For
\(2\le n\le233\), it is a compression of the finite matrices already proved
positive in (E71).  For \(n\ge234\), write
\(\ell_{n-1}=\xi'(n)/\xi(n)\).  The standard inequalities

\[
 \psi(x)\ge\log x-\frac1x,qquad
 \psi_1(x)\le\frac1x+\frac1{x^2}
\]

and \(\Lambda(r)\le\log r\), followed by the integral test, give

\[
 \ell_{n-1}\ge
 \frac1{n-1}+\frac12\log\frac n{2\pi}-E_0(n)>1,                 \tag{E102}
\]

where

\[
 E_0(n)=\frac{\log2}{2^n}
 +2^{1-n}\left(\frac{\log2}{n-1}+\frac1{(n-1)^2}\right),
\]

and, throughout \(\sigma\in[n,n+1]\),

\[
 0<L'(\sigma-\tfrac12)
 \le\frac1{2\sigma}+\frac1{\sigma^2}+E_1(\sigma)
 <\frac1\sigma.                                                   \tag{E103}
\]

Here an explicit decreasing majorant is

\[
E_1(\sigma)=\frac{(\log2)^2}{2^\sigma}
 +2^{1-\sigma}\left(
 \frac{(\log2)^2}{\sigma-1}
 +\frac{2\log2}{(\sigma-1)^2}
+\frac2{(\sigma-1)^3}\right).
\]

The function \(\sigma E_1(\sigma)\) is decreasing on this range and its
value at \(234\) is less than \(1/4\).  Together with
\(1/\sigma^2<1/(4\sigma)\), this proves the final strict inequality in
(E103).  The lower bound in (E102) is increasing for \(n\ge234\) and equals
\(1.8130138\ldots\) at the endpoint.

Integrating (E103) yields
\(0<\ell_n-\ell_{n-1}<1/n\).  Substitution in (E101) gives the strict
lower bound

\[
 4\ell_{n-1}\ell_n-(4n^2-1)(\ell_n-\ell_{n-1})^2
 >4-\frac{4n^2-1}{n^2}=\frac1{n^2}>0.              \tag{E104}
\]

Thus every adjacent \(2\times2\) Jacobi block is unconditionally positive,
at every degree.  This is stronger than a finite-order computation but is
still not RH: positive adjacent blocks do not imply positivity of the whole
matrix.

The next coupling is also explicit.  With
\(\Delta_n=\ell_n-\ell_{n-1}\), the same triangular calculation gives

\[
 \boxed{
 B_{n-2,n}=\sqrt{(2n-3)(2n+1)}
 \bigl(n\Delta_n-(n-1)\Delta_{n-1}\bigr).}          \tag{E105}
\]

Hence the first genuinely new tail obstruction is not the nearest-neighbour
slope but the weighted curvature in (E105), followed by the longer Jacobi
bands.  In fact every band has a closed finite formula.  Write

\[
 p_n(t)=\sum_{k=1}^n a_{n,k}t^k,
\]

where

\[
 a_{n,k}=(-1)^{n-k}\binom{n-1}{k-1}
 \frac{(n+k)!}
 {(n-1)!(k+1)!\binom{2n}{n-1}}.                    \tag{E106}
\]

The projection of a monomial onto the monic Jacobi polynomial is

\[
 r_{m,k}:=\frac{\langle p_m,t^k\rangle}{h_m}
 =\frac{(2m+1)!(k+1)!}{(m+1)!(k+m+1)!}
   \binom{k-1}{m-1}.                                \tag{E107}
\]

Therefore, for \(m<n\), the complete upper triangle is

\[
 \boxed{
 B_{m,n}=\sqrt{\frac{h_m}{h_n}}
 \sum_{k=m}^n a_{n,k}r_{m,k}\ell_k.}               \tag{E108}
\]

The coefficients in the sum vanish on constant sequences when \(m<n\), so
(E108) is an explicit weighted finite-difference hierarchy.  Equations
(E100) and (E105) are its first two cases.

An absolute row-sum proof, however, is already too strong for the elementary
positive-real atoms which generate the RH-side kernel.  Take

\[
 f_a(x)=\frac{2x}{x^2+a^2}\qquad(a>0).
\]

Its kernel has the rank-two Gram factorization

\[
 \boxed{
 \frac{f_a(x)+f_a(y)}{x+y}
 =2\frac{xy+a^2}{(x^2+a^2)(y^2+a^2)}.}             \tag{E109}
\]

Thus it is positive semidefinite on every finite set.  Nevertheless, choose
\(a=1\) and the first three arithmetic nodes.  Then

\[
 (\ell_1,\ell_2,\ell_3)
 =\left(\frac{12}{13},\frac{20}{29},\frac{28}{53}\right).
\]

In the orthonormal Jacobi basis, exact rational arithmetic gives

\[
 B_{22}=\frac{40}{29},\qquad
 B_{12}^2=\frac{116160}{142129}>\frac{81}{100},
 \qquad
 B_{23}^2=\frac{2152640}{2362369}>\frac{81}{100}.   \tag{E110}
\]

Both off-diagonal entries are negative, so

\[
 |B_{12}|+|B_{23}|>\frac95>\frac{40}{29}=B_{22}.   \tag{E111}
\]

The matrix is PSD by (E109) but is not diagonally dominant.  Consequently a
full absolute row-sum estimate cannot be extracted from positivity of the
individual spectral atoms and is not a necessary feature of the target.
The continuation target after (E108) must preserve cancellations between
Jacobi bands--for example through a block Gram factorization--rather than
replace every band by its absolute value.

There is nevertheless enough decay to close the next *fixed* local block.
Let

\[
 g(\sigma)=\frac d{d\sigma}\frac{\xi'(\sigma)}{\xi(\sigma)},
 \qquad r(\sigma)=g(\sigma)-\frac1{2\sigma}.
\]

The series formulas for \(\psi_1\) and \(\psi_2\), together with the same
integral test used in (E102)--(E103), give for \(\sigma\ge233\)

\[
 \boxed{
 |r(\sigma)|\le\frac3{(\sigma-1)^2},
 \qquad 0\le r'(\sigma)\le\frac4{(\sigma-1)^3}.}     \tag{E112}
\]

For the derivative bound, the remaining prime term is at most

\[
 E_2(\sigma)=\frac{(\log2)^3}{2^\sigma}
 +2^{1-\sigma}\left(
 \frac{(\log2)^3}{\sigma-1}
 +\frac{3(\log2)^2}{(\sigma-1)^2}
 +\frac{6\log2}{(\sigma-1)^3}
 +\frac6{(\sigma-1)^4}\right),
\]

and \(E_2(233)<2/232^3\).  This supplies the lower sign in the second
inequality of (E112); the upper sign follows from the integral bounds for
\(-\psi_2\).  Likewise \(E_1(233)<1/232^2\); the relevant products with
\(\sigma\) are decreasing, so these comparisons persist throughout the
tail.

Write \(d_n=\int_n^{n+1}r(\sigma)\,d\sigma\).  Then

\[
 \Delta_n=\frac12\log\left(1+\frac1n\right)+d_n,
\]

and (E112) yields

\[
 \Delta_n\le\frac1{2n}+\frac3{(n-1)^2},                         \tag{E113}
\]

\[
 \left|n\Delta_n-(n-1)\Delta_{n-1}\right|
 \le\frac1{4(n-1)^2}+\frac{7n-6}{(n-2)^3}.                     \tag{E114}
\]

Indeed \(x\log(1+1/x)\) has derivative between zero and
\(1/(2x^2)\), while
\(|d_n-d_{n-1}|\le4/(n-2)^3\).  It follows from (E100) and (E105) that,
for \(k\ge233\) and \(n\ge234\),

\[
 |B_{k-1,k}|<A_*:=1+\frac{6\cdot233}{232^2}
 =1.025974\ldots,
\]

\[
 |B_{n-2,n}|<C_*:=2\cdot234\left(
 \frac1{4\cdot233^2}+\frac{7\cdot234-6}{232^3}\right)
 =0.063321\ldots.                                      \tag{E115}
\]

On the other hand (E102), now at \(233\), gives

\[
 B_{jj}=2\ell_j>3.62178\qquad(j\ge232).
\]

Every consecutive \(3\times3\) block with largest index at least \(234\)
is therefore strictly diagonally dominant, since even the deliberately
overcounted row sum \(2A_*+C_*<2.116\).  Blocks ending at index at most
\(233\) are compressions of (E71).  Hence

\[
 \boxed{
 B[\{n-2,n-1,n\}]\succeq0\quad\text{for every }n\ge3.}           \tag{E116}
\]

This is a second unconditional infinite-band theorem.  It still does not
control nonconsecutive triples or blocks whose bandwidth grows with their
degree.  Those long-range couplings are now the first remaining Jacobi
obstruction.

There is a natural operator-calculus interpretation of the same arithmetic
matrix tower.  Define the unitary map

\[
 (Up)(v)=e^{-v/2}p(e^{-v}),\qquad
 U:L^2(0,1)\longrightarrow L^2(0,\infty).
\]

On the polynomial core it conjugates the Euler generator to a translation
generator:

\[
 \boxed{
 U\left(t\frac d{dt}+\frac12\right)U^{-1}
 =\mathfrak D:=-\frac d{dv}.}                       \tag{E117}
\]

The operator \(-\mathfrak D=d/dv\), with its maximal translation domain,
generates the left-translation contraction semigroup
\((S_r f)(v)=f(v+r)\).  Hence \(\mathfrak D\) is maximal accretive.  Moreover

\[
 \mathfrak D e^{-(n+1/2)v}=(n+1/2)e^{-(n+1/2)v},
\]

so the multiplier in (E96) is precisely the functional calculus

\[
 \boxed{U\mathcal L U^{-1}=L(\mathfrak D),\qquad
 L(z)=\frac{\xi'(1/2+z)}{\xi(1/2+z)}}               \tag{E118}
\]

on the span of these exponentials.  This suggests a short sufficient route.
If \(L\) were a Bernstein function, its Levy--Khintchine representation

\[
 L(z)=a+bz+\int_0^\infty(1-e^{-rz})\,d\mu(r)
\]

would give

\[
 \operatorname {Re}\langle f,L(\mathfrak D)f\rangle
 =a\lVert f\rVert^2+b\operatorname {Re}\langle f,\mathfrak Df\rangle
 +\int_0^\infty
   \operatorname {Re}\langle f,(I-S_r)f\rangle\,d\mu(r)\ge0. \tag{E119}
\]

Here every term is nonnegative because \(\mathfrak D\) is accretive and
\(S_r\) is contractive.  Equation (E119) would prove the whole arithmetic
Pick tower without estimating its individual Jacobi bands.

This shortcut, however, fails by a strict unconditional sign.  In the
absolutely convergent Euler region,

\[
 \boxed{
 L'''\!\left(\frac52\right)
 =-6\left(\frac1{3^4}+\frac1{2^4}\right)
 +\frac{\pi^4-96}{16}
 +\sum_{n\ge2}\frac{\Lambda(n)(\log n)^3}{n^3}.}    \tag{E120}
\]

Let

\[
 T=6\left(\frac1{3^4}+\frac1{2^4}\right)
   -\frac{\pi^4-96}{16}
  =0.3610058844489217467\ldots.
\]

Direct enumeration of prime powers through \(R=10^5\), using
\(\Lambda(p^k)(\log p^k)^3/p^{3k}=k^3(\log p)^4/p^{3k}\), gives

\[
 S_R=0.3606577241464848909\ldots.
\]

Since \(\Lambda(n)\le\log n\) and \((\log x)^4/x^3\) is decreasing on
this tail,

\[
 \begin{aligned}
 0\le\sum_{n>R}\frac{\Lambda(n)(\log n)^3}{n^3}
 &\le\int_R^\infty\frac{(\log x)^4}{x^3}\,dx\\
 &=\frac1{R^2}\left(\frac{(\log R)^4}{2}+(\log R)^3
 +\frac32(\log R)^2+\frac32\log R+\frac34\right)\\
 &=1.0527263128402504\ldots\,10^{-6}.               \tag{E121}
 \end{aligned}
\]

Consequently

\[
 \boxed{L'''\!\left(\frac52\right)
 <-0.0003471075761240<0.}                           \tag{E122}
\]

For a Bernstein function the derivative is completely monotone, in
particular \(L'''\ge0\).  Thus \(L\) is not Bernstein, and generic positive
semigroup subordination cannot prove (E89).  This does **not** refute the
positive-real/Herglotz property of \(L\): that larger property is exactly the
RH-side Pick criterion.  The obstruction is specifically to obtaining its
positivity for free from the Bernstein subclass.

The Hardy-space boundary of the translation model does not provide a weaker
positive density.  Let \(\mathscr P:L^2(0,\infty)\to H^2(\mathbb C_+)\) be
the Paley--Wiener Laplace transform.  If
\(A_0=d/dv\) has domain \(H^1_0(0,\infty)\), then

\[
 \mathscr P A_0\mathscr P^{-1}=M_z,
 \qquad \mathfrak D=A_0^*,
 \qquad \mathscr P\mathfrak D\mathscr P^{-1}=M_z^*.             \tag{E123}
\]

The exponentials in (E117) become the reproducing kernels
\(k_x(z)=1/(z+x)\), and

\[
 M_L^*k_x=L(x)k_x,qquad
 \langle k_x,k_y\rangle=\frac1{x+y}.                            \tag{E124}
\]

Thus the real part of \(M_L^*\) on finite kernel spans is exactly the Pick
matrix (E4), not a relaxation of it.  More sharply, put
\(\Xi(\tau)=\xi(1/2+i\tau)\).  This is real on the real axis and, wherever
\(\Xi(\tau)\ne0\),

\[
 \boxed{L(i\tau)=-i\frac{\Xi'(\tau)}{\Xi(\tau)},
 \qquad \operatorname {Re}L(i\tau)=0.}                         \tag{E125}
\]

The ordinary boundary real part is therefore zero almost everywhere,
unconditionally.  On RH, the positive Herglotz measure is singular and its
atoms sit at the critical zeros; if RH fails, \(L\) instead has poles inside
\(\mathbb C_+\).  A proof based only on an ordinary nonnegative boundary
density consequently loses the entire distinction.  It must either recover
the singular atoms or first exclude the interior poles, and the latter is
already RH.  The Hardy model clarifies the location of the missing sign but
does not weaken the Volterra gate (E85).

### One Jacobi polynomial controls every prime-dilation band

The long-range sum in (E108) has an exact compression on each individual
dilation.  For \(1\le m<n\), put \(d=n-m\) and

\[
 Q_{m,n}(u):=\langle e_m,\mathcal D_u e_n\rangle.
\]

Combining (E106)--(E107), and using
\(\binom{n-1}{k-1}\binom{k-1}{m-1}
=\binom{n-1}{m-1}\binom{n-m}{k-m}\), gives

\[
 \boxed{
 Q_{m,n}(u)=\sqrt{\frac{h_m}{h_n}},a_{n,m}u^m
 {}_2F_1(-d,m+n+1;2m+2;u).}                       \tag{E126}
\]

The terminating contiguous relation for this hypergeometric polynomial is

\[
 \boxed{
 Q_{m,n}(u)=\sqrt{\frac{h_m}{h_n}},a_{n,m}
 \frac{(d-1)!}{(2m+2)_{d-1}}u^m(1-u)
 P_{d-1}^{(2m+1,1)}(1-2u).}                       \tag{E127}
\]

This identity is coefficientwise rational.  It replaces an alternating sum
of \(d+1\) terms by one Jacobi polynomial and exposes a nontrivial constant
sign window for the prime part.

Indeed set \(\alpha=2m+1\).  The zeros of
\(P_{d-1}^{(\alpha,1)}\) are the eigenvalues of its symmetric Jacobi
recurrence matrix.  Its diagonal and off-diagonal recurrence coefficients
are

\[
 b_k=\frac{1-\alpha^2}
 {(2k+\alpha+1)(2k+\alpha+3)},
\]

\[
 c_k=\frac2{2k+\alpha+1}
 \sqrt{\frac{k(k+\alpha)(k+1)(k+\alpha+1)}
 {(2k+\alpha)(2k+\alpha+2)}}.
\]

For the truncated matrix of order \(d-1\), elementary bounds give

\[
 |b_k|\ge\frac{\alpha^2-1}{(\alpha+2d)^2},
 \qquad c_k+c_{k+1}le
 \frac{4d(\alpha+d)}{\alpha^2}.                    \tag{E128}
\]

If \(d\ge2\) and \(\alpha\ge16d\), then \(\alpha\ge32\), and

\[
 \frac{\alpha^2-1}{(\alpha+2d)^2}>\frac34,
 \qquad
 \frac{4d(\alpha+d)}{\alpha^2}\le\frac{17}{64}.   \tag{E129}
\]

Gershgorin therefore puts every zero of
\(P_{d-1}^{(\alpha,1)}\) strictly in \((-1,0)\).  Since the polynomial is
positive at \(1\), (E127) and
\(\operatorname {sgn}a_{n,m}=(-1)^d\) imply the exact sign theorem

\[
 \boxed{
 (-1)^d Q_{m,n}(u)>0
 \quad\left(0<u\le\frac12,\quad
 d\le\frac{2m+1}{16}\right).}                     \tag{E130}
\]

Consequently all prime powers agree in sign throughout this linearly growing
band.  If

\[
 \mathcal P=\sum_{r\ge2}\frac{\Lambda(r)}r\mathcal D_{1/r},
\]

then

\[
 \operatorname {sgn}\langle e_m,\mathcal P e_n\rangle=(-1)^d,
 \qquad
 \operatorname {sgn}B^{\rm prime}_{m,n}=(-1)^{d+1}.             \tag{E131}
\]

There is also an exact source-side formula for what must cancel that signed
prime band.  The elementary digamma integral

\[
 \frac12\psi\!\left(\frac{k+1}{2}\right)
 =-\frac\gamma2+
 \int_0^1\frac{u(1-u^{k-1})}{1-u^2}\,du
\]

and \(Q_{m,n}(1)=0\) give, coefficient by coefficient,

\[
 \boxed{
 B_{m,n}=\int_0^1\omega(u)Q_{m,n}(u)\,du
 -\sum_{r\ge2}\frac{\Lambda(r)}rQ_{m,n}(1/r),
 \qquad
 \omega(u)=\frac{1-u^2-u^3}{u(1-u^2)}.}            \tag{E132}
\]

The apparent endpoint singularities are removable in the pairing because
(E127) contains both \(u^m\) and \(1-u\).  The weight \(\omega\) is positive
on the whole prime support \((0,1/2]\), changes sign only at

\[
 u_*=0.754877666246693\ldots,
 \qquad u_*^3+u_*^2=1,                              \tag{E133}
\]

and is negative thereafter.  Thus, inside (E130), cancellation among prime
powers is no longer available: (E132) is literally a quadrature discrepancy
between one continuous archimedean weight and same-signed von Mangoldt atoms.
The symbolic audit evaluates both sides as an exact rational number plus an
exact rational multiple of \(\log2\); no numerical integration enters.

The discrepancy can be bounded uniformly over the first 29 tail bands.  Put

\[
 H_{m,d}(u)={}_2F_1(1-d,2m+d+2;2m+2;u),
 \qquad
 J_k=\int_0^1u^{m-1}(1-u)^kH_{m,d}(u)\,du.          \tag{E134}
\]

The shifted Rodrigues formula writes

\[
 H_{m,d}(u)=\frac{u^{-2m-1}(1-u)^{-1}}
 {(2m+2)_{d-1}}
 \frac{d^{d-1}}{du^{d-1}}
 \left[u^{2m+d}(1-u)^d\right].                     \tag{E135}
\]

For \(k\ge1\), integrate (E135) by parts \(d-1\) times.  Every term in

\[
 (-1)^{d-1}\frac{d^{d-1}}{du^{d-1}}
 \left[u^{-m-2}(1-u)^{k-1}\right]
\]

is positive.  Repeating the argument after inserting one extra factor \(u\)
shows

\[
 \boxed{J_k>J_{k+1}>0\qquad(k\ge1).}                \tag{E136}
\]

The first two moments have closed terminating beta sums.  Saalschutz gives

\[
 \boxed{
 J_1=\frac{d!(2m+1)!}{m(m+1)(2m+d)!}.}             \tag{E137}
\]

Writing \(r=(d+1)/2\) when \(d\) is odd, the adjacent beta sum gives

\[
 \boxed{
 \frac{J_0}{J_1}=
 \begin{cases}
 1,&d\ \text{even},\\[2mm]
 \displaystyle\frac1d\left(m+r+\frac{r(r-1)}{m+r}\right),
    &d\ \text{odd}.
 \end{cases}}                                      \tag{E138}
\]

The cancellation in (E132) is now elementary.  With \(y=1-u\),

\[
 \frac1{1+u}-u^2
 =-\frac12+\frac94y-\frac78y^2
 +\sum_{k\ge3}\frac{y^k}{2^{k+1}}.                \tag{E139}
\]

Define

\[
 G_{m,d}=\binom{2m+d}{d}
 \sqrt{\frac{2m+2d+1}{2m+1}},
 \qquad
 A_{m,d}:=G_{m,d}J_1
 =\frac{\sqrt{(2m+1)(2m+2d+1)}}{m(m+1)}.
\]

Equations (E127), (E132), and (E139) give

\[
 B^{\rm arch}_{m,m+d}=(-1)^dG_{m,d}
 \left(-\frac12J_0+\frac94J_1-\frac78J_2+T\right),
 \qquad 0<T\le\frac18J_1,                         \tag{E140}
\]

where (E136) bounds the positive geometric tail.  If \(d\) is even,
(E136), (E138), and (E140) imply

\[
 0<B^{\rm arch}_{m,m+d}<\frac{15}{8}A_{m,d}
 <\frac1{50}
 \qquad(m\ge232,\ 2\le d\le28).                  \tag{E141}
\]

For odd \(d\), put

\[
 R_{m,d}=\frac1d\left(m+r+\frac{r(r-1)}{m+r}\right).
\]

Then

\[
 A_{m,d}\left(\frac{R_{m,d}}2-\frac{19}{8}\right)
 <B^{\rm arch}_{m,m+d}<
 A_{m,d}\left(\frac{R_{m,d}}2-\frac{11}{8}\right)
 <\frac1d.                                         \tag{E142}
\]

For the registered range, \(R_{m,d}\ge m/d\ge232/29>19/4\), so the
lower bound is positive.  For the last upper bound use
\(\sqrt{(2m+1)(2m+2d+1)}\le2m+d+1\) and
\(r(r-1)/(m+r)\le r(r-1)/m\).  After clearing positive denominators, the
required inequality reduces to

\[
 14dm^2+7d(d+1)m-(d-1)(d+1)^2>0,
\]

which is immediate for \(m\ge232\) and \(1\le d\le29\).

It remains to bound the discrete prime term.  The
[classical Jacobi endpoint maximum inequality](https://dlmf.nist.gov/18.14.E1),
applicable because \(2m+1\ge1\), gives
\(|H_{m,d}(u)|\le1\) on \([0,1]\).  Therefore

\[
 \begin{aligned}
 |B^{\rm prime}_{m,m+d}|
 &\le G_{m,d}\sum_{r\ge2}\frac{\Lambda(r)}{r^{m+1}}\\
 &<G_{m,d}2^{-m}\\
 &<2\left(\frac{3(2m+d)}d\right)^d2^{-m}
 <10^{-20}                                          \tag{E143}
 \end{aligned}
\]

for \(m\ge232\) and \(1\le d\le29\).  Here
\(\Lambda(r)\le\log r\), the integral test makes its moment less than
\(2^{-m}\), and
\(\binom{2m+d}{d}\le(e(2m+d)/d)^d\) with \(e<3\).  The last elementary
majorant decreases with \(m\); checking the 29 exact rational values at
\(m=232\) gives its maximum

\[
 9.585308795674\ldots\,10^{-21}qquad(d=29).
\]

Combining (E141)--(E143),

\[
 |B_{m,m+d}|<
 \begin{cases}
 d^{-1}+10^{-20},&d\ \text{odd},\\
 1/50+10^{-20},&d\ \text{even},
 \end{cases}
 \quad(m\ge232,\ 1\le d\le29).                    \tag{E144}
\]

Every principal \(3\times3\) Jacobi block whose smallest index is at least
232 and whose diameter is at most 29 is therefore strictly diagonally
dominant: each off-diagonal row sum is less than
\(2+2\cdot10^{-20}\), while (E115) gives every diagonal entry greater than
3.62178.  Hence

\[
 \boxed{
 B[\{i,j,k\}]\succ0
 \quad(232\le i<j<k,\ k-i\le29).}                  \tag{E145}
\]

This strictly extends (E116) from consecutive triples to every triple in a
width-29 tail window, with parity-sensitive bounds.  A coarser estimate below
enlarges that window further.

The sign window is not needed for a coarser absolute estimate, so the local
diameter can be enlarged once more.  Equations (E136) and (E140) give for
every \(d\ge1\)

\[
 |B^{\rm arch}_{m,m+d}|<
 \begin{cases}
 \displaystyle A_{m,d}\left(\frac{R_{m,d}}2+\frac{13}{4}\right),
     &d\ \text{odd},\\[2mm]
 \displaystyle\frac{15}{8}A_{m,d},&d\ \text{even}.
 \end{cases}                                       \tag{E146}
\]

For \(m\ge232\), use

\[
 A_{m,d}\le\frac2m+\frac{d+1}{m^2},
\]

and, for odd \(d\) with \(r=(d+1)/2\),

\[
 \frac{R_{m,d}}2+\frac{13}{4}
 \le\frac{m}{2d}+\frac{r}{2d}
 +\frac{r(r-1)}{2dm}+\frac{13}{4}.
\]

Every term after multiplication is a nonnegative power of \(1/m\), so the
resulting bound decreases with \(m\).  The exact rational values at \(m=232\)
therefore prove

\[
 |B^{\rm arch}_{m,m+d}|<
 \begin{cases}
 21/20,&d\ \text{odd},\\
 1/20,&d\ \text{even},
 \end{cases}
 \qquad 1\le d\le45.                              \tag{E147}
\]

The elementary prime majorant from (E143) is also decreasing in \(m\).  Over
the enlarged finite set of gaps its exact maximum is now

\[
 2\left(\frac{3(2\cdot232+45)}{45}\right)^{45}2^{-232}
 =0.2189094698801\ldots<\frac14.                    \tag{E148}
\]

No assertion about the sign of the prime polynomial is used here.  Combining
(E147)--(E148) gives the uniform absolute band estimate

\[
 \boxed{|B_{m,m+d}|<\frac{13}{10}
 \qquad(m\ge232,\ 1\le d\le45).}                   \tag{E149}
\]

The largest absolute off-diagonal row sum in a three-point compression is
therefore less than \(13/5=2.6<3.62178\).  Hence the stronger local theorem is

\[
 \boxed{
 B[\{i,j,k\}]\succ0
 \quad(232\le i<j<k,\ k-i\le45).}                  \tag{E150}
\]

The gap-46 failure of the endpoint maximum can be removed without using a
zero or a sign assumption.  Put (q=d-1) and (c=2m+2).  Pfaff's terminating
transformation gives the exact identity

\[
 H_{m,d}(u)=(1-u)^{d-1}
 {}_2F_1\left(1-d,-d;c;-\frac{u}{1-u}\right).      \tag{E151}
\]

For (u=1/p), (p\ge2), the absolute value of the last polynomial is at
most the sum of the absolute values of its coefficients.  Since
(1/(p-1)\le1), Chu--Vandermonde then gives

\[
 \boxed{
 |H_{m,d}(1/p)|\le
 \left(1-\frac1p\right)^{d-1}
 \frac{(2m+d+2)_{d-1}}{(2m+2)_{d-1}}.}            \tag{E152}
\]

Unlike the endpoint bound used in (E143), (E152) retains the exponential
factor ((1-1/p)^{d-1}).  Consequently, if

\[
 S_{m,d}:=\sum_{r\ge2}\log r\,r^{-m-1}(1-1/r)^d,
 \qquad
 C_{m,d}:=\frac{(2m+d+2)_{d-1}}{(2m+2)_{d-1}},
\]

then

\[
 |B^{\rm prime}_{m,m+d}|\le G_{m,d}C_{m,d}S_{m,d}. \tag{E153}
\]

This infinite sum has a completely rational majorant.  Its summand is
decreasing for (r\ge3) when (d<2m).  Keep (r=2,3), bound the remainder
by its integral from (3) to infinity, substitute (u=1/r), and split the
integral at (u=1/4).  On ([1/4,1/3]), the logarithmic derivative of
(u^{m-1}(1-u)^d) is at least
(lambda=3(m-1)-3d/2).  Using
(log2<1) and (log3,log4<3/2) yields

\[
\begin{aligned}
 S_{m,d}<&\;2^{-m-d-1}
 +\frac32\frac{2^d}{3^{m+d+1}}
 +4^{-m}\left(\frac3{2m}+\frac1{m^2}\right)\\
 &+\frac32\frac{2^d}{3^{m+d-1}
       \left(3(m-1)-3d/2\right)}.                 \tag{E154}
\end{aligned}
\]

Every constant in (E154) is rational.  In the range (m\ge232),
(d\le68),

\[
 \sqrt{\frac{2m+2d+1}{2m+1}}<\frac87,
 \qquad
 \frac{\binom{2m+d+2}{d}}{\binom{2m+d}{d}}<\frac32.
\]

The Chu factor (C_{m,d}) decreases with (m), while every summand on the
right of (E154) loses at least a factor (2) when (m) is increased by
one.  Hence the resulting prime majorant decreases with (m).  Exact
rational evaluation at (m=232) gives

\[
 |B^{\rm prime}_{m,m+d}|<
 \begin{cases}
 1/3,&d\text{ odd},\\
 8/5,&d\text{ even},
 \end{cases}
 \qquad 1\le d\le68,                              \tag{E155}
\]

with the parity maxima
\(0.3153321955186\ldots\) at \(d=67\) and
\(1.5634365835641\ldots\) at \(d=68\).  The archimedean estimates in
(E146)--(E147) remain valid over this enlarged range, so

\[
 |B_{m,m+d}|<
 \begin{cases}
 83/60,&d\text{ odd},\\
 33/20,&d\text{ even}.
 \end{cases}                                      \tag{E156}
\]

Thus every off-diagonal row sum in a three-point compression is less than
\(33/10=3.3<3.62178\).  Strict diagonal dominance proves the larger local
theorem

\[
 \boxed{
 B[\{i,j,k\}]\succ0
 \quad(232\le i<j<k,\ k-i\le68).}                 \tag{E157}
\]

This argument is unconditional and uses neither RH nor verified zero data.
At gap 69 the same Pfaff--Chu majorant is \(7.6759\ldots>7\), so it no
longer fits the diagonal budget.  This is again a failure of this absolute
majorant, not a negative matrix witness.

The cancellation at the central value can in fact be retained by a contour
estimate.  Specialize Lemma 2 (the two-integral representation) of
[Szehr--Zarouf](https://arxiv.org/abs/1605.02509) to
\(\lambda=2^{-1/2}\), \(\alpha=0\), \(\beta=1\), \(n=d-1\), and
\(a=(2m+1)/n\).  Since \(an+\alpha=2m+1\) is an integer, the second
integral, whose coefficient is \(\sin(\pi(an+\alpha))\), vanishes.  Taking absolute values on the
circle of radius \(x\in(\lambda,1)\) gives

\[
\left|\lambda^{2m+1}(1-\lambda^2)
P_{d-1}^{(2m+1,1)}(0)\right|
\le
x^{2m+d+1}\left(\frac{1-\lambda x}{x-\lambda}\right)^d.
                                                               \tag{E158}
\]

This specializes the amplitude before taking the maximum: when \(\beta=1\),
its remaining Blaschke quotient is the same quotient as in the \(n\)-th
power, so the general-purpose prefactor can be absorbed as one additional
power.  Combining (E158) with (E127),
\(P_{d-1}^{(2m+1,1)}(1)=\binom{2m+d}{d-1}\), and
\(\binom{2m+d}{d}/\binom{2m+d}{d-1}=(2m+1)/d\), yields

\[
\boxed{
|Q_{m,m+d}(1/2)|\le
\sqrt{\frac{2m+2d+1}{2m+1}}\frac{2m+1}{d}\sqrt2\,
x^{2m+d+1}\left(\frac{1-\lambda x}{x-\lambda}\right)^d.}
                                                        \tag{E159}
\]

For a rational certificate use \(x_d=89/100\) through \(d=85\), followed by

\[
\begin{array}{c|ccccccc}
d&86&87&88&89&90&91&92\\ \hline
x_d&9/10&181/200&91/100&229/250&461/500&116/125&187/200.
\end{array}
\]

The exact rational enclosures are

\[
\frac{7071}{10000}<\lambda<\frac{7072}{10000},
\qquad
\sqrt2<\frac{14143}{10000},
\qquad
\sqrt{\frac{2m+2d+1}{2m+1}}<\frac65
\]

for \(m\ge232\), \(2\le d\le92\).  Replacing each occurrence in (E159)
in the direction that enlarges the right-hand side gives the rational bound

\[
\boxed{
U_{m,d}:=\frac65\frac{2m+1}{d}\frac{14143}{10000}
x_d^{2m+d+1}
\left(\frac{1-\underline\lambda x_d}
{x_d-\overline\lambda}\right)^d,}
\qquad
\underline\lambda=\frac{7071}{10000},\quad
\overline\lambda=\frac{7072}{10000}.              \tag{E160}
\]

Thus the \(p=2\) contribution is less than \(U_{m,d}/2\).  For \(p\ge3\)
use (E152)--(E154) with the first, \(r=2\), summand removed.  The resulting
bound decreases with \(m\): explicitly

\[
\frac{U_{m+1,d}}{U_{m,d}}
=x_d^2\frac{2m+3}{2m+1}<1,
\]

while the remaining Mangoldt majorant loses at least a factor \(3\), the
binomial factor gains less than \(3/2\), and the Chu factor decreases.
The archimedean bounds in (E146) decrease as well.  Exact rational
evaluation at \(m=232\) therefore proves

\[
\boxed{|B_{m,m+d}|<\frac95
\qquad(m\ge232,\ 1\le d\le92).}                   \tag{E161}
\]

The exact maximum of the registered rational majorants is
\(1.7633293899192\ldots\), at \(d=92\).  Hence every off-diagonal row sum
in a three-point compression is less than \(18/5=3.6<3.62178\), and

\[
\boxed{
B[\{i,j,k\}]\succ0
\quad(232\le i<j<k,\ k-i\le92).}                  \tag{E162}
\]

The circle maximum still discards the angular width of the peak.  That width
can be retained without stationary-phase asymptotics.  On the circle
\(z=xe^{i\theta}\), write

\[
R_x(\theta)=\left|\frac{1-\lambda xe^{i\theta}}
{xe^{i\theta}-\lambda}\right|,
\qquad y=1-\cos\theta.
\]

With

\[
a=\frac{2\lambda x}{(1-\lambda x)^2},\qquad
b=\frac{2\lambda x}{(x-\lambda)^2},
\]

direct division gives

\[
\frac{R_x(\theta)^2}{R_x(0)^2}
=\frac{1+ay}{1+by}
\le1-c_xy\le e^{-c_xy},
\qquad
c_x=\frac{\lambda x(1-x^2)}
{(1-\lambda x)^2(x+\lambda)^2}.                  \tag{E163}
\]

Indeed \(1-(1+ay)/(1+by)=(b-a)y/(1+by)\), and replacing
\(1+by\) by \(1+2b\) gives exactly the displayed \(c_x\).  Apply
Cauchy--Schwarz to the integral in (E158).  Since
\(1-\cos\theta\ge2\theta^2/\pi^2\) on \([0,\pi]\),

\[
\begin{aligned}
\left(\frac1\pi\int_0^\pi
\left(\frac{R_x(\theta)}{R_x(0)}\right)^{2d}
d\theta\right)^{1/2}
&\le
\left(\frac{\sqrt\pi}{2\sqrt{2dc_x}}\right)^{1/2}\\
&=\left(\frac{\pi}{8dc_x}\right)^{1/4}.           \tag{E164}
\end{aligned}
\]

Thus (E159) gains the multiplicative factor in (E164).  For a certificate
free of transcendental evaluation, use \(\pi<22/7\), the same rational
brackets for \(\lambda\), and

\[
\begin{array}{c|ccccc}
d&93&94&95&96&97\\ \hline
x_d&469/500&473/500&477/500&963/1000&971/1000\\
F_d&179/500&183/500&47/125&49/125&103/250.
\end{array}
\]

Exact rational fourth-power comparison proves
\[
F_d^4>\frac{11}{28d\,\underline c_{x_d}},
\]
where \(\underline c_x\) is obtained from (E163) by putting
\(\underline\lambda\) in the numerator and in \(1-\lambda x\), and
\(\overline\lambda\) in \(x+\lambda\).  Hence \(F_d\) is a rigorous upper
bound for the factor in (E164).  Combining it with the \(p\ge3\) tail from
(E154) gives, at \(d=93,94,95,96\), respectively,

\[
0.8974426128\ldots,\quad
1.1377108675\ldots,\quad
1.4653088169\ldots,\quad
1.7380655007\ldots
\]

as upper bounds for the full off-diagonal entry, including its
archimedean part.  All are below \(9/5\); the global maximum through this
range remains the \(d=92\) value in (E161).  Therefore

\[
\boxed{|B_{m,m+d}|<\frac95
\qquad(m\ge232,\ 1\le d\le96),}                   \tag{E165}
\]

and strict diagonal dominance proves

\[
\boxed{
B[\{i,j,k\}]\succ0
\quad(232\le i<j<k,\ k-i\le96).}                  \tag{E166}
\]

At \(d=97\) the same \(L^2\) majorant is
\(2.0458728881\ldots\), so it no longer fits the diagonal budget.  This is
a failure of the one-entry absolute estimate, not a negative matrix
witness.

For the scalar coefficient, Cauchy--Schwarz is unnecessary: applying the
triangle inequality directly to the integral retains the same Gaussian
profile in \(L^1\).  From (E163),

\[
\begin{aligned}
\frac1\pi\int_0^\pi
\left(\frac{R_x(\theta)}{R_x(0)}\right)^d\,d\theta
&\le\frac1\pi\int_0^\pi
e^{-dc_x(1-\cos\theta)/2}\,d\theta\\
&\le\frac{\sqrt\pi}{2\sqrt{dc_x}}.                \tag{E167}
\end{aligned}
\]

This is the missing \(d^{-1/2}\) rather than \(d^{-1/4}\) factor.  Tighten
the algebraic brackets, still rationally, to

\[
\frac{70710678}{10^8}<\lambda<\frac{70710679}{10^8},
\qquad
\sqrt2<\frac{141421357}{10^8},
\]

and use

\[
\begin{array}{c|rrrrrr}
d&97&98&99&100&101&102\\ \hline
x_d&481/500&969/1000&487/500&489/500&491/500&9841/10000\\
F_d&2133/10000&2311/10000&31/125&166/625&2893/10000&3047/10000.
\end{array}
\]

The exact inequalities
\[
F_d^2>\frac{11}{14d\,\underline c_{x_d}}
>\frac{\pi}{4d c_{x_d}}
\]
certify the factor in (E167), using only \(\pi<22/7\).  After adding the
\(p\ge3\) and archimedean bounds, the registered totals for \(d=97,\ldots,101\)
are

\[
1.1319097820\ldots,\quad
1.2844546241\ldots,\quad
1.4832644606\ldots,\quad
1.6060543736\ldots,\quad
1.7721660203\ldots.
\]

Consequently

\[
\boxed{|B_{m,m+d}|<\frac95
\qquad(m\ge232,\ 1\le d\le101),}                  \tag{E168}
\]

and

\[
\boxed{
B[\{i,j,k\}]\succ0
\quad(232\le i<j<k,\ k-i\le101).}                 \tag{E169}
\]

At \(d=102\) the same rational \(L^1\) certificate gives
\(1.8636453221\ldots>9/5\).  This moves the one-entry frontier to 102;
it does not exhibit a negative entry or principal minor.

The global quadratic estimate in (E167) is sharp at the wrong endpoint for
this integral.  Split the arc at \(\pi/2\).  Concavity of sine on
\([0,\pi/4]\) gives
\[
1-\cos\theta=2\sin^2(\theta/2)\ge\frac{4\theta^2}{\pi^2}
\quad(0\le\theta\le\pi/2),
\]
while \(1-\cos\theta\ge1\) on the complementary half.  Therefore

\[
\frac1\pi\int_0^\pi e^{-dc_x(1-\cos\theta)/2}\,d\theta
\le
\frac{\sqrt\pi}{2\sqrt{2dc_x}}+\frac12e^{-dc_x/2}. \tag{E170}
\]

Both terms admit rational certificates.  For the Gaussian term use
\(\pi<22/7\).  If \(z=dc_x/2\), then

\[
\frac12e^{-z}\le
\frac1{2(1+z+z^2/2+z^3/6+z^4/24)}.
\]

Using the same tight brackets as in (E167), together with

\[
\begin{array}{c|rrrrrr}
d&102&103&104&105&106&107\\ \hline
x_d&491/500&123/125&197/200&493/500&987/1000&247/250\\
M_d&509/2500&1069/5000&137/625&2253/10000&2321/10000&1199/5000,
\end{array}
\]

the exact checks are \(M_d^2>11/(28d\underline c_{x_d})\); the rational
Taylor denominator above supplies the tail in (E170).  Adding the
\(p\ge3\) and archimedean contributions gives, for \(d=102,\ldots,106\),

\[
1.4109050220\ldots,\quad
1.5404231153\ldots,\quad
1.6040954368\ldots,\quad
1.7230093611\ldots,\quad
1.7779607166\ldots.
\]

Hence

\[
\boxed{|B_{m,m+d}|<\frac95
\qquad(m\ge232,\ 1\le d\le106),}                  \tag{E171}
\]

and

\[
\boxed{
B[\{i,j,k\}]\succ0
\quad(232\le i<j<k,\ k-i\le106).}                 \tag{E172}
\]

At \(d=107\) the same split-arc certificate is
\(1.8882666915\ldots>9/5\).  The remaining loss is now within the main
Gaussian arc, so a further subdivision of the exponentially small tail
cannot by itself cross this frontier.

The angular majorant itself has an exact one-variable integral, so the
Gaussian replacement can be avoided.  Put \(a=dc_x/2\).  The defining
integral and power series of the modified Bessel function give

\[
 \frac1\pi\int_0^\pi e^{-dc_x(1-\cos\theta)/2}\,d\theta
 =e^{-a}I_0(a),
 \qquad
 I_0(a)=\sum_{q\ge0}\frac{(a^2/4)^q}{(q!)^2}.       \tag{E173}
\]

No transcendental evaluation is used in the certificate.  The \(I_0\)
series is stopped after \(q=16\), and its positive tail is bounded by the
geometric series whose first term is the \(q=17\) term and whose ratio is
\(a^2/(4\cdot18^2)\).  Since
\(e^a\ge\sum_{q=0}^{24}a^q/q!\), division by this latter rational sum
gives a rational upper bound for the whole expression in (E173).

At the rational radii

\[
\begin{array}{c|rrrr}
d&107&108&109&110\\ \hline
x_d&9897/10000&619/625&9911/10000&2479/2500,
\end{array}
\]

the resulting exact total bounds for \(d=107,108,109\) are

\[
1.6215085497\ldots,\qquad
1.6515948007\ldots,\qquad
1.7607492038\ldots.
\]

Consequently the entry and triple theorems improve to

\[
\boxed{|B_{m,m+d}|<\frac95
\qquad(m\ge232,\ 1\le d\le109),}                  \tag{E174}
\]

and

\[
\boxed{
B[\{i,j,k\}]\succ0
\quad(232\le i<j<k,\ k-i\le109).}                 \tag{E175}
\]

At \(d=110\) the same rational Bessel-series certificate is
\(1.9251590813\ldots>9/5\).  This is a frontier of this entrywise
diagonal-dominance estimate, not evidence of a negative entry or minor.

Indeed, using the determinant rather than a row-sum threshold crosses this
frontier.  Set

\[
D=\frac{181089}{50000}=3.62178,
\]

which is the diagonal lower bound from (E102), and let \(X_r\) denote the
rational absolute-entry bound at gap \(r\).  For a triple with consecutive
gaps \(a,b\), replace its three diagonal entries by \(D\), obtaining a
matrix \(C\).  The original compression is \(C\) plus a positive diagonal
matrix.  Irrespective of the signs of the three off-diagonal entries,

\[
\det C\ge
D^3-D\bigl(X_a^2+X_b^2+X_{a+b}^2\bigr)
-2X_aX_bX_{a+b}.
\]

The exact rational enumeration over \(a,b\ge1\), \(a+b\le110\), also checks
\(X_r<D\).  The smallest determinant certificate occurs at
\((a,b)=(1,109)\) or \((109,1)\) and is
\(11.9345327633\ldots>0\).  Sylvester's criterion for \(C\), followed by
monotonicity under addition of a positive diagonal matrix, proves

\[
\boxed{
B[\{i,j,k\}]\succ0
\quad(232\le i<j<k,\ k-i\le110).}                 \tag{E176}
\]

Thus the local theorem is no longer limited by the artificial \(9/5\)
entry threshold.  It remains a theorem about three-point compressions and
does not yet imply positivity of the infinite Jacobi operator.

The rapid loss in the Pfaff remainder at the next gap is caused almost
entirely by its first omitted integer, \(r=3\), rather than by the full
prime tail.  The contour argument is not special to \(r=2\): Lemma 2 is
stated for every \(\lambda\in(0,1)\).  Applying the same specialization
with \(\lambda=3^{-1/2}\) gives

\[
|Q_{m,m+d}(1/3)|\le
\sqrt{\frac{2m+2d+1}{2m+1}}\frac{2m+1}{d}\sqrt3\,
x^{2m+d+1}
\left(\frac{1-3^{-1/2}x}{x-3^{-1/2}}\right)^d
e^{-a_3}I_0(a_3),                                  \tag{E177}
\]

where \(a_3=dc_{3,x}/2\) and \(c_{3,x}\) is (E163) with
\(\lambda=3^{-1/2}\).  This is certified rationally with

\[
\frac{11547}{20000}<3^{-1/2}<\frac{577351}{10^6},
\qquad \sqrt3<\frac{1732051}{10^6},
\qquad x=\frac34,
\]

and the same finite-series enclosure from (E173).  The exact polynomial
value of \(Q(1/3)^2\) is checked independently.  Since
\(\log3/3<1/2\), the extracted \(r=3\) contribution is bounded by one half
of (E177); the Pfaff integral is then applied only to \(r\ge4\).

At \(d=111,112,113\), the resulting full entry bounds are

\[
1.8288571413\ldots,\qquad
1.8997569911\ldots,\qquad
2.2546519661\ldots.
\]

Re-running the sign-independent determinant certificate for every
\(a,b\ge1\), \(a+b\le113\), leaves a minimum
\(3.2507866669\ldots>0\), again at an endpoint split.  Therefore

\[
\boxed{
B[\{i,j,k\}]\succ0
\quad(232\le i<j<k,\ k-i\le113).}                 \tag{E178}
\]

This extraction exposes a repeatable analytic mechanism: when the Pfaff
tail becomes dominated by its smallest retained prime power, that term can
be moved to its own contour before bounding the remainder.  It still does
not supply the global coercivity needed for RH.

The next retained integer is the prime power \(r=4\), with
\(\Lambda(4)=\log2\).  Here \(\lambda=1/2\) is rational, so the contour
certificate uses no algebraic brackets; take \(x=13/20\) and the
normalization bound \(247/200\).  The extracted coefficient obeys
\(\Lambda(4)/4<1/4\).  For the remaining integers, the Pfaff-weighted
summand is decreasing on \([4,\infty)\) in the registered range, and

\[
\begin{aligned}
\sum_{r\ge5}\log r\,r^{-m-1}(1-1/r)^d
&\le\int_4^\infty\log x\,x^{-m-1}(1-1/x)^d\,dx\\
&\le4^{-m}\left(\frac{3}{2m}+\frac1{m^2}\right).
                                                               \tag{E179}
\end{aligned}
\]

For monotonicity, the logarithmic derivative is at most
\(x^{-1}(1-(m+1)+d/3)<0\), using \(d<2(m-1)\).  The last line of (E179)
uses \(\log4<3/2\).  Exact contour comparisons for
\(Q(1/2)^2,Q(1/3)^2,Q(1/4)^2\), followed by the integral tail, give the
entry bounds

\[
\begin{array}{c|rrrrrrrrr}
d&114&115&116&117&118&119&120&121&122\\ \hline
X_d&1.92318&1.98665&1.98965&2.04886&2.04831&2.10366&
2.09968&2.15302&2.15488.
\end{array}
\]

All displayed decimals round the exact rational upper bounds upward.  The
determinant enumeration over \(a+b\le122\) remains positive; its minimum is
\(0.3884147136\ldots\) at \((a,b)=(1,121)\) or its reversal.  Hence

\[
\boxed{
B[\{i,j,k\}]\succ0
\quad(232\le i<j<k,\ k-i\le122).}                 \tag{E180}
\]

The shrinking determinant margin is a quantitative warning: repeated
extraction improves the certified bandwidth, but a proof of the infinite
operator still needs a uniform block mechanism rather than a finite list
of separated dilations.

There is nevertheless a uniform finite-place reduction in a linear wedge.
Extract all integers \(2\le r\le145\).  For
\(1\le d<2(m-1)\), the Pfaff-weighted summand is decreasing from 145 onward,
and the integral test gives

\[
\sum_{r\ge146}\log r\,r^{-m-1}(1-1/r)^d
\le145^{-m}\left(\frac{H_{144}}m+\frac1{m^2}\right)
<4\,145^{-m}.                                      \tag{E181}
\]

The remaining algebraic factors admit bounds independent of \(d\) in this
wedge:

\[
\sqrt{\frac{2m+2d+1}{2m+1}}<2,qquad
\binom{2m+d}{d}\le16^m,qquad
\frac{(2m+d+2)_{d-1}}{(2m+2)_{d-1}}<9^m.
\]

For the last inequality, each of the fewer than \(2m\) factors is below
three.  Since \(H_{144}<6\), multiplication with (E181) proves the uniform
prime-tail estimate

\[
\boxed{
\operatorname{Tail}_{m,d}(r\ge146)
<8\left(\frac{144}{145}\right)^m
\qquad(1\le d<2(m-1)).}                            \tag{E182}
\]

For \(d\ge2\), the apparent loss outside this linear wedge comes from keeping the contour
radius fixed while the Jacobi parameter changes.  A moving radius restores
the missing power of the dilation.  Put

\[
 a=2m+1,
 \qquad
 t=1+\frac d a=\frac{2m+d+1}{2m+1}.
\]

For an integer \(r>t^2\), specialize the general form of (E159) to
\(\lambda=r^{-1/2}\) and choose \(x=t\lambda\).  This is an admissible
contour radius.  Moreover

\[
 \frac{1-\lambda x}{x-\lambda}
 =\sqrt r\,\frac{1-t/r}{t-1}.
\]

The powers of \(r\) in (E159) then cancel exactly down to \(r^{-m}\).
Writing
\(N_{m,d}=\sqrt{(2m+2d+1)/(2m+1)}=\sqrt{2t-1}\) gives the all-gap
estimate

\[
 \boxed{
 |Q_{m,m+d}(1/r)|
 \le C_{m,d}\,r^{-m}(1-t/r)^d,
 \qquad
 C_{m,d}:=N_{m,d}\frac{t^{\,2m+d+1}}{(t-1)^{d+1}}.}
                                                               \tag{E183}
\]

No asymptotic theorem is used here: (E183) is just the exact contour
representation with an explicit radius.  It applies, in particular, in the
previously untreated region \(d\ge2(m-1)\).

The square root can be enclosed rationally.  If
\(N_{m,d}^2=P/Q\) in lowest terms, set

\[
 \widehat N_{m,d}=\frac{\lfloor\sqrt{PQ}\rfloor+1}{Q},
 \qquad
 \widehat C_{m,d}
 =\widehat N_{m,d}\frac{t^{\,2m+d+1}}{(t-1)^{d+1}}.
                                                               \tag{E184}
\]

Then \(\widehat N_{m,d}>N_{m,d}\), using integer arithmetic only.  Let
\(R\ge3\), \(b=R-1>t^2\), and
\(L(b)=1+\lfloor\log_2 b\rfloor\).  Since
\(\Lambda(r)\le\log r\), while \(\log b<L(b)\), and
\(\log x\,x^{-m-1}\) is decreasing for \(x\ge2\) when \(m\ge2\), the
integral test yields

\[
 \boxed{
 \sum_{r\ge R}\frac{\Lambda(r)}r
       |Q_{m,m+d}(1/r)|
 <\widehat C_{m,d}\,b^{-m}
   \left(\frac{L(b)}m+\frac1{m^2}\right).}         \tag{E185}
\]

This is a terminating rational certificate for every \((m,d)\), with no
restriction on the gap.  For any prescribed rational \(\varepsilon>0\),
doubling \(b\) until the right-hand side of (E185) is below
\(\varepsilon\) produces a finite cutoff.  At fixed \(m\),

\[
 C_{m,d}
 =\sqrt{2t-1}\,t^{2m}
   \left(\frac{t}{t-1}\right)^{d+1}
 =O_m\!\left(t^{\,2m+1/2}\right),
 \qquad
 \widehat C_{m,d}=O_m\!\left(t^{\,2m+1/2}\right),
\]

so a cutoff of scale

\[
 b=O_{m,\varepsilon}\!\left(
 t^{\,2+1/(2m)}(\log t)^{1/m}\right)              \tag{E186}
\]

suffices.  Thus the dilation cutoff is essentially quadratic in
\(1+d/(2m+1)\); for \(m\ge232\), the power is at most
\(2+1/464\).

There is a sharp obstruction to turning this entrywise cutoff into an
operator-norm tail argument.  Let

\[
 \mathcal H_M=\overline{\operatorname {span}}\{e_n:n\ge M\},
 \qquad P_M:L^2(0,1)\to\mathcal H_M
\]

and recall that \((\mathcal D_u f)(t)=f(ut)\) for \(0<u<1\).  Then

\[
 \boxed{\|P_M\mathcal D_uP_M\|=u^{-1/2}
 \qquad(M\ge1,\ 0<u<1).}                          \tag{E187}
\]

The upper bound is immediate from

\[
 \|\mathcal D_uf\|_2^2
 =u^{-1}\int_0^u|f(s)|^2\,ds\le u^{-1}\|f\|_2^2.
\]

For the reverse inequality, work in the infinite-dimensional space
\(L^2(0,u)\), extended by zero to \((0,1)\).  Choose a nonzero \(f\)
orthogonal to the finite family

\[
 \left\{e_j(s),\ u^{-1}e_j(s/u):1\le j<M\right\}.
\]

Then \(f\in\mathcal H_M\), and the change of variables \(s=ut\) shows
that \(\mathcal D_uf\in\mathcal H_M\) as well.  Since \(f\) is supported
in \((0,u)\), equality holds in the preceding norm formula.  Hence
\(P_M\mathcal D_uP_Mf=\mathcal D_uf\) and the lower bound follows.

In particular, for every fixed integer \(r\ge2\),

\[
 \boxed{\|P_M\mathcal D_{1/r}P_M\|=\sqrt r,\qquad
 \left\|P_M\frac{\Lambda(r)}r\mathcal D_{1/r}P_M\right\|
 =\frac{\Lambda(r)}{\sqrt r},}                    \tag{E188}
\]

independently of \(M\).  Thus (E182) and (E185) are genuinely entrywise
finite-place reductions; they do not imply that the extracted dilation
operators become a small perturbation on the Jacobi tail.  Any infinite
block proof must use cancellation between the archimedean operator and the
finite signed dilation sum (or a stronger common quadratic form).  It
cannot be obtained by declaring the off-diagonal Jacobi blocks small after
raising the degree cutoff.

The obstruction persists for every fixed finite arithmetic window, even
after symmetrization.  If \(F\subset\{2,3,\ldots\}\) is finite and nonempty,
\(c_r\ge0\), and

\[
 T_F=\sum_{r\in F}c_r\mathcal D_{1/r},
\]

then

\[
 \boxed{
 \|P_M(T_F+T_F^*)P_M\|
 \ge\left(\sum_{r\in F}r c_r^2\right)^{1/2}.}     \tag{E189}
\]

To prove this, choose an interval \(I\Subset(0,1)\) so small that the
intervals \(nI\), indexed by the distinct integers in
\(\{1\}\cup F\cup(F\cdot F)\), are pairwise disjoint and remain in
\((0,1)\).  Inside
\(L^2(I)\), impose the finitely many moment conditions that put a unit
vector \(f_0\), and every normalized image
\(g_r=r^{-1/2}\mathcal D_{1/r}f_0\), in \(\mathcal H_M\).  Such an
\(f_0\ne0\) exists because only finitely many continuous linear conditions
are imposed on an infinite-dimensional space.  The vectors
\(f_0,(g_r)_{r\in F}\) are orthonormal and

\[
 \langle g_r,\mathcal D_{1/r}f_0\rangle=\sqrt r.
\]

Put \(w_r=c_r\sqrt r\), choose
\(a=2^{-1/2}\), and
\(b_r=w_r/(\sqrt2\|w\|_2)\).  For
\(x=af_0+\sum_rb_rg_r\), the root-to-first-generation terms give
\(\langle x,(T_F+T_F^*)x\rangle=\|w\|_2\), plus only nonnegative
overlaps among later integer multiples.  Since \(x\in\mathcal H_M\) and
\(\|x\|=1\), (E189) follows.  Taking
\(c_r=\Lambda(r)/r\) gives the cutoff-independent lower bound

\[
 \boxed{
 \left\|P_M\sum_{r\in F}\frac{\Lambda(r)}r
 (\mathcal D_{1/r}+\mathcal D_{1/r}^*)P_M\right\|
 \ge\left(\sum_{r\in F}\frac{\Lambda(r)^2}{r}\right)^{1/2}.}  \tag{E190}
\]

Thus even a fixed extracted prime window does not disappear in the tail.
What may still be positive is the *combined* archimedean--arithmetic form;
(E190) says that proving this requires its signed structure, not compactness
or tail norm decay of the arithmetic summand.

The exact implementation, with target \(2^{-m}\), returns the following
registered (not claimed minimal) cutoffs:

\[
\begin{array}{c|r|r|r}
m&d&t&R\\ \hline
232&462&1.993548\ldots&33\\
232&1000&3.150537\ldots&161\\
232&10000&22.505376\ldots&8113.
\end{array}
\]

Thus infinitely many prime powers can now be removed from the analytic gate
at every gap: inside the linear wedge, (E182) leaves the fixed dilations
\(2\le r\le145\); outside it, (E185) leaves a finite but gap-dependent
set \(2\le r<R(m,d)\).  This is not RH.  A global argument must still
preserve the signed cancellation of those finite dilations with the
archimedean term and prove coercivity uniformly in \((m,d)\).  Equations
(E187)--(E188) show that this requirement cannot be replaced by an
operator-norm-small Jacobi tail.

At the analytic cutoff \(m=232\), (E130) already covers every gap
\(d\le29\), rather than only the first two bands.  This does not yet prove
positivity of the corresponding full blocks: the archimedean contribution
must be compared with the signed pattern (E131).  It does remove absolute
values from the prime part over a growing bandwidth and makes that comparison
the next explicit target.

Thus no finite verification height can make this particular absolute-value
argument uniform in \(n\). Raising \(T\) only moves the finite cutoff.  The
column-sum argument removes the \(n^5\) loss of (E55), but its
\(n^3\log n\) loss and node-perturbation factor remain.  A route to RH must
obtain a genuinely uniform frame inequality or exploit signed
prime--archimedean cancellation rather than bounding every hypothetical
off-line orbit absolutely.

The module `euler_axis_pick.py` implements the orbit algebra and the exact
interval-rapidity form (E30)--(E31), while `zero_band_variance.py` audits the
constants in (E26)--(E28), and `order_four_rapidity_counterexample.py`
records the first open gate (E35). The script `order_four_verified_gram.py`
checks (E38)--(E45), and `degree_seven_sampling_audit.py` records the constants
in (E46)--(E48). The generalized budget and its cutoff are reproduced by
`finite_order_sampling_budget.py`.  The sharper column-sum proof
(E56)--(E71) is audited by `l1_column_sampling_budget.py`.  The separate
`chebyshev_cardinal_l1_checkpoint.json` records the exploratory numerical
observation that led to (E59), but that observation is not used in the proof.
The algebraic Fourier and prime identities (E73)--(E79) are checked by
`prime_side_pick_identity.py`.  The arithmetic uniqueness reduction
(E89)--(E98a), including the exact Hilbert-multiplier identity and the
indefiniteness of both separated blocks, is checked by
`arithmetic_pick_sequence.py`.
The Jacobi normalization, the full band formula, the first two
off-diagonal formulas, the row-sum counterexample, the consecutive
three-band theorem (E99)--(E116), and the large-degree Euler bounds are
checked by
`jacobi_band_pick.py`.
The translation/Hardy-generator identities (E117)--(E119), (E123)--(E125)
and the failure of the Bernstein shortcut (E120)--(E122) are audited by
`bernstein_functional_calculus_gate.py`; its finite sum is enclosed by the
displayed elementary analytic tail rather than treated as evidence for RH.
The exact dilation connection formula, the constant-sign prime window, and
the bandwise archimedean--prime discrepancy (E126)--(E133) are checked
coefficientwise over rational numbers (with a symbolic \(\log2\) component) by
`jacobi_dilation_connection.py`.
The Rodrigues moment inequalities, closed beta sums, uniform archimedean
bounds, prime remainder, local triple theorems, and the extracted
finite-place estimates (E134)--(E186) are
audited by `jacobi_local_band_bound.py`.
The compression-norm identities (E187)--(E190) are proved directly by the
finite-codimension and disjoint-support constructions displayed above; no
floating-point experiment is used in those claims.
The floating-point checks elsewhere in this audit are not used in place of
the displayed analytic inequalities. Global claims still require all
separated principal minors.

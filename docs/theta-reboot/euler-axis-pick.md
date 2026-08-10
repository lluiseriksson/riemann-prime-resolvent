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
`prime_side_pick_identity.py`.  These
floating-point checks are not used in place of the displayed analytic
inequalities. Global claims still require all separated principal minors.

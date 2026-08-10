# An Euler-axis Pick criterion

## The data use only the Euler half-plane

Let

\[
 M_\Xi(z)=\frac{\Xi(z)}{\Xi'(z)},\qquad
 F_\Xi(z)=\frac{M_\Xi(z)}{c_\Xi},\qquad F_\Xi(i)=i,
\]

with the positive normalization constant (c_\Xi=M_\Xi(i)/i). For
\(\eta>1/2\), put (s=1/2+\eta>1) and

\[
 F_\Xi(i\eta)=i f_\Xi(\eta),\qquad
 f_\Xi(\eta)=\frac1{c_\Xi}
 \frac{\xi(s)}{\xi'(s)}.
\]

These values lie wholly in the absolutely convergent Euler-product region.
Writing (L(\eta)=\xi'(1/2+\eta)/\xi(1/2+\eta)), one has

\[
 L(\eta)=\frac1s+\frac1{s-1}-\frac12\log\pi
 +\frac12\psi\!\left(\frac s2\right)
 -\sum_{n\ge2}\frac{\Lambda(n)}{n^s}.                 \tag{E1}
\]

No zero locations occur in (E1).

## Countable Nevanlinna--Pick equivalence

Let (E\subset(1/2,\infty)) be countable, contain (1), and have an
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

For the forward direction, RH is equivalent to (F_\Xi) being Herglotz, and
(EP) is its Pick kernel restricted to the imaginary axis. Conversely, finite
Pick positivity supplies a Herglotz interpolant for each initial finite set.
The node (eta=1) fixes the normalization, hence the interpolants form a
normal family. A diagonal subsequence interpolates every point of (E).
The identity theorem identifies its limit with (F_\Xi) first in the Euler
region and then by analytic continuation. Thus (F_\Xi) is Herglotz, which is
equivalent to RH.

The criterion is useful only if positivity is proved directly from (E1).
Introducing (EP) as a hypothesis merely renames RH.

## The first finite gate

For two heights (x,y>0\), write (a=f_\Xi(x)) and (b=f_\Xi(y)). Direct
factorization gives

\[
 \boxed{
 \det K^{(2)}=
 \frac{(xa-yb)(xb-ya)}{xy(x+y)^2}.}                    \tag{E2}
\]

If (x<y) and (f_\Xi) is positive and decreasing, the second factor is
negative. In that regime the two-point condition is equivalent to
\(x f_\Xi(x)\le y f_\Xi(y)). Since (f_\Xi=1/(c_\Xi L)), the coalescing-node
gate is

\[
 \boxed{L(\eta)-\eta L'(\eta)\ge0.}                    \tag{E3}
\]

Equivalently, (L(\eta)/\eta) must be nonincreasing. This is only the first
Pick minor. Even a proof of (E3) for every (eta>1/2) would not prove RH;
the full matrix hierarchy in (EC) remains.

The module `euler_axis_pick.py` implements (EP)--(E3) as exact floating-point
algebra for falsification and cross-checking. Rigorous claims require interval
evaluation of (E1) and all relevant principal minors.

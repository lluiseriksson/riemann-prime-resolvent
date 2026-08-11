# Two-extension Weyl ratio: a corrected resolvent target

## Starting point from Suzuki

Suzuki proves unconditionally that, after choosing
\(\lambda<\lambda_a\), the derivative operator in the Hilbert space defined
by \(T_{a,\lambda}=A_a-\lambda I>0\) has deficiency indices \((1,1)\).
Every self-adjoint extension has an entire characteristic function
\(W(a,\theta;z)\) whose zeros are all real. See
[Suzuki, *Weil's quadratic form via the screw function*](https://arxiv.org/abs/2606.09096),
Theorem 1.5.

This is stronger raw material than a positive finite Ritz value: the reality
of every finite-support spectrum is exact and unconditional.

## Analytic-type audit of the proposed single-function limit

Corollary 1.6 proposes a normalized limit with target

\[
 z^2\frac{\xi(1/2-iz)}{\xi'(1/2-iz)}.
\]

Under the holomorphic, zero-free normalization needed to preserve zeros and
apply Hurwitz, every normalized \(W(a,\theta;\cdot)\) is entire. A locally
uniform limit on every compact subset of \(\mathbb C\) must therefore be
entire as well.

The displayed target is meromorphic. Indeed, the real entire function
\(\Xi(t)=\xi(1/2+it)\) has infinitely many real zeros unconditionally.
Between two consecutive positive real zeros, Rolle's theorem gives a zero of
\(\Xi'\) at which \(\Xi\ne0\); the factor \(z^2\) does not remove that pole.

Thus the literal entire-function convergence cannot hold on all compact
subsets of \(\mathbb C\). If the normalizing factor is allowed to be
non-holomorphic, the zero-preservation argument is lost. The correct analytic
category is meromorphic convergence away from the real axis.

## The two-extension correction

Write

\[
 A_a(z)=(z-i)\int_{-a}^a v_+(a,x)e^{izx}\,dx,
 \qquad
 B_a(z)=(z+i)\int_{-a}^a v_-(a,x)e^{izx}\,dx.
\]

Then \(W(a,\theta;z)=A_a(z)+e^{i\theta}B_a(z)\). For two distinct extension
parameters, the quotient

\[
 R_a(z)=\frac{W(a,\theta_0;z)}{W(a,\theta_1;z)}
\]

is meromorphic, with real interlacing zeros and poles. Equivalently, a real
Möbius transform of \(-A_a/B_a\) is the Weyl \(m\)-function of the symmetric
operator. It is a Herglotz function on the upper half-plane.

This has exactly the analytic type needed for a ratio involving \(\xi'\).
For

\[
 M_\Xi(z)=\frac{\Xi(z)}{\Xi'(z)},
\]

one has the useful equivalence

\[
 \boxed{\mathrm{RH}\iff M_\Xi
 \text{ is Herglotz on }\mathbb C_+.}
\]

If RH holds, the canonical product with real zeros makes
\(-\Xi'/\Xi\) Herglotz, and \(M_\Xi=-1/(-\Xi'/\Xi)\) is Herglotz. Conversely,
an off-real zero \(\rho\) of multiplicity \(m\) gives
\(\Xi/\Xi'=(z-\rho)/m+O((z-\rho)^2)\), an interior zero impossible for a
nonconstant Herglotz function.

The extension pair used below has the canonical normalization \(m_a(i)=i\).
Set

\[
 c_\Xi=\frac{M_\Xi(i)}{i}>0,
 \qquad F_\Xi(z)=\frac{M_\Xi(z)}{c_\Xi}.
\]

Positive scaling preserves the Herglotz class, so RH is equally equivalent to
\(F_\Xi\) being Herglotz. Consequently, the correctly normalized locally
uniform limit is

\[
 m_a(z)\longrightarrow F_\Xi(z),\qquad z\in\mathbb C_+,
\]

of the two-extension Weyl functions would prove RH by closure of the
Herglotz class. This is the resolvent form of the corrected target.

## The shift-circularity lemma

There is a sharp restriction on how \(T_{a,\lambda}\) may be used. Let
\(a_j\to\infty\) and suppose

\[
 \lambda_j<\lambda_{a_j},\qquad \lambda_j\to0.
\]

Since \(a\mapsto\lambda_a\) is nonincreasing, for every fixed \(a\) and all
large \(j\),

\[
 \lambda_a\ge\lambda_{a_j}>\lambda_j.
\]

Taking the limit gives \(\lambda_a\ge0\) for every \(a\), which is Weil
positivity and hence RH. Therefore **constructing admissible shifts tending
to zero is already equivalent to crossing the global positivity frontier**.
It cannot be inserted as a harmless normalization.

The dependence on the shift is governed by the exact resolvent identity

\[
 (A_a-\mu)^{-1}-(A_a-\lambda)^{-1}
 = (\mu-\lambda)(A_a-\mu)^{-1}(A_a-\lambda)^{-1}.
\]

If both shifts lie below the spectrum at distances \(\delta_\mu,\delta_\lambda\),
the change on a vector \(f\) is bounded by

\[
 \frac{|\mu-\lambda|}{\delta_\mu\delta_\lambda}\|f\|.
\]

Thus shift independence cannot be claimed uniformly when either spectral gap
collapses. The finite executable model in `finite_weyl_ratio.py` checks both
the Herglotz sign and this resolvent identity.

## Exact two-channel shift defect

The dependence can be localized more sharply. Put

\[
 R_\lambda=(A_a-\lambda I)^{-1},\qquad
 N_\lambda(z)=L_z(R_\lambda e^x),\qquad
 D_\lambda(z)=L_z(R_\lambda e^{-x}),
\]

where \(L_z(f)=\int_{-a}^a f(x)e^{izx}\,dx\). Apart from the fixed factor
\(-(z-i)/(z+i)\), the characteristic quotient is
\(q_\lambda=N_\lambda/D_\lambda\). The resolvent identity gives the exact
formula

\[
 q_\mu-q_\lambda=
 \frac{(\mu-\lambda)
 \left[
 L_z(R_\mu R_\lambda e^x)D_\lambda
 -N_\lambda L_z(R_\mu R_\lambda e^{-x})
 \right]}
 {D_\mu D_\lambda}.                                      \tag{SD}
\]

Consequently, shift invariance is equivalent to the vanishing of the
bracketed \(2\times2\) determinant. It is not a consequence of
self-adjointness.  For example, with

\[
 A=\operatorname{diag}(a,b),\quad e^x=(1,1),\quad
 e^{-x}=(1,-1),\quad L=(X,Y),
\]

one obtains

\[
 q_\lambda=
 \frac{X(b-\lambda)+Y(a-\lambda)}
      {X(b-\lambda)-Y(a-\lambda)},\qquad
 q_\lambda'=
 \frac{2XY(a-b)}{[X(b-\lambda)-Y(a-\lambda)]^2}.
\]

Thus the quotient is generically shift-dependent already in dimension two.

Reflection symmetry identifies the exact source of the defect in the Suzuki
model. Write \(e^x=\cosh x+\sinh x\) and use that \(A_a\) commutes with
reflection. If

\[
 C_\lambda=L_z(R_\lambda\cosh x),\qquad
 S_\lambda=L_z(R_\lambda\sinh x),
\]

then \(N_\lambda=C_\lambda+S_\lambda\),
\(D_\lambda=C_\lambda-S_\lambda\), and

\[
 N_\mu D_\lambda-N_\lambda D_\mu
 =2(S_\mu C_\lambda-C_\mu S_\lambda).                  \tag{PS}
\]

Exact invariance would therefore require the relative odd/even response
\(S_\lambda/C_\lambda\) to be independent of the shift. The even and odd
resolvents have different spectra, so there is no formal reason for this
identity.

The source-normalized Galerkin diagnostic at \(a=0.72\), 32 Dirichlet modes,
8193 quadrature points and \(z=0.7+0.8i\) gives

| \(\lambda\) | characteristic quotient | \(S_\lambda/C_\lambda\) |
|---:|---:|---:|
| -0.1 | \(-0.0842316+0.2858732i\) | \(-0.1180225+0.0959359i\) |
| -1 | \(-0.0866869+0.2794367i\) | \(-0.1273774+0.1028080i\) |
| -10 | \(-0.0880132+0.2756963i\) | \(-0.1329035+0.1067382i\) |

The relative spread is \(0.0364293\). Formula (SD) closes to
\(1.4\cdot10^{-14}\), and (PS) to \(1.3\cdot10^{-15}\). This is a finite
diagnostic, not a theorem about the infinite operator, but it falsifies
automatic shift invariance as an algebraic principle.

Nor is the finite change merely one constant Möbius reparametrization. A
constant Möbius map preserves the cross-ratio of four values. At the four
pre-registered upper-half-plane probes, the cross-ratios for shifts
\(-0.1,-1,-10\) are respectively

\[
 0.6045327-0.2287167i,\quad
 0.6104453-0.2268132i,\quad
 0.6145781-0.2255178i.
\]

The largest defect is \(0.0105424\). Thus any Möbius covariance needed in
the limit must emerge asymptotically after a canonical boundary
normalization; it is not present exactly in the raw finite quotient.

The production diagnostic is reproducible with

    python -m experiments.theta_pencil.screw_weyl_shift_diagnostic \
      --half-width 0.72 --grid 8193 --basis 32 \
      --z-real 0.7 --z-imag 0.8 --shifts -0.1 -1 -10

The captured JSON artifact has SHA-256
`8E8635066E31E7FC952D0102BBDD37CBE572031C2CD5CC59B81344AA8C0F14BB`.

### The dominant-shift limit is universal

There is a second guardrail on very negative shifts.  If the resolvent is
dominated by its scalar leading term

\[
 (A_a-\lambda I)^{-1}=-\lambda^{-1}I+o(|\lambda|^{-1})
\]

on the two source vectors, then the transforms reduce to those of
\(e^{\pm x}\).  Direct integration gives

\[
 \Theta_a^{(\infty)}(z)
 =-\frac{\sinh(a(1+iz))}{\sinh(a(-1+iz))},             \tag{DL}
\]

and hence

\[
 \mathfrak m_a^{(\infty)}(z)
 =i\frac{1+\Theta_a^{(\infty)}(z)}
        {1-\Theta_a^{(\infty)}(z)}.
\]

For every compact (K\Subset\mathbb C_+\), (DL) tends uniformly to zero,
with exponential scale

\[
 |\Theta_a^{(\infty)}(z)|
 =O_K\!\left(e^{-2a\min\{\operatorname{Im}z,1\}}\right).
\]

Therefore \(\mathfrak m_a^{(\infty)}\to i\), a universal limit containing no
zeta information.  A successful safe-shift argument must consequently prove
that the arithmetic part remains visible at leading order after canonical
normalization; mere domination by the safety shift kills the signal.  The
module `dominant_shift_limit.py` evaluates (DL) directly.

### The first operator-sensitive coefficient

The first correction can be separated exactly. In a weak Galerkin basis with
metric \(G\), write the negative shift as \(\lambda=-R\), \(R>0\), and set

\[
 u_\pm^{(0)}=G^{-1}f_\pm,\qquad
 u_\pm^{(1)}=G^{-1}AG^{-1}f_\pm.
\]

For \(N_j=L_z(u_+^{(j)})\) and \(D_j=L_z(u_-^{(j)})\),

\[
 (A+RG)^{-1}f_\pm
 =R^{-1}u_\pm^{(0)}-R^{-2}u_\pm^{(1)}+O(R^{-3}),
\]

so

\[
 q_R=q_0+\frac{q_1}{R}+O(R^{-2}),\qquad
 q_0=\frac{N_0}{D_0},\quad
 q_1=\frac{N_0D_1-N_1D_0}{D_0^2}.                    \tag{LS}
\]

After the fixed characteristic prefactor \(p(z)=-(z-i)/(z+i)\), the
canonical Weyl expansion is

\[
 \mathfrak m_R
 =i\frac{1+pq_0}{1-pq_0}
 +\frac{2ipq_1}{(1-pq_0)^2}\frac1R+O(R^{-2}).         \tag{LC}
\]

The coefficient in (LC) is linear in \(A\). It therefore splits without
approximation into polar, archimedean and prime pieces. The source-normalized
diagnostic at \(z=0.7+0.8i\), 32 modes and 4097 grid points gives:

| \(a\) | relative component cancellation | total signal \( |m_1|/R\) | prime signal \( |m_{1,P}|/R\) | first-order residual |
|---:|---:|---:|---:|---:|
| 0.40 | \(7.88\cdot10^{-2}\) | \(2.14\cdot10^{-3}\) | \(3.11\cdot10^{-3}\) | \(3.62\cdot10^{-4}\) |
| 0.72 | \(1.79\cdot10^{-2}\) | \(1.42\cdot10^{-3}\) | \(2.02\cdot10^{-2}\) | \(1.41\cdot10^{-4}\) |
| 1.50 | \(1.17\cdot10^{-3}\) | \(1.23\cdot10^{-4}\) | \(4.24\cdot10^{-2}\) | \(8.84\cdot10^{-6}\) |
| 3.00 | \(4.87\cdot10^{-4}\) | \(5.10\cdot10^{-5}\) | \(5.16\cdot10^{-2}\) | \(9.68\cdot10^{-7}\) |

At \(a=3\), the absolute first-coefficient sizes of the polar,
archimedean and prime pieces are respectively \(12.7381\), \(0.2226\) and
\(12.5437\), while their vector sum has size \(0.0124\). Thus the prime
window is individually visible but cancels against the completed
archimedean/polar contribution. This is the finite-operator manifestation of
the explicit-formula/PNT cancellation. It also explains why the total
safe-shift Weyl function approaches the universal limit even though the
prime block itself does not become small.

The next coefficient repeats the same phenomenon. At \(a=3\), the total
second-order signal is \(9.93\cdot10^{-7}\), whereas the change in that
coefficient caused by inserting the prime block is
\(1.30\cdot10^{-3}\). Adding the polar and archimedean pieces cancels more
than three further orders of magnitude. The second-order approximation then
matches the finite resolvent to \(2.46\cdot10^{-8}\). Thus neither of the
first two operator-sensitive orders supplies an uncancelled \(O(1)\) limit.

These numbers are a diagnostic, not an asymptotic theorem. The exact
coefficient identity (LS)--(LC) is implemented in
<code>large_negative_shift_channel_expansion</code>; the component audit is
<code>safe_shift_signal_diagnostic.py</code>.

### An all-orders projective response identity

The preceding cancellation is not restricted to an expansion in the safe
shift. Let $A=A_0+P$, where $P$ is any additive component, and put

\[
 R=(A-\lambda G)^{-1},\qquad R_0=(A_0-\lambda G)^{-1}.
\]

For the two sources $f_\pm$ and an observation functional $\ell_z$, write

\[
 N=\ell_z(Rf_+),\quad D=\ell_z(Rf_-),\qquad
 N_0=\ell_z(R_0f_+),\quad D_0=\ell_z(R_0f_-).
\]

The second resolvent identity $R-R_0=-RPR_0$ gives the exact wedge formula

\[
 \boxed{
 ND_0-N_0D
 =N_0\,\ell_z(RPR_0f_-)-D_0\,\ell_z(RPR_0f_+).}       \tag{PW}
\]

No smallness assumption and no truncation in powers of $P$ occurs here.
If $q=N/D$, $q_0=N_0/D_0$, and
$p(z)=-(z-i)/(z+i)$, then

\[
 q-q_0=\frac{ND_0-N_0D}{DD_0},\qquad
 \Theta-\Theta_0=p(z)\frac{ND_0-N_0D}{DD_0},          \tag{PR}
\]

and the Cayley transform gives

\[
 \mathfrak m-\mathfrak m_0
 =\frac{2i(\Theta-\Theta_0)}
 {(1-\Theta)(1-\Theta_0)}.                            \tag{PC}
\]

Equations (PW)--(PC) are a pointwise necessary-and-sufficient visibility
test whenever the displayed denominators do not vanish.  With
$A_0=A_{\rm polar}-A_{\rm arch}$ and $P=-A_{\rm prime}$, they isolate the
prime contribution to all orders. With $A_0=0$ and $P=A$, they isolate
the *completed* operator signal from the universal source geometry.  The
latter is the relevant gate: since the zero-operator Weyl function tends to
$i$, a nonconstant Riemann limit requires its completed projective response
in (PR)--(PC) to survive on at least one point of an open set.

The distinction is visible already in the reproducible finite model at
$z=0.7+0.8i$:

| $a$ | exact prime-only Weyl change | exact completed Weyl change | resolvent-identity residual |
|---:|---:|---:|---:|
| 0.40 | $2.7790\cdot10^{-3}$ | $1.7803\cdot10^{-3}$ | $2.8\cdot10^{-18}$ |
| 0.72 | $2.0758\cdot10^{-2}$ | $1.2823\cdot10^{-3}$ | $8.9\cdot10^{-19}$ |
| 1.50 | $4.2394\cdot10^{-2}$ | $1.1527\cdot10^{-4}$ | $1.9\cdot10^{-18}$ |
| 3.00 | $5.1059\cdot10^{-2}$ | $5.0059\cdot10^{-5}$ | $1.1\cdot10^{-17}$ |

Thus the prime channel remains plainly visible relative to the
prime-deleted operator, while the *completed* response is three orders of
magnitude smaller at $a=3$. The cancellation is therefore an exact
projective phenomenon, not an artefact of stopping the large-shift series at
first or second order.  The table remains numerical evidence, not a proof
that the completed response tends to zero.  The function
<code>audit_component_channel_response</code> implements (PW), and the same
production diagnostic reports both choices of $A_0$.

There is a geometric restriction on any attempted repair. Automorphisms of
\(\mathbb C_+\) are hyperbolic isometries. After fixing the canonical
basepoint value \(m(i)=i\) (or \(ic\) after unshifting), the remaining
automorphisms correspond to rotations of the disk and cannot magnify a
family converging locally uniformly to the basepoint. Therefore, once the
dominant-shift collapse \(\mathfrak m_a\to i\) is established, no
positivity-preserving Möbius renormalization can recover a nonconstant
Riemann target from its vanishing Euclidean residual. One must either prove
that the arithmetic term prevents this collapse or choose a substantially
less dominant admissible shift.

### The opposite endpoint is universal too

Choosing the shift just below the ground state avoids large-shift domination,
but taking it *too* close creates a different collapse. Let
$\mu_0<\mu_1$ be the first two generalized eigenvalues of $(A,G)$, let
$g_0$ be a $G$-normalized ground state, and put
$\lambda=\mu_0-\delta$, $\delta>0$. The spectral resolution gives

\[
 (A-\lambda G)^{-1}f
 =\frac{\langle g_0,f\rangle}{\delta}g_0
  +\sum_{j\ge1}\frac{\langle g_j,f\rangle}
  {\mu_j-\mu_0+\delta}g_j.                            \tag{GE}
\]

Consequently, provided the relevant ground-state and observation overlaps do
not vanish, $\delta/(\mu_1-\mu_0)\to0$ implies

\[
 \frac{\ell_z((A-\lambda G)^{-1}f_+)}
 {\ell_z((A-\lambda G)^{-1}f_-)}
 \longrightarrow
 \frac{\langle g_0,f_+\rangle}{\langle g_0,f_-\rangle}. \tag{GR}
\]

The localized Weil operator commutes with reflection. A simple ground state
therefore has definite parity. Since $f_+(x)=e^x$ and
$f_-(x)=e^{-x}$, reflection gives

\[
 q_{\rm edge}\to
 \begin{cases}1,&g_0\text{ even},\\-1,&g_0\text{ odd}.
 \end{cases}
\]

Substitution into the characteristic prefactor and Cayley transform is
elementary and yields the second universal endpoint

\[
 \boxed{
 \mathfrak m_{\rm edge}(z)=
 \begin{cases}-1/z,&g_0\text{ even},\\ z,&g_0\text{ odd}.
 \end{cases}}                                      \tag{UE}
\]

For the Galerkin ground states at $a=0.4,0.72,1.5,3$, the channel ratio is
$1$ to at least eight digits, so the observed endpoint is $-1/z$. At
$z=0.7+0.8i$, it equals
$-0.6194690265+0.7079646018i$. The canonically normalized Riemann target is
$-0.6173555008+0.7081174133i$, only $2.1190\cdot10^{-3}$ away. This close
agreement is universal rank-one geometry, not recovered zeta information.

The shift problem is therefore narrowed to a genuine intermediate regime:

\[
 \boxed{
 |\lambda(a)|\ \text{must not dominate the observed operator channels, and}
 \quad
 \frac{\lambda_a-\lambda(a)}{\mu_1(a)-\lambda_a}
 \not\longrightarrow0.}                            \tag{IG}
\]

The first exclusion avoids the limit $i$; the second avoids $z$ or
$-1/z$. A successful construction must keep more than one spectral mode
alive while remaining unconditionally below the spectrum. The helper
<code>rank_one_channel_weyl_limit</code> implements (UE).

### A canonical intermediate family

There is one scale-free way to remain between the two universal endpoints.
For any fixed $c>0$, define

\[
 d_a=\mu_1(a)-\mu_0(a),\qquad
 \lambda_a^{(c)}=\mu_0(a)-c d_a.                    \tag{GS}
\]

This choice is unconditionally admissible whenever the ground state is
simple, because $\lambda_a^{(c)}<\mu_0(a)$. Moreover,

\[
 A_a-\lambda_a^{(c)}M_a
 =d_a\left(
 \frac{A_a-\mu_0(a)M_a}{d_a}+cM_a\right).           \tag{GN}
\]

The scalar $d_a^{-1}$ in the inverse cancels from the two-channel quotient.
Thus the Weyl function depends only on the dimensionless pencil

\[
 B_a=\frac{A_a-\mu_0(a)M_a}{d_a},\qquad
 \operatorname{spec}_{M_a}(B_a)=\{0,1,\ldots\}.      \tag{BO}
\]

This construction is invariant under every positive affine change
$A_a\mapsto\alpha A_a+\beta M_a$ with $\alpha>0$. Here $M_a$ is the
mass metric in a weak discretization (the identity in the abstract Hilbert
space). The construction neither assumes positivity of $A_a$ nor imports a
zero of zeta. It gives a concrete new operator-theoretic obligation:

> Prove compact/strong-resolvent convergence of the gap-normalized pencils
> $B_a$ together with their two source and observation channels, and identify
> the resulting Weyl function on one Euler-product open set.

That statement would genuinely advance the route; merely knowing the first
two eigenvalues does not. The present Galerkin model cannot yet test it
reliably. The computed first gaps change substantially under refinement:

| $a$ | grid/basis | computed $d_a$ | grid/basis | computed $d_a$ |
|---:|---:|---:|---:|---:|
| 0.40 | 4097/32 | $1.623\cdot10^{-2}$ | 8193/40 | $1.592\cdot10^{-2}$ |
| 0.72 | 4097/32 | $7.256\cdot10^{-8}$ | 8193/40 | $1.733\cdot10^{-8}$ |
| 1.50 | 4097/32 | $2.678\cdot10^{-7}$ | 8193/40 | $3.812\cdot10^{-8}$ |
| 3.00 | 4097/32 | $6.440\cdot10^{-7}$ | 8193/40 | $5.899\cdot10^{-7}$ |

The attractive three-point fits obtained by tuning $c$ are therefore not
evidence: for $a\ge0.72$ they use a gap at or below the discretization scale,
and the fitted $c$ drifts toward the already universal rank-one endpoint.
The module <code>gap_normalized_weyl.py</code> records only the exact
construction and its affine invariance; it deliberately makes no convergence
claim.

### A scalar parity-balance calibration

The first derivative at the canonical base point has an exact parity-sector
form. At $z=i$, the observation channel is $f_-=e^{-x}$. Put

\[
 c(x)=\cosh x,\qquad s(x)=\sinh x,\qquad
 R_{a,\lambda}=(A_a-\lambda I)^{-1},
\]

and, for an admissible real shift, define

\[
 E_a(\lambda)=\langle c,R_{a,\lambda}c\rangle,
 \qquad
 O_a(\lambda)=\langle s,R_{a,\lambda}s\rangle.
\]

Reflection symmetry kills the mixed parity term. Since
$f_+=c+s$ and $f_-=c-s$, direct differentiation of the characteristic
prefactor at $i$ gives

\[
 \boxed{
 \mathfrak m_{a,\lambda}'(i)
 =-q_{a,\lambda}(i)
 =-\frac{E_a(\lambda)-O_a(\lambda)}
 {E_a(\lambda)+O_a(\lambda)}.}                       \tag{PB}
\]

This supplies a scalar calibration derived from the Riemann target itself.
Let $F_\Xi=M_0/c_0$ with $c_0=M_0(i)/i$. In terms of derivatives of the
classical completed function with respect to $s$,

\[
 F_\Xi'(i)
 =\frac{\xi'}{\xi}\!\left(\frac32\right)
  -\frac{\xi''}{\xi'}\!\left(\frac32\right)
 =-0.9968019520324009035\ldots                       \tag{XD}
\]

and hence matching the first derivative is equivalent to

\[
 \boxed{
 \frac{O_a(\lambda)}{E_a(\lambda)}
 =\kappa_\Xi
 :=\frac{1+F_\Xi'(i)}{1-F_\Xi'(i)}
 =0.0016015849565571757\ldots.}                     \tag{KB}
\]

The value in (XD)--(KB) is evaluated wholly in the absolutely convergent
half-plane at $s=3/2$; no zero data or RH assumption enters it. A 200-bit
Arb power-series evaluation certifies

\[
 F_\Xi'(i)
 \in[-0.99680195203240090352889670478775783257375005566523721961
      \mathbin{\pm}7.35\cdot10^{-57}],
\]

and

\[
 \kappa_\Xi
 \in[0.00160158495655717571706007323750804007113993279814736277
      \mathbin{\pm}7.04\cdot10^{-57}].
\]

The executable certificate is
<code>arb_riemann_weyl_basepoint.py</code>.

There is also an existence statement. Suppose the ground state at support
$a$ is simple and even. As $\lambda\uparrow\mu_0(a)$, its pole occurs only
in the even sector, so $O_a(\lambda)/E_a(\lambda)\to0$. As
$\lambda\to-\infty$,

\[
 \frac{O_a(\lambda)}{E_a(\lambda)}
 \longrightarrow
 \frac{\|\sinh\|_{L^2(-a,a)}^2}
 {\|\cosh\|_{L^2(-a,a)}^2}.
\]

The last ratio is exactly

\[
 \frac{\sinh(2a)-2a}{\sinh(2a)+2a},
\]

and exceeds $\kappa_\Xi$ for
$a>0.0693385697853391\ldots$. On that range, continuity supplies at least
one admissible derivative-calibrated shift $\lambda_*(a)$ whenever the
ground state is simple and even. This is a genuine construction from the
finite operator, but it does not prove convergence of the Weyl functions.

It does yield a sharp sufficient criterion:

\[
 \boxed{
 \lambda_*(a_j)\longrightarrow0
 \text{ along some }a_j\to\infty
 \quad\Longrightarrow\quad \mathrm{RH}.}            \tag{SC}
\]

Indeed $\lambda_*(a_j)<\mu_0(a_j)$, while $a\mapsto\mu_0(a)$ is
nonincreasing. Passing to the limit gives $\mu_0(a)\ge0$ for every fixed
$a$, which is Weil positivity. Thus (SC) is not yet a proof: establishing
the zero limit is the entire remaining arithmetic estimate in scalar form.

At the reliable small-support points, the finite model is consistent with
this calibration: the root is about $-3.03\cdot10^{-4}$ at $a=0.4$ and the
resulting Weyl values agree with the normalized target to roughly
$10^{-5}$ across three probes. From $a=0.72$ onward the root is governed by
gaps below the discretization error, so the apparent approach to zero cannot
be used as evidence for (SC). The module
<code>parity_weyl_derivative.py</code> implements the exact identity (PB) and
the derivative-to-balance conversion in (KB).

## Common-factor cancellation: the full-line multiplier is not the Weyl ratio

There is a structural cancellation that must be imposed before using the
shifted target below.  In the continuous-kernel formulation, write

\[
 S_{a,\lambda}v_{a,\pm}=h_{a,\pm},
 \qquad h_{a,\pm}(x)=e^{\pm x}\pm i\quad (|x|<a).
\]

After extending the left-hand convolution to the full line, the formal
Fourier equations are

\[
 \widehat v_{a,\pm}(z)
 =\frac{\widehat h_{a,\pm}(z)}{\widehat S_\lambda(z)},
 \qquad
 \widehat S_\lambda(z)
 =z^{-2}\left(\frac{\Xi'(z)}{\Xi(z)}-\lambda\right).
\]

Put

\[
 F_{a,\theta}(z)=(z-i)\widehat h_{a,+}(z)
 +e^{i\theta}(z+i)\widehat h_{a,-}(z).
\]

Then the characteristic functions have the common factor

\[
 W(a,\theta;z)=
 z^2\frac{\Xi(z)}{\Xi'(z)-\lambda\Xi(z)}F_{a,\theta}(z). \tag{CF}
\]

Consequently, for every two extension parameters,

\[
 \boxed{
 \frac{W(a,\theta_0;z)}{W(a,\theta_1;z)}
 =\frac{F_{a,\theta_0}(z)}{F_{a,\theta_1}(z)}.}          \tag{FC}
\]

The reciprocal logarithmic derivative cancels exactly.  This does not make
the quotient arithmetically trivial: the continuation of (h_{a,\pm})
outside the interval depends on (S_{a,\lambda}).  It does show that the
full-line multiplier alone cannot identify the two-extension quotient with
\(M_\lambda\).  A boundary-continuation theorem would be needed to recover a
specific limiting Weyl function from the right-hand side of (FC).

This corrects the previous inference from analytic type.  The two-extension
quotient is unconditionally Herglotz, and (M_\Xi) is the right *kind* of
possible limit, but no convergence to (M_\Xi) follows from Suzuki's Fourier
multiplier formula.  In particular, the estimate (BE) below is a conditional
renormalization lemma, not yet the boundary estimate of the actual quotient.

### Exact projective reduction to one parity ratio

The bilateral problem can be reduced further without factoring the common
scalar multiplier. The localized Weil operator is real and commutes with
reflection. With compatible normalizations of the deficiency vectors,

\[
 v_{a,-}(x)=v_{a,+}(-x),\qquad
 V_a(z):=\widehat v_{a,+}(z),\qquad
 \widehat v_{a,-}(z)=V_a(-z).
\]

Split the single entire function into its even and odd parts,

\[
 C_a(z)=\frac{V_a(z)+V_a(-z)}2,\qquad
 S_a(z)=\frac{V_a(z)-V_a(-z)}2,\qquad
 r_a(z)=\frac{S_a(z)}{C_a(z)}.
\]

For the extension pair \(\theta=0,\pi\), direct algebra in Suzuki's
characteristic formula gives

\[
 W_0=2C_a(z)(z-ir_a(z)),\qquad
 W_\pi=2C_a(z)(zr_a(z)-i).
\]

Hence the canonically normalized Weyl function is exactly

\[
 \boxed{
 \mathfrak m_a(z)=-i\frac{W_\pi}{W_0}
 =-\frac{1+izr_a(z)}{z-ir_a(z)}.}                       \tag{PF}
\]

Away from its removable normalization degeneracy, the inverse map is

\[
 \boxed{
 r_a(z)=\frac{1+z\mathfrak m_a(z)}
 {i(\mathfrak m_a(z)-z)}.}                             \tag{PI}
\]

This identifies exactly what a bilateral glue must control: the single
odd/even transform ratio \(r_a\), not a scalar factorization of
\(\Xi'/\Xi-\lambda\). Any scalar Wiener--Hopf factor multiplies \(C_a\) and
\(S_a\) equally and cancels from (PF), so its index cannot determine the
missing projective limit. A useful factorization must instead control the
finite-section boundary transfer that changes \(S_a/C_a\). The functions
\`canonical_weyl_from_fourier_parity_ratio\` and
\`fourier_parity_ratio_from_canonical_weyl\` verify (PF)--(PI) independently
against the original two-channel formula.

### Fixed-support first-crossing boundary limit

There is now an exact boundary value of the projective construction at a
hypothetical first crossing, distinct from the conjectural limit
\(a\to\infty\). Use the notation of Proposition 4.9 in
[`first-crossing-real-rooted-witness.md`](first-crossing-real-rooted-witness.md).
For every \(c>0\), put

\[
 \Theta_c(z)=\frac{E_c^\#(z)}{E_c(z)}
 =\frac{(z-ic)U_c(z)}{(z+ic)U_c(-z)}.                    \tag{BG1}
\]

The strict Hermite--Biehler inequality (HB2) says exactly that \(\Theta_c\)
is analytic and Schur on \(\mathbb C_+\):

\[
 |\Theta_c(z)|<1\qquad(\operatorname{Im}z>0).
\]

Consequently the Cayley transform

\[
 \boxed{
 m_{0,c}(z)=i\frac{1+\Theta_c(z)}{1-\Theta_c(z)}}          \tag{BG2}
\]

is a meromorphic Herglotz function, canonically normalized by
\(m_{0,c}(ic)=i\). Its poles are real and are drawn from the real-rooted
self-adjoint-extension pencil (HB3). No limiting assertion or RH is used in
(BG1)--(BG2): they are the strong-resolvent boundary
\(\varepsilon(A_{a_*}+\varepsilon I)^{-1}\to P_{\ker A_{a_*}}\) of
Suzuki's positive-shift construction at fixed support.

If

\[
 U_c(z)=\mathcal C_c(z)+\mathcal S_c(z),
 \quad \mathcal C_c(-z)=\mathcal C_c(z),
 \quad \mathcal S_c(-z)=-\mathcal S_c(z),
 \quad r_{0,c}=\mathcal S_c/\mathcal C_c,
\]

then direct cancellation gives the projective formula

\[
 \boxed{
 m_{0,c}(z)=i\frac{z-ic\,r_{0,c}(z)}{ic-zr_{0,c}(z)}.}    \tag{BG3}
\]

On the imaginary axis, with \(C_{c,y},S_{c,y}\) from (HB5), this becomes

\[
 \Theta_c(iy)=
 \frac{(y-c)(C_{c,y}-S_{c,y})}
 {(y+c)(C_{c,y}+S_{c,y})}\in(-1,1),                      \tag{BG4}
\]

and \(\operatorname{Im}m_{0,c}(iy)>0\) is precisely (HB4)--(HB6). Thus
the signed prime identity (HB7a) and the Herglotz sign now constrain the
same generic even--odd collision pair.

This closes one conceptual gap in the Weyl route: a canonical projective
object does survive when the positive shift reaches a degenerate localized
operator. It does **not** close the global boundary-continuation theorem.
No relation between \(m_{0,c}\) at the unknown finite \(a_*\) and the Riemann
target \(F_\Xi\) has been proved, and asserting one would reinsert RH.

For the normalized Riemann target, (PI) defines

\[
 r_\Xi(z)=\frac{1+zF_\Xi(z)}{i(F_\Xi(z)-z)}.             \tag{PX}
\]

Both numerator and denominator vanish at \(z=i\), but the singularity is
removable. L'Hopital's rule and (XD)--(KB) give

\[
 \boxed{r_\Xi(i)=
 \frac{1+F_\Xi'(i)}{F_\Xi'(i)-1}=-\kappa_\Xi.}          \tag{PV}
\]

On the finite side, evaluation of the Fourier parity split at \(i\) gives
\(C_a(i)=E_a(\lambda)\) and \(S_a(i)=-O_a(\lambda)\).
Thus (PV) proves that the scalar calibration (KB) is precisely
\(r_a(i)=r_\Xi(i)\): it is the base-point value of the full projective target,
not an independent surrogate for it. The Arb certificate records the same
identity with outward-rounded intervals.

### A countable real-correlation criterion

The projective target can be evaluated without a bilateral transform. For
\(z=i\eta\), \(\eta>0\), reflection and parity separation give the exact real
formula

\[
 \boxed{
 r_{a,\lambda}(i\eta)=
 -\frac{\langle\sinh(\eta x),
 R_{a,\lambda}\sinh x\rangle}
 {\langle\cosh(\eta x),
 R_{a,\lambda}\cosh x\rangle}.}                         \tag{IR}
\]

The denominator is required to be nonzero. At \(\eta=1\), (IR) reduces to
\(-O_a/E_a\), as above. For \(\eta>1/2\), put

\[
 f_\Xi(\eta)=\frac{1}{c_\Xi}
 \frac{\xi(1/2+\eta)}{\xi'(1/2+\eta)}.
\]

All quantities in this expression lie in the absolutely convergent
Euler-product half-plane, and

\[
 F_\Xi(i\eta)=if_\Xi(\eta),\qquad
 r_\Xi(i\eta)=\frac{1-\eta f_\Xi(\eta)}{\eta-f_\Xi(\eta)}. \tag{IT}
\]

For a nonzero safe shift, the raw ratio in (IR) must first be converted by
(PF), the canonical shift must be undone by (CI), and the result divided by
\(c_\Xi\). Applying (PI) to that normalized unshifted value defines
\(\rho_{a,\lambda}\). This composition is implemented exactly by
\`renormalized_fourier_parity_ratio\`.

Let \(a_j\to\infty\), use any explicit admissible shifts \(\lambda(a_j)\),
and let \(E\subset(1/2,\infty)\) have an accumulation point in that interval;
for example, \(E=\{3+1/k:k\ge1\}\). Then

\[
 \boxed{
 \rho_{a_j,\lambda(a_j)}(i\eta)\longrightarrow r_\Xi(i\eta)
 \quad(\eta\in E)
 \quad\Longrightarrow\quad\mathrm{RH}.}                \tag{CC}
\]

Indeed, undoing the real Möbius shift and dividing by \(c_\Xi>0\) preserves
the Herglotz class and restores the normalization \(m(i)=i\). The normalized
family is therefore normal. Formula (PF) turns the assumed convergence into
pointwise convergence to \(F_\Xi\) on a uniqueness set. Every subsequential
limit equals \(F_\Xi\) by the identity theorem, so \(F_\Xi\) is Herglotz and
RH follows. Thus the next arithmetic obligation is only a countable family of
real resolvent-correlation ratios in the Euler region; neither a bilateral
ordinary Fourier transform nor convergence on a two-dimensional open set is
required. The audit function \`imaginary_axis_parity_ratio_audit\` checks
(IR) against the direct Fourier-channel ratio.

There is an exact universal constraint on every such one-point calibration.
Let \(m\) be a real-symmetric Herglotz function with \(m(i)=i\), put
\(d=m'(i)\in(-1,1)\), and set

\[
 \kappa=\frac{1+d}{1-d},\qquad
 w=\frac{z-i}{z+i},\qquad
 g(w)=\frac{m(z)-i}{m(z)+i},\qquad h(w)=\frac{g(w)}w.
\]

Schwarz's lemma makes \(h\) a Schur function and \(h(0)=d\).  At
\(z=i\eta\), \(\eta\ge1\), the disk coordinate
\(w=(\eta-1)/(\eta+1)\) is real.  Real symmetry and Schwarz--Pick give

\[
 \frac{d-w}{1-dw}\le h(w)\le\frac{d+w}{1+dw}.
\]

Substitution in the Cayley inverse and then in (PI) yields the sharp interval

\[
 \boxed{-\eta\kappa\le r(i\eta)\le-\frac{\kappa}{\eta}.} \tag{SP}
\]

Consequently, agreement at a second imaginary point is not by itself an
arithmetic prediction: every calibrated Herglotz function is already confined
to (SP).  The lower endpoint is an extremal, not merely a Taylor
approximation.  Equality at one \(\eta>1\) forces equality in Schwarz--Pick and
hence the unique real disk automorphism

\[
 h_*(w)=\frac{d+w}{1+dw},\qquad g_*(w)=w h_*(w).          \tag{SE}
\]

Transforming back to the upper half-plane makes the geometry explicit:

\[
 \boxed{
 m_*(z)=\frac{(1+d)z^2+d-1}{2z}
 =\frac{\kappa}{1+\kappa}z
  +\frac1{1+\kappa}\left(-\frac1z\right).}              \tag{SM}
\]

The extremal is exactly the convex Herglotz mixture of the two universal
parity endpoints in (UE). It contains no intermediate spectral information.
Moreover, if a sequence of calibrated Schur functions has
\(q_a(w_0)\to1\) at just one \(w_0\in(0,1)\), normality and the
maximum-modulus principle force \(q_a\to1\) locally uniformly. Consequently
\(m_a\to m_*\) locally uniformly throughout the upper half-plane. Thus a
single-point proof of second-Schur collapse would close the entire calibrated
route, rather than only one numerical probe.

Thus the quantity with actual discriminatory content is the nonnegative
Schwarz--Pick excess

\[
 \Delta_m(\eta)=r(i\eta)+\eta\kappa.                    \tag{SX}
\]

It has an exact Schur-algorithm coordinate.  Define

\[
 q_m(w)=\frac{h(w)-d}{w(1-dh(w))},\qquad
 w=\frac{\eta-1}{\eta+1}.                              \tag{SQ}
\]

For real \(w\in(0,1)\), Schwarz--Pick says \(-1\le q_m(w)\le1\), and direct
algebra gives

\[
 \boxed{
 \Delta_m(\eta)=\kappa(\eta-1)
 \frac{1-q_m(w)}{1-wq_m(w)}.}                           \tag{SD}
\]

The dangerous universal collapse is therefore exactly \(q_m(w)\to1\), not
merely qualitative proximity of two Weyl values.  Equality \(q_m(w)=1\) at
one interior real point is the rigidity case (SE).

For the Riemann target at \(\eta=3\), the certified value is strictly inside
(SP):

\[
 \Delta_\Xi(3)=r_\Xi(3i)+3\kappa_\Xi
 =8.4511702985\ldots\,10^{-5}>0.                         \tag{SR}
\]

The same Arb calculation certifies

\[
 q_\Xi(1/2)=0.9866317619939\ldots,qquad
 1-q_\Xi(1/2)=0.0133682380060\ldots>0.                  \tag{SG}
\]

The first predictive Galerkin test calibrates only at \(i\) and then evaluates
the untouched ratio at \(3i\).  For small support one additionally has

\[
 \sinh(\eta x)=\eta\sinh x+O_\eta(a^3),\qquad
 \cosh(\eta x)=\cosh x+O_\eta(a^2),
\]

so small-support geometry drives the finite ratio toward the lower
Schwarz--Pick extremal \(-\eta\kappa_\Xi\), before any arithmetic mechanism is
used. At \(\eta=3\), this extremal is
\(-0.004804754869671527\ldots\), already within
\(8.4512\cdot10^{-5}\) of the certified Riemann target. The apparent
multi-point agreement at small support must therefore be judged only by its
improvement over this baseline.

| \(a\) | calibrated \(\lambda\) | gap multiple \((\mu_0-\lambda)/(\mu_1-\mu_0)\) | predicted \(r_a(3i)\) | target error |
|---:|---:|---:|---:|---:|
| 0.40 | \(-3.1062\cdot10^{-4}\) | 0.03191 | -0.00477072 | \(5.05\cdot10^{-5}\) |
| 0.50 | \(-4.9053\cdot10^{-6}\) | 0.02536 | -0.00479019 | \(6.99\cdot10^{-5}\) |
| 0.55 | \(-3.6477\cdot10^{-7}\) | 0.02409 | -0.00478825 | \(6.80\cdot10^{-5}\) |
| 0.60 | \(-1.9780\cdot10^{-8}\) | 0.02271 | -0.00479678 | \(7.65\cdot10^{-5}\) |

These rows use 4097 points and 32 modes. Refinements through 8193/48 change
the displayed prediction by less than \(6\cdot10^{-7}\) on this support
range, but the error does not decrease toward zero; most of the agreement is
the universal calibration geometry.  In excess coordinates the four rows are
approximately \(3.40,1.46,1.65,0.80\) times \(10^{-5}\), whereas the target
excess is \(8.45\cdot10^{-5}\).  The observed trend is toward the wrong object,
the extremal (SE).  Equivalently, their second Schur parameters are about
\(0.99466,0.99772,0.99742,0.99875\), all closer to (1) than the certified
Riemann value.  These finite computations do not prove an
infinite-support limit. Beyond this range the spectral gap falls
below the discretization error. The command

    python -m experiments.theta_pencil.calibrated_parity_diagnostic

records the target, the Schwarz--Pick lower extremal, and the incremental
excess.
It is a falsifier for claimed predictive power, not an asymptotic theorem.

There is a sharp guardrail for the explicit safety shift. From (CT), for any
fixed point where \(M_0\ne0\),

\[
 \mathcal T_{\lambda,c_\Xi}(M_0)(z)
 \longrightarrow-\frac{c_\Xi}{M_0(z)}=-\frac1{F_\Xi(z)}
 \qquad(|\lambda|\to\infty).                            \tag{ST}
\]

Therefore, if a finite-support regime is so shift-dominated that its canonical
Weyl function tends to the universal value \(i\), it cannot converge to the
shifted Riemann target on any open set: \(-1/F_\Xi\) is nonconstant. This is a
theorem about such a dominant-shift regime, not yet a theorem that the explicit
shift (SS) always enters it.

The floating Galerkin falsifier at \(z=3i\) nevertheless shows exactly this
drift for the currently available discretization. Arb certifies
\(r_\Xi(3i)=-0.0047202431666865457\ldots\); after the exact unshift and
normalization, the finite values are

| \(a\) | \(\lambda_{\rm safe}(a)\) | raw \(r_{a,\lambda}(3i)\) | renormalized \(\rho_{a,\lambda}(3i)\) | target error |
|---:|---:|---:|---:|---:|
| 0.40 | -7.9675 | -0.13714 | \(-7.2791+0.3016i\) | 7.2806 |
| 0.72 | -12.5734 | -0.37178 | \(-2.6895+0.0229i\) | 2.6849 |
| 1.50 | -49.4110 | -0.81513 | \(-1.2268+0.0005i\) | 1.2221 |
| 3.00 | -243.1637 | -0.99476 | \(-1.0053+0.000002i\) | 1.0005 |

These rows use 4097 quadrature points and 32 Dirichlet modes and are not
infinite-dimensional certificates. They reject the explicit safety shift as
the default convergence ansatz; they do not reject the safe-shift construction
or RH. The reproducible command is

    python -m experiments.theta_pencil.safe_shift_parity_diagnostic

The next admissible shift must therefore remain far enough from scalar
domination to preserve the nonconstant target, while still being certified
below the finite-support spectrum. This is the quantitative design constraint
for the next step.

## Conditional shifted Herglotz target

There is nevertheless a better route than exact invariance. Let

\[
 M_0(z)=\frac{\Xi(z)}{\Xi'(z)},\qquad
 M_\tau(z)=\frac{M_0(z)}{1-\tau M_0(z)}
 =\frac{\Xi(z)}{\Xi'(z)-\tau\Xi(z)},\quad \tau\in\mathbb R.
\]

The real Möbius map \(w\mapsto w/(1-\tau w)\) has determinant one and maps
the upper half-plane to itself. Hence

\[
 \boxed{\mathrm{RH}\iff M_\tau\text{ is Herglotz on }\mathbb C_+}
 \qquad(\tau\in\mathbb R).                              \tag{SH}
\]

The forward implication follows from the corresponding property of \(M_0\).
Conversely, every off-real zero \(\rho\) of multiplicity \(m\) gives
\(M_\tau(z)=(z-\rho)/m+O((z-\rho)^2)\), an interior zero impossible for a
nonconstant Herglotz function.

### An explicit admissible shift for every support

The safe shift need not be existential. The archimedean Fourier multiplier is

\[
 h(t)=\operatorname{Re}\psi\!\left(\frac14+\frac{it}{2}\right)-\log\pi.
\]

The series for the digamma function shows term by term that
\(h(t)\ge h(0)\), with

\[
 h(0)=\psi(1/4)-\log\pi
 =-\gamma-\frac{\pi}{2}-3\log2-\log\pi.                 \tag{AF}
\]

The polar contribution is the rank-two operator
\(u\otimes v+v\otimes u\), where \(u(x)=e^{x/2}\) and
\(v(x)=e^{-x/2}\). Since
\(\|u\|^2=\|v\|^2=2\sinh a\) and
\(\langle u,v\rangle=2a\), its two nonzero eigenvalues are
\(2a\pm2\sinh a\). Therefore the exact lower bound is

\[
 2\operatorname{Re}(V_+\overline{V_-})
 \ge-2(\sinh a-a)\|v\|_2^2.
\]

For every active prime power, the same inequality bounds its two translation
correlations below by \(-2\Lambda(n)\|v\|_2^2/\sqrt n\). Therefore

\[
 \lambda_a\ge h(0)-2(\sinh a-a)
 -2\sum_{2\le n\le e^{2a}}\frac{\Lambda(n)}{\sqrt n}.   \tag{LB1}
\]

This already gives a finite computable shift. A closed elementary version
follows from

\[
 \Lambda(n)\le\log n\le2a,\qquad
 \sum_{n=2}^{N}\frac1{\sqrt n}
 \le\int_1^N\frac{dx}{\sqrt x}=2(\sqrt N-1).
\]

Namely,

\[
 \sum_{2\le n\le e^{2a}}\frac{\Lambda(n)}{\sqrt n}
 \le4a(e^a-1),
\]

There is a better elementary estimate for large support. Let
\(\psi(X)=\sum_{n\le X}\Lambda(n)\). For powers of two, the fact that the
prime-power product in \((N,2N]\) divides the central binomial coefficient
gives

\[
 \psi(2N)-\psi(N)\le\log {2N\choose N}\le2N\log2.
\]

Dyadic summation followed by comparison with the next power of two yields
\(\psi(X)\le4X\log2\) for every \(X\ge1\). Partial summation then gives

\[
\begin{aligned}
 \sum_{n\le X}\frac{\Lambda(n)}{\sqrt n}
 &=\frac{\psi(X)}{\sqrt X}
   +\frac12\int_1^X\frac{\psi(t)}{t^{3/2}}\,dt\\
 &\le8\log2\,\sqrt X.
\end{aligned}
\]

Taking the better of the two bounds, we obtain

\[
 \boxed{\lambda_a\ge
 L(a):=h(0)-2(\sinh a-a)
 -2\min\{4a(e^a-1),\,8\log2\,e^a\}.}                   \tag{LB2}
\]

Thus

\[
 \lambda_{\mathrm{safe}}(a)=L(a)-1<\lambda_a            \tag{SS}
\]

is an explicit unconditional choice for every \(a>0\). It uses neither zero
locations nor RH. Its magnitude is
\((1+16\log2)e^a(1+o(1))\).

Section 8 of Suzuki writes the continuous-kernel shift
as \(S_a=G_a-\lambda R_a\), with the inverse Laplacian \(R_a\). Formally on
the full line its Fourier multiplier changes from
\(z^{-2}\xi'/\xi\) to \(z^{-2}(\xi'/\xi-\lambda)\). The corresponding
candidate limit is therefore the shifted logarithmic-derivative reciprocal,
not the zero-shift target.  A safe shift need not tend to zero if this
full-line passage and its boundary normalization can be made rigorous.

Define the exactly unshifted finite function by

\[
 \widetilde m_a(z)=\frac{m_{a,\lambda(a)}(z)}
 {1+\lambda(a)m_{a,\lambda(a)}(z)}.                     \tag{UN}
\]

For every real \(\lambda(a)\), (UN) remains Herglotz. Therefore local uniform
convergence \(\widetilde m_a\to M_0\) would prove RH without ever assuming an
admissible sequence \(\lambda(a)\to0\).

The quantitative price is exact. If

\[
 w=\frac{m}{1-\lambda m},\qquad \widehat w=w+\varepsilon,
\]

then

\[
 \frac{\widehat w}{1+\lambda\widehat w}-m
 =\frac{\varepsilon(1-\lambda m)^2}
 {1+\lambda\varepsilon(1-\lambda m)}.                  \tag{AE}
\]

Thus a safety shift with \(|\lambda(a)|\to\infty\) amplifies an ordinary
boundary error quadratically. Away from zeros and poles, the required raw
convergence scale is \(o(|\lambda(a)|^{-2})\). This is the new quantitative
gate: prove a boundary/full-line resolvent estimate at that scale, or the
renormalized route does not close.

The compact-uniform statement has explicit constants.  On a compact set
\(K\Subset\mathbb C_+\), put
\(B_K=\sup_{z\in K}|M_0(z)|\) and
\(A_{K,a}=1+|\lambda(a)|B_K\).  If

\[
 \sup_K|\varepsilon_a|\le
 \frac{1}{2|\lambda(a)|A_{K,a}},                       \tag{DG}
\]

then the denominator in (AE) has modulus at least \(1/2\), and hence

\[
 \boxed{\sup_K|\widetilde m_a-M_0|
 \le 2A_{K,a}^2\sup_K|\varepsilon_a|.}                \tag{UB}
\]

Consequently \(\sup_K|\varepsilon_a|=o(|\lambda(a)|^{-2})\) implies local
uniform convergence after unshifting.  This is a theorem about the final
renormalization step, not an estimate for the finite-interval boundary error.
The latter remains the analytic obligation.

For the explicit choice (SS), the *unnormalized* gauge would require

\[
 \boxed{\varepsilon_a(z)=o\!\left(e^{-2a}\right)}
 \quad\text{locally uniformly on }\mathbb C_+.           \tag{BE}
\]

The module safe_weil_shift.py implements (AF)--(SS) and this unnormalized
inverse-Mobius error scale.

### Canonical boundary normalization removes the exponential precision tax

The preceding (e^{-2a}) loss is not intrinsic.  The characteristic function
gives the Livsic function

\[
 \Theta_{a,\lambda}(z)=-\frac{A_a(z)}{B_a(z)},
\]

which satisfies \(\Theta_{a,\lambda}(i)=0\).  Its canonical Weyl function is

\[
 \mathfrak m_{a,\lambda}(z)
 =i\frac{1+\Theta_{a,\lambda}(z)}
        {1-\Theta_{a,\lambda}(z)}
 =-i\frac{W(a,\pi;z)}{W(a,0;z)},
 \qquad \mathfrak m_{a,\lambda}(i)=i.                  \tag{CN}
\]

Thus the limiting target must be put in the same gauge.  Write

\[
 M_0(i)=ic,\qquad c>0.
\]

For the Riemann xi function, numerical evaluation gives
\(c=21.6750814829\ldots\); its positivity can also be reduced by the
functional equation to the sign of \(\xi'(3/2)\).  The canonically normalized
shift is the real Möbius map

\[
 \boxed{\mathcal T_{\lambda,c}(m)
 =\frac{m+\lambda c^2}{c(1-\lambda m)}.}               \tag{CT}
\]

It has positive determinant \(c(1+\lambda^2c^2)\), preserves the upper
half-plane, and sends \(M_0(i)=ic\) to (i).  Its inverse is

\[
 \mathcal T_{\lambda,c}^{-1}(y)
 =\frac{c(y-\lambda c)}{1+c\lambda y}.                 \tag{CI}
\]

If \(\widehat y=\mathcal T_{\lambda,c}(m)+\varepsilon\), direct algebra gives

\[
 \mathcal T_{\lambda,c}^{-1}(\widehat y)-m
 =\frac{c\varepsilon(1-\lambda m)^2}
 {1+\lambda^2c^2+c\lambda\varepsilon(1-\lambda m)}.  \tag{CE}
\]

On a compact \(K\), let \(B_K=\sup_K|M_0|\).  If

\[
 |c\lambda|\sup_K|\varepsilon|
 (1+|\lambda|B_K)\le\frac12(1+\lambda^2c^2),
\]

then

\[
 \sup_K|\mathcal T_{\lambda,c}^{-1}(\widehat y)-M_0|
 \le
 \frac{2c(1+|\lambda|B_K)^2}{1+\lambda^2c^2}
 \sup_K|\varepsilon|.                                \tag{CB}
\]

The amplification factor tends to \(2B_K^2/c\), not infinity.  Therefore
ordinary \(o(1)\) convergence to the canonically normalized shifted target
is sufficient even for the explicit \(|\lambda(a)|\asymp e^a\).  The earlier
\(o(e^{-2a})\) gate was a gauge artifact.  The functions
`canonically_normalized_shifted_value` and
`normalized_unshift_error_bound` implement (CT)--(CB).

## New proof obligation

The conditional implication is now precise:

1. use the explicit safety shift (SS);
2. fix a canonical boundary triple and hence a canonical Herglotz
   \(m_{a,\lambda(a)}\);
3. prove from the boundary continuations in (FC), not merely from the common
   multiplier, that this particular function differs by \(o(1)\) from
   \(\mathcal T_{\lambda(a),c}(M_0)\) on compact subsets of
   \(\mathbb C_+\);
4. apply (CI) and (CB) to obtain local uniform convergence to
   \(\Xi/\Xi'\).

Step 4 would prove RH. No near-zero admissible shift may be assumed in its
proof, by the lemma above.  Formula (FC) shows that step 3 is not an ordinary
full-line resolvent estimate: it is an arithmetic boundary-continuation
theorem, and it remains wholly open.

## Exact exterior-curvature equation

The boundary continuation in (FC) is not featureless. For \(t>0\), away
from prime-power thresholds, differentiating Suzuki's explicit formula for
the screw function gives

\[
 g''(t)=
 -e^{t/2}-e^{-t/2}
 +\frac{e^{-t/2}}{1-e^{-2t}}
 +\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}
   \delta(t-\log n).                                  \tag{GK}
\]

Let \(v\) be a mean-zero source supported on \([-a,a]\), and extend
\(h=S_{a,\lambda}v\) by the same convolution formula to \(x>a\). The
inverse-Neumann part has zero second derivative there: for the polynomial
kernel its remaining constant is multiplied by \(\int v=0\). Consequently

\[
\begin{aligned}
 h''(x)={}&
 -e^{x/2}\int_{-a}^a e^{-y/2}v(y)\,dy
 -e^{-x/2}\int_{-a}^a e^{y/2}v(y)\,dy\\
 &+\sum_{j\ge0}e^{-(2j+1/2)x}
   \int_{-a}^a e^{(2j+1/2)y}v(y)\,dy\\
 &+\sum_{e^{x-a}<n<e^{x+a}}
   \frac{\Lambda(n)}{\sqrt n}\,v(x-\log n).           \tag{EC}
\end{aligned}
\]

The identity holds classically between thresholds and distributionally
across them. It is independent of the safety shift outside the interval.
Thus the arithmetic data in the Weyl quotient reside in a moving
prime-power window of logarithmic width \(2a\), not in the common multiplier
that cancels in (FC). Equation (EC) is an exact reformulation of the missing
boundary theorem; it does not establish the required convergence or a sign.
The module \`exterior_boundary_curvature.py\` checks the smooth geometric
series and evaluates the moving-window term on sampled sources.

### Exact PNT centering of the exterior window

The apparently dominant exponential in (EC) cancels exactly against the
prime-number-theorem main term. Put

\[
 \psi(X)=\sum_{n\le X}\Lambda(n),\qquad R(X)=\psi(X)-X,
\]

and write the finite prime-power window as a Stieltjes integral:

\[
 P_v(x)=\int_{e^{x-a}}^{e^{x+a}}
 t^{-1/2}v(x-\log t)\,d\psi(t).
\]

Splitting \(d\psi=dt+dR\) gives the exact identity

\[
 P_v(x)=e^{x/2}\int_{-a}^{a}e^{-y/2}v(y)\,dy
          +\mathcal R_v(x),                              \tag{PC}
\]

where

\[
 \mathcal R_v(x)=\int_{e^{x-a}}^{e^{x+a}}
 t^{-1/2}v(x-\log t)\,dR(t).
\]

Consequently (EC) reduces to

\[
 h''(x)=\mathcal R_v(x)
 -e^{-x/2}M_+
 +\sum_{j\ge0}e^{-(2j+1/2)x}M_j,                         \tag{ECP}
\]

with \(M_+=\int_{-a}^{a}e^{y/2}v(y)\,dy\) and
\(M_j=\int_{-a}^{a}e^{(2j+1/2)y}v(y)\,dy\). Thus no
uncancelled \(e^{x/2}\) contribution remains.

For \(v\in H^1[-a,a]\), Stieltjes integration by parts makes the remaining
obligation completely explicit:

\[
\begin{aligned}
 \mathcal R_v(x)={}&
 e^{-(x+a)/2}v(-a)R(e^{x+a})
 -e^{-(x-a)/2}v(a)R(e^{x-a})\\
 &+\int_{-a}^{a}
 \frac{R(e^{x-y})}{e^{(x-y)/2}}
 \left(v'(y)+\frac12v(y)\right)dy.                       \tag{PR}
\end{aligned}
\]

The two endpoint terms are essential: the relevant deficiency vectors are
not known to satisfy Dirichlet boundary conditions. Formula (PR) identifies
the precise analytic input still missing from the Weyl route: signed control
of the normalized PNT remainder against the resolvent source, together with
its endpoint traces.

There is one further exact cancellation. Set

\[
 r(u)=e^{-u/2}R(e^u).
\]

Because \(\int_{-a}^{a}v=0\), the right-hand side of (PR) is unchanged when
\(r\) is replaced by \(r-C\) for any constant \(C\). Indeed, the coefficient
of \(C\) is

\[
 v(-a)-v(a)+\int_{-a}^{a}(v'(y)+\tfrac12v(y))\,dy=0.
\]

For real \(r\), choosing the midpoint of its range as \(C\) therefore yields
the quantitative oscillation gate

\[
 |\mathcal R_v(x)|\le\frac12
 \operatorname{osc}_{[x-a,x+a]}r\,
 \left(
 |v(-a)|+|v(a)|+
 \|v'+\tfrac12v\|_{L^1(-a,a)}
 \right).                                               \tag{OG}
\]

Thus a raw bound for \(|R(X)|/\sqrt X\) is not the correct target: the
mean-zero source removes its locally constant component. The remaining
absolute-value route nevertheless requires a shrinking local oscillation in
(OG), weighted by the actual resolvent source. Standard unconditional PNT
remainder bounds control the size of \(r\), not this shrinking product, and
do not close (OG); even RH gives only the classical von-Koch size estimate
\(R(X)=O(\!\sqrt X\log^2 X)\). A viable continuation must therefore prove the
oscillation-source product directly, exploit stronger signed cancellation,
or find a structural identity for the endpoint traces. The helpers
\`pnt_centered_prime_window\` and \`normalized_remainder_pairing\` check the
two exact cancellations without treating them as evidence for the missing
asymptotic estimate.

### Mellin closure and a one-open-set reduction

Write the arithmetic term in (EC) on the whole logarithmic line as

\[
 P_v(x)=\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}\,
 v(x-\log n).
\]

Since \(v\) is compactly supported, this is pointwise a finite moving-window
sum. For \(\operatorname{Im}z>1/2\), absolute convergence permits termwise
Fourier transformation and gives

\[
\begin{aligned}
 \int_{\mathbb R}P_v(x)e^{izx}\,dx
 &=\widehat v(z)
   \sum_{n\ge2}\frac{\Lambda(n)}{n^{1/2-iz}}\\
 &=-\widehat v(z)\,
   \frac{\zeta'}{\zeta}\!\left(\frac12-iz\right).       \tag{MT}
\end{aligned}
\]

Thus the moving window is exactly the Euler-product part of the full-line
multiplier in the half-plane where the Dirichlet series is honest. The polar
and archimedean terms in (EC) provide the completion and cancel the pole at
\(s=1\) only after the full expression is assembled.

There is also a useful normal-family reduction. Define

\[
 \widetilde{\mathfrak m}_a
 =\mathcal T_{\lambda(a),c}^{-1}
   (\mathfrak m_{a,\lambda(a)}).
\]

Every \(\widetilde{\mathfrak m}_a\) is Herglotz and
\(\widetilde{\mathfrak m}_a(i)=ic\). Hence

\[
 \frac{\widetilde{\mathfrak m}_a-ic}
      {\widetilde{\mathfrak m}_a+ic}
\]

is a disk-valued family vanishing at \(i\), and Montel's theorem makes the
family normal. Consequently it is enough to prove convergence to \(M_0\) on
one nonempty open set \(U\Subset\mathbb C_+\) where \(M_0\) is holomorphic.
Every subsequential Herglotz limit then agrees with \(M_0\) on \(U\); the
identity theorem forces the same meromorphic continuation, makes every
putative pole in \(\mathbb C_+\) removable, and gives convergence throughout
\(\mathbb C_+\). This would prove RH.

Formula (MT) therefore lowers the analytic target from all of
\(\mathbb C_+\) to one safe open set in the absolutely convergent
Euler-product region. It does not by itself control the ratio of the two
boundary continuations in (FC).

### A one-sided tail theorem, and why it does not yet glue

There is an unconditional estimate on either exterior half-line. Let
\(z=\tau+i\eta\) with \(\eta>1/2\). Swapping the finite source integral with
the absolutely convergent prime sum gives

\[
\begin{aligned}
 \int_a^\infty e^{-\eta x}|P_v(x)|\,dx
 &\le \int_{-a}^{a}|v(y)|e^{-\eta y}
 \sum_{n>e^{a-y}}\frac{\Lambda(n)}{n^{\eta+1/2}}\,dy.
\end{aligned}
\]

The elementary Chebyshev bound \(\psi(X)\le4(\log2)X\), followed by partial
summation, implies for \(\sigma>1\)

\[
 \sum_{n>N}\frac{\Lambda(n)}{n^\sigma}
 \le4(\log2)\frac{\sigma}{\sigma-1}N^{1-\sigma}.
\]

With \(\sigma=\eta+1/2\), the two displays give

\[
 \int_a^\infty e^{-\eta x}|P_v(x)|\,dx
 \le4(\log2)\frac{\eta+1/2}{\eta-1/2}
 e^{-(\eta-1/2)a}
 \int_{-a}^{a}|v(y)|e^{-y/2}\,dy.                       \tag{RT}
\]

For the explicit safety shift, \(T_{a,\lambda}\ge I\). If
\(T_{a,\lambda}v=e^{\pm x}\), then

\[
 \|v\|_2\le\sqrt{\sinh(2a)},\qquad
 \int_{-a}^{a}|v(y)|e^{-y/2}dy
 \le\sqrt{2\sinh a\,\sinh(2a)}.
\]

Thus the right prime tail in (RT) is
\(O_\eta(e^{-(\eta-2)a})\) and tends to zero on every closed half-plane
\(\eta>2\). The smooth terms in (EC) obey the same or a better threshold.

This does **not** prove the boundary-continuation theorem. The reflected left
tail is damped by the same argument only when \(\operatorname{Im}z<-2\).
There is no common open strip in which both ordinary one-sided transforms
converge with these estimates. This is exactly where a Wiener--Hopf-type glue,
an analytic subtraction, or a projective cancellation between the two
deficiency channels is required. Treating (RT) as a bilateral Fourier bound
would silently replace the missing theorem. The functions
\`chebyshev_right_prime_tail_bound\` and
\`safe_shift_right_prime_tail_bound\` record the rigorous one-sided result
and its sharp exponent under these elementary norm estimates.

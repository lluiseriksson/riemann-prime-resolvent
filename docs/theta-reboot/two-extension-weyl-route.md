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

Consequently, a nondegenerate locally uniform limit

\[
 m_a(z)\longrightarrow M_\Xi(z),\qquad z\in\mathbb C_+,
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

On a compact (K), let (B_K=\sup_K|M_0|).  If

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

The amplification factor tends to (2B_K^2/c), not infinity.  Therefore
ordinary (o(1)) convergence to the canonically normalized shifted target
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
   multiplier, that this particular function differs by (o(1)) from
   \(\mathcal T_{\lambda(a),c}(M_0)\) on compact subsets of
   \(\mathbb C_+\);
4. apply (CI) and (CB) to obtain local uniform convergence to
   \(\Xi/\Xi'\).

Step 4 would prove RH. No near-zero admissible shift may be assumed in its
proof, by the lemma above.  Formula (FC) shows that step 3 is not an ordinary
full-line resolvent estimate: it is an arithmetic boundary-continuation
theorem, and it remains wholly open.

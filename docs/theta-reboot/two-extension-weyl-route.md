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
| -0.1 | \(-0.0542640+0.3443723i\) | \(-0.0390826+0.0318106i\) |
| -1 | \(-0.0792823+0.2960457i\) | \(-0.1038478+0.0838308i\) |
| -10 | \(-0.0871021+0.2778648i\) | \(-0.1297620+0.1042172i\) |

The relative spread is \(0.21276\). Formula (SD) closes to
\(4.6\cdot10^{-14}\), and (PS) to \(1.4\cdot10^{-15}\). This is a finite
diagnostic, not a theorem about the infinite operator, but it falsifies
automatic shift invariance as an algebraic principle.

Nor is the finite change merely one constant Möbius reparametrization. A
constant Möbius map preserves the cross-ratio of four values. At the four
pre-registered upper-half-plane probes, the cross-ratios for shifts
\(-0.1,-1,-10\) are respectively

\[
 0.6036746-0.2287135i,\quad
 0.6103380-0.2268093i,\quad
 0.6145658-0.2255171i.
\]

The largest defect is \(0.0113506\). Thus any Möbius covariance needed in
the limit must emerge asymptotically after a canonical boundary
normalization; it is not present exactly in the raw finite quotient.

The production diagnostic is reproducible with

    python -m experiments.theta_pencil.screw_weyl_shift_diagnostic \
      --half-width 0.72 --grid 8193 --basis 32 \
      --z-real 0.7 --z-imag 0.8 --shifts -0.1 -1 -10

The captured JSON artifact has SHA-256
`04C337EE4339CD9268179CB0EE237180985FDDAC015D23FC1E4D52013B8AAE81`.

## Shifted Herglotz targets remove the near-zero-shift requirement

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

This matters because Section 8 of Suzuki writes the continuous-kernel shift
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

## New proof obligation

The viable branch is now more precise:

1. choose an explicit, provably admissible safety shift \(\lambda(a)\);
2. fix a canonical boundary triple and hence a canonical Herglotz
   \(m_{a,\lambda(a)}\);
3. prove the full-line shifted target and a boundary error
   \(o(|\lambda(a)|^{-2})\) on compact subsets of \(\mathbb C_+\);
4. apply (UN) and prove local uniform convergence to \(\Xi/\Xi'\).

Step 4 would prove RH. No near-zero admissible shift may be assumed in its
proof, by the lemma above. The missing theorem is no longer exact shift
invariance: it is the quantitative boundary-resolvent estimate in step 3.

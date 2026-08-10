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

## New proof obligation

The viable branch is now precise:

1. define the two-extension Weyl function with an explicit safe shift;
2. derive its dependence on the screw kernel without assuming positivity;
3. either prove exact shift invariance, or renormalize the shift contribution;
4. prove local uniform convergence on \(\mathbb C_+\) to \(\Xi/\Xi'\).

Step 4 would prove RH. No near-zero admissible shift may be assumed in its
proof, by the lemma above.

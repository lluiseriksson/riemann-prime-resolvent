# Theta-pencil research reboot

## Status and claim boundary

This is a new research track started on 2026-08-09. It does not prove the
Riemann hypothesis. Its purpose is to replace repeated equivalent criteria by
one concrete operator problem with explicit domains, a falsifier, and a
non-circular success condition.

The previous prime-resolvent work remains useful as infrastructure for finite
spectral estimates, Stieltjes compactness, formal verification, and numerical
gates. It is not taken as the starting axiom of this track.

## First starting point and decision

Let

\[
 \psi(x)=\Theta_{00}(i e^{2x}),\qquad \Phi(x)=-\log \psi(x),
 \qquad D=-i\frac{d}{dx},\qquad L=D-i\Phi'(x).
\]

Here \(\Theta_{00}\) is the positive theta density whose Fourier transform is
the Riemann \(\Xi\)-function. Hedenmalm's boundary-value formulation gives the
explicit pencil

\[
 LD u+\alpha Lu=0.
\]

Its admissible eigenvalues are exactly the zeros of \(\Xi(\alpha)\), including
hypothetical non-real zeros. The missing object is not another eigenvalue
formula. It is a positive, zero-independent Hilbert metric in which this pencil
is self-adjoint and nondegenerate on every admissible eigenfunction.

## Research target TP-M

Construct a positive operator or closed positive form \(C\), defined directly
from \(\psi\) and not from the zeros of \(\Xi\), such that on a common dense
core

\[
 (LD)^* C L=L^* C(LD),
\]

and prove all of the following:

1. the theta-pencil eigenfunctions belong to the completed form domain;
2. \(\langle Lu,CLu\rangle=0\) implies \(Lu=0\) for those eigenfunctions;
3. the boundary conditions used in the eigenvalue characterization are
   preserved by the closure;
4. no statement equivalent to RH is imported in the construction of \(C\).

These four clauses, together with Hedenmalm's characterization theorem, would
imply RH. The local and global obstructions proved in the first audit show that
TP-M cannot be realized by a local weight or by a bounded ambient metric on
ordinary logarithmic \(L^2\). The theta-pencil is therefore retained as a
structural no-go and as a source of exact theta identities, but it is not the
active proof track.

## Active track: finite-place Weil positivity

The active target is now the semilocal operator problem isolated by Connes and
Consani. For compactly supported test functions, the explicit formula uses
only the archimedean place and finitely many primes. The archimedean operator
positivity mechanism is known; the first genuinely new gate is to extend the
source-level trace identity and positivity estimate to the first arithmetic
window \(4<q\le5\), where \(S_q=\{\infty,2,3\}\), then to arbitrary finite
\(S\), with uniform support bookkeeping. See
[the semilocal programme](semilocal-weil.md).

## Current quantitative frontier

The semilocal programme has produced a concrete continuous realization that
is now the active numerical-analytic track: Suzuki's localized Weil operator
\(A_a\).  Exact cut-adapted Legendre sources, Arb tail Grams and a full Schur
reconstruction prove

\[
 A_{0.72}\succeq9.86850102990163\cdot10^{-17}I>0.
\]

Domain monotonicity then gives the unconditional interval theorem

\[
 \lambda_a>0\qquad(0<a\le0.72).
\]

This does not prove RH: Suzuki's criterion requires nonnegativity for every
support.  The new certificate crosses the prime-power-four threshold with the
full operator, not merely its high-degree complement.  It uses a thirteen-block
exact source and a two-denominator directional Schur estimate.  The active gate
is now to replace support-by-support certificates by a uniform threshold
mechanism whose constants remain controlled as further prime powers enter.
The complementary
[first-crossing reduction](first-crossing-real-rooted-witness.md) shows that
failure of RH would force, at the first zero of the lowest branch, a nonzero
null state whose full Fourier transform is real-rooted. A resolvent rank-one
argument removes every parity and node-symmetry restriction from the finite
real-zero theorem. Positive Fourier-evaluation perturbations reduce any
multiple kernel to a simple null direction without leaving the Loewner class,
so multiplicity is no longer a separate branch. The same calculation yields
an exact Loewner--Cauchy identity on every shifted Fourier lattice. Minimality
of the first crossing forces the witness to saturate the whole interval;
Cartwright theory then upgrades real-rootedness to the exact density law
\(N(R)=2a_*R/\pi+o(R)\) and a constant-phase conjugate-reflection symmetry.
Splitting that symmetry into real and imaginary parts gives an exact
dichotomy: either the witness has pure parity, or the even and odd ground
levels collide at zero at the first crossing; a mixed witness is not a third
branch.
In the pure branch, pairing the real zeros produces a canonical Stieltjes
transform in the radial variable and an explicit Hausdorff measure with atoms
\(x/(x+\lambda_j^2)\). These are witness zeros, not xi zeros; identifying the
two measures is now a sharply stated prime--theta obligation rather than an
implicit analogy.  The same product also forces every physical moment in the
allowed parity, after factorial normalization and one global sign choice, to
be a positive elementary symmetric sum of the inverse squared witness zeros.
This coefficient sequence is a locally uniform negative-real-zero product;
it is the precise positive cone available for an arithmetic attack.
In the collision branch, the even and odd half-interval operators saturate
the two opposite endpoints of the same normalized Hankel contraction. Their
cross pairing vanishes and yields an exact signed identity between the
archimedean Hankel block and the prime reflections at every \(\log n\).
Approaching the degenerate operator through Suzuki's positive shifts
\(A_{a_*}+\varepsilon I\) now gives a second, independent constraint.  The
rescaled self-adjoint-extension characteristic functions converge, at every
pair of deficiency points \(\pm ic\), to a nonzero real-rooted pencil
\(E_c^\#+e^{i\theta}E_c\), where
\(E_c(z)=(z+ic)\widehat{P_{\ker A_{a_*}}e^{cx}}(-z)\) is strictly
Hermite--Biehler.  On the imaginary axis this is the two-parameter strict
projection inequality
\((y+c)|U_c(-iy)|>|y-c||U_c(iy)|\).  Thus a parity collision must satisfy both
the signed prime--archimedean identity and a canonical projective/de Branges
constraint.  For all deficiency scales outside a discrete exceptional set,
the projected pair
\((P_{\rm e}\cosh(cx),P_{\rm o}\sinh(cx))\) is nonzero in both sectors and
satisfies the two constraints simultaneously; neither condition is asserted
to exclude it yet. If the first-crossing kernel is one-dimensional, all of
the real-rooted factor instead cancels from this projective object and the
boundary Weyl function is the universal \(z/c\) (even) or \(-c/z\) (odd).
Hence this fixed-support quotient carries new arithmetic information only in
a genuinely multidimensional kernel. In the simple branch the discarded
scalar is not lost: its squared norm is the zero-energy resolvent residue, and
one radial logarithmic derivative recovers exactly the Stieltjes transform
and Hausdorff battery of the witness zeros. This separates the projective and
scalar channels without identifying the witness measure with the incompatible
xi-zero measure.  The scalar channel is in fact projectively complete for a
simple kernel: its entire square root recovers the full null vector up to
sign.  Testing the null equation against every truncated exponential gives an
ordinary Laplace identity with an explicit `Ein` weight, a finite sum over
\(\log n\le2a\), and the smooth archimedean kernel.  The identity is proved
equivalent to the original weak kernel equation, so it preserves all
arithmetic information but is not itself a new positivity input.  A compact
B-spline construction supplies the complementary no-go: form-domain vectors
can have real-rooted transforms, saturated support, maximal Cartwright zero
density and arbitrarily many physical-space sign changes simultaneously.
Thus zero geometry alone cannot give the sign needed in the exponential
identity; the remaining argument must use its explicit prime--archimedean
weight.
Dividing by finite products of these real zeros gives exact rational
interpolants that isolate any hypothetical off-line zeta quartet with negative
spectral sign while Hermite-cancelling an arbitrary finite set of other zeros
with their spectral multiplicities. Jensen's formula now quantifies the price
of an exhaustive cancellation through height \(H\): the Paley--Wiener norm is
at least
\(\exp((\log 2/\pi+o(1))H\log H)\). Thus no bounded-norm or merely
exponential-norm diagonal argument can close the construction. The remaining
analytic gate is a uniform weighted-tail estimate for these necessarily
ill-conditioned interpolants, not their finite construction. An explicit
Riemann--von Mangoldt bound combined with complex Kadec sampling goes further:
that tail estimate is impossible in \(PW_a\) for
\(a<0.8508610646\ldots\). Pairing the conjugate spectral samples cancels the
vertical perturbation to first order and raises the rigorous obstruction to
\(a<0.9908731338\ldots\). Centering every even vertical coefficient at the
midpoint of its allowed interval halves the perturbation and raises the
rigorous obstruction again to \(a<1.0839780274\ldots\). Replacing the lattice
basis argument by a direct max-gap Poincare--Wirtinger sampling frame raises
the final rigorous obstruction to \(a<1.8868645429\ldots\). Hence the
exhaustive-Hermite rational-localization mechanism is now closed for a
hypothetical first crossing in
\(0.72<a_*<1.8868645429\ldots\); no known argument places every hypothetical
first crossing in that interval, so larger support remains open.

## Why this track is different

- The coefficients are explicit theta functions, not guessed zero locations.
- The theta audit reduces a tempting operator congruence to an exact no-go
  before long formalization work begins.
- Candidate metrics can be rejected at finite resolution by symmetry and
  coercivity tests.
- The first structural test already rules out every local weighted
  \(L^2(w\,dx)\) metric; see [the theta-pencil note](theta-pencil.md).
- Mathlib already contains Jacobi theta functions, their functional equation,
  differentiability, and bounds, so a formal path exists without defining the
  analytic substrate from scratch.

## Milestones

| Gate | Deliverable | Success condition |
|---|---|---|
| T0 | source audit | exact conventions and theorem numbers, with no inferred claims |
| T1 | local-metric obstruction | complete proof and independent executable check |
| T2 | global-metric obstruction | prove the cyclic-vector/Fourier-multiplier no-go |
| W0 | semilocal source extraction | exact trace identity, support thresholds, and sign conventions |
| W1 | finite-place falsifier | preregistered positivity and support judges |
| W2 | first arithmetic window | prove the operator inequality for \(4<q\le5\), \(S_q=\{\infty,2,3\}\) |
| W3 | induction in finite places | a uniform theorem for arbitrary finite \(S\) |
| W4 | support-to-primes bridge | match every compactly supported Weil test to a finite \(S\) |
| W5 | Lean kernel | formalize the abstract positivity implication and finite-place induction |
| W6 | RH review gate | independent review of the whole chain and its conventions |

A failure at T2--T5 closes the candidate class and is still a useful result.
It does not authorize changing the success condition.

## Navigation

- [Primary-literature matrix](literature-matrix.md)
- [Theta-pencil derivation and local no-go](theta-pencil.md)
- [Scaling Hamiltonian source extraction](source-extraction-scaling-hamiltonian.md)
- [One-prime moment model](one-prime-moments.md)
- [First arithmetic-window falsifier](first-window-falsifier.md)
- [Semilocal Weil programme](semilocal-weil.md)
- [Continuous Weil--Suzuki operator](screw-operator.md)
- [Explicit unconditional small-support bound](explicit-small-support.md)
- [Legendre tail coercivity and finite reduction](legendre-tail.md)
- [Exact Legendre matrix and mode-resolved Feshbach diagnostic](legendre-feshbach.md)
- [Endpoint-jump tail and Kato--Temple route](endpoint-jump-tail.md)
- [Certified localized positivity at `a = 0.42`](support-042-certificate.md)
- [Quantitative support continuity and its logarithmic barrier](support-parameter-continuity.md)
- [Certified localized positivity at support one half](support-05-certificate.md)
- [Certified localized positivity at support 0.51](support-051-certificate.md)
- [Certified second-window Schur frontier through support 0.675](second-window-schur.md)
- [Directional self-tail Gram](directional-self-tail.md)
- [Joint pointwise two-prime complement floor](joint-two-prime-floor.md)
- [Historical non-closure and resolution at support 0.675](support-0675-no-close.md)
- [Separable prime-power chain floor](prime-power-chain-floor.md)
- [Thirteen-block prime-power-four window](third-window-partition.md)
- [Certified localized positivity through support 0.7](support-070-certificate.md)
- [No form-level differential propagation in the support](support-derivative-no-go.md)
- [Historical common-denominator non-closure at support 0.72](support-072-no-close.md)
- [Certified localized positivity through support 0.72](support-072-certificate.md)
- [Uniform harmonic stratification of the Schur correction](harmonic-schur-stratification.md)
- [First-crossing real-rooted witness](first-crossing-real-rooted-witness.md)
- [Ground-simplicity cone no-go](ground-simplicity-cone-no-go.md)
- [Two-extension Weyl ratio and shift-circularity gate](two-extension-weyl-route.md)
- [Cut-adapted exact prime basis](cut-adapted-prime-basis.md)
- [Support-extension audit](support-extension-audit.md)
- [Falsifiers and abandonment conditions](falsifiers.md)

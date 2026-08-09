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
- [Falsifiers and abandonment conditions](falsifiers.md)

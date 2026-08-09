# Semilocal Weil positivity: active programme

## Claim boundary

Weil's criterion is equivalent to RH. Merely restating its positivity is not
progress. This track is admitted only because the explicit formula for a
compactly supported test function involves finitely many places and Connes--
Consani provide an operator mechanism at the archimedean place. The research
question is whether that mechanism extends by one finite place through a
concrete operator inequality.

## Source-level target

Let \(g\) be a compactly supported smooth function on the positive
multiplicative group, satisfying the two moment constraints in the Weil
criterion, and let \(h=g*g^*\). Fix the sign and Mellin/Fourier conventions of
Connes--Consani before any calculation.

For support contained in \((q^{-1/2},q^{1/2})\), only

\[
 S_q=\{\infty\}\cup\{p:p<q\}
\]

contributes to the geometric side. The active target is an operator identity
and inequality, built on the semilocal Hilbert space for \(S_q\), whose trace
is exactly the finite sum of local Weil distributions and whose sign is the
one required by Weil's criterion.

Although \(2<q\le3\) gives \(S=\{\infty,2\}\), its support does not reach
the first power of (2), so the finite-place distribution is inactive. The
first source-faithful window with an arithmetic contribution is \(4<q\le5\):

\[
 S=\{\infty,2,3\}.
\]

No induction over larger support windows will be attempted before this case is
closed.

The equation-level conventions and the failure of the naive local-sign
argument are recorded in
[Scaling Hamiltonian: equation-level extraction](source-extraction-scaling-hamiltonian.md).

## W0: exact source extraction

Before constructing an operator, record from the primary sources:

1. the semilocal Hilbert space and scaling representation;
2. the cutoff projections and their domains;
3. the trace identity for the sum of local distributions;
4. the involution and convolution convention for \(h=g*g^*\);
5. the two moment constraints;
6. the support-to-finite-places lemma;
7. every trace-class and boundary hypothesis.

This is an equation-level transcription task. A missing sign or modular factor
invalidates the track.

## W1: the first arithmetic restricted form

For \(S=\{\infty,2,3\}\), represent the exact trace form

\[
 \mathcal W_S(h_1)=\operatorname{Tr}\!\left(
 \widehat h_1\widehat h_1^*\frac12u^{-1}[F,u]\right)
\]

on the subspace where \(h=h_1\star h_1^*\) has the registered support and
\(h_1\) satisfies both Weil constraints. The ambient logarithmic derivative
does not have a constant sign, so no pointwise or place-by-place positivity
claim is allowed. The first-window theorem is complete only if the restricted
quadratic form has the required sign uniformly over this whole subspace.

The exact one-prime moment and Jacobi model is recorded in
[One-prime moment model](one-prime-moments.md). It supplies structured blocks
for the places (2) and (3), not the missing sign theorem.

## W2: why the sibling repositories are relevant

- `lean-os-positivity` supplies reusable algebra for reflection-positive
  sesquilinear forms. It may verify a proposed factorization but cannot supply
  the arithmetic sign.
- `lean-transfer-matrix` supplies finite positive-operator and spectral-gap
  patterns. It may control a one-prime block after the block is derived.
- `lean-gaussian-field` and Mathlib's Jacobi theta development supply heat-
  kernel identities for the archimedean component.
- `lean-connes-kreimer` may organize signed inclusion--exclusion over finite
  places only after a genuine coproduct/antipode identity is proved.

No Yang--Mills dimension argument, reflection-positivity slogan, or Hopf-
algebra vocabulary is accepted as an input theorem.

## Success and failure

**Success in the first arithmetic window:** an exact trace identity plus a proved operator
inequality for every admissible \(g\) in the support class, with domains and
trace norms controlled.

**Failure:** a concrete admissible \(g\) for which the proposed defect operator
has the wrong sign, loss of trace class, or constants that diverge at the
support boundary.

**Not success:** a finite matrix that is positive on sampled test vectors, an
inequality assumed as a field of a structure, or a proof that starts from Weil
positivity.

## Dependency chain

\[
 \text{archimedean theorem}
 \longrightarrow \text{first arithmetic support window}
 \longrightarrow \text{finite-place induction}
 \longrightarrow \text{all compact supports}
 \longrightarrow \text{Weil criterion}
 \longrightarrow \mathrm{RH}.
\]

Only the first node is currently available in the cited literature. The
one-prime local-factor Jacobi model is also available, but it does not prove the
first-window Weil inequality. Every displayed implication after the first node
is open.

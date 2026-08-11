# Falsifiers and abandonment conditions

## Purpose

The theta-pencil track is allowed to continue only while it produces a
zero-independent metric candidate with improving symmetry and coercivity. A
candidate is not promoted because its finite spectrum resembles Riemann zeros.

## Exact gates

### F0 - source identity

Reproduce the theta density, inversion symmetry, Fourier/Mellin transform, and
boundary eigenfunction from the primary source with fixed conventions. Any
normalization mismatch stops downstream work.

### F1 - locality

Every multiplication metric \(C=M_w\) is rejected by the local-metric
obstruction. No parameter search over positive weights is permitted.

### F2 - finite nonlocal metric

For a zero-independent discretization \((A_{X,N},B_{X,N})\), solve or bound
the feasibility problem

\[
 C=C^*\succeq\varepsilon I,\qquad
 \operatorname{tr}C=1,\qquad
 \|A^*CB-B^*CA\|\le r_{X,N}.
\]

The candidate fails if any of the following persists under refinement:

1. infeasibility for a fixed positive \(\varepsilon\);
2. symmetry residual \(r_{X,N}\) bounded away from zero;
3. coercivity decaying at least as fast as the residual;
4. concentration of \(C\) on the numerical kernel of \(B\);
5. dependence of the construction on tabulated zeta zeros.

### F3 - domain stability

Finite feasibility is rejected unless the proposed continuum form has a common
dense core for \(L\), \(LD\), \(C^{1/2}L\), and the adjoint expressions. A
formal integration by parts without vanishing boundary forms is a failure.

### F4 - complex-zero branch

The metric must apply to the complex-parameter eigenfunctions in Hedenmalm's
Theorem 3.3.3, not only to the already-known real zeros. Proving orthogonality
of real-zero eigenfunctions does not advance RH.

### F5 - nondegeneracy

The implication

\[
 \langle Lu,CLu\rangle=0\Longrightarrow Lu=0
\]

must be proved on the admissible eigenfunction class. Positivity without this
clause allows every hypothetical off-line zero to survive as a null vector.

## Abandonment rule

Close a candidate family after one exact obstruction or after three successive
refinements with no improvement in both normalized symmetry residual and
coercivity. Record the failure; do not repair it by weakening F2--F5.

## Semilocal Weil gates

### W-F0a - Lambert identity oracle

For (S=\{\infty,p\}), evaluate the one-prime contribution both as a sum
over powers of (p) and as the Lambert series (L1). Any disagreement outside
the registered truncation tail invalidates the normalization before the signed
Weil matrix is formed.

### W-F0b - source exactness

The semilocal operator must reproduce every source-normalized local Weil term on
a symbolic test class before any positivity experiment. A residual modular
factor or sign mismatch closes the implementation.

### W-F1 - adversarial test functions

Test functions are generated subject to the two moment constraints and the
registered multiplicative support. The candidate fails if one certified test
vector produces the wrong sign.

### W-F2 - support edge

Constants must remain controlled as the support approaches the first-prime
threshold. Positivity only on a smaller support where the prime 2 term vanishes
is the already-known archimedean case and does not count.

### W-F3 - induction honesty

The passage from \(S\) to \(S\cup\{p\}\) must expose the new operator and its
norm. A statement that assumes positivity for the enlarged set is rejected as
a wrapper around Weil's criterion.

### W-F4 - inertia is not positivity

A trace/Frobenius or rank--trace certificate is accepted as a full finite
positivity proof only if rigorous enclosures force every dimension of the
actual Schur complement to be positive.  A positive proportion of directions,
an inertia count for the raw source block, or a bandwidth-one density theorem
does not discharge a missing negative-index direction.  At support one the
current two-moment diagnostic forces only 39 of 58 source directions.

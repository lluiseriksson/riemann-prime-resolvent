# Mathematical status and claim boundary

## Verified in Lean

The kernel-checked source proves:

- the finite atomic identity
  \[
  D^k b_n=\sum_i w_i p_i^n(1-p_i)^k;
  \]
- nonnegativity for \(w_i\ge0\) and \(0\le p_i\le1\);
- compactification of a finite nonnegative spectrum by
  \[
  p_i=\frac{x_0}{\lambda_i+x_0},\qquad
  w_i=\frac1{\lambda_i+x_0};
  \]
- finite Hankel and localizing sum-of-squares certificates;
- a deterministic three-term comparison inequality.

## Documented conventional argument

The manuscript gives detailed proofs, using standard complex analysis and the Hausdorff moment theorem, of:

1. the slit-plane extension criterion;
2. the one-point Hausdorff equivalence;
3. finite scalar and PSD certificate consequences;
4. an integer-cutoff prime-tail estimate;
5. the positive Stieltjes normal-family implication.

These statements are not yet all named Lean theorems. They must not be advertised as kernel checked.

## Not proved by this repository

- RH;
- the complete analytic chain in Lean;
- novelty over every existing moment criterion;
- existence or convergence of a concrete Hilbert–Pólya operator;
- the construction-side hypotheses in the shared interface.

## Honest headline

> A criterion-oriented research repository with an integrated mathematical argument and a kernel-checked finite Hausdorff/resolvent certificate layer.

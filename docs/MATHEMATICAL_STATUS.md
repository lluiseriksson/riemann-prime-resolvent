# Mathematical status and claim boundary

## What is proved in the paper

The manuscript supplies complete mathematical arguments for the following abstract statements, subject to the standard background results explicitly cited there:

1. **Slit-plane extension criterion.** A holomorphic extension of the target \(\mathcal S_\Xi\) to \(\mathbb C\setminus(-\infty,0]\), agreeing on one nonempty interval in \((1/4,\infty)\), excludes non-real zeros of \(\Xi\).
2. **One-point Hausdorff formulation.** At a fixed \(x_0>1/4\), the infinite derivative jet can be encoded as a Hausdorff moment sequence; conversely, the Hausdorff representation builds the needed slit-plane extension.
3. **Finite certificate hierarchy.** Hausdorff complete monotonicity yields scalar finite-difference tests and positive Hankel/localizing quadratic forms.
4. **Prime-side target.** On \(\sigma>1\), the logarithmic derivative gives an absolutely convergent von Mangoldt expansion and an explicit elementary truncation error.

## What Lean currently proves

The kernel-checked files prove only the finite, source-independent algebra:

- the exact finite atomic identity
  \[
  D^k b_n=\sum_i w_i p_i^n(1-p_i)^k;
  \]
- nonnegativity when \(w_i\ge0\) and \(0\le p_i\le1\);
- compactification of a finite nonnegative spectrum by
  \[
  p_i=\frac{x_0}{\lambda_i+x_0},\qquad
  w_i=\frac1{\lambda_i+x_0};
  \]
- finite Gram and localizing sum-of-squares certificates;
- the three-component deterministic comparison budget.

## What is not proved

This repository does not establish:

- the Riemann hypothesis;
- the infinite Hausdorff moment theorem in Lean;
- the Mathlib bridge from the project’s \(\Xi\) conventions to `RiemannHypothesis`;
- a concrete unbounded self-adjoint Hilbert–Pólya operator;
- trace-class properties of a limiting squared resolvent;
- the uniform one-point bound and compactness for a concrete spectral family;
- convergence of concrete prime-built spectral approximants to \(\mathcal S_\Xi\);
- novelty relative to every existing moment criterion without specialist literature review.

## Honest headline

The strongest accurate description is:

> A research programme and formalized finite certificate layer for a one-point resolvent–Hausdorff reduction of RH.

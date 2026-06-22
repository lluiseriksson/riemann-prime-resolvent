# Formal proof plan

The order below minimizes circularity and API churn.

## Milestone A — conventions and geometry

1. Define the project's \(\xi\), \(\Xi\) and \(\mathcal S_\Xi\) in terms of Mathlib's completed zeta API.
2. Prove the exact equivalence between real zeros of \(\Xi\) and Mathlib's `RiemannHypothesis` proposition.
3. Prove that \(z\mapsto-z^2\) sends the open upper half-plane into `Complex.slitPlane`.

## Milestone B — logarithmic-derivative criterion

4. Establish differentiability of the composed slit-plane function.
5. State the meromorphic identity theorem in the form needed on the upper half-plane minus a discrete zero set.
6. Use local factorization at a zero to show that \(-\Xi'/\Xi\) has a nonremovable pole.
7. Close the slit-plane extension theorem with no project axioms.

## Milestone C — Hausdorff reconstruction

8. Connect the derivative normalization to Taylor coefficients.
9. Import or formalize the Hausdorff moment theorem for finite positive measures on `[0,1]`.
10. Prove holomorphy of the parameterized integral
    \[
    F(w)=\int_0^1\frac{d\mu(v)}{1+((w-x_0)/x_0)v}.
    \]
11. Identify the Taylor series near \(x_0\) and apply the slit-plane theorem.

## Milestone D — arithmetic and compactness

12. Formalize the integer-cutoff von Mangoldt tail.
13. Formalize one-point local boundedness for positive Stieltjes transforms.
14. Package the normal-family criterion in the exact shared-interface form.

Only after A–D should the companion repository import a released criterion theorem.

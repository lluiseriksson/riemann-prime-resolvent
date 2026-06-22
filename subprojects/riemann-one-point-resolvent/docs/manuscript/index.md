# Integrated manuscript: one-point resolvent–Hausdorff criterion

## Scope

This documentation develops an abstract reduction associated with the Riemann \(\Xi\)-function, finite certificate hierarchies and a formalization programme. It does **not** claim a proof of RH. The difficult concrete spectral convergence input is delegated to the companion construction repository.

## Abstract

For \(x>1/4\), define

\[
\mathcal S_\Xi(x)=\frac{1}{2\sqrt{x}}
\frac{\xi'}{\xi}\!\left(\frac12+\sqrt{x}\right),
\qquad
\Xi(z)=\xi\!\left(\frac12+iz\right).
\]

A holomorphic slit-plane extension of \(\mathcal S_\Xi\) agreeing on one real interval excludes non-real zeros of \(\Xi\). At a fixed \(x_0>1/4\), normalize the derivative jet by

\[
b_n(x_0)=x_0^n\frac{(-1)^n}{n!}\mathcal S_\Xi^{(n)}(x_0).
\]

Using the Hausdorff moment theorem, the documented argument identifies RH with the existence of a finite positive measure on `[0,1]` representing \((b_n)\), equivalently with nonnegativity of all signed forward differences. Under RH the representing atoms arise from the compactification \(\gamma^2\mapsto x_0/(\gamma^2+x_0)\). Conversely, a representing measure reconstructs the needed slit-plane extension.

The finite atomic identities, compactification inequalities and Gram/localizing certificates are represented in Lean. The analytic equivalence remains on the formalization roadmap.

## Contents

1. [Target and conventions](01-target-and-conventions.md)
2. [Slit-plane criterion](02-slit-plane-criterion.md)
3. [One-point Hausdorff criterion](03-one-point-hausdorff.md)
4. [Finite certificates](04-finite-certificates.md)
5. [Arithmetic target](05-arithmetic-target.md)
6. [Positive approximants](06-positive-approximants.md)
7. [Lean formalization](07-lean-formalization.md)
8. [Status and novelty](08-status-and-novelty.md)
9. [References](references.md)

# Certified localized positivity through support 0.7

## Theorem and scope

For Suzuki's localized Weil operator in the conventions fixed by this
repository, the interval-arithmetic certificate proves

\[
 \boxed{A_{0.7}\succeq
 1.0783783252951832\cdot10^{-15}I>0}.
\]

Domain monotonicity consequently gives

\[
 \lambda_a>0\qquad(0<a\le0.7).
\]

This is an unconditional bounded-support theorem.  It is not RH: Suzuki's
criterion requires nonnegativity for every support radius.

## Exact architecture

The interval is partitioned by the active translations for prime powers
\(2,3,4\) into thirteen exact blocks.  Reflection reduces the finite source
to even and odd matrices of dimension 78.  Each block retains 12 local
Legendre modes.  The complement is split at degree 176 and the directional
tail is computed explicitly through degree 8191.

The high complement has the operator lower bound

\[
 D\succeq d_0P_{[12,176)}+d_1P_{[176,\infty)},
\]

where

\[
 d_0\ge0.3268232544521020,
 \qquad d_1\ge2.974150455025881.
\]

Since inversion reverses the positive-operator order, the source coupling to
the two orthogonal ranges is charged at \(d_0^{-1}\) and \(d_1^{-1}\)
separately.  No invariance of either range under \(D\) is assumed.

## Certified output

| sector | negative | positive | unresolved | Schur lower | full coercive lower | inertia method |
|---|---:|---:|---:|---:|---:|---|
| even | 0 | 78 | 0 | `1.5700644483114687e-13` | `1.0783783252951832e-15` | point spectrum + Weyl budget |
| odd | 0 | 78 | 0 | `2.5162073334751495e-10` | `1.7204741789623543e-12` | direct Arb/Rump balls |

The maximum entry radii of the two Schur matrices are respectively
`2.835089938845513e-15` and `2.8350913053478847e-15`.  The even-sector
fallback isolates the symmetric midpoint spectrum with Arb and expands every
eigenvalue interval by the rigorous bound \(n r\), because an entrywise
perturbation of radius \(r\) has operator norm at most \(nr\).

## Reproduction

The deterministic component cache used for the recorded run has SHA-256

```text
51d0dca911211c57e206fe5b22c975071fc83670ddd8ea1a01f576c9c6fa149f
```

and metadata

```text
a=0.7, local degrees=12, tail start=176, explicit end=8192,
smooth order=47, self remainder end=32768, precision=512 bits,
pointwise subdivisions=1024, tail balance=0.2, residual balance=0.0001.
```

Given that cache, the certificate is rerun by

```python
from experiments.theta_pencil.support_070_certificate import certify_support_070

result = certify_support_070("theta-schur-a070-d12-p47-tail8192.npz")
print(result)
```

The cache is a performance artifact, not an axiom: every component has a
source-level Arb generator, and a metadata mismatch forces regeneration.
The public theorem boundary is the operator inequality above; neither the
finite Ritz spectrum nor the cache alone is treated as a proof.

## Next gate

Further isolated support certificates would extend the numerical-analytic
frontier but cannot by themselves reach all support radii.  The next accepted
advance must expose a threshold-uniform lower-bound mechanism, or prove a
recurrence/induction whose constants do not collapse as new prime powers enter.

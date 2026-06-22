# Target and conventions

Define

\[
\xi(s)=\frac12s(s-1)\pi^{-s/2}\Gamma\!\left(\frac s2\right)\zeta(s),
\qquad
\Xi(z)=\xi\!\left(\frac12+iz\right).
\]

Then \(\Xi\) is entire, even and real on the real axis. A nontrivial zero \(\rho=\beta+i\gamma\) corresponds to

\[
z=\gamma-i\left(\beta-\frac12\right)
\]

as a zero of \(\Xi\). Thus RH is equivalent to all zeros of \(\Xi\) being real, once this convention is connected exactly to the library definition.

For \(x>1/4\), set

\[
\mathcal S_\Xi(x)=\frac{1}{2\sqrt{x}}
\frac{\xi'}{\xi}\!\left(\frac12+\sqrt{x}\right).
\]

The domain ensures \(1/2+\sqrt{x}>1\), where the Euler product is absolutely convergent and zeta has no zero.

## Spectral representation conditional on RH

If RH holds and the positive zeros of \(\Xi\), counted with multiplicity, are \(\gamma_j\), the symmetric canonical product yields

\[
\mathcal S_\Xi(x)=\sum_{j\ge1}\frac{1}{\gamma_j^2+x},
\qquad x>0.
\]

Hence the target is a Stieltjes transform of a positive discrete measure on the squared ordinates. This representation motivates the compactification but is not assumed in the converse slit-plane criterion.

## Formal convention obligation

The Lean project must prove, rather than presume, the exact bridge among Mathlib's `completedRiemannZeta₀`, the project's \(\xi\), the rotated function \(\Xi\), and `RiemannHypothesis`. Constants and removable factors cannot be dismissed informally in the final theorem statement.

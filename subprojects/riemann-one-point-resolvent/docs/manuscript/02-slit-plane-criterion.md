# Slit-plane extension criterion

Let

\[
\Omega=\mathbb C\setminus(-\infty,0].
\]

## Quadratic map

If \(\operatorname{Im}z>0\), then \(-z^2\in\Omega\). Write \(z=a+ib\) with \(b>0\). When \(a=0\), \(-z^2=b^2>0\). When \(a\ne0\),

\[
\operatorname{Im}(-z^2)=-2ab\ne0,
\]

so the image is not on the closed negative real axis.

## Criterion

**Theorem (documented, not yet fully formalized).** Let \(I\subset(1/4,\infty)\) be a nonempty open interval. Suppose a holomorphic function \(S:\Omega\to\mathbb C\) satisfies

\[
S(x)=\mathcal S_\Xi(x),\qquad x\in I.
\]

Then all zeros of \(\Xi\) are real.

### Proof

For \(z\) in the upper half-plane define

\[
M(z)=2zS(-z^2).
\]

The quadratic lemma makes \(M\) holomorphic. If \(z=iy\) and \(y^2\in I\), the functional equation gives

\[
M(iy)=2iy\mathcal S_\Xi(y^2)
=i\frac{\xi'}{\xi}\!\left(\frac12+y\right)
=-\frac{\Xi'(iy)}{\Xi(iy)}.
\]

On the upper half-plane minus the discrete zero set, the identity theorem identifies \(M\) with \(-\Xi'/\Xi\). If \(z_0\) were a zero of multiplicity \(m>0\), local factorization

\[
\Xi(z)=(z-z_0)^m g(z),\qquad g(z_0)\ne0,
\]

gives

\[
-\frac{\Xi'(z)}{\Xi(z)}=-\frac{m}{z-z_0}-\frac{g'(z)}{g(z)},
\]

a nonremovable pole contradicting holomorphy of \(M\). Conjugation symmetry excludes lower-half-plane zeros.

## Formal obligations

The Lean proof must make explicit the connectedness of the punctured upper half-plane, meromorphic identity theorem, local factorization, nonremovable pole and conjugation symmetry. Those are roadmap items, not implicit axioms.

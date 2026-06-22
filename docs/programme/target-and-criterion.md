# Target and abstract criterion

For \(x>1/4\), define

\[
\mathcal S_\Xi(x)=\frac{1}{2\sqrt{x}}
\frac{\xi'}{\xi}\!\left(\frac12+\sqrt{x}\right).
\]

The restriction puts \(\sigma=1/2+\sqrt{x}\) in the absolutely convergent Euler-product half-plane.

The criterion subproject documents the following implication. Suppose positive Stieltjes transforms

\[
S_j(w)=\int_0^\infty\frac{d\nu_j(t)}{t+w},
\qquad w\in\mathbb C\setminus(-\infty,0],
\]

are uniformly bounded at one positive point and converge to \(\mathcal S_\Xi\) on one nonempty open interval in \((1/4,\infty)\). Montel compactness supplies a holomorphic slit-plane limit. Agreement on the interval identifies its logarithmic derivative with \(-\Xi'/\Xi\), whose nonremovable poles would reveal non-real zeros. Holomorphy therefore excludes such zeros.

This page records the consumer interface only. The canonical proof and one-point Hausdorff equivalent are maintained in `subprojects/riemann-one-point-resolvent`.

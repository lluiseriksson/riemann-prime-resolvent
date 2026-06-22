# Positive spectral approximants

Let \(\nu_j\) be positive measures on `[0,∞)` and

\[
S_j(w)=\int_0^\infty\frac{d\nu_j(t)}{t+w},
\qquad w\in\Omega.
\]

For a paired finite spectrum \(\{\pm\gamma_{j,k}\}\),

\[
S_j(x)=\sum_k\frac1{\gamma_{j,k}^2+x}
=\frac12\operatorname{Tr}(D_j^2+xI)^{-1}.
\]

## One-point normal-family control

Fix \(x_*>0\). If \(\sup_jS_j(x_*)<\infty\), then the family is locally bounded on \(\Omega\). For every compact \(K\subset\Omega\), there is \(C_K\) such that

\[
\frac1{|t+w|}\le\frac{C_K}{t+x_*},
\qquad t\ge0,\ w\in K.
\]

Integration gives \(|S_j(w)|\le C_KS_j(x_*)\). Montel's theorem supplies compact-open subsequential limits.

## Abstract criterion input

If the same family converges pointwise to \(\mathcal S_\Xi\) on one nonempty interval in \((1/4,\infty)\), every subsequential holomorphic limit agrees there with the target. The slit-plane criterion then implies RH.

This is the exact interface the companion repository must discharge. Positivity makes one scalar bound enough for normality, but does not supply the convergence itself.

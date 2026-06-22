# Arithmetic target and integer-cutoff tail

For real \(\sigma>1\), logarithmic differentiation yields

\[
\frac{\xi'}{\xi}(\sigma)=
\frac1\sigma+\frac1{\sigma-1}-\frac12\log\pi
+\frac12\psi(\sigma/2)
-\sum_{m=2}^{\infty}\frac{\Lambda(m)}{m^\sigma}.
\]

With \(y=\sqrt{x}\) and \(\sigma=1/2+y\), this gives an explicit prime-side expression for \(\mathcal S_\Xi(x)\).

For an **integer** cutoff \(N\ge3\), let \(P_N(x)\) use only \(m\le N\). If \(\delta>0\) and \(y\ge1/2+\delta\), then \(\sigma\ge1+\delta\), and

\[
|\mathcal S_\Xi(x)-P_N(x)|
\le
\frac{N^{-\delta}}{1+2\delta}
\left(\frac{\log N}{\delta}+\frac1{\delta^2}\right).
\]

Indeed, \(0\le\Lambda(m)\le\log m\), and for \(N\ge3\) the standard sum–integral comparison gives

\[
\sum_{m>N}\frac{\log m}{m^{1+\delta}}
\le
\int_N^\infty\frac{\log t}{t^{1+\delta}}\,dt.
\]

The integer-cutoff wording avoids the off-by-one ambiguity present when an arbitrary real cutoff is used.

The complete discrete tail theorem remains a formalization target. The companion construction repository owns its use in the three-part error budget.

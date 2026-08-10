# Certified second-mode floors after prime three enters

## The cancellation that must not be split

Let a target interval of length $a$ touch a source interval of length $b$.
For a source polynomial $f$, polynomial division writes the logarithmic
potential as a polynomial plus

\[
 -\frac12 f(-u)\log(u+b)+\frac12 f(-u)\log u.
\]

The second term produces the endpoint flux and the algebraic
$R_f(u)\log u$ tail.  On a very short source interval the two pieces of the
second-Green decomposition can separately be enormous even though their sum
is small.  Taking their norms separately caused the previous $10^{24}$
artifact.

For $z=1+2b/a>1$, the normalized target-Legendre coefficient of the analytic
logarithm is exact:

\[
 \ell_m=(-1)^m\sqrt{\frac{a}{2m+1}}
       \bigl(Q_{m+1}(z)-Q_{m-1}(z)\bigr).
\]

Multiplication by the degree-$j$ part of $f(-u)$ is finite banded, with Gaunt
coefficient

\[
 \int_{-1}^1P_jP_mP_n
   =2\begin{pmatrix}j&m&n\\0&0&0\end{pmatrix}^{\!2}.
\]

`arb_adjacent_full_map.py` therefore adds endpoint flux, singular tail and
analytic tail entry by entry before taking an outer product.  The squared
Wigner coefficients are computed by an exact rational recurrence.  For a
strictly separated pair, the same formula is used with the difference of the
two $Q$ sequences belonging to $\log(g+u+b)-\log(g+u)$.  Tests compare both
identities against the independent closed-form moment implementation entry
by entry.

The remaining analytic tail is bounded without evaluating the source
polynomial outside its interval.  Positivity of Legendre linearization gives

\[
 \sum_m
 \begin{pmatrix}j&m&n\\0&0&0\end{pmatrix}^{\!2}
 \le \frac1{2(n-j)+1},
\]

and Heine's bound for $Q_m(\cosh\eta)$ supplies a geometric majorant.  At
$a=0.551$ and cutoff 640 the formerly catastrophic orientation is below
`8.531986622355512e-13`.

## Registered Schur certificate

The registered parameters are

\[
 a=0.551,\qquad d=16,\qquad 16\le n<640,
 \qquad 640\le n<4096.
\]

The first band contains all seven source blocks and the degree-23 smooth
kernel in the same Arb row before squaring.  In the infinite tail, the
endpoint-flux and adjacent-singular Grams remain matrix valued.  The
self-regularized, adjacent-analytic and separated remainder has certified
operator norm

\[
 \eta_{\rm other}<6.49774678632731\,10^{-6}.
\]

The common complement floor is
`0.6126659781618331`.  With balance parameter `0.1`, the final interval
inertias are:

| sector | shift | negative | positive | unresolved | first positive Schur lower |
|---|---:|---:|---:|---:|---:|
| even | $0.001$ | 1 | 55 | 0 | `0.0003583471624191602` |
| odd | $0.05$ | 1 | 55 | 0 | `0.021884290361950456` |

The maximum entry radii are respectively
`3.645030522554882e-15` and `3.653069970337624e-15`.  Hence the exact
localized operator at this point has at most one eigenvalue below `0.001` in
the even sector and at most one below `0.05` in the odd sector.  Equivalently,
these are rigorous lower floors for the second spectral point in the two
sectors.

The certificate is reproduced by

```python
from experiments.theta_pencil.second_window_schur_certificate import (
    certify_second_window_schur,
)

print(certify_second_window_schur(tail_start=640))
```

## Scope

This closes the seven-block spectral-gap premise at one point after the
prime-three translation becomes active.  It does **not** yet prove positivity
of the lowest even eigenvalue.  The ordinary polynomial Kato--Temple trial
has a best measured even residual of about `2.42e-5`, while the certified
gap and Rayleigh quotient require about `7.05e-6`.  A certified tail-corrected
or Feshbach trial remains the next obligation.  No claim about RH follows
from this second-mode certificate alone.

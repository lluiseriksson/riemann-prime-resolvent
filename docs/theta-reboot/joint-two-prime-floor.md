# Joint pointwise floor for the two-prime window

## Why the old floor failed

The first second-window complement estimate retained the prime-two boundary
comparison and subtracted the full norm of prime three.  At \(a=0.675\) this
gives only `0.250182716428273`.  Dividing the exact degree-16--639 band Gram
by that common number creates two large negative directions and one small
negative direction in the even Schur matrix.  A complete balance sweep proves
that no scalar Young parameter repairs this floor.

## Fiber graph

The seven cut intervals split into three invariant fibers under the active
translations:

1. the four equal edge intervals form the path
   \(4\mathbin{-_2}0\mathbin{-_3}6\mathbin{-_2}2\);
2. bridge intervals 1 and 5 form one prime-two edge;
3. the centre interval 3 is isolated.

At fixed local coordinate \(t\), an edge labelled \(p\) has weight
\(-\log(p)/\sqrt p\).  Adding
\(V(x)=-\frac12\log(1-x^2)\) on the diagonal gives matrices of sizes four,
two and one whose least eigenvalues bound boundary potential plus both prime
translations.

## Arb certification

The proof divides \([-1,1]\) into 1024 cells.  On each cell it encloses all
physical coordinates, replaces every potential by its rigorous minimum, and
isolates the eigenvalues of the resulting constant matrices.  At
\(a=0.675\):

| component | lower bound |
|---|---:|
| four-edge graph | `-0.5279028197822501` |
| bridge graph | `-0.3372001950043946` |
| centre | `-5e-324` |

Adding the scalar term, subtracting the rigorous order-39 smooth loss
`0.1370895210544908`, and adding \(H_{16}\) gives the Loewner bound

\[
 \boxed{D\succeq0.6936865091909813I}.
\]

## Resulting frontier

With tail balance \(0.05\), directional self-tail Gram and residual balance
\(0.01\), the final interval inertias are

| sector | negative | positive | unresolved | Schur lower | coercive lower |
|---|---:|---:|---:|---:|---:|
| even | 0 | 56 | 0 | `3.3725139852259157e-12` | `1.5531308365921327e-13` |
| odd | 0 | 56 | 0 | `2.4017941599485156e-9` | `1.1008427768841639e-10` |

Therefore

\[
 \boxed{A_{0.675}\succeq1.5531308365921327\cdot10^{-13}I>0},
\]

and domain monotonicity proves \(\lambda_a>0\) for every
\(0<a\le0.675\).  This remains below the prime-power-four threshold
\(a=\log2\) and does not prove RH.

The executable proofs are `second_window_pointwise_floor.py` and
`support_0675_certificate.py`.

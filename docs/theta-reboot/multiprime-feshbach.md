# Multiprime Feshbach bookkeeping

## Combined correction

For active primes $p$ and retained endpoint jets $0\le j<J$, write the
high-mode cross map as

\[
 J_{m n}=\sum_p\sum_{j<J}
  \left(-\frac{2\log p}{\sqrt p}\right)
  e_m^{(j)}(1)\,q_{p,j,n}.
\]

The Schur correction is $JD^{-1}J^*$.  It is not the sum of the individual
prime corrections: it also contains
$J_2D^{-1}J_3^*+J_3D^{-1}J_2^*$.  The Arb implementation now forms a single
Gram matrix on the combined $(p,j)$ index, so these terms are retained.
For a small two-prime example it agrees with an independently assembled
floating matrix to $2\,10^{-13}$.

The same generalization has been made in four other places required by a
complete Schur calculation:

- the exact finite Legendre matrix of each prime translation;
- the vector-valued continuous remainder variation;
- the omitted endpoint-jet tail;
- the source-box reconstruction.

The old prime-two entry points remain wrappers and reproduce their previous
tests.

## Global-basis pilot at $a=0.551$

A floating design audit with 64 low modes, finite cutoff 1024, four jets and
jet end 10000 gives the correct finite inertia after the shifts used by
Temple:

| sector | shift | first source eigenvalue | second source eigenvalue |
|---|---:|---:|---:|
| even | $0.001$ | $-9.9995\,10^{-4}$ | $3.61\,10^{-4}$ |
| odd | $0.05$ | $-4.9986\,10^{-2}$ | $2.26\,10^{-2}$ |

Thus the finite source has exactly the desired one-low-direction geometry.
The global omitted-tail bound does not close: the common high denominator is
almost zero at degree 1024, and the unstructured boundary-potential tail is
already of order $10^{-1}$.  Raising the cutoff enough to respect the even
margin would require impractically large global sections.  This diagnoses why
the cut-adapted second-Green estimate is essential; the multiprime Feshbach
code is correct infrastructure, but the crude global tail is not a proof
route near the prime-three boundary.

## Exact support-window guards

Python's binary float for `log(3)/2` renders as the decimal
`0.5493061443340549`, which is slightly larger than the exact value.  Feeding
that decimal into Arb activates a nonzero prime-three overlap.  A validation
based on the same rounded float incorrectly classified it as the endpoint.

All support-window guards now compare the exact input decimal against
80-digit `Decimal.ln()` values.  Consequently:

- `0.5493061443340549` belongs to the second prime window and requires $p=3$;
- `0.5493061443340548` lies rigorously below the boundary and belongs to the
  first prime window.

The distinction is regression-tested.  No certificate may use the rounded-up
decimal while omitting the prime-three term.

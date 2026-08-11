# Two-thirds theorem: finite Weil inertia and its exact scope

## Verified source

On 2026-08-10 Anthropic released Claude's paper
[*More than two thirds of the zeros of the Riemann zeta function lie on the
critical line*](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf),
an accompanying
[Lean repository](https://github.com/anthropics/zeta-23-lean), and a
[methodology report](https://www.anthropic.com/research/riemann-zeta).
The paper proves unconditionally that at least two thirds of the zeros are
simple and on the critical line; the optimized test family raises the
constant to approximately `0.6725`.  This is a density theorem, not RH.

The result builds on the unconditional pair-correlation formula of Baluyot,
Goldston, Suriajaya and Turnage-Butterbaugh and on Bombieri's inertia reading
of finite compressions of the Weil form.  The new step is a rank--trace
inequality that retains the indefinite off-line blocks instead of discarding
the zero side when termwise positivity fails.

The external Lean repository states a sorry-free proof against Mathlib's
`riemannZeta`, with no nonstandard axioms.  This project has inspected the
statement and source layout but has not replayed that multi-hour build; kernel
reproduction is therefore not claimed here.

## Signature decomposition

For a finite test space, write the compression of Weil's form as

\[
 G=P+Q.
\]

Every distinct zero on the line contributes a positive rank-one block to
\(P\).  The functional-equation partner of an off-line zero contributes a
block of signature at most \((1,1)\) to \(Q\).  If

\[
 P\succeq0,\qquad \operatorname{rank}P\le r,
 \qquad n_+(Q)\le b,
\]

then the paper's rank--trace lemma gives

\[
 r\ge 2\operatorname{tr}P+4\operatorname{tr}Q-4b-
       \lVert P+Q\rVert_F^2.                       \tag{ZT1}
\]

Independently, every Hermitian \(G\) with positive trace satisfies

\[
 n_+(G)\ge
 \frac{(\operatorname{tr}G)^2}{\lVert G\rVert_F^2}. \tag{ZT2}
\]

`rank_trace_inertia.py` implements the exact rational right sides of (ZT1)
and (ZT2), plus a floating design audit for finite point matrices.  The exact
functions do not infer the hypotheses: a convenient prime--archimedean split
is not automatically the zero-side decomposition \(P+Q\).

## Integration with the support-one certificate

The present repository has already proved

\[
 Q_{58}L_1Q_{58}\succeq0.0046006509\,Q_{58}.
\]

This reduces support-one positivity to the finite Schur complement

\[
 S_{58}=P_{58}L_1P_{58}
 -P_{58}L_1Q_{58}(Q_{58}L_1Q_{58})^{-1}Q_{58}L_1P_{58}. \tag{ZT3}
\]

The two-thirds theorem supplies a new diagnostic for (ZT3), but does not
remove its cross correction.  In particular:

1. an inertia count for the raw \(58\)-mode source block is not an inertia
   count for \(S_{58}\);
2. forcing some positive directions is not positive semidefiniteness;
3. (ZT2) closes the finite gate only if a rigorous lower trace and upper
   Frobenius enclosure force all 58 directions (parity by parity), or if a
   separate interval-inertia calculation certifies zero negative directions.

The registered executable therefore reports the raw even and odd source
blocks as floating diagnostics and prints that scope in every result.

At dimension 58 and Gauss order 1024 the point-matrix audit gives

| block | dimension | \((\operatorname{tr}G)^2/\lVert G\rVert_F^2\) | forced positive directions |
|---|---:|---:|---:|
| even | 29 | `18.9385240493` | 19 |
| odd | 29 | `19.4277199110` | 20 |
| direct sum | 58 | `38.3661592384` | **39** |

Thus the imported two-moment mechanism forces exactly \(39/58=0.672413\ldots\)
of this finite source discretization, numerically mirroring the global
two-thirds constant.  It leaves 19 directions uncertified.  Small negative
point eigenvalues shrink by approximately a factor four when the quadrature
order doubles from 256 to 512 to 1024, so they are recorded as quadrature
sensitivity, not as negative spectrum.  Neither observation encloses (ZT3).

Retaining modes 58 through 255 and taking their finite Schur complement does
not improve the moment count.  At the same Gauss order its tail Ritz value is
`1.4948996912`, while the even, odd and combined moment ratios are
`18.7729830828`, `19.2532106344` and `38.0260158439`: again exactly 19, 20
and 39 forced directions.  This is closer to (ZT3) than the raw block, but it
still omits every cross column beyond mode 255 and is not an enclosure.

## Structural barrier and next gate

The paper proves that bandwidth-one, first/second-moment information cannot
reach proportion one: its formal companion gives a ceiling near `0.68183` for
that certificate class.  The paper also notes that wider Fourier support
requires prime-correlation input beyond the presently unconditional range.
Consequently it would be circular to extrapolate `0.6725` to RH.

The useful target for this repository is narrower and falsifiable:

> Construct rigorous trace and Frobenius enclosures for the actual Schur
> complement (ZT3), including its certified cross tail.  Accept the moment
> route only if it forces the full parity dimensions.  Otherwise retain the
> rank--trace result as an inertia diagnostic and seek a third, local invariant
> that detects one residual hyperbolic plane.

This imports a successful linear-algebraic mechanism while preserving the
existing RH success condition: every support and zero negative directions.

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
| even | 29 | `18.9385242113` | 19 |
| odd | 29 | `19.4277200629` | 20 |
| direct sum | 58 | `38.3661595521` | **39** |

Thus the imported two-moment mechanism forces exactly \(39/58=0.672413\ldots\)
of this finite source discretization, numerically mirroring the global
two-thirds constant.  It leaves 19 directions uncertified.  The raw source
uses the smooth Legendre series through power 95, whose analytic remainder is
`4.9808002138e-17`.  At tolerance `1e-12` the point matrix observes 26
positive and three unresolved directions in each parity, with no observed
negative direction.  These are still floating observations, not enclosures
of (ZT3).

The corresponding statement about the **raw source** is now rigorous rather
than floating.  `arb_support_one_source.py` encloses every entry using Arb:
the five active prime powers \(2,3,4,5,7\) are integrated with ball
arithmetic, the smooth kernel is summed through power 95, and its analytic
remainder is charged as an operator-norm loss.  Congruence by point trial
vectors followed by interval Gershgorin proves a 26-dimensional positive
subspace in each parity.  At 512-bit source precision and 2048-bit prime
precision the certified lower spectral bounds are

| parity | certified dimension | lower spectral bound |
|---|---:|---:|
| even | 26 of 29 | `4.484080139063457e-12` |
| odd | 26 of 29 | `4.800583144111085e-10` |

The trial transforms have certified Gram lower bounds
`0.9999999999999939` and `0.9999999999999948`.  The calculation is
reproduced by

```console
python -m experiments.theta_pencil.run_arb_support_one_source
```

This result proves neither that the three-dimensional complements are
nonnegative nor that these 52 directions survive the subtraction in (ZT3).
The infinite Schur correction is positive semidefinite before subtraction and
can reduce the positive index.  The certificate therefore narrows the raw
near-null cluster but does not discharge the actual Schur gate.

The rational complement proof also yields a strictly stronger Schur
majorant than the single floor in (GS32).  Write the tail operator as

\[
 D=\operatorname{diag}(H_n)_{n\ge58}+R,
 \qquad R\succeq\beta I,
\]

where the exact rational number
`beta = complement_margin - harmonic_floor` is extracted from the registered
certificate.  Operator monotonicity of inversion then gives

\[
 D^{-1}\preceq
 \operatorname{diag}\bigl((H_n+\beta)^{-1}\bigr)_{n\ge58}. \tag{ZT5}
\]

Thus, if $b_n$ is the cross column into degree $n$, the true Schur
correction is bounded above by

\[
 CD^{-1}C^*\preceq
 \sum_{n\ge58}\frac{b_nb_n^*}{H_n+\beta}.          \tag{ZT6}
\]

`support_one_degreewise_schur.py` computes every denominator in (ZT5) as an
exact `Fraction`.  The first is exactly the degree-58 rational margin and the
next differs by exactly `1/59`; no floating input enters this step.  Its
recoverable finite audit is run with

```console
python -m experiments.theta_pencil.support_one_degreewise_schur \
  --matrix-cache support-one-256.npz --output support-one-256.json
```

The 256-mode production run is intentionally not reported here: it exceeded
the registered local resource envelope and the available Colab browser is
permission-blocked.  The executable and atomic post-build cache are deposited
so that the first remote run yields a reproducible falsifier rather than a transient
screen value.  Even a positive finite result would still require an interval
enclosure of the entries and the infinite sum in (ZT6).

The first analytic treatment of that infinite sum is decisively too coarse.
Splitting each prime translation into endpoint jets plus a Wang remainder,
then applying the triangle inequality to the five prime powers, the boundary
potential and the smooth remainder gives, from degree 256 onward,

| parity | weighted cross norm upper | correction norm upper |
|---|---:|---:|
| even | `212.6978526831` | `45240.3765360` |
| odd | `225.4706199305` | `50837.0004519` |

These are the best values in the registered sweep over one through six
endpoint jets; more jets amplify the high derivatives of the 58-dimensional
source.  They are fourteen to sixteen orders of magnitude larger than the raw
positive-subspace margins.  The figures are reproduced locally in seconds by

```console
python -m experiments.theta_pencil.support_one_degreewise_schur \
  --absolute-tail-only --tail-first-degree 256 --jet-count 1 --partitions 128
```

A large **upper** bound is not a lower bound on the true correction and hence
is not an impossibility theorem.  It does falsify this particular
triangle-inequality closure.  Any viable tail proof must retain cancellations
between prime powers and between endpoint jets, for example as signed
matrix-valued band Grams; treating the components by separate norms cannot
reach the certified margins.

There is nevertheless useful structure inside the large endpoint term.  In a
fixed parity block, retaining $J$ endpoint jets gives the exact
factorization

\[
 C_J=E_JP_J,
 \qquad
 C_JD_0^{-1}C_J^*=E_J(P_JD_0^{-1}P_J^*)E_J^*,       \tag{ZT7}
\]

where $E_J$ has exactly $J$ columns and all five prime powers have already
been summed in $P_J$.  Consequently this Gram has rank at most $J$,
independently of the number of high degrees or prime powers.  The certified
26-dimensional raw positive subspace therefore retains at least $26-J$
positive directions after subtraction of this isolated Gram.  This is an
exact inertia statement, but it does not order the isolated Gram against the
full correction, whose cross terms with the regular remainder can have either
sign.

On the floating band 256--4095, the one-jet Gram has rank one and norms
`1.2062610369` (even) and `1.2617739163` (odd).  Summing prime Grams separately
gives `1.2088289425` and `1.2317511138`, so the signed/separate ratios are
`0.9978757080` and `1.0243740819`: cross-prime interference is not the missing
cancellation.  The reproducible audit is

```console
python -m experiments.theta_pencil.support_one_degreewise_schur \
  --endpoint-jet-band-only --tail-first-degree 256 \
  --tail-last-degree 4096 --jet-count 1
```

Thus the next Gram must keep endpoint jets, their regular remainders, the
boundary potential and the smooth kernel together.  It cannot gain the
required orders of magnitude merely by summing prime powers before taking a
norm.

The failure of the two moments is sharp, not merely a weak estimate.  For
dimension \(n\), trace \(t>0\), squared Frobenius norm \(f\), and
\(p=\lceil t^2/f\rceil<n\), put \(q=n-p\),

\[
 m=\frac tn,\qquad V=f-\frac{t^2}{n},\qquad
 a=m+\sqrt{\frac{qV}{pn}},\qquad
 c=m-\sqrt{\frac{pV}{qn}}.                         \tag{ZT4}
\]

The spectrum with \(p\) copies of \(a\) and \(q\) copies of \(c\) has
exactly trace \(t\) and squared Frobenius norm \(f\).  Moreover \(c<0\) iff
\(pf>t^2\).  For the raw 58-mode moments, (ZT4) gives 39 eigenvalues
`2.9672691489` and 19 eigenvalues `-0.04929079085`, reproducing both moments.
Thus those two scalar observables are literally compatible with negative
index 19.  No argument using only them can certify a fortieth positive
direction, regardless of numerical precision.

Retaining modes 58 through 255 and taking their finite Schur complement does
not improve the moment count.  At the same Gauss order its tail Ritz value is
`1.4948996912`, while the even, odd and combined moment ratios are
`18.7729830828`, `19.2532106344` and `38.0260158439`: again exactly 19, 20
and 39 forced directions.  This is closer to (ZT3) than the raw block, but it
still omits every cross column beyond mode 255 and uses a quadrature smooth
block.  Its tiny negative eigenvalues decay by approximately a factor four
when the quadrature order doubles, so they are treated as quadrature
sensitivity; this finite Schur matrix is not an enclosure.

## Structural barrier and next gate

The paper proves that bandwidth-one, first/second-moment information cannot
reach proportion one: its formal companion gives a ceiling near `0.68183` for
that certificate class.  The paper also notes that wider Fourier support
requires prime-correlation input beyond the presently unconditional range.
Consequently it would be circular to extrapolate `0.6725` to RH.

The useful target for this repository is narrower and falsifiable:

> Construct an interval enclosure of the actual Schur complement (ZT3),
> including its certified cross tail.  Use the 26+26 raw-source trial
> decomposition to expose the three-dimensional near-null complement in each
> parity, but control the Schur subtraction on the full trial space before
> transferring any inertia statement.  Trace and Frobenius data alone are
> closed by the explicit adversary (ZT4).

This imports a successful linear-algebraic mechanism while preserving the
existing RH success condition: every support and zero negative directions.

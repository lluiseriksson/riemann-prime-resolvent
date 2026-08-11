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

## Degreewise majorant versus the true finite high block

The 58--255 production falsifier has now been completed without lowering its
registered parameters.  A rectangular constructor computes only the
58-by-58 source and 58-by-198 cross blocks; the high--high block is assembled
from twelve atomic caches (dominant/scalar, five prime powers and six smooth
power ranges).  Gauss order 1024 integrates the prime polynomial products
exactly in exact arithmetic: their maximum degree is 510, below the
Gauss--Legendre exactness limit 2047.  The reconstructed source differs from
the independent Arb midpoint by at most `7.7715611724e-14`.

Using the exact rational degreewise denominators in (ZT5) gives

| parity | negative | positive | unresolved | first eigenvalue |
|---|---:|---:|---:|---:|
| even | 6 | 20 | 3 | `-183.1498063273` |
| odd | 6 | 20 | 3 | `-45.5326999806` |

This is a robust falsification of the diagonal-majorant *design*, not of the
operator: replacing the full high block by its diagonal lower minorant loses
the correlations that its inverse needs.

Keeping the complete 198-dimensional high block reverses the verdict.  Its
least eigenvalue is `1.4948997122004581`, and the finite Schur complement has

| parity | negative | positive | unresolved | first resolved positive |
|---|---:|---:|---:|---:|
| even | 0 | 26 | 3 | `1.3553476401530287e-12` |
| odd | 0 | 26 | 3 | `2.3248384822321485e-10` |

The three smallest values per parity remain at floating roundoff scale, so
this is not an interval positivity certificate.  It does identify the right
finite object: an Arb enclosure of the full 58+198 block (or an equivalent
block-LDL factorization), followed by a signed enclosure of the cross columns
above degree 255.  Further scalar or degreewise denominators are now rejected
by the production falsifier.

The full Arb proof need not invert a 198-dimensional interval matrix.  Let
$Y$ be any trial map from the 58-dimensional source into the high block and
put $R=C^*-DY$.  Completing the square a second time gives the exact residual
inequality

\[
 A-CD^{-1}C^*\succeq
 A-CY-Y^*C^*+Y^*DY-\delta^{-1}R^*R,               \tag{ZT8}
\]

whenever $D\succeq\delta I$.  Here $\delta$ is the already certified
rational margin `0.004600650916100899`.  Unlike direct interval inversion,
(ZT8) only needs certified actions of $D$ on the columns of $Y$.

Taking $Y$ from a truncated SVD of the floating solve $D^{-1}C^*$ sizes
that obligation sharply.  Rank 16 still leaves one negative direction per
parity (`-5.57e-12` even and `-2.23e-10` odd).  Rank 20 gives

| parity | residual norm | next omitted singular value | positive/unresolved |
|---|---:|---:|---:|
| even | `1.2925208593e-9` | `3.3445210862e-10` | 26 / 3 |
| odd | `1.6431117749e-9` | `4.4736077984e-10` | 26 / 3 |

Thus the production interval task is reduced from certifying an arbitrary
198-by-198 inverse to forty parity-pure high-vector actions plus finite Gram
arithmetic.  The inequality and its Loewner direction are unit-tested on an
independent positive block.  The rank-20 numerical data remain a design
audit until the trial vectors, actions and residual tail are enclosed with
Arb.

The rank-20 trial is now a deterministic, portable artifact rather than an
implicit SVD choice.  The exporter writes parity-pure `float64` vectors (used
as exact dyadic rationals by Arb), right factors, index maps and metadata.
The registered factor hashes are

| factor | SHA-256 |
|---|---|
| even action vectors | `ac7d5cc191fefb4836f2f7a2e76b351efca9bc6fed5b3a978c3f529a38417ae2` |
| even right factor | `b3aba60b0a3a70445e936e9743e65f31cc894ef058e5d4ec72a822402ade7607` |
| odd action vectors | `fcd36d510fdb71187203e2086038b658bc5a0ca0a37e47e982082592e2079eeb` |
| odd right factor | `ac94e9f3a7104a28ba90d6007f28adb0a6a96c8034afd0a0ab99e66f67768e5a` |

It is regenerated, rather than trusted as an opaque binary, by

```console
python -m experiments.theta_pencil.support_one_degreewise_schur \
  --component-cache-dir <parts> --matrix-cache <source-cross.npz> \
  --residual-schur-rank 20 --export-residual-trial <trial.npz>
```

The complete NPZ had SHA-256
`ddeab8ca1557a0c3d7216f92963b83bd46eb17fd1d62089c41b35c516470cdc5`
in the registered run.  Reproduction should compare the internal factor
hashes, which are independent of ZIP container metadata.

Each prime-power action is now an independent resumable unit.  For example,

```console
python -m experiments.theta_pencil.run_arb_support_one_residual_action \
  --trial <trial.npz> --output <even-00-p2.npz> \
  --parity even --column 0 --prime 2 \
  --maximum-degree <cutoff> --precision <bits>
```

The runner verifies both factor hashes before calling Arb and hashes the
resulting midpoint and radius arrays.  Existing outputs are reused only when
all request metadata and result hashes match.  The production grid contains
two parities, twenty columns and the five active prime powers
`2, 3, 4, 5, 7`; it has not yet been run.  In particular, the existence of
this runner is reproducibility infrastructure, not an interval certificate.

### Endpoint preflight for the frozen trial

The expensive grid now has a mandatory floating preflight.  For the frozen
rank-20 trial, the endpoint value of `e_low - Y` has norm
`21.4362130848` in the even block and `21.1600463454` in the odd block.
These are respectively `74.56%` and `72.34%` of the uncorrected endpoint
norms: the finite SVD has not cancelled the leading jump.

Using the registered Bernstein jump bound from degree 256 gives leading-jet
weighted-norm upper bounds `7.31035` and `7.21617`, hence Schur-correction
uppers `53.4412` and `52.0731`.  Keeping the five prime powers signed over
the diagnostic band 256--4096 still gives leading-jet Gram norms `0.670648`
and `0.660381`.  The latter values are diagnostics, not lower bounds for the
complete residual, because higher jets can cancel on a finite band.

This closes only the **absolute-tail proof design** for the frozen cutoff-256
trial; it says neither that the exact residual has those norms nor that the
operator is nonpositive.  The next trial must build the endpoint condition
into the solve (or move the cutoff far enough that enforcing it is cheap)
before the 200 Arb prime-power actions are worth running.  Reproduce the gate
with

```console
python -m experiments.theta_pencil.support_one_residual_endpoint_audit \
  --trial <trial.npz> --first-degree 256 --last-degree 4096
```

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

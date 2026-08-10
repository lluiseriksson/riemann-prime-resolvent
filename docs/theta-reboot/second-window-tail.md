# The regularized seven-block tail

## Blockwise second-Green estimate

In the second prime window the cut-adapted logarithmic operator has seven
local blocks.  For a retained polynomial source on block $j$ and an omitted
target tail on block $i$, the regularized map is

\[
 Q_{N_i}D_iL_{ij}P_{d_j}.
\]

There are three cases.

1.  A self block uses the exact Legendre coefficients after its two endpoint
    fluxes have been removed.
2.  A touching block uses the second-Green polynomial/logarithmic
    decomposition already used in the first prime window.
3.  A separated block has no endpoint flux.  If its gap is $g>0$, its kernel
    is analytic on the closed target interval.  An Arb Taylor enclosure of
    $D_iL_{ij}f$ followed by Wang's Legendre coefficient estimate therefore
    bounds its entire omitted tail.

The separated estimate is checked independently against an explicit Arb sum
of the regularized coefficients.  It is important to bound the omitted tail,
not the whole separated operator: when a gap is short the latter can be many
orders of magnitude too large.

## Seven-by-seven comparison

Let $C_{ij}$ be the certified operator-norm bound for the corresponding
block.  For block vectors $f_j$,

\[
 \|(QDL P f)_i\|\le\sum_j C_{ij}\|f_j\|,
\]

so $\|QDLP\|\le\|C\|_2$.  `arb_second_window_tail.py` encloses this spectral
norm by applying Arb/Rump to $C^TC$.  Reflection of the comparison matrix and
the inequality against the elementary row--column bound are tested.

At

\[
 a=0.62,\qquad d_i=16,\qquad N_i=128,
\]

the result is

\[
 \boxed{\|Q_{128}DLP_{16}\|<69.69302376068656}.
\]

The corresponding regularized logarithmic tail is below

\[
 \frac{69.69302376068656}{128\cdot129}<0.004222.
\]

This is a rigorous analytic-tail result, not positivity of $A_{0.62}$.
Finite sections resolve a near-zero mode as the local degree is increased;
therefore a direct positive Schur complement is not expected to close.  As at
$a=0.54$, the tail bound must instead support a one-negative-direction gap
certificate followed by Kato--Temple.

## Adaptive-degree warning

Close to $a=\log(3)/2$ the four edge intervals are very short.  Keeping 16
source modes on such an interval can make an oriented second-Green bound of
order $10^{15}$.  With one retained edge mode the same bound at $a=0.56$
falls below $60$.  This is a conditioning fact about the local basis, not a
positivity theorem: removing edge modes can also hide the near-zero trial
direction.  Any final certificate must resolve that direction and may not use
adaptive truncation merely because it improves a tail constant.

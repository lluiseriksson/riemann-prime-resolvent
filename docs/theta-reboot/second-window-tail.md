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

## Legendre-Q repair of the short-gap loss

The Taylor/Wang estimate for a separated block is qualitatively wrong when
the gap $g$ is short: differentiating the kernel produces powers of $g^{-1}$
even though the original operator remains bounded.  The normalized target
coefficient has the exact form

\[
 c_n(v)=-\sqrt{\frac{2n+1}{a}}\,
 Q_n\!\left(1+\frac{2(g+v)}a\right).
\]

For $1+2g/a=\cosh\eta$, Heine's positive integral representation and
$\cosh t\ge 1+t^2/2$ give

\[
 Q_n(\cosh\eta)
 \le \sqrt{\frac{\pi e^\eta}{2n\sinh\eta}}
 e^{-(n+1)\eta}.
\]

After multiplication by the Legendre eigenvalue $n(n+1)$, the squared
Hilbert--Schmidt tail is bounded by a polynomial of degree four times
$e^{-2n\eta}$.  Its successive terms have a certified geometric ratio.
This bounds all retained source degrees simultaneously because the source
projection is contractive.  The implementation is checked against an
independent exact low-degree band.  The integral representation is
[DLMF 14.25.2](https://dlmf.nist.gov/14.25.E2), after converting Olver's
normalization to the classical integer-degree $Q_n$.

There is a related exact repair for a touching block whose source space is
the normalized constant.  After the first Green flux cancels the algebraic
term, its residual coefficient is

\[
 \frac12\sqrt{\frac ab}\frac{n(n+1)}{\sqrt{2n+1}}
 \left(Q_{n-1}(1+2b/a)-Q_{n+1}(1+2b/a)\right),
\]

and the same geometric argument applies.  This identity is regression-tested
against the exact moment matrix after subtracting the flux.

At $a=0.551$, local degrees $(1,8,1,24,1,8,1)$ and target degree 128 now give

\[
 \|Q_{128}DLP\|<44.62567850346515,
 \qquad
 \|Q_{128}LP\|<0.002702621033397841.
\]

The previous derivative estimate for the same short-gap geometry could be
as large as $10^{15}$.  This is a rigorous removal of that artifact, not yet
a second-mode certificate: using one edge mode does not by itself provide
the common complement floor required by Schur.

For general polynomial sources the reflected polynomial is evaluated outside
its source interval.  A sound envelope must include
$P_k(1+2a/b)$; omitting this factor gives a false improvement.  The code
retains that factor and does not automatically replace Wang in this case.

Finally, the signed singular expansion now also accumulates the genuinely
weighted logarithmic norm

\[
 \sum_{n\ge N}\frac{\|r_n\|^2}{n^2(n+1)^2},
\]

rather than dividing the unweighted sum globally by $N^2(N+1)^2$.  This adds
four powers to every moment-tail exponent and is strictly sharper in the
registered tests.  At the current near-threshold parameters it is still too
large by itself (`0.2194` for the worst 16-mode oriented block), so a final
Schur proof must retain its signed low-rank Gram structure instead of taking
one Frobenius norm.

# A multiprime Temple pipeline in the second window

## Exact action of the new prime

For a prime $p$ with $\log p/a<2$, the translated Legendre action has the
same endpoint-jet expansion as the prime-two action.  Only

\[
 c_p=1-\frac{\log p}{a},\qquad
 -\frac{2\log p}{\sqrt p}
\]

change.  `build_arb_prime_action` now implements this formula for arbitrary
prime $p$, and `build_arb_active_prime_action` adds certified actions with an
outward-rounded radius.  Independent Gauss--Legendre tests check the new
$p=3$ action.  The weighted variation and jump estimates have been
generalized in the same way.

The Temple routine accepts an explicit tuple of active primes.  In the
second window it uses `(2, 3)` in all four places where omitting the new prime
would be unsound: the finite trial matrix, the Arb action, the endpoint jumps,
and the variation remainder.

## Registered pilot at $a=0.551$

The following numbers use dimension 128, residual cutoff 8192, 768-bit
operator arithmetic and 8192-bit prime jets.  The spectral floors in this
table are assumptions for the pilot; they are not yet certified.

| sector | assumed second floor | Rayleigh interval | residual upper | Temple lower |
|---|---:|---:|---:|---:|
| even | $10^{-3}$ | $[4.97808,4.98655]10^{-8}$ | $3.09827\,10^{-5}$ | $-9.10194\,10^{-7}$ |
| odd | $5\,10^{-2}$ | $[1.3474459,1.3474544]10^{-5}$ | $4.42255\,10^{-4}$ | $9.56161\,10^{-6}$ |

Thus the odd trial already closes conditionally on its gap floor.  The even
trial does not: its residual must fall below roughly $7\,10^{-6}$.  Merely
extending the terminal degree is insufficient because the finite residual
above the trial dimension is already about $1.5\,10^{-5}$.

## Endpoint constraints do not solve the residual problem

The endpoint value is responsible for the slow $N^{-1/2}$ jump tail.  Trials
constrained by $f(1)=0$ increase the Rayleigh quotient only by about
$10^{-10}$ at dimension 128 and eliminate the numerical jump.  They do not
solve Temple, because a constrained Ritz vector is not stationary in the
full parity space: it acquires a large low residual normal to the constraint.
Adding derivative constraints has the same defect.  The implementation keeps
this option as a falsifier, but no positivity claim uses it.

## Next analytic target

The correct response to the endpoint jump is a tail-corrected trial, not a
hard boundary constraint.  If $r_n$ is the explicit high-mode residual, add

\[
 u_n\simeq-\frac{r_n}{H_n-\lambda}
\]

over a controlled high band and certify the remaining jet tail.  This is the
trial-vector analogue of the existing prime-jet Feshbach correction.  A full
second-window point certificate still requires two independent ingredients:

1. a positive Temple lower bound in both parity sectors; and
2. rigorous second-mode floors from the seven-block Schur comparison.

Neither ingredient is equivalent to RH, but neither is complete yet.

## Higher jets and the first Feshbach response

The variation certificate and Temple tail now accept any retained jet order
$m\ge1$.  The Arb implementation differentiates the fixed trial exactly,
certifies the weighted variation of order $m$, and adds the explicit tails of
jets $0,\ldots,m-1$.  A prime-three, order-two result is checked against an
independent quadrature.

This generalization does not by itself solve the even pilot.  At dimension
512 and terminal degree 8192, increasing $m$ from one to two makes the tail
larger: endpoint derivatives grow faster than the extra powers of 8192 help.
The value jump remains the asymptotically dominant term.

A genuine Feshbach response is different.  In a floating 1024-mode even
section, start from the 512-mode Ritz vector, let $r$ be its residual in modes
512--1023, and put

\[
 u_n=-\frac{r_n}{A_{nn}-\lambda}.
\]

The resulting normalized vector has finite-section residual
$8.80\,10^{-7}$; solving the full high block instead gives
$3.59\,10^{-7}$.  Both are well below the approximately $7\,10^{-6}$ target
set by the even Rayleigh quotient and the provisional $10^{-3}$ gap.

These are diagnostics, not interval bounds.  They identify the next precise
lemma: extend the diagonal response to the infinite high block and bound the
residual created by the bounded off-diagonal perturbation.  Merely increasing
the polynomial trial dimension leaves the value jump in the residual and is
much more expensive to certify.

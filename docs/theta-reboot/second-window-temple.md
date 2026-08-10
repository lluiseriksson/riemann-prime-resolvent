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

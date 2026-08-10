# Certified positivity immediately below the prime-three threshold

## Theorem

Let $A_a$ be Suzuki's Friedrichs operator for the localized Weil quadratic
form, in the normalization used throughout this directory, and set

\[
 a_*=0.5493061443340548.
\]

Then

\[
 \boxed{A_{a_*}\succeq
 1.746002657254026\,10^{-8}I>0.}
\]

This is an unconditional, computer-assisted theorem at one support radius.
It does not prove positivity on the whole support axis and does not prove the
Riemann hypothesis.

The registered decimal is strictly below the next arithmetic threshold:

\[
 \frac{\log 3}{2}-a_*
 =4.5697622618461262852\ldots\,10^{-17}>0.
\]

Thus only the prime-two translation is active.  In particular, this theorem
does not use the rounded binary value `math.log(3) / 2`, whose printed decimal
is slightly *above* the exact threshold and would require the prime-three
term.

## Certified second-mode floors

The degree-16/128 cut-adapted Schur calculation at 1024 bits gives

| parity | shift | negative | positive | unresolved | first positive lower |
|---|---:|---:|---:|---:|---:|
| even | $10^{-3}$ | 1 | 23 | 0 | $4.480586217909427\,10^{-4}$ |
| odd | $5\,10^{-2}$ | 1 | 23 | 0 | $2.788728089988670\,10^{-2}$ |

The common complement floor is `1.2527242280234323`.  The regularized
logarithmic tail is at most `0.002256786669946098`, and the omitted smooth
series is at most `3.909853760586346e-11`.  Therefore the second spectral
points are at least $10^{-3}$ and $5\,10^{-2}$ in the even and odd sectors.

## Kato--Temple discharge

| parity | dimension / residual end | Rayleigh upper | residual upper | Temple lower |
|---|---:|---:|---:|---:|
| even | $512/131072$ | $5.536495749122181\,10^{-8}$ | $6.150174158407603\,10^{-6}$ | $1.746002657254026\,10^{-8}$ |
| odd | $256/8192$ | $1.492082921986068\,10^{-5}$ | $2.925861216345902\,10^{-4}$ | $1.3208107172562633\,10^{-5}$ |

Both lower bounds are strict.  Taking their minimum proves the displayed
operator inequality.

## Reproduction and evidence

The top-level from-scratch reproducer is
`experiments/theta_pencil/support_near_prime3_certificate.py`.  The long
prime actions can instead be reproduced checkpoint-by-checkpoint with
`experiments.theta_pencil.run_arb_temple_checkpointed`, using the parameter
tuples encoded by that module.

The production artifacts generated on 2026-08-10 have SHA-256 hashes

| artifact | SHA-256 |
|---|---|
| even certificate JSON | `f8919ab2cffec9d74bceeed4aa7b399716202acdd156d0d137f81e49e9acb3d9` |
| even prime cache | `2c1361a43db18040a21b8b2e43a568793091de63149e6fab9211739cc479e83a` |
| odd certificate JSON | `067191d2dc3e834f654141df3e515cf052b7d9fb769a34b8cced0f8e8e1a9030` |
| odd prime cache | `96a27eaa9da8d9b0b5b47c99a2e18bcc0e0102d14d8880f92981a0d506a277a8` |

The caches contain midpoint/radius arrays together with the support,
precision, terminal degree and SHA-256 hash of the trial coefficients.  A
cache whose metadata does not match is rejected rather than reused.

## Next boundary

The result reaches the last representable binary64 point below
$\log(3)/2$, but it does not cross that number.  Above the threshold the
prime-three translation is nonzero and the correct cut-adapted graph has
seven blocks.  The next proof obligation is therefore a two-prime
Schur--Temple certificate, not another refinement of this one-prime point.

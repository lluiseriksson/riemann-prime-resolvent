# Certified localized positivity at \(a=0.42\)

## Claim and boundary

Let \(A_a\) be the Friedrichs operator representing Suzuki's localized
Weil quadratic form on \([-a,a]\).  The source formulas, form domain, compact
resolvent, parity reduction, Schur lemma, and Kato--Temple inequality are
developed in [the endpoint-tail note](endpoint-jump-tail.md).  Applying that
machinery at the rational input \(a=21/50\) gives the unconditional bound

\[
 \boxed{\lambda_1(A_{21/50})
        \ge 7.117220758560887\cdot 10^{-5}>0.}
\]

This is a localized theorem.  It is **not** the Riemann hypothesis: Weil's
criterion requires positivity for every compact support, equivalently for
every \(a>0\).

## Why two parity certificates suffice

Reflection commutes with \(A_a\), so its even and odd subspaces reduce the
closed form.  It is therefore enough to prove a positive lower bound for the
ground state in each subspace.  We certify a second-eigenvalue floor inside
each parity sector by a quadratic-form Schur complement, and then use a
separate Kato--Temple trial vector in that same sector:

| sector | shift \(\beta\) | low modes | source inertia | first positive source interval begins | omitted Schur correction |
|---|---:|---:|---:|---:|---:|
| odd | \(0.5\) | 176 | 1 negative, 87 positive | \(0.3979686224758113\) | \(0.09545418273526979\) |
| even | \(0.1\) | 128 | 1 negative, 63 positive | \(0.09900347540822979\) | \(0.04396964770977490\) |

The post-tail margins are respectively

\[
 0.3025144397405415>0,
 \qquad
 0.0550338276984549>0.
\]

The high block of \(A_a-\beta I\) is positive by the harmonic-number lower
bound.  The Schur inertia and the margins above therefore show that each
parity restriction has at most one eigenvalue below its displayed \(\beta\).

## Source-level enclosure

The finite Schur targets were computed by polynomial-exact Gauss--Legendre
quadrature.  Independently, Arb reconstructed the prime-2 translation from
endpoint jets, the smooth kernel from its Bernoulli power series, the
logarithmic boundary block from its closed formula, and the degree
4096--100000 jet correction from the stable Legendre recurrence.  The exact
sources lie in the registered entrywise balls of radius \(10^{-9}\):

| sector | maximum source-to-target distance | target radius |
|---|---:|---:|
| odd | \(4.372821520504176\cdot10^{-12}\) | \(10^{-9}\) |
| even | \(2.448471667318322\cdot10^{-12}\) | \(10^{-9}\) |

At 768-bit precision, interval eigendecomposition resolves every eigenvalue
of both boxes.  The infinite corrections combine the endpoint-jet tail, the
continuous prime remainder, the logarithmic boundary potential, and the
smooth kernel.  All bounds are outward rounded.

## Parity Kato--Temple bounds

The trial vectors are exact dyadic roundings of independent 256-mode Ritz
vectors.  Their residuals are enclosed through mode 8191 and the remaining
tails are bounded analytically.  The resulting interval budgets are:

| sector | Rayleigh interval | residual upper bound | second floor | Temple lower bound |
|---|---:|---:|---:|---:|
| odd | \([0.007572693700178843,0.007572693700262811]\) | \(0.003625650725897315\) | \(0.5\) | \(0.007545998707805297\) |
| even | \([0.00007423736086014931,0.00007423736094437140]\) | \(0.0005534327227082892\) | \(0.1\) | \(0.00007117220758560887\) |

Taking the smaller parity lower bound proves the boxed claim.

## Reproduction

Run:

```powershell
$env:PYTHONPATH='.'
python -m experiments.theta_pencil.support_042_certificate
```

The complete run uses 16,384-bit Arb arithmetic for the prime source matrices
and is expected to take tens of minutes and several gigabytes of memory.  The
driver fails closed if a source escapes its pre-registered ball, an inertia
interval is unresolved, an omitted tail exhausts the positive margin, or a
Temple lower bound is nonpositive.

## What remains

The direct finite scan stays positive beyond \(0.42\), but the ground-state
scale decays rapidly.  Repeating this calculation at isolated supports would
only produce more localized theorems.  Progress toward RH requires a
support-uniform comparison or continuation mechanism that prevents the
lowest branch from crossing zero as \(a\to\infty\).

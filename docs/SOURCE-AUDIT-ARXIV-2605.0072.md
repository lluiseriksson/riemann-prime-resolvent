# Source Audit: arXiv:2605.0072

Classification: rejected as proof source / methodological negative audit.

Local source SHA-256:

```text
1249e5bae56762e74aa3d3766a7ac8f4811326bdc6095d99874d2c646c2f26fb
```

## Scope

This note records a negative source audit for a manuscript whose pages 8--9
attempt to pass from cutoff-dependent continuity to a limit statement. The
source is not used as evidence for RF-1, RF-2, RF-3 or RF-4, and it does not
discharge any release or publication gate in this repository.

## Exact Obstruction

For

```text
eta_N(u + i t) = sum_{k=1}^N (-1)^(k-1) / k^(u+i t),
```

the cross term considered in the source satisfies

```text
F_N(u,t) = 1/2 * ( |eta_N(u+i t)|^2 - sum_{k=1}^N k^(-2u) ).
```

Since `eta_N(u+i t)` converges for every `u > 0`, the harmonic square-sum term
at `u = 1/2` forces

```text
F_N(1/2,t) -> -infinity
```

for every fixed `t`. If `eta(sigma' + i t) = 0` with `sigma' > 1/2`, then

```text
F_N(sigma',t) -> -zeta(2 sigma') / 2,
```

and consequently

```text
F_N(sigma',t) - F_N(1/2,t) -> +infinity.
```

Thus the continuity estimate used in the manuscript,

```text
|F_N(sigma') - F_N(1/2)| < epsilon,
```

is not merely unjustified as a uniform statement; it is false for all
sufficiently large cutoffs in the setting above.

## Quantifier Error

The invalid step treats a cutoff-dependent modulus

```text
forall N, forall epsilon, exists delta_{N,epsilon}
```

as though it supplied a single `delta` valid while `N` varies. In addition,
`sigma' = 1 - sigma` is fixed by the assumed zero and cannot be chosen after the
fact to satisfy a cutoff-dependent proximity condition.

Secondary issues such as the passage from `t_j` to `t`, omitted trigonometric
subcases and strict positivity versus nonnegativity of squared norms are
repairable. The missing uniformity is not.

## Repository Consequence

The useful lesson is negative and methodological: finite-cutoff continuity must
not be promoted to a limiting argument unless the modulus is proved independent
of the cutoff. The follow-up module
`OnePointResolvent.StieltjesLocalBound` now proves the concrete finite-disk
estimate

```text
|S_j(z)| <= 2 S_j(x_0),    |z - x_0| <= x_0 / 2,
```

with the support, weights and spectrum varying with `j`. Thus the constant is
independent of atom count and cutoff. This is the first positive repair of the
audit obstruction, but it is deliberately narrower than the full
normal-family input.

The remaining theorem must replace the fixed disk by every compact subset of
the slit plane and then combine that domination with convergence and Montel
compactness. No finite-to-limit conclusion is claimed here.

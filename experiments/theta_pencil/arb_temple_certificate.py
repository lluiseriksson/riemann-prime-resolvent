"""Source-level Arb certificate for the localized Kato--Temple test."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import (
    ArbPrimeAction,
    _arb_radius_as_float,
    build_arb_active_prime_action,
)
from experiments.theta_pencil.arb_smooth_kernel import build_arb_smooth_matrix
from experiments.theta_pencil.arb_trial_variation import (
    certify_active_prime_remainder_variation,
)
from experiments.theta_pencil.temple_trial_budget import run_temple_trial_audit


@dataclass(frozen=True)
class ArbTempleCertificate:
    half_width: float
    trial_parity: int
    dimension: int
    residual_end: int
    rayleigh_lower: float
    rayleigh_upper: float
    low_residual_upper: float
    finite_high_residual_upper: float
    finite_residual_upper: float
    jump_tail_upper: float
    prime_remainder_tail_upper: float
    potential_tail_upper: float
    smooth_tail_upper: float
    series_remainder: float
    total_residual_upper: float
    second_floor: float
    temple_lower: float
    variation_upper: float
    endpoint_constraints: int
    prime_jet_count: int
    prime_precision: int
    precision: int


def _ball_from_export(arb, midpoint: float, radius: float):
    pad = math.ulp(midpoint) if midpoint != 0.0 else math.ulp(0.0)
    return arb(midpoint, radius + pad)


def _float_upper(value) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def _float_lower(value) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def _trial_build_residual_end(dimension: int, residual_end: int) -> int:
    """Small auxiliary cutoff sufficient to construct the finite trial."""

    return min(residual_end, max(8192, dimension + 1))


def _minimum_prime_precision(dimension: int, residual_end: int) -> int:
    """Conservative preflight precision for the endpoint-jet cancellation.

    The stable integration-by-parts recurrence removes growth with the target
    cutoff.  The remaining cancellation recombines endpoint derivatives of a
    degree-``dimension`` trial and is governed by the source dimension.  This
    guard is not used as an error estimate (the returned balls provide that);
    it keeps an under-resolved computation from spending a long time only to
    export an infinite radius.  ``residual_end`` remains in the signature so
    callers need not maintain a second preflight interface.
    """

    del residual_end
    return 2 * dimension * math.ceil(math.log2(dimension)) + 1024


def certify_temple_trial(
    half_width: float = 0.4,
    trial_parity: int = 0,
    dimension: int = 256,
    residual_end: int = 8192,
    second_floor: float = 0.005,
    variation_partitions: int = 32,
    precision: int = 1024,
    prime_precision: int = 10240,
    prime_action: ArbPrimeAction | None = None,
    active_primes: tuple[int, ...] = (2,),
    endpoint_constraints: int = 0,
    prime_jet_count: int = 1,
) -> ArbTempleCertificate:
    """Certify positivity of the lowest point assuming the supplied gap floor."""
    if trial_parity not in (0, 1):
        raise ValueError("trial_parity must be zero or one")
    if not active_primes:
        raise ValueError("at least one active prime is required")
    if any(math.log(float(prime)) >= 2 * half_width for prime in active_primes):
        raise ValueError("every active prime must have positive translation overlap")
    if prime_jet_count < 1 or prime_jet_count >= dimension:
        raise ValueError("prime_jet_count must lie below dimension")
    if dimension < 4 or residual_end <= dimension:
        raise ValueError("require 4 <= dimension < residual_end")
    minimum_prime_precision = _minimum_prime_precision(dimension, residual_end)
    if prime_precision < minimum_prime_precision:
        raise ValueError(
            "prime_precision is too small for the endpoint-jet preflight: "
            f"need at least {minimum_prime_precision} bits"
        )
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    # The finite trial vector depends only on ``dimension``.  Asking the
    # floating audit to follow a very long certified tail would construct a
    # dense Gauss rule of order O(residual_end), even though only its
    # coefficients are used below.  Cap this auxiliary build; all residual
    # coefficients through ``residual_end`` are subsequently recomputed in
    # Arb by the linear-memory recurrence.
    trial_build_end = _trial_build_residual_end(dimension, residual_end)
    floating = run_temple_trial_audit(
        half_width=half_width,
        trial_dimension=dimension,
        residual_end=trial_build_end,
        second_floor=second_floor,
        trial_parity=trial_parity,
        endpoint_constraints=endpoint_constraints,
        prime_jet_count=prime_jet_count,
    )
    coefficients = floating.coefficients.copy()
    coefficients[1 - trial_parity :: 2] = 0.0
    if prime_action is None:
        prime = build_arb_active_prime_action(
            half_width,
            coefficients,
            residual_end,
            active_primes,
            prime_precision,
        )
    else:
        prime = prime_action
        if len(prime.midpoint) != residual_end or len(prime.radius) != residual_end:
            raise ValueError("the cached prime action has the wrong degree cutoff")
        if prime.precision != prime_precision:
            raise ValueError("the cached prime action has the wrong precision")
        if not np.all(np.isfinite(prime.midpoint)) or not np.all(
            np.isfinite(prime.radius)
        ):
            raise ValueError("the cached prime action is not finite")
    smooth_power = 23
    # The kernel |x-y|^p maps an input polynomial of degree < dimension to
    # a polynomial of degree at most dimension+p.  Hence the truncated smooth
    # series has a finite action; only its analytic remainder has an infinite
    # Legendre tail.
    smooth_extent = min(residual_end, dimension + smooth_power + 2)
    smooth = build_arb_smooth_matrix(
        half_width, smooth_extent, smooth_extent, smooth_power, precision
    )
    variation = certify_active_prime_remainder_variation(
        half_width,
        coefficients,
        active_primes,
        variation_partitions,
        precision,
        prime_jet_count,
    )

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = arb(str(half_width))
        vector = [arb(float(value)) for value in coefficients]
        norm_squared = sum((value * value for value in vector), arb(0))
        scalar = -a.log() - (arb(2) * arb.pi()).log() - arb.const_euler()

        harmonic = [arb(0)]
        diagonal = [arb(1)]
        for degree in range(1, dimension):
            harmonic.append(harmonic[-1] + arb(1) / degree)
            diagonal.append(
                diagonal[-1]
                + arb(1) / (degree * (2 * degree - 1) * (2 * degree + 1))
            )

        def boundary(left: int, right: int):
            if (left + right) % 2:
                return arb(0)
            if left == right:
                return diagonal[left] - arb.const_log2()
            return arb((2 * left + 1) * (2 * right + 1)).sqrt() / (
                abs(left - right) * (left + right + 1)
            )

        smooth_action = [arb(0) for _ in range(smooth_extent)]
        for left in range(trial_parity, smooth_extent, 2):
            smooth_action[left] = sum(
                (
                    _ball_from_export(
                        arb,
                        smooth.midpoint[left, right],
                        smooth.radius[left, right],
                    )
                    * vector[right]
                    for right in range(trial_parity, dimension, 2)
                ),
                arb(0),
            )

        low_action = [arb(0) for _ in range(dimension)]
        for left in range(trial_parity, dimension, 2):
            value = (harmonic[left] + scalar) * vector[left]
            value += _ball_from_export(arb, prime.midpoint[left], prime.radius[left])
            for right in range(trial_parity, dimension, 2):
                value += boundary(left, right) * vector[right]
            value += smooth_action[left]
            low_action[left] = value

        energy = sum(
            (vector[index] * low_action[index] for index in range(dimension)),
            arb(0),
        )
        rayleigh_truncated = energy / norm_squared
        series_tail = arb(str(smooth.analytic_remainder))
        rayleigh_lower = _float_lower(rayleigh_truncated - series_tail)
        rayleigh_upper = _float_upper(rayleigh_truncated + series_tail)

        low_residual_square = arb(0)
        for degree in range(dimension):
            residual = low_action[degree] - rayleigh_truncated * vector[degree]
            low_residual_square += residual.abs_upper() ** 2

        weighted = [
            vector[degree] * arb(2 * degree + 1).sqrt()
            for degree in range(dimension)
        ]
        eigenvalues = [arb(degree * (degree + 1)) for degree in range(dimension)]
        high_residual_square = arb(0)
        first_high = dimension + ((dimension - trial_parity) % 2)
        for high in range(first_high, residual_end, 2):
            potential = arb(2 * high + 1).sqrt() * sum(
                (
                    weighted[low]
                    / (arb(high * (high + 1)) - eigenvalues[low])
                    for low in range(trial_parity, dimension, 2)
                ),
                arb(0),
            )
            prime_value = _ball_from_export(
                arb, prime.midpoint[high], prime.radius[high]
            )
            smooth_value = smooth_action[high] if high < smooth_extent else arb(0)
            high_value = prime_value + potential + smooth_value
            high_residual_square += high_value.abs_upper() ** 2
        residual_square = low_residual_square + high_residual_square
        finite_residual = residual_square.sqrt() / norm_squared.sqrt()
        finite_residual_upper = _float_upper(finite_residual)

        endpoint_jets = []
        for jet in range(prime_jet_count):
            endpoint_jet = arb(0)
            for degree in range(trial_parity, dimension, 2):
                if degree < jet:
                    continue
                derivative = arb(1)
                for factor in range(degree - jet + 1, degree + jet + 1):
                    derivative *= factor
                derivative /= arb(2) ** jet * math.factorial(jet) ** 2
                endpoint_jet += (
                    vector[degree]
                    * (arb(2 * degree + 1) / 2).sqrt()
                    * derivative
                )
            endpoint_jets.append(endpoint_jet)
        jump_constant = (arb(8) / (3 * arb.pi())).sqrt()
        jump_tail = arb(0)
        for active_prime in active_primes:
            prime_ball = arb(active_prime)
            cut = arb(1) - prime_ball.log() / a
            cut_weight = (arb(1) - cut * cut).sqrt().sqrt()
            value_jump = (
                arb(2)
                * prime_ball.log()
                / prime_ball.sqrt()
                * abs(endpoint_jets[0])
            )
            jump_tail += jump_constant * value_jump / (
                cut_weight * arb(residual_end - 1).sqrt()
            )
            for jet in range(1, prime_jet_count):
                scalar_tail = (
                    arb(2) ** (jet + 1)
                    * math.factorial(jet)
                    / (
                        arb.pi().sqrt()
                        * arb(2 * jet + 1).sqrt()
                        * arb(residual_end - 1) ** (jet + arb("0.5"))
                        * cut_weight
                    )
                )
                jump_tail += (
                    arb(2)
                    * prime_ball.log()
                    / prime_ball.sqrt()
                    * abs(endpoint_jets[jet])
                    * scalar_tail
                )

        variation_ball = arb(str(variation.upper))
        prime_remainder_tail = (
            arb(2) ** (prime_jet_count + 1)
            * variation_ball
            / (
                (arb((2 * prime_jet_count + 1)) * arb.pi()).sqrt()
                * arb(residual_end - 1)
                ** (prime_jet_count + arb("0.5"))
            )
        )

        potential_tail = arb(0)
        for order in range(2):
            moment = abs(
                sum(
                    (
                        weighted[degree] * eigenvalues[degree] ** order
                        for degree in range(trial_parity, dimension, 2)
                    ),
                    arb(0),
                )
            )
            potential_tail += (
                arb(3).sqrt()
                * moment
                / arb(4 * order + 2).sqrt()
                * arb(residual_end - 1) ** (-(2 * order + 1))
            )
        absolute_moment = sum(
            (
                abs(weighted[degree]) * eigenvalues[degree] ** 2
                for degree in range(trial_parity, dimension, 2)
            ),
            arb(0),
        )
        last_active = dimension - 1 - ((dimension - 1 - trial_parity) % 2)
        largest = eigenvalues[last_active]
        ratio = largest / (residual_end * residual_end)
        potential_tail += (
            arb(3).sqrt()
            * absolute_moment
            / (1 - ratio)
            / arb(10).sqrt()
            * arb(residual_end - 1) ** (-5)
        )

        smooth_tail = arb(0)

        # Two copies of the smooth power-series error cover both the operator
        # action and the shift from the truncated to the exact Rayleigh value.
        prime_potential_tail_upper = math.nextafter(
            _float_upper(jump_tail)
            + _float_upper(prime_remainder_tail)
            + _float_upper(potential_tail),
            math.inf,
        )
        low_residual_upper = _float_upper(
            low_residual_square.sqrt() / norm_squared.sqrt()
        )
        finite_high_upper = _float_upper(
            high_residual_square.sqrt() / norm_squared.sqrt()
        )
        prime_potential_high_upper = math.nextafter(
            math.hypot(finite_high_upper, prime_potential_tail_upper), math.inf
        )
        total_upper = math.nextafter(
            math.hypot(
                low_residual_upper,
                math.nextafter(
                    prime_potential_high_upper + _float_upper(smooth_tail),
                    math.inf,
                ),
            )
            + 2.0 * math.nextafter(smooth.analytic_remainder, math.inf),
            math.inf,
        )
        if rayleigh_upper >= second_floor:
            raise ArithmeticError("the Rayleigh interval reaches the gap floor")
        endpoint_lowers = (
            rayleigh_lower
            - total_upper**2 / (second_floor - rayleigh_lower),
            rayleigh_upper
            - total_upper**2 / (second_floor - rayleigh_upper),
        )
        temple_lower = min(endpoint_lowers)
    finally:
        ctx.prec = previous_precision

    return ArbTempleCertificate(
        half_width=half_width,
        trial_parity=trial_parity,
        dimension=dimension,
        residual_end=residual_end,
        rayleigh_lower=rayleigh_lower,
        rayleigh_upper=rayleigh_upper,
        low_residual_upper=low_residual_upper,
        finite_high_residual_upper=finite_high_upper,
        finite_residual_upper=finite_residual_upper,
        jump_tail_upper=_float_upper(jump_tail),
        prime_remainder_tail_upper=_float_upper(prime_remainder_tail),
        potential_tail_upper=_float_upper(potential_tail),
        smooth_tail_upper=_float_upper(smooth_tail),
        series_remainder=smooth.analytic_remainder,
        total_residual_upper=total_upper,
        second_floor=second_floor,
        temple_lower=temple_lower,
        variation_upper=variation.upper,
        endpoint_constraints=endpoint_constraints,
        prime_jet_count=prime_jet_count,
        prime_precision=prime_precision,
        precision=precision,
    )

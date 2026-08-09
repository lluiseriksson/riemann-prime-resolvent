"""Source-level Arb certificate for the localized Kato--Temple test."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import (
    _arb_radius_as_float,
    build_arb_prime_two_action,
)
from experiments.theta_pencil.arb_smooth_kernel import build_arb_smooth_matrix
from experiments.theta_pencil.arb_trial_variation import (
    certify_prime_remainder_variation,
)
from experiments.theta_pencil.temple_trial_budget import run_temple_trial_audit


@dataclass(frozen=True)
class ArbTempleCertificate:
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
    prime_precision: int
    precision: int


def _ball_from_export(arb, midpoint: float, radius: float):
    pad = math.ulp(midpoint) if midpoint != 0.0 else math.ulp(0.0)
    return arb(midpoint, radius + pad)


def _float_upper(value) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def _float_lower(value) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def certify_temple_trial(
    dimension: int = 256,
    residual_end: int = 8192,
    second_floor: float = 0.005,
    variation_partitions: int = 32,
    precision: int = 1024,
    prime_precision: int = 10240,
) -> ArbTempleCertificate:
    """Certify positivity of the lowest point assuming the supplied gap floor."""
    if dimension < 4 or residual_end <= dimension:
        raise ValueError("require 4 <= dimension < residual_end")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    floating = run_temple_trial_audit(
        trial_dimension=dimension,
        residual_end=residual_end,
        second_floor=second_floor,
    )
    coefficients = floating.coefficients.copy()
    coefficients[1::2] = 0.0
    prime = build_arb_prime_two_action(
        0.4, coefficients, residual_end, prime_precision
    )
    smooth = build_arb_smooth_matrix(0.4, dimension, dimension, 23, precision)
    variation = certify_prime_remainder_variation(
        0.4, coefficients, variation_partitions, precision
    )

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = arb(2) / 5
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

        low_action = [arb(0) for _ in range(dimension)]
        for left in range(0, dimension, 2):
            value = (harmonic[left] + scalar) * vector[left]
            value += _ball_from_export(arb, prime.midpoint[left], prime.radius[left])
            for right in range(0, dimension, 2):
                value += boundary(left, right) * vector[right]
                smooth_entry = _ball_from_export(
                    arb, smooth.midpoint[left, right], smooth.radius[left, right]
                )
                value += smooth_entry * vector[right]
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
            low_residual_square += residual * residual

        weighted = [
            vector[degree] * arb(2 * degree + 1).sqrt()
            for degree in range(dimension)
        ]
        eigenvalues = [arb(degree * (degree + 1)) for degree in range(dimension)]
        high_residual_square = arb(0)
        for high in range(dimension + dimension % 2, residual_end, 2):
            potential = arb(2 * high + 1).sqrt() * sum(
                (
                    weighted[low]
                    / (arb(high * (high + 1)) - eigenvalues[low])
                    for low in range(0, dimension, 2)
                ),
                arb(0),
            )
            prime_value = _ball_from_export(
                arb, prime.midpoint[high], prime.radius[high]
            )
            high_residual_square += (prime_value + potential) ** 2
        residual_square = low_residual_square + high_residual_square
        finite_residual = residual_square.sqrt() / norm_squared.sqrt()
        finite_residual_upper = _float_upper(finite_residual)

        endpoint = sum(
            (
                vector[degree] * (arb(2 * degree + 1) / 2).sqrt()
                for degree in range(0, dimension, 2)
            ),
            arb(0),
        )
        cut = arb(1) - arb.const_log2() / a
        cut_weight = (arb(1) - cut * cut).sqrt().sqrt()
        jump_total = arb(2) * arb.const_log2() / arb(2).sqrt() * abs(endpoint)
        jump_constant = (arb(8) / (3 * arb.pi())).sqrt()
        jump_tail = jump_constant * jump_total / (
            cut_weight * arb(residual_end - 1).sqrt()
        )

        variation_ball = arb(str(variation.upper))
        prime_remainder_tail = (
            arb(4)
            * variation_ball
            / (
                (arb(3) * arb.pi()).sqrt()
                * arb(residual_end - 1) ** arb("1.5")
            )
        )

        potential_tail = arb(0)
        for order in range(2):
            moment = abs(
                sum(
                    (
                        weighted[degree] * eigenvalues[degree] ** order
                        for degree in range(0, dimension, 2)
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
                for degree in range(0, dimension, 2)
            ),
            arb(0),
        )
        largest = eigenvalues[dimension - 2]
        ratio = largest / (residual_end * residual_end)
        potential_tail += (
            arb(3).sqrt()
            * absolute_moment
            / (1 - ratio)
            / arb(10).sqrt()
            * arb(residual_end - 1) ** (-5)
        )

        weighted_l1 = arb.pi().sqrt() * arb("0.75").gamma() / arb("1.25").gamma()
        smooth_variation = (
            a * a * arb.pi().sqrt() / 24
            + a**3 * arb(2).sqrt() * weighted_l1
        )
        smooth_tail = (
            arb(4)
            * smooth_variation
            / ((arb(3) * arb.pi()).sqrt() * arb(dimension - 1) ** arb("1.5"))
        )

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
        prime_precision=prime_precision,
        precision=precision,
    )

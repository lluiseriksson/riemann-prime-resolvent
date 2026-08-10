"""Rigorous piecewise variation bound for a fixed Legendre trial vector."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.prime_power_arithmetic import prime_power_base

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.support_window import (
    in_first_prime_window,
    prime_overlap_positive,
)


@dataclass(frozen=True)
class ArbVariationBound:
    midpoint: float
    radius: float
    upper: float
    partitions: int
    precision: int


def certify_prime_operator_remainder_variation_for_prime(
    half_width: float,
    prime: int,
    low_degrees: np.ndarray,
    derivative_order: int = 6,
    partitions: int = 128,
    precision: int = 768,
) -> ArbVariationBound:
    """Vector-valued version used by the parity Schur tail certificate."""
    degrees = np.asarray(low_degrees, dtype=int)
    if prime < 2:
        raise ValueError("prime must be at least two")
    if not prime_overlap_positive(half_width, prime):
        raise ValueError("the prime translation must have positive overlap")
    if len(degrees) < 1 or derivative_order < 1 or partitions < 1:
        raise ValueError("invalid degrees, derivative order, or partition count")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        derivative_rows = []
        endpoint_square = arb(0)
        for degree_value in degrees:
            degree = int(degree_value)
            row = [arb(0) for _ in range(degree + 1)]
            row[degree] = (arb(2 * degree + 1) / 2).sqrt()
            for _ in range(derivative_order + 1):
                row = _differentiate_standard_legendre(row, arb)
            derivative_rows.append(row)

            if degree >= derivative_order:
                endpoint = (arb(2 * degree + 1) / 2).sqrt()
                for factor in range(degree - derivative_order + 1, degree + derivative_order + 1):
                    endpoint *= factor
                endpoint /= arb(2) ** derivative_order * math.factorial(derivative_order)
                endpoint_square += endpoint * endpoint

        maximum_derivative_degree = max(len(row) - 1 for row in derivative_rows)
        order = maximum_derivative_degree + 1
        nodes_weights = [arb.legendre_p_root(order, k, weight=True) for k in range(order)]
        a = arb(str(half_width))
        prime_ball = arb(prime)
        translation = prime_ball.log() / a
        cut = arb(1) - translation
        length = cut + 1
        total = arb(0)
        for part in range(partitions):
            left = -arb(1) + length * part / partitions
            right = -arb(1) + length * (part + 1) / partitions
            midpoint = (right + left) / 2
            scale = (right - left) / 2
            square_integral = arb(0)
            for node, weight in nodes_weights:
                source = midpoint + scale * node + translation
                squared_norm = arb(0)
                for row in derivative_rows:
                    value = _legendre_series_value(row, source, arb)
                    squared_norm += value * value
                square_integral += scale * weight * squared_norm
            arcsine_mass = right.asin() - left.asin()
            total += (arcsine_mass * square_integral).sqrt()

        cut_weight = (arb(1) - cut * cut).sqrt().sqrt()
        prime_factor = (
            arb(2) * arb(prime_power_base(prime)).log() / prime_ball.sqrt()
        )
        bound = prime_factor * (total + endpoint_square.sqrt() / cut_weight)
        midpoint = float(bound.mid())
        radius = _arb_radius_as_float(bound)
        upper = math.nextafter(float(bound.upper()), math.inf)
    finally:
        ctx.prec = previous_precision
    return ArbVariationBound(
        midpoint=midpoint,
        radius=radius,
        upper=upper,
        partitions=partitions,
        precision=precision,
    )


def certify_prime_operator_remainder_variation(
    half_width: float,
    low_degrees: np.ndarray,
    derivative_order: int = 6,
    partitions: int = 128,
    precision: int = 768,
) -> ArbVariationBound:
    """Backward-compatible vector-valued prime-two certificate."""

    if not in_first_prime_window(half_width):
        raise ValueError(
            "the exact Arb implementation requires log(2)/2 < a <= log(3)/2"
        )
    return certify_prime_operator_remainder_variation_for_prime(
        half_width,
        2,
        low_degrees,
        derivative_order,
        partitions,
        precision,
    )


def certify_active_prime_operator_remainder_variation(
    half_width: float,
    low_degrees: np.ndarray,
    active_primes: tuple[int, ...],
    derivative_order: int = 6,
    partitions: int = 128,
    precision: int = 768,
) -> ArbVariationBound:
    """Sum vector-valued remainder bounds over all active prime cuts."""

    if not active_primes:
        raise ValueError("at least one active prime is required")
    bounds = [
        certify_prime_operator_remainder_variation_for_prime(
            half_width,
            prime,
            low_degrees,
            derivative_order,
            partitions,
            precision,
        )
        for prime in active_primes
    ]
    midpoint = math.fsum(bound.midpoint for bound in bounds)
    radius = math.fsum(bound.radius for bound in bounds) + math.ulp(midpoint)
    upper = math.nextafter(math.fsum(bound.upper for bound in bounds), math.inf)
    return ArbVariationBound(
        midpoint=midpoint,
        radius=radius,
        upper=upper,
        partitions=partitions,
        precision=precision,
    )


def _differentiate_standard_legendre(coefficients, arb):
    """Differentiate coefficients in the unnormalized P_n basis."""
    if len(coefficients) <= 1:
        return [arb(0)]
    result = [arb(0) for _ in range(len(coefficients) - 1)]
    for output in range(len(result)):
        factor = 2 * output + 1
        for source in range(output + 1, len(coefficients), 2):
            result[output] += factor * coefficients[source]
    return result


def _legendre_series_value(coefficients, point, arb):
    if not coefficients:
        return arb(0)
    previous = arb(1)
    value = coefficients[0] * previous
    if len(coefficients) == 1:
        return value
    current = point
    value += coefficients[1] * current
    for degree in range(1, len(coefficients) - 1):
        following = (
            arb(2 * degree + 1) * point * current - degree * previous
        ) / (degree + 1)
        value += coefficients[degree + 1] * following
        previous, current = current, following
    return value


def certify_prime_remainder_variation_for_prime(
    half_width: float,
    prime: int,
    coefficients: np.ndarray,
    partitions: int = 32,
    precision: int = 1024,
    derivative_order: int = 1,
) -> ArbVariationBound:
    """Upper-bound the weighted variation after removing both jump steps.

    On each subinterval Cauchy--Schwarz uses the exact arcsine mass and an
    Arb Gauss--Legendre evaluation of the polynomial ``phi''**2``.  The rule
    order integrates that polynomial exactly.
    """
    vector = np.asarray(coefficients, dtype=float)
    if prime < 2:
        raise ValueError("prime must be at least two")
    if not prime_overlap_positive(half_width, prime):
        raise ValueError("the prime translation must have positive overlap")
    if derivative_order < 1 or len(vector) <= derivative_order + 1:
        raise ValueError("the derivative order must fit the trial polynomial")
    if partitions < 1:
        raise ValueError("need at least one partition")
    if np.any(vector[::2] != 0.0) and np.any(vector[1::2] != 0.0):
        raise ValueError("the registered trial variation requires one parity")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        standard = [
            arb(float(value)) * (arb(2 * degree + 1) / 2).sqrt()
            for degree, value in enumerate(vector)
        ]
        retained_derivative = standard
        for _ in range(derivative_order):
            retained_derivative = _differentiate_standard_legendre(
                retained_derivative, arb
            )
        remainder_derivative = _differentiate_standard_legendre(
            retained_derivative, arb
        )
        order = len(vector) - derivative_order - 1
        nodes_weights = [arb.legendre_p_root(order, k, weight=True) for k in range(order)]

        a = arb(str(half_width))
        prime_ball = arb(prime)
        translation = prime_ball.log() / a
        cut = arb(1) - translation
        length = cut + 1
        total = arb(0)
        for part in range(partitions):
            left = -arb(1) + length * part / partitions
            right = -arb(1) + length * (part + 1) / partitions
            midpoint = (right + left) / 2
            scale = (right - left) / 2
            square_integral = arb(0)
            for node, weight in nodes_weights:
                source = midpoint + scale * node + translation
                value = _legendre_series_value(
                    remainder_derivative, source, arb
                )
                square_integral += scale * weight * value * value
            arcsine_mass = right.asin() - left.asin()
            total += (arcsine_mass * square_integral).sqrt()

        endpoint_derivative = _legendre_series_value(
            retained_derivative, arb(1), arb
        )
        cut_weight = (arb(1) - cut * cut).sqrt().sqrt()
        prime_factor = arb(2) * prime_ball.log() / prime_ball.sqrt()
        bound = prime_factor * (total + abs(endpoint_derivative) / cut_weight)
        midpoint = float(bound.mid())
        radius = _arb_radius_as_float(bound)
        upper = math.nextafter(float(bound.upper()), math.inf)
    finally:
        ctx.prec = previous_precision
    return ArbVariationBound(
        midpoint=midpoint,
        radius=radius,
        upper=upper,
        partitions=partitions,
        precision=precision,
    )


def certify_prime_remainder_variation(
    half_width: float,
    coefficients: np.ndarray,
    partitions: int = 32,
    precision: int = 1024,
) -> ArbVariationBound:
    """Backward-compatible prime-two variation certificate."""

    if not in_first_prime_window(half_width):
        raise ValueError(
            "the exact Arb implementation requires log(2)/2 < a <= log(3)/2"
        )
    return certify_prime_remainder_variation_for_prime(
        half_width, 2, coefficients, partitions, precision, 1
    )


def certify_active_prime_remainder_variation(
    half_width: float,
    coefficients: np.ndarray,
    primes: tuple[int, ...],
    partitions: int = 32,
    precision: int = 1024,
    derivative_order: int = 1,
) -> ArbVariationBound:
    """Add the certified variation bounds for all active prime jumps."""

    if not primes:
        raise ValueError("at least one active prime is required")
    bounds = [
        certify_prime_remainder_variation_for_prime(
            half_width,
            prime,
            coefficients,
            partitions,
            precision,
            derivative_order,
        )
        for prime in primes
    ]
    midpoint = math.fsum(bound.midpoint for bound in bounds)
    radius = math.fsum(bound.radius for bound in bounds) + math.ulp(midpoint)
    upper = math.nextafter(math.fsum(bound.upper for bound in bounds), math.inf)
    return ArbVariationBound(
        midpoint=midpoint,
        radius=radius,
        upper=upper,
        partitions=partitions,
        precision=precision,
    )

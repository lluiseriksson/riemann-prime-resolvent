"""Arb enclosure of the prime-2 Legendre matrix without quadrature.

The translated low polynomial is expanded exactly at the two overlap cuts.
Large endpoint-jet terms cancel, so production dimensions deliberately use
thousands of bits; Arb retains a certified enclosure through that cancellation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.prime_power_arithmetic import prime_power_base
from experiments.theta_pencil.support_window import (
    in_first_prime_window,
    prime_overlap_positive,
)


@dataclass(frozen=True)
class ArbPrimeMatrix:
    midpoint: np.ndarray
    radius: np.ndarray
    precision: int


@dataclass(frozen=True)
class ArbPrimeAction:
    midpoint: np.ndarray
    radius: np.ndarray
    precision: int


def _arb_radius_as_float(value) -> float:
    """Work around a high-precision python-flint radius conversion edge case."""
    rendered = value.rad().str(20)
    if rendered == "0":
        return 0.0
    midpoint = rendered.lstrip("[").split()[0]
    return float(midpoint)


def _restarted_arb_legendre_values(cut, count: int, arb, stride: int = 4096):
    """Enclose ``P_n(cut)`` without long interval-dependency growth.

    A single three-term interval recurrence eventually widens even though the
    underlying Legendre values remain bounded.  Direct Arb seeds at each block
    make every subsequent recurrence short while preserving exact enclosure.
    """

    if count < 1 or stride < 2:
        raise ValueError("require a positive count and restart stride at least two")
    values = [arb(0) for _ in range(count)]
    for start in range(0, count, stride):
        stop = min(count, start + stride)
        values[start] = cut.legendre_p(start)
        if start + 1 >= stop:
            continue
        values[start + 1] = cut.legendre_p(start + 1)
        for degree in range(start + 1, stop - 1):
            values[degree + 1] = (
                (2 * degree + 1) * cut * values[degree]
                - degree * values[degree - 1]
            ) / (degree + 1)
    return values


def build_arb_prime_matrix(
    half_width: float,
    prime: int,
    low_dimension: int,
    maximum_degree: int,
    precision: int = 8192,
) -> ArbPrimeMatrix:
    """Enclose rows ``m < low_dimension`` and columns ``n < maximum_degree``."""
    if prime < 2:
        raise ValueError("prime must be at least two")
    if not prime_overlap_positive(half_width, prime):
        raise ValueError("the prime translation must have positive overlap")
    if not 1 <= low_dimension <= maximum_degree:
        raise ValueError("require 1 <= low_dimension <= maximum_degree")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        two = arb(2)
        prime_ball = arb(prime)
        a = arb(str(half_width))
        cut = 1 - prime_ball.log() / a
        jet_count = low_dimension
        padded = maximum_degree + jet_count

        legendre = _restarted_arb_legendre_values(cut, padded + 2, arb)

        normalizations = [
            (arb(2 * degree + 1) / 2).sqrt()
            for degree in range(padded + 1)
        ]
        rows: list[list] = []
        step = [arb(0)] * padded
        step[0] = (cut + 1) / two.sqrt()
        for degree in range(1, padded):
            step[degree] = (
                normalizations[degree]
                * (legendre[degree + 1] - legendre[degree - 1])
                / (2 * degree + 1)
            )
        rows.append(step)
        for jet in range(1, jet_count):
            previous = rows[-1]
            following = [arb(0) for _ in previous]
            following[0] = -(-arb(1) - cut) ** (jet + 1) / (
                (jet + 1) * two.sqrt()
            )
            # Integration by parts using
            # (2n+1)P_n = P'_{n+1}-P'_{n-1}.  Unlike repeated application
            # of X-cut, this computes the small high-mode truncated-power
            # coefficients directly and does not destroy bits by cancellation.
            for degree in range(1, padded - 1):
                following[degree] = (
                    -arb(jet)
                    * normalizations[degree]
                    / (2 * degree + 1)
                    * (
                        previous[degree + 1] / normalizations[degree + 1]
                        - previous[degree - 1] / normalizations[degree - 1]
                    )
                )
            rows.append(following)

        endpoint = []
        for degree in range(low_dimension):
            normalization = (arb(2 * degree + 1) / 2).sqrt()
            endpoint_row = []
            for jet in range(jet_count):
                if degree < jet:
                    endpoint_row.append(arb(0))
                    continue
                derivative = arb(1)
                for factor in range(degree - jet + 1, degree + jet + 1):
                    derivative *= factor
                derivative /= 2**jet * math.factorial(jet) ** 2
                endpoint_row.append(normalization * derivative)
            endpoint.append(endpoint_row)

        product = arb_mat(endpoint) * arb_mat(
            [row[:maximum_degree] for row in rows]
        )
        mangoldt = arb(prime_power_base(prime)).log()
        coefficient = -2 * mangoldt / prime_ball.sqrt()
        midpoint = np.empty((low_dimension, maximum_degree), dtype=float)
        radius = np.empty_like(midpoint)
        for left in range(low_dimension):
            for right in range(maximum_degree):
                if (left + right) % 2:
                    midpoint[left, right] = 0.0
                    radius[left, right] = 0.0
                    continue
                value = coefficient * product[left, right]
                midpoint[left, right] = float(value.mid())
                radius[left, right] = _arb_radius_as_float(value)
    finally:
        ctx.prec = previous_precision
    return ArbPrimeMatrix(midpoint=midpoint, radius=radius, precision=precision)


def build_arb_prime_two_matrix(
    half_width: float,
    low_dimension: int,
    maximum_degree: int,
    precision: int = 8192,
) -> ArbPrimeMatrix:
    """Backward-compatible matrix wrapper for the first prime window."""

    if not in_first_prime_window(half_width):
        raise ValueError(
            "the prime-2-only formula requires log(2)/2 < a <= log(3)/2"
        )
    return build_arb_prime_matrix(
        half_width, 2, low_dimension, maximum_degree, precision
    )


def build_arb_prime_action(
    half_width: float,
    prime: int,
    coefficients: np.ndarray,
    maximum_degree: int,
    precision: int = 8192,
) -> ArbPrimeAction:
    """Enclose one prime translation applied to a parity-pure trial vector.

    Collapsing the endpoint jets before generating the truncated powers keeps
    memory linear in ``maximum_degree``. Coefficients are interpreted as the
    exact dyadic rationals represented by their input floats.
    """
    vector = np.asarray(coefficients, dtype=float)
    dimension = len(vector)
    if prime < 2:
        raise ValueError("prime must be at least two")
    if not prime_overlap_positive(half_width, prime):
        raise ValueError("the prime translation must have positive overlap")
    if dimension < 1 or maximum_degree < dimension:
        raise ValueError("require a nonempty vector and maximum_degree >= dimension")
    even_active = np.any(vector[::2] != 0.0)
    odd_active = np.any(vector[1::2] != 0.0)
    if even_active and odd_active:
        raise ValueError("the trial vector must have one parity")
    parity = 1 if odd_active else 0
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        two = arb(2)
        prime_ball = arb(prime)
        a = arb(str(half_width))
        cut = 1 - prime_ball.log() / a
        padded = maximum_degree + dimension
        legendre = _restarted_arb_legendre_values(cut, padded + 2, arb)

        endpoint_action = []
        for jet in range(dimension):
            value = arb(0)
            first_degree = jet + ((jet - parity) % 2)
            for degree in range(first_degree, dimension, 2):
                derivative = arb(1)
                for factor in range(degree - jet + 1, degree + jet + 1):
                    derivative *= factor
                derivative /= 2**jet * math.factorial(jet) ** 2
                normalization = (arb(2 * degree + 1) / 2).sqrt()
                value += arb(float(vector[degree])) * normalization * derivative
            endpoint_action.append(value)

        normalizations = [
            (arb(2 * degree + 1) / 2).sqrt()
            for degree in range(padded + 1)
        ]
        row = [arb(0)] * padded
        row[0] = (cut + 1) / two.sqrt()
        for degree in range(1, padded):
            row[degree] = (
                normalizations[degree]
                * (legendre[degree + 1] - legendre[degree - 1])
                / (2 * degree + 1)
            )
        action = [endpoint_action[0] * value for value in row]
        for jet in range(1, dimension):
            previous = row
            row = [arb(0) for _ in previous]
            row[0] = -(-arb(1) - cut) ** (jet + 1) / (
                (jet + 1) * two.sqrt()
            )
            for degree in range(1, padded - 1):
                row[degree] = (
                    -arb(jet)
                    * normalizations[degree]
                    / (2 * degree + 1)
                    * (
                        previous[degree + 1] / normalizations[degree + 1]
                        - previous[degree - 1] / normalizations[degree - 1]
                    )
                )
            factor = endpoint_action[jet]
            for degree in range(maximum_degree):
                action[degree] += factor * row[degree]

        mangoldt = arb(prime_power_base(prime)).log()
        coefficient = -2 * mangoldt / prime_ball.sqrt()
        midpoint = np.zeros(maximum_degree, dtype=float)
        radius = np.zeros_like(midpoint)
        for degree in range(parity, maximum_degree, 2):
            value = coefficient * action[degree]
            exported_midpoint = float(value.mid())
            exported_radius = _arb_radius_as_float(value)
            if not math.isfinite(exported_midpoint) or not math.isfinite(
                exported_radius
            ):
                raise ArithmeticError(
                    "non-finite prime-action enclosure at degree "
                    f"{degree}; increase precision above {precision} bits"
                )
            midpoint[degree] = exported_midpoint
            radius[degree] = exported_radius
    finally:
        ctx.prec = previous_precision
    return ArbPrimeAction(midpoint=midpoint, radius=radius, precision=precision)


def build_arb_prime_two_action(
    half_width: float,
    coefficients: np.ndarray,
    maximum_degree: int,
    precision: int = 8192,
) -> ArbPrimeAction:
    """Backward-compatible wrapper for the prime-two action."""

    if not in_first_prime_window(half_width):
        raise ValueError(
            "the prime-2-only formula requires log(2)/2 < a <= log(3)/2"
        )
    return build_arb_prime_action(
        half_width, 2, coefficients, maximum_degree, precision
    )


def build_arb_active_prime_action(
    half_width: float,
    coefficients: np.ndarray,
    maximum_degree: int,
    primes: tuple[int, ...],
    precision: int = 8192,
) -> ArbPrimeAction:
    """Sum certified actions for the supplied active primes."""

    if not primes:
        raise ValueError("at least one active prime is required")
    actions = [
        build_arb_prime_action(
            half_width, prime, coefficients, maximum_degree, precision
        )
        for prime in primes
    ]
    midpoint = np.sum([action.midpoint for action in actions], axis=0)
    radius = np.sum([action.radius for action in actions], axis=0)
    # The floating additions incur one final rounding per component.
    radius += np.array(
        [
            math.ulp(float(value)) if value != 0.0 else math.ulp(0.0)
            for value in midpoint
        ]
    )
    return ArbPrimeAction(midpoint=midpoint, radius=radius, precision=precision)

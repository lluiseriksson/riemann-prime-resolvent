"""Audit constants in the dyadic degree-seven sampling proof."""

from __future__ import annotations

import math


VERIFIED_HEIGHT = 3.0e12
POLYNOMIAL_DEGREE = 14
SAMPLING_RADIUS = 1.0 / (24.0 * POLYNOMIAL_DEGREE**2)
SAMPLING_CONSTANT = 2.0e11


def zero_count_main(height: float) -> float:
    return height / (2.0 * math.pi) * math.log(
        height / (2.0 * math.pi * math.e)
    )


def zero_count_error(height: float) -> float:
    return (
        0.112 * math.log(height)
        + 0.278 * math.log(math.log(height))
        + 3.385
        + 0.2 / height
    )


def interval_zero_count_lower(left: float, right: float) -> float:
    return (
        zero_count_main(right)
        - zero_count_main(left)
        - zero_count_error(right)
        - zero_count_error(left)
    )


def zero_count_main_derivative(height: float) -> float:
    return math.log(height / (2.0 * math.pi)) / (2.0 * math.pi)


def zero_count_error_derivative(height: float) -> float:
    return (
        0.112 / height
        + 0.278 / (height * math.log(height))
        - 0.2 / (height * height)
    )


def scaled_interval_lower_derivative(left_scale: float, right_scale: float) -> float:
    """Derivative at the verified height of a proportionally scaled interval."""

    height = VERIFIED_HEIGHT
    return (
        right_scale * zero_count_main_derivative(right_scale * height)
        - left_scale * zero_count_main_derivative(left_scale * height)
        - right_scale * zero_count_error_derivative(right_scale * height)
        - left_scale * zero_count_error_derivative(left_scale * height)
    )


def audit() -> dict[str, float]:
    """Check the worst first-band count and the rounded Markov budget."""

    roots = [
        math.cos((2 * index + 1) * math.pi / (2 * 15))
        for index in range(15)
    ]
    centers = [1.5 + 0.5 * root for root in roots]
    counts = [
        interval_zero_count_lower(
            (center - SAMPLING_RADIUS) * VERIFIED_HEIGHT,
            (center + SAMPLING_RADIUS) * VERIFIED_HEIGHT,
        )
        for center in centers
    ]
    count_derivatives = [
        scaled_interval_lower_derivative(
            center - SAMPLING_RADIUS, center + SAMPLING_RADIUS
        )
        for center in centers
    ]
    assert min(counts) > 5.45e9
    assert min(count_derivatives) > 1.88e-3

    degree = POLYNOMIAL_DEGREE
    real_derivative_budget = (
        4.0 * degree**4 + 64.0 * degree**2 + 16.0**2 + 16.0
    )
    real_sampling_constant = 4.0 * 4.0**8 * real_derivative_budget
    assert real_sampling_constant < 4.37e10
    assert 4.0 * real_sampling_constant < SAMPLING_CONSTANT

    worst_band_fraction = (
        0.25
        * SAMPLING_CONSTANT
        * math.log(VERIFIED_HEIGHT)
        / VERIFIED_HEIGHT
    )
    assert worst_band_fraction < 0.479

    band_count_upper = (
        zero_count_main(2.0 * VERIFIED_HEIGHT)
        - zero_count_main(VERIFIED_HEIGHT)
        + zero_count_error(2.0 * VERIFIED_HEIGHT)
        + zero_count_error(VERIFIED_HEIGHT)
    )
    assert band_count_upper < VERIFIED_HEIGHT * math.log(VERIFIED_HEIGHT)
    return {
        "sampling_radius": SAMPLING_RADIUS,
        "minimum_first_band_zero_count": min(counts),
        "minimum_count_derivative": min(count_derivatives),
        "real_sampling_constant": real_sampling_constant,
        "rounded_strip_constant": SAMPLING_CONSTANT,
        "worst_band_fraction": worst_band_fraction,
        "first_band_count_ratio": band_count_upper
        / (VERIFIED_HEIGHT * math.log(VERIFIED_HEIGHT)),
    }


if __name__ == "__main__":
    print(audit())

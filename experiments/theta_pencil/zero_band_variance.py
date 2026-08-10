"""Audit the explicit constants in the local order-three variance proof.

This script is numerical bookkeeping for the displayed rational and
zero-counting inequalities.  It is not a substitute for the analytic proof.
"""

from __future__ import annotations

import math


def zero_count_main(height: float) -> float:
    """Riemann--von Mangoldt main term used by the explicit error bound."""

    return height / (2.0 * math.pi) * math.log(
        height / (2.0 * math.pi * math.e)
    )


def conservative_zero_count_error(height: float) -> float:
    """A deliberately enlarged explicit zero-counting error envelope."""

    return (
        0.112 * math.log(height)
        + 0.278 * math.log(math.log(height))
        + 3.385
        + 0.2 / height
    )


def band_count_lower(left: float, right: float, eta: float) -> float:
    """Lower bound for N(right*eta)-N(left*eta)."""

    return (
        zero_count_main(right * eta)
        - zero_count_main(left * eta)
        - conservative_zero_count_error(right * eta)
        - conservative_zero_count_error(left * eta)
    )


def scaled_main_derivative(scale: float, eta: float) -> float:
    """Derivative of the Riemann--von Mangoldt main term at scale*eta."""

    return scale / (2.0 * math.pi) * math.log(scale * eta / (2.0 * math.pi))


def scaled_error_derivative(scale: float, eta: float) -> float:
    """Derivative of the conservative error envelope at scale*eta."""

    return (
        0.112 / eta
        + 0.278 / (eta * math.log(scale * eta))
        - 0.2 / (scale * eta * eta)
    )


def band_margin_derivative(
    left: float, right: float, rate: float, eta: float
) -> float:
    """Derivative after subtracting rate*eta*log(eta) from a band bound."""

    return (
        scaled_main_derivative(right, eta)
        - scaled_main_derivative(left, eta)
        - scaled_error_derivative(right, eta)
        - scaled_error_derivative(left, eta)
        - rate * (math.log(eta) + 1.0)
    )


def band_margin_second_derivative_lower(
    left: float, right: float, rate: float, eta: float
) -> float:
    """Simple analytic lower bound for the second margin derivative."""

    return (
        ((right - left) / (2.0 * math.pi) - rate) / eta
        - 0.4 * (1.0 / left + 1.0 / right) / eta**3
    )


def orbit_slope(height_ratio: float, centered_ratio_square: float) -> float:
    """Dimensionless orbit slope p(u,e)."""

    u = height_ratio
    e = centered_ratio_square
    denominator_base = 1.0 + u * u - e
    return (
        1.0
        + 2.0 / denominator_base
        - 4.0
        * denominator_base
        / (denominator_base * denominator_base + 4.0 * e * u * u)
    )


def audit_constants() -> dict[str, float]:
    """Return and assert the constants used in (E26)--(E28)."""

    eta = 100.0
    first_band = band_count_lower(0.5, 0.75, eta)
    second_band = band_count_lower(1.5, 2.0, eta)
    assert first_band > 1.0e-3 * eta * math.log(eta)
    assert second_band > 2.0e-2 * eta * math.log(eta)
    assert band_margin_derivative(0.5, 0.75, 1.0e-3, eta) > 0.12
    assert band_margin_derivative(1.5, 2.0, 2.0e-2, eta) > 0.22
    assert band_margin_second_derivative_lower(0.5, 0.75, 1.0e-3, eta) > 0.0
    assert band_margin_second_derivative_lower(1.5, 2.0, 2.0e-2, eta) > 0.0

    epsilon = 2.5e-5
    first_slopes = [
        orbit_slope(0.5 + 0.25 * index / 10_000.0, edge)
        for index in range(10_001)
        for edge in (0.0, epsilon)
    ]
    second_slopes = [
        orbit_slope(1.5 + 0.5 * index / 10_000.0, edge)
        for index in range(10_001)
        for edge in (0.0, epsilon)
    ]
    assert max(first_slopes) < -0.279
    assert min(second_slopes) > 0.383

    compact_floor = min(
        432.0**2 * radius**3 / ((radius + 225.0) ** 3 * (radius + 484.0) ** 3)
        for radius in (0.25, 10_000.0)
    )
    large_floor = (1024.0 / 769_000.0) * (0.24 / 29.0) * 0.6**2
    assert compact_floor > 2.24e-12
    assert large_floor > 3.96e-6
    return {
        "first_band_at_100": first_band,
        "second_band_at_100": second_band,
        "compact_variance_floor": compact_floor,
        "large_variance_floor": large_floor,
        "first_band_max_slope": max(first_slopes),
        "second_band_min_slope": min(second_slopes),
    }


if __name__ == "__main__":
    print(audit_constants())

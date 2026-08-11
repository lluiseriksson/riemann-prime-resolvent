"""Light audit for Proposition 4.1d.

The theorem is analytic. This script only cross-checks the transform and
autocorrelation identities and exhibits both residual signs in the first
prime window. It is not evidence for RH or for the Haar-recurrence proof.
"""

from __future__ import annotations

import cmath
import math


def h_cusp(t: float) -> float:
    if t == 0:
        return 0.25
    return math.exp(1.5 * t) / math.expm1(2 * t) - 1 / (2 * t)


def simpson(function, left: float, right: float, intervals: int):
    assert intervals % 2 == 0
    step = (right - left) / intervals
    total = function(left) + function(right)
    total += 4 * sum(function(left + step * index) for index in range(1, intervals, 2))
    total += 2 * sum(function(left + step * index) for index in range(2, intervals, 2))
    return total * step / 3


def transform_closed(a: float, frequency: float, z: complex) -> complex:
    numerator = 2 * (
        z * cmath.sin(a * z) * math.cos(a * frequency)
        - frequency * cmath.cos(a * z) * math.sin(a * frequency)
    )
    return numerator / (z * z - frequency * frequency)


def transform_quadrature(a: float, frequency: float, z: complex) -> complex:
    return complex(
        simpson(
            lambda x: math.cos(frequency * x) * cmath.exp(1j * z * x),
            -a,
            a,
            20_000,
        )
    )


def autocorrelation_closed(a: float, frequency: float, lag: float) -> float:
    return (
        (2 * a - lag) * math.cos(frequency * lag) / 2
        + math.sin(2 * a * frequency - frequency * lag) / (2 * frequency)
    )


def autocorrelation_quadrature(a: float, frequency: float, lag: float) -> float:
    return float(
        simpson(
            lambda x: math.cos(frequency * (x + lag)) * math.cos(frequency * x),
            -a,
            a - lag,
            20_000,
        )
    )


def residual_first_window(a: float, frequency: float) -> float:
    log_two = math.log(2)

    def correlation(lag: float) -> float:
        return (
            (2 * a - lag) * math.cos(frequency * lag) / 2
            + math.sin(2 * a * frequency - frequency * lag) / (2 * frequency)
        )

    cusp = 2 * simpson(
        lambda lag: lag**2 * h_cusp(lag) * correlation(lag), 0, 2 * a, 20_000
    )
    prime_weight = log_two**3 / math.sqrt(2)
    return float(cusp + 2 * prime_weight * correlation(log_two))


def allowed(frequency: float, a: float) -> bool:
    return frequency * math.tan(a * frequency) > 0


def find_phase(a: float, sign: int) -> float:
    log_two = math.log(2)
    for index in range(2_000, 200_000):
        frequency = index / 100
        if allowed(frequency, a) and sign * math.cos(frequency * log_two) > 0.9:
            return frequency
    raise AssertionError("phase search failed")


def audit() -> None:
    a = 0.4  # exp(2a) is between 2 and 3: only n=2 is active.
    frequency = find_phase(a, 1)
    z = 1.3 + 0.4j
    closed = transform_closed(a, frequency, z)
    quadrature = transform_quadrature(a, frequency, z)
    assert abs(closed - quadrature) < 1e-11

    lag = 0.37
    closed_correlation = autocorrelation_closed(a, frequency, lag)
    quadrature_correlation = autocorrelation_quadrature(a, frequency, lag)
    assert abs(closed_correlation - quadrature_correlation) < 1e-12

    positive_frequency = find_phase(a, 1)
    negative_frequency = find_phase(a, -1)
    positive = residual_first_window(a, positive_frequency)
    negative = residual_first_window(a, negative_frequency)
    assert positive > 0
    assert negative < 0
    assert allowed(positive_frequency, a)
    assert allowed(negative_frequency, a)

    print("ROBIN-REAL-ROOTED-SIGN-NO-GO: PASS")
    print(
        {
            "a": a,
            "positive_frequency": positive_frequency,
            "positive_residual": positive,
            "negative_frequency": negative_frequency,
            "negative_residual": negative,
        }
    )


if __name__ == "__main__":
    audit()

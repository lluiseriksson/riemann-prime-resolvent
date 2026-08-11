"""Lightweight audit for the exponential null-tomography identity.

The script evaluates the polarized logarithmic, prime-translation, and smooth
convolution terms in two independent coordinate systems.  It does not test RH
or the existence of a first crossing.  Only elementary quadrature is used;
the run is intentionally single-process and small enough for the local desk.
"""

from __future__ import annotations

import math
from collections.abc import Callable


def midpoint_integral(function: Callable[[float], float], left: float, right: float, count: int) -> float:
    step = (right - left) / count
    return step * sum(function(left + (index + 0.5) * step) for index in range(count))


def entire_ein(value: float) -> float:
    """Return Ein(z) = integral_0^z (1-exp(-t))/t dt by its entire series."""

    term = value
    total = term
    for order in range(1, 200):
        term *= -value * order / (order + 1) ** 2
        total += term
        if abs(term) <= 2.0e-16 * max(1.0, abs(total)):
            return total
    raise AssertionError("Ein series did not converge")


def trial(point: float) -> float:
    return 1.0 - 0.3 * point + 0.2 * point * point


def audit_logarithmic_polarization(half_width: float, exponent: float) -> float:
    # The first expression is the original symmetric double integral.  The
    # second first integrates the exponential difference and uses Ein.
    count = 700
    step = 2.0 * half_width / count
    points = [-half_width + (index + 0.5) * step for index in range(count)]
    values = [trial(point) for point in points]
    exponentials = [math.exp(exponent * point) for point in points]

    direct = 0.0
    for left in range(count):
        for right in range(count):
            if left == right:
                continue
            direct += (
                (values[left] - values[right])
                * (exponentials[left] - exponentials[right])
                / abs(points[left] - points[right])
            )
    direct *= 0.25 * step * step

    reduced = 0.5 * midpoint_integral(
        lambda point: trial(point)
        * math.exp(exponent * point)
        * (
            entire_ein(exponent * (half_width + point))
            + entire_ein(-exponent * (half_width - point))
        ),
        -half_width,
        half_width,
        20_000,
    )
    return abs(direct - reduced)


def audit_prime_translation(half_width: float, exponent: float, shift: float) -> float:
    count = 30_000
    direct = midpoint_integral(
        lambda point: trial(point + shift) * math.exp(exponent * point),
        -half_width,
        half_width - shift,
        count,
    ) + midpoint_integral(
        lambda point: trial(point - shift) * math.exp(exponent * point),
        -half_width + shift,
        half_width,
        count,
    )

    reduced = math.exp(-exponent * shift) * midpoint_integral(
        lambda point: trial(point) * math.exp(exponent * point),
        -half_width + shift,
        half_width,
        count,
    ) + math.exp(exponent * shift) * midpoint_integral(
        lambda point: trial(point) * math.exp(exponent * point),
        -half_width,
        half_width - shift,
        count,
    )
    return abs(direct - reduced)


def smooth_kernel(point: float) -> float:
    # An independent even C^2 surrogate for r''; only the change of variables
    # in the claimed identity is under audit here.
    return 1.0 + point * point


def audit_smooth_convolution(half_width: float, exponent: float) -> float:
    outer_count = 500
    inner_count = 500
    step = 2.0 * half_width / outer_count
    points = [-half_width + (index + 0.5) * step for index in range(outer_count)]

    direct = 0.0
    for x in points:
        for y in points:
            direct += smooth_kernel(x - y) * trial(y) * math.exp(exponent * x)
    direct *= step * step

    reduced = midpoint_integral(
        lambda y: trial(y)
        * math.exp(exponent * y)
        * midpoint_integral(
            lambda offset: smooth_kernel(offset) * math.exp(exponent * offset),
            -half_width - y,
            half_width - y,
            inner_count,
        ),
        -half_width,
        half_width,
        outer_count,
    )
    return abs(direct - reduced)


def main() -> None:
    half_width = 0.7
    exponent = 0.9
    logarithmic_error = audit_logarithmic_polarization(half_width, exponent)
    prime_error = audit_prime_translation(half_width, exponent, 0.45)
    smooth_error = audit_smooth_convolution(half_width, exponent)

    # The direct double midpoint rule sees a removable diagonal cusp, hence a
    # deliberately looser deterministic tolerance than the 1D identities.
    assert logarithmic_error < 3.0e-6, logarithmic_error
    assert prime_error < 2.0e-13, prime_error
    assert smooth_error < 2.0e-12, smooth_error
    print(
        "EXPONENTIAL-NULL-TOMOGRAPHY-AUDIT: PASS "
        f"(log={logarithmic_error:.3e}, prime={prime_error:.3e}, "
        f"smooth={smooth_error:.3e})"
    )


if __name__ == "__main__":
    main()

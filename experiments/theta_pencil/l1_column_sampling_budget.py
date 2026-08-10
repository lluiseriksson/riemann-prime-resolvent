"""Audit the L1 column-sum refinement of the Euler-axis Pick proof.

This is scalar bookkeeping only.  The analytic inequalities and their scope
are stated in ``docs/theta-reboot/euler-axis-pick.md``.
"""

from __future__ import annotations

import math
from fractions import Fraction


VERIFIED_HEIGHT = 3.0e12
SAMPLING_RADIUS = 2.0
UNIT_ZERO_COUNT_FACTOR = 0.69


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


def radius_two_zero_count_lower(height: float = VERIFIED_HEIGHT) -> float:
    return (
        zero_count_main(height + SAMPLING_RADIUS)
        - zero_count_main(height - SAMPLING_RADIUS)
        - zero_count_error(height + SAMPLING_RADIUS)
        - zero_count_error(height - SAMPLING_RADIUS)
    )


def unit_zero_count_coefficient(height: float = VERIFIED_HEIGHT) -> float:
    """A simple upper coefficient valid for every interval of length <= 1."""

    logarithm = math.log(height)
    return (
        1.0 / (2.0 * math.pi)
        + 0.224
        + 0.556 * math.log(logarithm) / logarithm
        + 6.77 / logarithm
        + 0.4 / (height * logarithm)
    )


def cardinal_bounds(node_count: int) -> dict[str, float]:
    """Return explicit Chebyshev-cardinal W^{j,1}/sup bounds."""

    m = float(node_count)
    return {
        "l1_second": 2.0 / 3.0 * m**2 * (2.0 * math.log(2.0 * m) + 7.0 / 3.0),
        "l1_third": 56.0 / 5.0 * m**4,
        "sup_first": 2.0 / 3.0 * m**2,
        "sup_second": 2.0 / 15.0 * m**4,
        "sup_third": 2.0 / 105.0 * m**6,
        "sup_fourth": 2.0 / 945.0 * m**8,
    }


def order_budget(order: int, height: float = VERIFIED_HEIGHT) -> dict[str, float]:
    """Return the explicit L1 sampling budget for one Pick-matrix order."""

    if order < 4:
        raise ValueError("order must be at least four")
    degree = 4 * order - 2
    node_count = degree + 1
    band_ratio = 1.0 / node_count
    band_length = height / node_count
    lebesgue = 1.0 + 2.0 / math.pi * math.log(node_count)

    # A selected zero lies within absolute distance two of each exact
    # Chebyshev root.  Markov on an interval of length L gives this error.
    perturbation = 4.0 * degree**2 / band_length
    if lebesgue * perturbation >= 1.0:
        raise ValueError("perturbed interpolation is not certified")
    interpolation = lebesgue / (1.0 - lebesgue * perturbation)
    column_sum = 1.0 + node_count * perturbation * interpolation

    bounds = cardinal_bounds(node_count)
    vertical_exponent = degree**2 / band_length
    vertical = math.exp(vertical_exponent)

    # Integrated suprema on |Im w| <= 1/2, per sum of sampled numerator
    # values.  The first term is the real-axis L1 norm; the second is the
    # vertical fundamental-theorem correction.
    a0 = band_length * interpolation + vertical * bounds["sup_first"] * column_sum
    a1 = column_sum * (
        2.0 * node_count
        + 2.0 * vertical * bounds["sup_second"] / band_length
    )
    a2 = column_sum * (
        2.0 * bounds["l1_second"] / band_length
        + 4.0 * vertical * bounds["sup_third"] / band_length**2
    )
    a3 = column_sum * (
        4.0 * bounds["l1_third"] / band_length**2
        + 8.0 * vertical * bounds["sup_fourth"] / band_length**3
    )

    tiny = 1.0 / (4.0 * height**2)
    denominator_loss = (1.0 - tiny) ** (-2 * order)
    kappa0 = (1.0 + 1.0 / (2.0 * height)) / (1.0 - tiny)
    kappa1 = (
        (1.0 + 1.0 / height + tiny) / (1.0 - tiny) ** 2
    )
    kappa2 = (
        (1.0 + 1.0 / (2.0 * height))
        * (1.0 + 1.0 / height + tiny)
        / (1.0 - tiny) ** 3
    )
    h0 = 4.0 * kappa0 * order / height
    h1 = 4.0 * kappa1 * order / height**2
    h2 = 24.0 * kappa2 * order / height**3

    denominator_ratio = (1.0 + band_ratio) ** (4 * order)
    common = denominator_loss * denominator_ratio
    integrated_second = common * (
        a2 + 2.0 * h0 * a1 + (h0**2 + h1) * a0
    )
    integrated_third = common * (
        a3
        + 3.0 * h0 * a2
        + 3.0 * (h0**2 + h1) * a1
        + (h0**3 + 3.0 * h0 * h1 + h2) * a0
    )

    unit_count = UNIT_ZERO_COUNT_FACTOR * math.log(
        (1.0 + band_ratio) * height
    )
    fraction = unit_count / 8.0 * (
        2.0 * integrated_second + integrated_third
    )
    return {
        "order": float(order),
        "degree": float(degree),
        "node_count": float(node_count),
        "perturbation": perturbation,
        "interpolation_factor": interpolation,
        "column_sum_factor": column_sum,
        "vertical_exponent": vertical_exponent,
        "integrated_second": integrated_second,
        "integrated_third": integrated_third,
        "budget_fraction": fraction,
    }


def coarse_order_233_certificate() -> Fraction:
    """Return an exact-rational upper envelope for every order n <= 233.

    The only transcendental inputs have first been rounded upward:
    ``Lambda < 5.356``, ``I < 5.39``, ``J < 6.39``,
    ``exp(mu) < 1.0011``, and the unit-bin factor is below ``19.872``.
    The band denominator ratio is bounded by ``2.82``.  The document gives
    the elementary inequalities behind these decimal rational bounds.
    """

    q = Fraction
    order = 233
    node_count = 931
    height = q(3_000_000_000_000)
    minimum_length = height / node_count
    maximum_length = height / 15
    interpolation = q(539, 100)
    column_sum = q(639, 100)
    vertical = q(10011, 10000)
    log_two_m = q(753, 100)

    m = q(node_count)
    l1_second = q(2, 3) * m**2 * (2 * log_two_m + q(7, 3))
    l1_third = q(56, 5) * m**4
    sup_first = q(2, 3) * m**2
    sup_second = q(2, 15) * m**4
    sup_third = q(2, 105) * m**6
    sup_fourth = q(2, 945) * m**8

    # For a uniform envelope, only a0 uses the largest possible band length;
    # all derivative terms use the smallest one.
    a0 = maximum_length * interpolation + vertical * sup_first * column_sum
    a1 = column_sum * (
        2 * m + 2 * vertical * sup_second / minimum_length
    )
    a2 = column_sum * (
        2 * l1_second / minimum_length
        + 4 * vertical * sup_third / minimum_length**2
    )
    a3 = column_sum * (
        4 * l1_third / minimum_length**2
        + 8 * vertical * sup_fourth / minimum_length**3
    )

    kappa = q(1_000_001, 1_000_000)
    h0 = 4 * kappa * order / height
    h1 = 4 * kappa * order / height**2
    h2 = q(2401, 100) * order / height**3
    common = q(141, 50) * kappa
    integrated_second = common * (
        a2 + 2 * h0 * a1 + (h0**2 + h1) * a0
    )
    integrated_third = common * (
        a3
        + 3 * h0 * a2
        + 3 * (h0**2 + h1) * a1
        + (h0**3 + 3 * h0 * h1 + h2) * a0
    )
    unit_bin_bound = q(2484, 125)
    return unit_bin_bound / 8 * (
        2 * integrated_second + integrated_third
    )


def audit() -> dict[str, object]:
    """Check every scalar gate used by the order-234 statement."""

    assert radius_two_zero_count_lower() > 2.04
    assert unit_zero_count_coefficient() < UNIT_ZERO_COUNT_FACTOR

    rational_certificate = coarse_order_233_certificate()
    assert rational_certificate < Fraction(987, 1000)
    diagnostic_234 = order_budget(234)
    diagnostic_235 = order_budget(235)

    node_count = 4 * 234 - 1
    band_length = VERIFIED_HEIGHT / node_count
    edge_clearance = band_length / 2.0 * (
        1.0 - math.cos(math.pi / (2.0 * node_count))
    )
    minimum_spacing = band_length / 2.0 * (
        math.cos(math.pi / (2.0 * node_count))
        - math.cos(3.0 * math.pi / (2.0 * node_count))
    )
    assert edge_clearance > 2260.0
    assert minimum_spacing > 18100.0
    return {
        "radius_two_lower_zero_count": radius_two_zero_count_lower(),
        "unit_zero_count_coefficient": unit_zero_count_coefficient(),
        "certified_through": 233,
        "order_233_rational_upper": float(rational_certificate),
        "order_234_floating_diagnostic": diagnostic_234,
        "order_235_floating_diagnostic": diagnostic_235,
        "order_234_edge_clearance": edge_clearance,
        "order_234_minimum_spacing": minimum_spacing,
    }


if __name__ == "__main__":
    print(audit())

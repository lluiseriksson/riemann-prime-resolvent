"""Compute the explicit finite-order Pick sampling budget."""

from __future__ import annotations

import math


VERIFIED_HEIGHT = 3.0e12
COMPLEX_STRIP_FACTOR = 1.01
ZERO_COUNT_FACTOR = 0.161


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


def minimum_sampling_interval_count(order: int) -> float:
    """Return the first-band lower zero count over all Chebyshev samples."""

    degree = 4 * order - 2
    count = degree + 1
    band_ratio = 1.0 / count
    relative_radius = band_ratio / (100.0 * degree * degree)
    centers = [
        1.0
        + band_ratio / 2.0
        + band_ratio
        / 2.0
        * math.cos((2 * index + 1) * math.pi / (2 * count))
        for index in range(count)
    ]
    lower_counts = []
    for center in centers:
        left = (center - relative_radius) * VERIFIED_HEIGHT
        right = (center + relative_radius) * VERIFIED_HEIGHT
        lower_counts.append(
            zero_count_main(right)
            - zero_count_main(left)
            - zero_count_error(right)
            - zero_count_error(left)
        )
    return min(lower_counts)


def first_band_zero_count_ratio(order: int) -> float:
    """Return the explicit upper count divided by q*T*log(T)."""

    band_ratio = 1.0 / (4 * order - 1)
    height = VERIFIED_HEIGHT
    upper = (
        zero_count_main((1.0 + band_ratio) * height)
        - zero_count_main(height)
        + zero_count_error((1.0 + band_ratio) * height)
        + zero_count_error(height)
    )
    return upper / (band_ratio * height * math.log(height))


def order_budget(order: int) -> dict[str, float]:
    """Return constants (E49)--(E52) for one matrix order."""

    if order < 2:
        raise ValueError("order must be at least two")
    degree = 4 * order - 2
    band_ratio = 1.0 / (4 * order - 1)
    lebesgue = 1.0 + 2.0 / math.pi * math.log(degree + 1.0)
    interpolation = lebesgue / (1.0 - 0.02 * lebesgue)
    derivative = (
        4.0 * degree**4 / band_ratio**2
        + 16.0 * order * degree**2 / band_ratio
        + (4.0 * order) ** 2
        + 4.0 * order
    )
    sampling = (
        COMPLEX_STRIP_FACTOR
        * interpolation
        * (1.0 + band_ratio) ** (4 * order)
        * derivative
    )
    fraction = (
        ZERO_COUNT_FACTOR
        * sampling
        * band_ratio
        * math.log(VERIFIED_HEIGHT)
        / (8.0 * VERIFIED_HEIGHT)
    )
    return {
        "order": float(order),
        "degree": float(degree),
        "band_ratio": band_ratio,
        "lebesgue_bound": lebesgue,
        "interpolation_factor": interpolation,
        "sampling_constant": sampling,
        "budget_fraction": fraction,
    }


def audit() -> dict[str, object]:
    """Verify that the conservative method closes exactly through order 40."""

    rows = [order_budget(order) for order in range(4, 42)]
    interval_counts = {
        order: minimum_sampling_interval_count(order) for order in range(4, 41)
    }
    count_ratios = {
        order: first_band_zero_count_ratio(order) for order in range(4, 42)
    }
    assert all(row["budget_fraction"] < 1.0 for row in rows[:-1])
    assert rows[-2]["order"] == 40.0
    assert rows[-2]["budget_fraction"] < 0.972
    assert rows[-1]["order"] == 41.0
    assert rows[-1]["budget_fraction"] > 1.105
    assert min(interval_counts.values()) > 6.46e4
    assert max(count_ratios.values()) < 0.15
    assert max(
        (4 * order - 2) ** 2
        * (4 * order - 1)
        / VERIFIED_HEIGHT
        for order in range(4, 42)
    ) < 1.5e-6
    return {
        "last_closed": rows[-2],
        "first_unclosed": rows[-1],
        "order_39": rows[-3],
        "minimum_sampling_zero_count": min(interval_counts.values()),
        "maximum_first_band_count_ratio": max(count_ratios.values()),
    }


if __name__ == "__main__":
    print(audit())

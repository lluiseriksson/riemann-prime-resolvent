"""Regression checks for the integer-cutoff von Mangoldt tail theorem."""

from __future__ import annotations

import math


def von_mangoldt_table(limit: int) -> list[float]:
    values = [0.0] * (limit + 1)
    composite = [False] * (limit + 1)
    for p in range(2, limit + 1):
        if composite[p]:
            continue
        log_p = math.log(p)
        power = p
        while power <= limit:
            values[power] = log_p
            if power > limit // p:
                break
            power *= p
        if p * p <= limit:
            for multiple in range(p * p, limit + 1, p):
                composite[multiple] = True
    return values


def majorant(delta: float, cutoff: int) -> float:
    return cutoff ** (-delta) * (
        math.log(cutoff) / delta + 1.0 / delta**2
    )


def test_finite_von_mangoldt_tails_stay_below_majorant() -> None:
    limit = 200_000
    mangoldt = von_mangoldt_table(limit)
    for delta, cutoff in ((0.05, 3), (0.25, 10), (0.5, 100), (1.0, 1000)):
        partial_tail = sum(
            mangoldt[n] * math.exp(-(1.0 + delta) * math.log(n))
            for n in range(cutoff + 1, limit + 1)
        )
        assert 0.0 <= partial_tail < majorant(delta, cutoff)


def test_integral_antiderivative_matches_closed_form() -> None:
    for delta, cutoff in ((0.05, 3), (0.25, 10), (1.0, 1000)):
        primitive_at_cutoff = -cutoff ** (-delta) * (
            math.log(cutoff) / delta + 1.0 / delta**2
        )
        assert math.isclose(
            -primitive_at_cutoff,
            majorant(delta, cutoff),
            rel_tol=2e-15,
            abs_tol=0.0,
        )

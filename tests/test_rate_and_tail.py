from __future__ import annotations

import math


def rate(q: float) -> float:
    return min((2 * q - 1) / 3, 2 / 3)


def tail(delta: float, n: int) -> float:
    return math.exp(-delta * math.log(n)) * (math.log(n) / delta + 1 / delta**2)


def test_rate_thresholds() -> None:
    assert rate(0.5) == 0
    assert rate(1.5) == 2 / 3
    assert rate(2.0) == 2 / 3
    assert rate(1.0) > 0


def test_tail_positive_and_eventually_decreasing() -> None:
    for delta in (0.1, 0.25, 0.5):
        assert tail(delta, 3) > 0
        assert tail(delta, 1_000_000) < tail(delta, 10_000)

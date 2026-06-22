from __future__ import annotations

import math


def majorant(delta: float, n: int) -> float:
    return n ** (-delta) * (math.log(n) / delta + 1 / delta**2)


def test_integer_cutoff_majorant_positive() -> None:
    for delta in (0.1, 0.25, 0.5):
        assert majorant(delta, 3) > 0
        assert majorant(delta, 1_000_000) < majorant(delta, 10_000)

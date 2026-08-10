"""Elementary arithmetic shared by the prime-power translation routines."""

from __future__ import annotations

import math


def prime_power_base(value: int) -> int:
    """Return ``p`` when ``value = p^k`` for a prime ``p``; reject otherwise."""

    if value < 2:
        raise ValueError("prime powers must be at least two")
    for candidate in range(2, math.isqrt(value) + 2):
        if any(
            candidate % divisor == 0
            for divisor in range(2, math.isqrt(candidate) + 1)
        ):
            continue
        remainder = value
        while remainder % candidate == 0:
            remainder //= candidate
        if remainder == 1:
            return candidate
    if all(value % divisor for divisor in range(2, math.isqrt(value) + 1)):
        return value
    raise ValueError(f"{value} is not a prime power")


def von_mangoldt(value: int) -> float:
    """Return the von Mangoldt weight of a validated prime power."""

    return math.log(prime_power_base(value))

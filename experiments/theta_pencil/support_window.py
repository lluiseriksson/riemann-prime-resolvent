"""Exact-decimal guards for support-window boundaries."""

from __future__ import annotations

from decimal import Decimal, localcontext


def _decimal(value: float) -> Decimal:
    return Decimal(str(value))


def _log(integer: int) -> Decimal:
    with localcontext() as context:
        context.prec = 80
        return Decimal(integer).ln()


LOG_TWO = _log(2)
LOG_THREE = _log(3)


def prime_overlap_positive(half_width: float, prime: int) -> bool:
    """Whether the exact input decimal satisfies ``log(prime) < 2a``."""

    if prime < 2:
        return False
    return _log(prime) < 2 * _decimal(half_width)


def in_first_prime_window(half_width: float) -> bool:
    """Exact-decimal test for ``log(2)/2 < a <= log(3)/2``."""

    value = 2 * _decimal(half_width)
    return LOG_TWO < value <= LOG_THREE


def in_second_prime_window(half_width: float) -> bool:
    """Exact-decimal test for ``log(3)/2 < a < log(2)``."""

    value = _decimal(half_width)
    return LOG_THREE / 2 < value < LOG_TWO


def at_most_prime_three_boundary(half_width: float) -> bool:
    """Exact-decimal test for ``a <= log(3)/2``."""

    return 2 * _decimal(half_width) <= LOG_THREE


def in_prime_two_comparison_window(half_width: float) -> bool:
    """Exact-decimal test for ``1/2 <= a < log(2)``."""

    value = _decimal(half_width)
    return Decimal(1) / 2 <= value < LOG_TWO

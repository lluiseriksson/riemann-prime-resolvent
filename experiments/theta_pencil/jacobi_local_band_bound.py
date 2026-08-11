"""Exact audit for the width-29 Jacobi tail bound.

This module checks the terminating beta-sum identities and the rational
inequalities used to control every band with m >= 232 and 1 <= n-m <= 29.
The infinite-in-m part is analytic; the finite checks below audit its exact
cutoff constants without using zero data or floating-point quadrature.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, factorial

try:
    from experiments.theta_pencil.jacobi_dilation_connection import rising
except ModuleNotFoundError:  # Direct ``python path/to/script.py`` execution.
    from jacobi_dilation_connection import rising


TAIL_START = 232
MAX_GAP = 29
EXTENDED_GAP = 45


def beta_integer(left: int, right: int) -> Fraction:
    """Exact beta(left,right) for positive integers."""

    return Fraction(
        factorial(left - 1) * factorial(right - 1),
        factorial(left + right - 1),
    )


def normalized_jacobi_coefficients(m: int, gap: int) -> list[Fraction]:
    """Coefficients of H_(m,d)=2F1(1-d,2m+d+2;2m+2;u)."""

    degree = gap - 1
    return [
        Fraction(
            (-1) ** j * comb(degree, j) * rising(2 * m + gap + 2, j),
            rising(2 * m + 2, j),
        )
        for j in range(degree + 1)
    ]


def jacobi_moment(m: int, gap: int, order: int) -> Fraction:
    """Exact J_order = integral u^(m-1)(1-u)^order H_(m,d)(u) du."""

    return sum(
        (
            coefficient * beta_integer(m + power, order + 1)
            for power, coefficient in enumerate(
                normalized_jacobi_coefficients(m, gap)
            )
        ),
        Fraction(0),
    )


def closed_j_one(m: int, gap: int) -> Fraction:
    """Saalschutz evaluation of J_1."""

    return Fraction(
        factorial(gap) * factorial(2 * m + 1),
        m * (m + 1) * factorial(2 * m + gap),
    )


def closed_j_zero_ratio(m: int, gap: int) -> Fraction:
    """Closed parity formula for J_0/J_1."""

    if gap % 2 == 0:
        return Fraction(1)
    half = (gap + 1) // 2
    center = m + half
    return Fraction(center * center + half * (half - 1), gap * center)


def odd_upper_polynomial(m: int, gap: int) -> int:
    """Positive numerator proving the odd-band archimedean bound < 1/d."""

    assert gap % 2 == 1
    return (
        14 * gap * m * m
        + 7 * gap * (gap + 1) * m
        - (gap - 1) * (gap + 1) ** 2
    )


def even_archimedean_rational_upper(m: int, gap: int) -> Fraction:
    """Rational majorant for the even-band archimedean contribution."""

    assert gap % 2 == 0
    # sqrt((2m+1)(2m+2d+1)) <= 2m+d+1.
    return Fraction(15 * (2 * m + gap + 1), 8 * m * (m + 1))


def odd_archimedean_crude_upper(m: int, gap: int) -> Fraction:
    """Monotone-in-m absolute upper bound for an odd archimedean band."""

    assert gap % 2 == 1
    half = (gap + 1) // 2
    correction = half * (half - 1)
    norm_upper = Fraction(2, m) + Fraction(gap + 1, m * m)
    bracket_upper = (
        Fraction(m, 2 * gap)
        + Fraction(half, 2 * gap)
        + Fraction(correction, 2 * gap * m)
        + Fraction(13, 4)
    )
    return norm_upper * bracket_upper


def even_archimedean_crude_upper(m: int, gap: int) -> Fraction:
    """Monotone-in-m absolute upper bound for an even archimedean band."""

    assert gap % 2 == 0
    norm_upper = Fraction(2, m) + Fraction(gap + 1, m * m)
    return Fraction(15, 8) * norm_upper


def crude_prime_upper(m: int, gap: int) -> Fraction:
    """Elementary prime-band bound using e<3 and Lambda(r)<=log(r)."""

    # binom(2m+d,d) <= (e(2m+d)/d)^d, the square-root norm ratio is <2,
    # and the entire Mangoldt moment is <2^-m.
    return (
        Fraction(2, 2**m)
        * Fraction(3 * (2 * m + gap), gap) ** gap
    )


def main() -> None:
    identity_checks = 0
    for m in range(4, 20):
        for gap in range(1, 14):
            j_zero = jacobi_moment(m, gap, 0)
            j_one = jacobi_moment(m, gap, 1)
            assert j_one == closed_j_one(m, gap)
            assert j_zero == j_one * closed_j_zero_ratio(m, gap)
            previous = j_one
            assert previous > 0
            for order in range(2, 7):
                current = jacobi_moment(m, gap, order)
                assert 0 < current < previous
                previous = current
            identity_checks += 1

    for gap in range(1, MAX_GAP + 1, 2):
        assert odd_upper_polynomial(TAIL_START, gap) > 0
        assert Fraction(TAIL_START, gap) > Fraction(19, 4)

    for gap in range(2, MAX_GAP + 1, 2):
        assert even_archimedean_rational_upper(TAIL_START, gap) < Fraction(1, 50)

    prime_bounds = [
        crude_prime_upper(TAIL_START, gap)
        for gap in range(1, MAX_GAP + 1)
    ]
    assert max(prime_bounds) < Fraction(1, 10**20)
    assert prime_bounds.index(max(prime_bounds)) + 1 == MAX_GAP

    # The cutoff bound decreases with m: at the worst gap the one-step ratio
    # is already below one, and it decreases thereafter.
    for gap in range(1, MAX_GAP + 1):
        current = crude_prime_upper(TAIL_START, gap)
        following = crude_prime_upper(TAIL_START + 1, gap)
        assert following < current

    for gap in range(1, EXTENDED_GAP + 1, 2):
        assert odd_archimedean_crude_upper(TAIL_START, gap) < Fraction(21, 20)
    for gap in range(2, EXTENDED_GAP + 1, 2):
        assert even_archimedean_crude_upper(TAIL_START, gap) < Fraction(1, 20)

    extended_prime_bounds = [
        crude_prime_upper(TAIL_START, gap)
        for gap in range(1, EXTENDED_GAP + 1)
    ]
    assert max(extended_prime_bounds) < Fraction(1, 4)
    assert extended_prime_bounds.index(max(extended_prime_bounds)) + 1 == EXTENDED_GAP
    for gap in range(1, EXTENDED_GAP + 1):
        assert crude_prime_upper(TAIL_START + 1, gap) < (
            crude_prime_upper(TAIL_START, gap)
        )

    print(f"exact_moment_identity_checks={identity_checks}")
    print(f"max_prime_bound={float(max(prime_bounds)):.12e}")
    print("odd_archimedean_bound=1/gap")
    print("even_archimedean_bound=1/50")
    print("tail_local_diameter=29")
    print(f"extended_prime_bound={float(max(extended_prime_bounds)):.12e}")
    print("extended_tail_local_diameter=45")


if __name__ == "__main__":
    main()

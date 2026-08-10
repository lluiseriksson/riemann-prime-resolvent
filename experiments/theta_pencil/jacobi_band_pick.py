"""Exact Jacobi-band algebra for the arithmetic Euler-axis Pick matrix.

This checks (E99)--(E105).  The finite sequence used for the exact algebra is
arbitrary; no zero data and no assumption about RH enter the computation.
"""

from __future__ import annotations

import math
from fractions import Fraction
from math import comb, factorial


def monic_jacobi_polynomial(degree: int) -> list[Fraction]:
    """Coefficients of t*P_(degree-1)^(0,2)(2t-1), made monic."""

    normalizer = comb(2 * degree, degree - 1)
    result: list[Fraction] = []
    for power in range(1, degree + 1):
        coefficient = (
            (-1) ** (degree - power)
            * comb(degree - 1, power - 1)
            * factorial(degree + power)
        )
        denominator = (
            factorial(degree - 1)
            * factorial(power + 1)
            * normalizer
        )
        result.append(Fraction(coefficient, denominator))
    return result


def hilbert_inner(left: list[Fraction], right: list[Fraction]) -> Fraction:
    """L2(0,1) inner product for polynomials with no constant term."""

    return sum(
        left_coefficient
        * right_coefficient
        * Fraction(1, left_degree + right_degree + 1)
        for left_degree, left_coefficient in enumerate(left, start=1)
        for right_degree, right_coefficient in enumerate(right, start=1)
    )


def multiplier_action(
    polynomial: list[Fraction], multiplier: list[Fraction]
) -> list[Fraction]:
    """Apply the monomial-diagonal multiplier l_n t^n."""

    return [
        coefficient * multiplier[degree - 1]
        for degree, coefficient in enumerate(polynomial, start=1)
    ]


def norm_formula(degree: int) -> Fraction:
    """Closed form h_n in (E99)."""

    return Fraction(1, (2 * degree + 1) * comb(2 * degree, degree - 1) ** 2)


def euler_tail_bounds(index: int) -> dict[str, float]:
    """Evaluate the explicit E0/E1 bounds at the start of the tail."""

    logarithm_two = math.log(2.0)
    e0 = logarithm_two / 2.0**index + 2.0 ** (1 - index) * (
        logarithm_two / (index - 1) + 1.0 / (index - 1) ** 2
    )
    lower = (
        1.0 / (index - 1)
        + 0.5 * math.log(index / (2.0 * math.pi))
        - e0
    )
    e1 = logarithm_two**2 / 2.0**index + 2.0 ** (1 - index) * (
        logarithm_two**2 / (index - 1)
        + 2.0 * logarithm_two / (index - 1) ** 2
        + 2.0 / (index - 1) ** 3
    )
    derivative_upper = 1.0 / (2 * index) + 1.0 / index**2 + e1
    return {
        "index": float(index),
        "E0": e0,
        "ell_lower": lower,
        "E1": e1,
        "derivative_upper": derivative_upper,
        "one_over_index": 1.0 / index,
    }


def audit() -> dict[str, object]:
    """Verify the Jacobi coefficients, norms, and first two bands exactly."""

    maximum_degree = 12
    polynomials = {
        degree: monic_jacobi_polynomial(degree)
        for degree in range(1, maximum_degree + 1)
    }
    multiplier = [
        sum(Fraction(1, k) for k in range(1, degree + 2))
        for degree in range(1, maximum_degree + 1)
    ]

    for degree, polynomial in polynomials.items():
        assert polynomial[-1] == 1
        assert hilbert_inner(polynomial, polynomial) == norm_formula(degree)
        if degree >= 2:
            assert polynomial[-2] == -Fraction(degree**2 - 1, 2 * degree)
        for lower_degree in range(1, degree):
            monomial = [Fraction(0)] * (lower_degree - 1) + [Fraction(1)]
            assert hilbert_inner(polynomial, monomial) == 0

    adjacent_checks = 0
    curvature_checks = 0
    for degree in range(2, maximum_degree + 1):
        current = polynomials[degree]
        previous = polynomials[degree - 1]
        raw = hilbert_inner(previous, multiplier_action(current, multiplier))
        normalized_square = raw**2 / (
            norm_formula(degree - 1) * norm_formula(degree)
        )
        difference = multiplier[degree - 1] - multiplier[degree - 2]
        assert normalized_square == (4 * degree**2 - 1) * difference**2
        assert raw > 0
        adjacent_checks += 1

        if degree >= 3:
            second_previous = polynomials[degree - 2]
            raw_second = hilbert_inner(
                second_previous, multiplier_action(current, multiplier)
            )
            expansion_coefficient = raw_second / norm_formula(degree - 2)
            previous_difference = (
                multiplier[degree - 2] - multiplier[degree - 3]
            )
            expected_coefficient = Fraction(
                (degree + 1) * (degree - 2), 4 * (2 * degree - 1)
            ) * (
                degree * difference
                - (degree - 1) * previous_difference
            )
            assert expansion_coefficient == expected_coefficient
            normalized_second_square = raw_second**2 / (
                norm_formula(degree - 2) * norm_formula(degree)
            )
            expected_second_square = (
                (2 * degree - 3)
                * (2 * degree + 1)
                * (
                    degree * difference
                    - (degree - 1) * previous_difference
                )
                ** 2
            )
            assert normalized_second_square == expected_second_square
            curvature_checks += 1

    tail = euler_tail_bounds(234)
    assert tail["ell_lower"] > 1.0
    assert 234.0 * tail["E1"] < 0.25
    assert tail["derivative_upper"] < tail["one_over_index"]
    return {
        "exact_adjacent_checks": adjacent_checks,
        "exact_curvature_checks": curvature_checks,
        "tail_bound_at_234": tail,
    }


if __name__ == "__main__":
    print(audit())

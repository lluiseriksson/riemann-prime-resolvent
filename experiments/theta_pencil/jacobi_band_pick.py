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


def projection_coefficient(lower_degree: int, monomial_degree: int) -> Fraction:
    """Coefficient r_(m,k) of p_m in the Jacobi expansion of t^k."""

    m = lower_degree
    k = monomial_degree
    if k < m:
        return Fraction(0)
    return Fraction(
        factorial(2 * m + 1)
        * factorial(k + 1)
        * comb(k - 1, m - 1),
        factorial(m + 1) * factorial(k + m + 1),
    )


def determinant_three(matrix: list[list[Fraction]]) -> Fraction:
    """Exact determinant of a three-by-three matrix."""

    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


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
    e2 = logarithm_two**3 / 2.0**index + 2.0 ** (1 - index) * (
        logarithm_two**3 / (index - 1)
        + 3.0 * logarithm_two**2 / (index - 1) ** 2
        + 6.0 * logarithm_two / (index - 1) ** 3
        + 6.0 / (index - 1) ** 4
    )
    derivative_upper = 1.0 / (2 * index) + 1.0 / index**2 + e1
    return {
        "index": float(index),
        "E0": e0,
        "ell_lower": lower,
        "E1": e1,
        "E2": e2,
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
    full_band_checks = 0
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

        for lower_degree in range(1, degree):
            lower = polynomials[lower_degree]
            raw_band = hilbert_inner(
                lower, multiplier_action(current, multiplier)
            )
            expansion_coefficient = raw_band / norm_formula(lower_degree)
            expected_band = sum(
                current[monomial_degree - 1]
                * projection_coefficient(lower_degree, monomial_degree)
                * multiplier[monomial_degree - 1]
                for monomial_degree in range(lower_degree, degree + 1)
            )
            assert expansion_coefficient == expected_band
            full_band_checks += 1

    # A positive-real rank-two atom whose Jacobi matrix is not diagonally
    # dominant.  All entries are exact rationals before normalization.
    atom_nodes = [Fraction(3, 2), Fraction(5, 2), Fraction(7, 2)]
    atom_multiplier = [
        2 * node / (node**2 + 1) for node in atom_nodes
    ]
    atom_kernel = [
        [
            (atom_multiplier[i] + atom_multiplier[j])
            / (atom_nodes[i] + atom_nodes[j])
            for j in range(3)
        ]
        for i in range(3)
    ]
    atom_gram = [
        [
            2
            * (atom_nodes[i] * atom_nodes[j] + 1)
            / ((atom_nodes[i] ** 2 + 1) * (atom_nodes[j] ** 2 + 1))
            for j in range(3)
        ]
        for i in range(3)
    ]
    assert atom_kernel == atom_gram
    assert determinant_three(atom_kernel) == 0

    raw_12 = hilbert_inner(
        polynomials[1], multiplier_action(polynomials[2], atom_multiplier)
    )
    raw_23 = hilbert_inner(
        polynomials[2], multiplier_action(polynomials[3], atom_multiplier)
    )
    normalized_12_square = raw_12**2 / (norm_formula(1) * norm_formula(2))
    normalized_23_square = raw_23**2 / (norm_formula(2) * norm_formula(3))
    assert raw_12 < 0 and raw_23 < 0
    assert normalized_12_square == Fraction(116160, 142129)
    assert normalized_23_square == Fraction(2152640, 2362369)
    assert normalized_12_square > Fraction(81, 100)
    assert normalized_23_square > Fraction(81, 100)
    assert 2 * atom_multiplier[1] == Fraction(40, 29) < Fraction(9, 5)

    tail = euler_tail_bounds(234)
    three_band_tail = euler_tail_bounds(233)
    adjacent_bound = 1.0 + 6.0 * 233.0 / 232.0**2
    curvature_bound = 2.0 * 234.0 * (
        1.0 / (4.0 * 233.0**2)
        + (7.0 * 234.0 - 6.0) / 232.0**3
    )
    three_band_diagonal_lower = 2.0 * three_band_tail["ell_lower"]
    assert tail["ell_lower"] > 1.0
    assert 234.0 * tail["E1"] < 0.25
    assert tail["derivative_upper"] < tail["one_over_index"]
    assert three_band_tail["E1"] < 1.0 / 232.0**2
    assert three_band_tail["E2"] < 2.0 / 232.0**3
    assert 2.0 * adjacent_bound + curvature_bound < three_band_diagonal_lower
    return {
        "exact_adjacent_checks": adjacent_checks,
        "exact_curvature_checks": curvature_checks,
        "exact_full_band_checks": full_band_checks,
        "rank_two_atom_determinant": str(determinant_three(atom_kernel)),
        "rank_two_atom_row_dominance": False,
        "tail_bound_at_234": tail,
        "three_band_tail": {
            "adjacent_bound": adjacent_bound,
            "curvature_bound": curvature_bound,
            "overcounted_row_sum": 2.0 * adjacent_bound + curvature_bound,
            "diagonal_lower": three_band_diagonal_lower,
        },
    }


if __name__ == "__main__":
    print(audit())

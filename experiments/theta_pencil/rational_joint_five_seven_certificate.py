"""Dependency-free rational certificate for ``V + T_5 + T_7 >= -267/1000``.

All transcendental inputs are replaced by one-sided rational series bounds.
The final positive-definiteness checks use exact ``Fraction`` arithmetic.
No floating-point value participates in the certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb, factorial, isqrt


TARGET = Fraction(267, 1000)


@dataclass(frozen=True)
class RationalJointFiveSevenCertificate:
    scale_digits: int
    cells: int
    logarithm_terms: int
    potential_terms: int
    log_five_lower: Fraction
    log_five_upper: Fraction
    log_seven_lower: Fraction
    log_seven_upper: Fraction
    edge_five_upper: Fraction
    edge_seven_upper: Fraction
    four_path_minor_lowers: tuple[Fraction, ...]
    four_path_argmin_cells: tuple[int, ...]
    two_path_minor_lowers: tuple[Fraction, ...]
    two_path_argmin_cells: tuple[int, ...]

    @property
    def certified_floor(self) -> Fraction:
        return -TARGET


@dataclass(frozen=True)
class RationalSupportOneTailCertificate:
    joint_five_seven: RationalJointFiveSevenCertificate
    local_degree: int
    harmonic_floor: Fraction
    log_two_pi_upper: Fraction
    euler_gamma_upper: Fraction
    smooth_loss_upper: Fraction
    joint_dyadic_lower: Fraction
    prime_three_lower: Fraction
    complement_margin: Fraction
    preceding_margin: Fraction


def _ceil_div(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    return -((-numerator) // denominator)


def _log_integer_bounds(value: int, terms: int) -> tuple[Fraction, Fraction]:
    """Bound log(value) by truncating its positive atanh series."""

    if value <= 1 or terms < 1:
        raise ValueError("value and terms must exceed one and zero")
    y = Fraction(value - 1, value + 1)
    y_squared = y * y
    power = y
    lower = Fraction(0)
    for index in range(terms):
        lower += 2 * power / (2 * index + 1)
        power *= y_squared
    tail = 2 * power / ((2 * terms + 1) * (1 - y_squared))
    return lower, lower + tail


def _log_rational_bounds(
    value: Fraction, terms: int
) -> tuple[Fraction, Fraction]:
    """Positive atanh-series enclosure of log(value) for value > 1."""

    if value <= 1 or terms < 1:
        raise ValueError("value and terms must exceed one and zero")
    y = (value - 1) / (value + 1)
    y_squared = y * y
    power = y
    lower = Fraction(0)
    for index in range(terms):
        lower += 2 * power / (2 * index + 1)
        power *= y_squared
    tail = 2 * power / ((2 * terms + 1) * (1 - y_squared))
    return lower, lower + tail


def _arctangent_bounds(
    inverse_argument: int, terms: int
) -> tuple[Fraction, Fraction]:
    """Alternating-series enclosure of arctan(1/inverse_argument)."""

    if inverse_argument <= 1 or terms < 1:
        raise ValueError("inverse_argument and terms must exceed one and zero")
    value = Fraction(1, inverse_argument)
    partial = sum(
        (
            (-1 if index % 2 else 1)
            * value ** (2 * index + 1)
            / (2 * index + 1)
            for index in range(terms)
        ),
        Fraction(0),
    )
    next_term = value ** (2 * terms + 1) / (2 * terms + 1)
    if terms % 2 == 0:
        return partial, partial + next_term
    return partial - next_term, partial


def _pi_bounds() -> tuple[Fraction, Fraction]:
    """Machin-formula enclosure of pi."""

    five = _arctangent_bounds(5, 24)
    two_thirty_nine = _arctangent_bounds(239, 6)
    return (
        16 * five[0] - 4 * two_thirty_nine[1],
        16 * five[1] - 4 * two_thirty_nine[0],
    )


def _bernoulli_numbers(maximum: int) -> list[Fraction]:
    numbers: list[Fraction] = []
    work = [Fraction(0) for _ in range(maximum + 1)]
    for order in range(maximum + 1):
        work[order] = Fraction(1, order + 1)
        for index in range(order, 0, -1):
            work[index - 1] = index * (work[index - 1] - work[index])
        numbers.append(work[0])
    if maximum >= 1:
        numbers[1] = Fraction(-1, 2)
    return numbers


def _bernoulli_polynomial(
    order: int, value: Fraction, numbers: list[Fraction]
) -> Fraction:
    return sum(
        (
            Fraction(comb(order, index))
            * numbers[index]
            * value ** (order - index)
            for index in range(order + 1)
        ),
        Fraction(0),
    )


def _smooth_loss_upper(maximum_power: int = 95) -> Fraction:
    """Exact rational version of the registered smooth Schur loss."""

    numbers = _bernoulli_numbers(maximum_power + 1)
    loss = Fraction(1, 24) + Fraction(3, 8)
    for power in range(3, maximum_power + 1):
        order = power + 1
        coefficient = (
            _bernoulli_polynomial(order, Fraction(3, 4), numbers)
            * 2**power
            / factorial(order)
        )
        if power % 2 == 0:
            coefficient -= Fraction(2, 2**power * factorial(power))
        loss += 2 * abs(coefficient) * 2**power / (power + 1)

    ratio = Fraction(2, 3)
    h_tail = Fraction(2, 3) * ratio ** (maximum_power + 1) / (1 - ratio)
    first_even = maximum_power + 1
    if first_even % 2:
        first_even += 1
    first_term = Fraction(2, factorial(first_even))
    next_ratio = Fraction(1, (first_even + 1) * (first_even + 2))
    cosh_tail = first_term / (1 - next_ratio)
    return loss + 2 * (h_tail + cosh_tail)


def _floor_scaled(value: Fraction, scale: int) -> int:
    return value.numerator * scale // value.denominator


def _ceil_scaled(value: Fraction, scale: int) -> int:
    return _ceil_div(value.numerator * scale, value.denominator)


def _minimum_absolute_scaled(lower: int, upper: int) -> int:
    if lower <= 0 <= upper:
        return 0
    return min(abs(lower), abs(upper))


def _potential_series_lower_scaled(
    absolute_lower: int, scale: int, terms: int
) -> int:
    """Lower-bound V(z) in fixed-point arithmetic using its positive series."""

    if not 0 <= absolute_lower < scale or terms < 1:
        raise ValueError("invalid absolute bound or truncation order")
    squared = absolute_lower * absolute_lower // scale
    power = squared
    result = 0
    for index in range(1, terms + 1):
        result += power // (2 * index)
        power = power * squared // scale
    return result


def _leading_minors(
    diagonal_lower: tuple[int, ...],
    edge_upper: tuple[int, ...],
    scale: int,
) -> tuple[Fraction, ...]:
    if len(diagonal_lower) != len(edge_upper) + 1:
        raise ValueError("a path with n vertices must have n-1 edges")
    previous_two = Fraction(1)
    previous = Fraction(diagonal_lower[0], scale) + TARGET
    minors = [previous]
    for diagonal, edge in zip(diagonal_lower[1:], edge_upper):
        current = (
            (Fraction(diagonal, scale) + TARGET) * previous
            - Fraction(edge, scale) ** 2 * previous_two
        )
        minors.append(current)
        previous_two, previous = previous, current
    return tuple(minors)


def _update_minima(
    minima: list[Fraction | None],
    argmin: list[int],
    values: tuple[Fraction, ...],
    cell: int,
) -> None:
    for index, value in enumerate(values):
        if minima[index] is None or value < minima[index]:
            minima[index] = value
            argmin[index] = cell


def certify_rational_joint_five_seven_floor(
    scale_digits: int = 50,
    cells: int = 64,
    logarithm_terms: int = 96,
    potential_terms: int = 80,
) -> RationalJointFiveSevenCertificate:
    """Return an exact rational proof of the registered joint floor."""

    if scale_digits < 10 or cells < 2:
        raise ValueError("the fixed-point scale or cell count is too small")
    scale = 10**scale_digits
    log_five = _log_integer_bounds(5, logarithm_terms)
    log_seven = _log_integer_bounds(7, logarithm_terms)
    l5, u5 = _floor_scaled(log_five[0], scale), _ceil_scaled(
        log_five[1], scale
    )
    l7, u7 = _floor_scaled(log_seven[0], scale), _ceil_scaled(
        log_seven[1], scale
    )

    sqrt_five_lower = isqrt(5 * scale * scale)
    sqrt_seven_lower = isqrt(7 * scale * scale)
    edge_five = _ceil_div(u5 * scale, sqrt_five_lower)
    edge_seven = _ceil_div(u7 * scale, sqrt_seven_lower)

    four_minima: list[Fraction | None] = [None] * 4
    four_argmin = [-1] * 4
    for cell in range(cells):
        left = -scale + cell * (2 * scale - u7) // cells
        right = -scale + _ceil_div(
            (cell + 1) * (2 * scale - l7), cells
        )
        coordinate_intervals = (
            (left + l5, right + u5),
            (left, right),
            (left + l7, right + u7),
            (left + l7 - u5, right + u7 - l5),
        )
        diagonal = tuple(
            _potential_series_lower_scaled(
                _minimum_absolute_scaled(lower, upper),
                scale,
                potential_terms,
            )
            for lower, upper in coordinate_intervals
        )
        minors = _leading_minors(
            diagonal, (edge_five, edge_seven, edge_five), scale
        )
        _update_minima(four_minima, four_argmin, minors, cell)

    left_lower, left_upper = scale - u7, scale - l7
    right_lower = l7 - u5 - scale
    right_upper = u7 - l5 - scale
    if not (right_lower > left_lower and right_upper > left_upper):
        raise ArithmeticError("the rational two-path endpoints did not order")

    two_minima: list[Fraction | None] = [None] * 2
    two_argmin = [-1] * 2
    for cell in range(cells):
        left = (
            (cells - cell) * left_lower + cell * right_lower
        ) // cells
        next_cell = cell + 1
        right = _ceil_div(
            (cells - next_cell) * left_upper
            + next_cell * right_upper,
            cells,
        )
        coordinate_intervals = (
            (left, right),
            (left + l5, right + u5),
        )
        diagonal = tuple(
            _potential_series_lower_scaled(
                _minimum_absolute_scaled(lower, upper),
                scale,
                potential_terms,
            )
            for lower, upper in coordinate_intervals
        )
        minors = _leading_minors(diagonal, (edge_five,), scale)
        _update_minima(two_minima, two_argmin, minors, cell)

    if any(value is None or value <= 0 for value in four_minima + two_minima):
        raise ArithmeticError("the registered rational LDL certificate failed")

    four_exact = tuple(value for value in four_minima if value is not None)
    two_exact = tuple(value for value in two_minima if value is not None)
    return RationalJointFiveSevenCertificate(
        scale_digits=scale_digits,
        cells=cells,
        logarithm_terms=logarithm_terms,
        potential_terms=potential_terms,
        log_five_lower=Fraction(l5, scale),
        log_five_upper=Fraction(u5, scale),
        log_seven_lower=Fraction(l7, scale),
        log_seven_upper=Fraction(u7, scale),
        edge_five_upper=Fraction(edge_five, scale),
        edge_seven_upper=Fraction(edge_seven, scale),
        four_path_minor_lowers=four_exact,
        four_path_argmin_cells=tuple(four_argmin),
        two_path_minor_lowers=two_exact,
        two_path_argmin_cells=tuple(two_argmin),
    )


def certify_rational_support_one_tail(
    local_degree: int = 58,
) -> RationalSupportOneTailCertificate:
    """Certify the support-one complement from degree 58 with rationals."""

    if local_degree != 58:
        raise ValueError("the registered rational certificate is for degree 58")
    joint = certify_rational_joint_five_seven_floor()

    pi_bounds = _pi_bounds()
    log_two_pi = _log_rational_bounds(2 * pi_bounds[1], 160)
    log_ten = _log_integer_bounds(10, 160)
    harmonic_100 = sum(
        (Fraction(1, degree) for degree in range(1, 101)), Fraction(0)
    )
    # The elementary Euler--Maclaurin inequality
    # 1/(2n+1) < H_n - log(n) - gamma gives this upper bound at n=100.
    gamma_upper = harmonic_100 - 2 * log_ten[0] - Fraction(1, 201)

    scale = 10**40
    sqrt_three_lower = Fraction(isqrt(3 * scale * scale), scale)
    sqrt_seventeen_upper = Fraction(
        isqrt(17 * scale * scale) + 1, scale
    )
    log_two = _log_integer_bounds(2, 160)
    log_three = _log_integer_bounds(3, 160)
    joint_dyadic = -log_two[1] * (1 + sqrt_seventeen_upper) / 4
    prime_three = -log_three[1] / sqrt_three_lower
    smooth = _smooth_loss_upper(95)
    harmonic = sum(
        (Fraction(1, degree) for degree in range(1, local_degree + 1)),
        Fraction(0),
    )
    bounded = (
        -log_two_pi[1]
        - gamma_upper
        - smooth
        + joint_dyadic
        + prime_three
        + joint.certified_floor
    )
    margin = harmonic + bounded
    preceding = harmonic - Fraction(1, local_degree) + bounded
    if margin <= 0 or preceding >= 0:
        raise ArithmeticError("the rational degree-58 tail gate did not close")

    return RationalSupportOneTailCertificate(
        joint_five_seven=joint,
        local_degree=local_degree,
        harmonic_floor=harmonic,
        log_two_pi_upper=log_two_pi[1],
        euler_gamma_upper=gamma_upper,
        smooth_loss_upper=smooth,
        joint_dyadic_lower=joint_dyadic,
        prime_three_lower=prime_three,
        complement_margin=margin,
        preceding_margin=preceding,
    )


def main() -> None:
    certificate = certify_rational_joint_five_seven_floor()
    print("floor", certificate.certified_floor)
    print("four minors", [float(value) for value in certificate.four_path_minor_lowers])
    print("four cells", certificate.four_path_argmin_cells)
    print("two minors", [float(value) for value in certificate.two_path_minor_lowers])
    print("two cells", certificate.two_path_argmin_cells)
    tail = certify_rational_support_one_tail()
    print("degree-58 tail margin", float(tail.complement_margin))
    print("degree-57 margin", float(tail.preceding_margin))


if __name__ == "__main__":
    main()

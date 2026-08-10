"""Exact Jacobi connection formula for the prime-dilation bands.

For the monic shifted Jacobi basis p_n used in ``euler-axis-pick.md``, this
module checks that <e_m, D_u e_n> is one Jacobi polynomial rather than the
alternating sum in (E108).  It also audits the rational inequalities in the
Gershgorin window where that polynomial has no zero on u in [0, 1/2].

All coefficient checks use ``Fraction``.  No zero data or RH assumption is
used.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, factorial


def rising(value: int, length: int) -> int:
    """Integer rising factorial."""

    result = 1
    for offset in range(length):
        result *= value + offset
    return result


def monic_coefficient(n: int, k: int) -> Fraction:
    """Coefficient a_(n,k) in (E106)."""

    return Fraction(
        (-1) ** (n - k) * comb(n - 1, k - 1) * factorial(n + k),
        factorial(n - 1) * factorial(k + 1) * comb(2 * n, n - 1),
    )


def projection_coefficient(m: int, k: int) -> Fraction:
    """Projection coefficient r_(m,k) in (E107)."""

    if k < m:
        return Fraction(0)
    return Fraction(
        factorial(2 * m + 1) * factorial(k + 1) * comb(k - 1, m - 1),
        factorial(m + 1) * factorial(k + m + 1),
    )


def direct_dilation_polynomial(m: int, n: int) -> list[Fraction]:
    """Coefficients of the unnormalized connection <p_m,D_u p_n>/h_m."""

    assert 1 <= m < n
    coefficients = [Fraction(0)] * (n + 1)
    for k in range(m, n + 1):
        coefficients[k] = monic_coefficient(n, k) * projection_coefficient(m, k)
    return coefficients


def hypergeometric_dilation_polynomial(m: int, n: int) -> list[Fraction]:
    """Same polynomial as one terminating 2F1 in (E126)."""

    assert 1 <= m < n
    gap = n - m
    coefficients = [Fraction(0)] * (n + 1)
    leading = monic_coefficient(n, m)
    for j in range(gap + 1):
        # (-gap)_j (m+n+1)_j / ((2m+2)_j j!)
        numerator = (-1) ** j * factorial(gap) // factorial(gap - j)
        numerator *= rising(m + n + 1, j)
        denominator = rising(2 * m + 2, j) * factorial(j)
        coefficients[m + j] = leading * Fraction(numerator, denominator)
    return coefficients


def factored_dilation_polynomial(m: int, n: int) -> list[Fraction]:
    """Coefficient form of u^m(1-u) times the Jacobi factor in (E127)."""

    assert 1 <= m < n
    gap = n - m
    degree = gap - 1
    leading = monic_coefficient(n, m)
    # The normalized Jacobi factor is
    # 2F1(1-gap, gap+2m+2; 2m+2; u).
    core = [Fraction(0)] * (degree + 1)
    for j in range(degree + 1):
        numerator = (-1) ** j * factorial(degree) // factorial(degree - j)
        numerator *= rising(gap + 2 * m + 2, j)
        denominator = rising(2 * m + 2, j) * factorial(j)
        core[j] = Fraction(numerator, denominator)
    coefficients = [Fraction(0)] * (n + 1)
    for j, coefficient in enumerate(core):
        coefficients[m + j] += leading * coefficient
        coefficients[m + j + 1] -= leading * coefficient
    return coefficients


def gershgorin_bounds(m: int, gap: int) -> tuple[Fraction, Fraction]:
    """Lower diagonal and upper row-radius bounds for the Jacobi zero matrix."""

    assert gap >= 2
    alpha = 2 * m + 1
    diagonal_lower = Fraction(alpha * alpha - 1, (alpha + 2 * gap) ** 2)
    row_radius_upper = Fraction(4 * gap * (alpha + gap), alpha * alpha)
    return diagonal_lower, row_radius_upper


def in_constant_sign_window(m: int, gap: int) -> bool:
    """Return the sufficient window alpha >= 16 gap from (E129)."""

    return 2 * m + 1 >= 16 * gap


def evaluate(polynomial: list[Fraction], value: Fraction) -> Fraction:
    """Evaluate an ascending coefficient list exactly."""

    result = Fraction(0)
    for coefficient in reversed(polynomial):
        result = result * value + coefficient
    return result


def divide_by_one_minus_u(polynomial: list[Fraction]) -> list[Fraction]:
    """Return q when ``polynomial = (1-u) q`` exactly."""

    degree = len(polynomial) - 1
    quotient = [Fraction(0)] * degree
    quotient[-1] = -polynomial[-1]
    for k in range(degree - 1, 0, -1):
        quotient[k - 1] = quotient[k] - polynomial[k]
    assert polynomial[0] == quotient[0]
    return quotient


def divide_by_one_plus_u(
    polynomial: list[Fraction],
) -> tuple[list[Fraction], Fraction]:
    """Exact quotient and remainder for division by ``1+u``."""

    degree = len(polynomial) - 1
    quotient = [Fraction(0)] * degree
    quotient[-1] = polynomial[-1]
    for k in range(degree - 1, 0, -1):
        quotient[k - 1] = polynomial[k] - quotient[k]
    remainder = polynomial[0] - quotient[0]
    return quotient, remainder


def archimedean_integral_symbolic(
    dilation: list[Fraction],
) -> tuple[Fraction, Fraction]:
    """Return rational and log(2) parts of integral omega(u) Q(u) du.

    Here omega=(1-u^2-u^3)/(u(1-u^2)).  The factors u and 1-u in Q
    cancel its endpoint singularities.  The remaining denominator is 1+u,
    so polynomial division gives an exact rational plus a rational multiple
    of log(2).
    """

    residual = divide_by_one_minus_u(dilation)
    numerator = [Fraction(0)] * (len(residual) + 3)
    for power, coefficient in enumerate(residual):
        numerator[power] += coefficient
        numerator[power + 2] -= coefficient
        numerator[power + 3] -= coefficient
    assert numerator[0] == 0
    after_u = numerator[1:]
    quotient, remainder = divide_by_one_plus_u(after_u)
    rational = sum(
        (coefficient / (power + 1) for power, coefficient in enumerate(quotient)),
        Fraction(0),
    )
    return rational, remainder


def harmonic(index: int) -> Fraction:
    """Exact harmonic number H_index."""

    return sum((Fraction(1, k) for k in range(1, index + 1)), Fraction(0))


def archimedean_eigenvalue_symbolic(index: int) -> tuple[Fraction, Fraction]:
    """Nonconstant rational and log(2) parts of a_index in (E92)."""

    rational = Fraction(1, index) + Fraction(1, index + 1)
    if index % 2:
        rational += harmonic((index - 1) // 2) / 2
        return rational, Fraction(0)
    rational += sum(
        (Fraction(1, 2 * k - 1) for k in range(1, index // 2 + 1)),
        Fraction(0),
    )
    return rational, Fraction(-1)


def archimedean_band_symbolic(m: int, n: int) -> tuple[Fraction, Fraction]:
    """Direct symbolic sum of the archimedean eigenvalues in one band."""

    dilation = direct_dilation_polynomial(m, n)
    rational = Fraction(0)
    log_two = Fraction(0)
    for index, coefficient in enumerate(dilation):
        if not coefficient:
            continue
        eigen_rational, eigen_log_two = archimedean_eigenvalue_symbolic(index)
        rational += coefficient * eigen_rational
        log_two += coefficient * eigen_log_two
    return rational, log_two


def main() -> None:
    checks = 0
    sign_checks = 0
    for n in range(2, 15):
        for m in range(1, n):
            direct = direct_dilation_polynomial(m, n)
            assert direct == hypergeometric_dilation_polynomial(m, n)
            assert direct == factored_dilation_polynomial(m, n)
            assert archimedean_integral_symbolic(direct) == (
                archimedean_band_symbolic(m, n)
            )
            checks += 1
            gap = n - m
            if in_constant_sign_window(m, gap):
                if gap >= 2:
                    diagonal, radius = gershgorin_bounds(m, gap)
                    assert diagonal > Fraction(3, 4)
                    assert radius <= Fraction(17, 64)
                expected_sign = (-1) ** gap
                for prime in (2, 3, 5, 7, 11):
                    value = evaluate(direct, Fraction(1, prime))
                    assert expected_sign * value > 0
                    sign_checks += 1
    # Audit the first nontrivial point at the registered tail cutoff.
    diagonal, radius = gershgorin_bounds(232, 20)
    assert in_constant_sign_window(232, 20)
    assert diagonal > Fraction(3, 4)
    assert radius < Fraction(17, 64)
    print(f"exact_connection_checks={checks}")
    print(f"exact_prime_sign_checks={sign_checks}")
    print(f"tail_diagonal_lower={float(diagonal):.12f}")
    print(f"tail_row_radius_upper={float(radius):.12f}")


if __name__ == "__main__":
    main()

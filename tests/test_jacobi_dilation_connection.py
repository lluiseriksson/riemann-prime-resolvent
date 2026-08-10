from fractions import Fraction

from experiments.theta_pencil.jacobi_dilation_connection import (
    archimedean_band_symbolic,
    archimedean_integral_symbolic,
    direct_dilation_polynomial,
    evaluate,
    factored_dilation_polynomial,
    gershgorin_bounds,
    hypergeometric_dilation_polynomial,
    in_constant_sign_window,
)


def test_connection_formula_exactly() -> None:
    for n in range(2, 11):
        for m in range(1, n):
            direct = direct_dilation_polynomial(m, n)
            assert direct == hypergeometric_dilation_polynomial(m, n)
            assert direct == factored_dilation_polynomial(m, n)
            assert archimedean_integral_symbolic(direct) == (
                archimedean_band_symbolic(m, n)
            )


def test_prime_dilations_have_constant_sign_in_window() -> None:
    for m, gap in ((32, 4), (64, 8), (232, 20)):
        assert in_constant_sign_window(m, gap)
        polynomial = direct_dilation_polynomial(m, m + gap)
        for prime in (2, 3, 5, 7):
            assert (-1) ** gap * evaluate(polynomial, Fraction(1, prime)) > 0


def test_gershgorin_constants_are_separated() -> None:
    diagonal, radius = gershgorin_bounds(232, 20)
    assert diagonal > Fraction(3, 4)
    assert radius < Fraction(17, 64)

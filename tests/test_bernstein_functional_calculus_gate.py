from decimal import Decimal

from experiments.theta_pencil.bernstein_functional_calculus_gate import (
    bernstein_certificate,
    logarithmic_tail_upper_bound,
    primes_through,
)


def test_sieve_small_values() -> None:
    assert primes_through(20) == [2, 3, 5, 7, 11, 13, 17, 19]


def test_tail_formula_is_positive_and_small() -> None:
    tail = logarithmic_tail_upper_bound(100_000)
    assert Decimal(0) < tail < Decimal("1.1e-6")


def test_third_derivative_obstructs_bernstein_class() -> None:
    certificate = bernstein_certificate()
    assert Decimal(certificate.l_third_upper_bound) < Decimal("-0.00034")

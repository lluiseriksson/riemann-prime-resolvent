from fractions import Fraction

from experiments.theta_pencil.jacobi_local_band_bound import (
    MAX_GAP,
    TAIL_START,
    closed_j_one,
    closed_j_zero_ratio,
    crude_prime_upper,
    even_archimedean_rational_upper,
    jacobi_moment,
    odd_upper_polynomial,
)


def test_closed_moment_formulas() -> None:
    for m in (4, 11, 32):
        for gap in range(1, 12):
            j_one = jacobi_moment(m, gap, 1)
            assert j_one == closed_j_one(m, gap)
            assert jacobi_moment(m, gap, 0) == (
                j_one * closed_j_zero_ratio(m, gap)
            )


def test_tail_archimedean_bounds_have_registered_margin() -> None:
    for gap in range(1, MAX_GAP + 1, 2):
        assert odd_upper_polynomial(TAIL_START, gap) > 0
    for gap in range(2, MAX_GAP + 1, 2):
        assert even_archimedean_rational_upper(TAIL_START, gap) < Fraction(1, 50)


def test_prime_remainder_is_below_registered_budget() -> None:
    bounds = [
        crude_prime_upper(TAIL_START, gap)
        for gap in range(1, MAX_GAP + 1)
    ]
    assert max(bounds) < Fraction(1, 10**20)

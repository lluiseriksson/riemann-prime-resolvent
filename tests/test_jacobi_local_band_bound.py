from fractions import Fraction

from experiments.theta_pencil.jacobi_local_band_bound import (
    EXTENDED_GAP,
    MAX_GAP,
    PFAFF_EXTENDED_GAP,
    TAIL_START,
    binomial_one_step_ratio,
    closed_j_one,
    closed_j_zero_ratio,
    crude_prime_upper,
    even_archimedean_rational_upper,
    even_archimedean_crude_upper,
    jacobi_moment,
    odd_upper_polynomial,
    odd_archimedean_crude_upper,
    normalized_jacobi_coefficients,
    pfaff_hypergeometric_ratio,
    pfaff_hypergeometric_upper,
    pfaff_mangoldt_moment_upper,
    pfaff_prime_upper,
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


def test_extended_width_45_budget() -> None:
    for gap in range(1, EXTENDED_GAP + 1, 2):
        assert odd_archimedean_crude_upper(TAIL_START, gap) < Fraction(21, 20)
    for gap in range(2, EXTENDED_GAP + 1, 2):
        assert even_archimedean_crude_upper(TAIL_START, gap) < Fraction(1, 20)
    prime_bounds = [
        crude_prime_upper(TAIL_START, gap)
        for gap in range(1, EXTENDED_GAP + 1)
    ]
    assert max(prime_bounds) < Fraction(1, 4)


def test_pfaff_hypergeometric_bound_exactly() -> None:
    for m in (4, 11):
        for gap in range(1, 9):
            coefficients = normalized_jacobi_coefficients(m, gap)
            for denominator in (2, 3, 5):
                value = sum(
                    (
                        coefficient * Fraction(1, denominator) ** power
                        for power, coefficient in enumerate(coefficients)
                    ),
                    Fraction(0),
                )
                assert abs(value) <= pfaff_hypergeometric_upper(
                    m,
                    gap,
                    denominator,
                )


def test_pfaff_width_68_budget_and_uniformity() -> None:
    odd_bounds = []
    even_bounds = []
    for gap in range(1, PFAFF_EXTENDED_GAP + 1):
        assert binomial_one_step_ratio(TAIL_START, gap) < Fraction(3, 2)
        assert pfaff_hypergeometric_ratio(TAIL_START + 1, gap) <= (
            pfaff_hypergeometric_ratio(TAIL_START, gap)
        )
        assert 2 * pfaff_mangoldt_moment_upper(TAIL_START + 1, gap) < (
            pfaff_mangoldt_moment_upper(TAIL_START, gap)
        )
        assert pfaff_prime_upper(TAIL_START + 1, gap) < (
            pfaff_prime_upper(TAIL_START, gap)
        )
        if gap % 2:
            assert odd_archimedean_crude_upper(TAIL_START, gap) < Fraction(
                21,
                20,
            )
            odd_bounds.append(pfaff_prime_upper(TAIL_START, gap))
        else:
            assert even_archimedean_crude_upper(TAIL_START, gap) < Fraction(
                1,
                20,
            )
            even_bounds.append(pfaff_prime_upper(TAIL_START, gap))
    assert max(odd_bounds) < Fraction(1, 3)
    assert max(even_bounds) < Fraction(8, 5)
    assert pfaff_prime_upper(TAIL_START, PFAFF_EXTENDED_GAP + 1) > 7

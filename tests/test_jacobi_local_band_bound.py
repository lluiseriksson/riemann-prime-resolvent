from fractions import Fraction

from experiments.theta_pencil.jacobi_local_band_bound import (
    CONTOUR_EXTENDED_GAP,
    CONTOUR_NORM_UPPER,
    CONTOUR_RADIUS,
    EXTENDED_GAP,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    MAX_GAP,
    PFAFF_EXTENDED_GAP,
    SQRT_TWO_UPPER,
    TAIL_START,
    binomial_one_step_ratio,
    closed_j_one,
    closed_j_zero_ratio,
    contour_prime_upper,
    contour_two_dilation_upper,
    crude_prime_upper,
    even_archimedean_rational_upper,
    even_archimedean_crude_upper,
    exact_two_dilation_square,
    jacobi_moment,
    odd_upper_polynomial,
    odd_archimedean_crude_upper,
    normalized_jacobi_coefficients,
    pfaff_hypergeometric_ratio,
    pfaff_hypergeometric_upper,
    pfaff_mangoldt_moment_upper,
    pfaff_mangoldt_tail_upper,
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


def test_contour_width_85_budget_and_uniformity() -> None:
    assert LAMBDA_LOWER**2 < Fraction(1, 2) < LAMBDA_UPPER**2
    assert SQRT_TWO_UPPER**2 > 2
    assert LAMBDA_UPPER < CONTOUR_RADIUS < 1
    for m, gap in (
        (TAIL_START, 2),
        (TAIL_START, 8),
        (TAIL_START, 68),
        (TAIL_START, 85),
    ):
        assert exact_two_dilation_square(m, gap) < (
            contour_two_dilation_upper(m, gap) ** 2
        )
    totals = []
    for gap in range(1, CONTOUR_EXTENDED_GAP + 1):
        norm_square = Fraction(
            2 * TAIL_START + 2 * gap + 1,
            2 * TAIL_START + 1,
        )
        assert norm_square < CONTOUR_NORM_UPPER**2
        assert 3 * pfaff_mangoldt_tail_upper(TAIL_START + 1, gap) < (
            pfaff_mangoldt_tail_upper(TAIL_START, gap)
        )
        assert contour_prime_upper(TAIL_START + 1, gap) < (
            contour_prime_upper(TAIL_START, gap)
        )
        archimedean = (
            odd_archimedean_crude_upper(TAIL_START, gap)
            if gap % 2
            else even_archimedean_crude_upper(TAIL_START, gap)
        )
        totals.append(contour_prime_upper(TAIL_START, gap) + archimedean)
    assert max(totals) < Fraction(17, 10)
    assert totals.index(max(totals)) + 1 == 85
    assert (
        contour_prime_upper(TAIL_START, CONTOUR_EXTENDED_GAP + 1)
        + even_archimedean_crude_upper(
            TAIL_START,
            CONTOUR_EXTENDED_GAP + 1,
        )
        > 2
    )

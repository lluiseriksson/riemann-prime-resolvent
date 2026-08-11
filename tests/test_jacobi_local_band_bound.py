from fractions import Fraction

from experiments.theta_pencil.jacobi_local_band_bound import (
    BESSEL_EXTENDED_GAP,
    ROBUST_TRIPLE_DIAMETER,
    THREE_SPLIT_EXTENDED_GAP,
    CONTOUR_EXTENDED_GAP,
    CONTOUR_NORM_UPPER,
    CONTOUR_RADIUS,
    EXTENDED_GAP,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    L2_EXTENDED_GAP,
    L1_EXTENDED_GAP,
    L1_LAMBDA_LOWER,
    L1_LAMBDA_UPPER,
    L1_SQRT_TWO_UPPER,
    MAX_GAP,
    PFAFF_EXTENDED_GAP,
    SQRT_TWO_UPPER,
    SPLIT_EXTENDED_GAP,
    TAIL_DIAGONAL_LOWER,
    TAIL_START,
    binomial_one_step_ratio,
    bessel_extended_prime_upper,
    closed_j_one,
    closed_j_zero_ratio,
    contour_prime_upper,
    contour_two_dilation_upper,
    contour_two_dilation_l2_upper,
    contour_two_dilation_l1_upper,
    contour_two_dilation_split_upper,
    contour_two_dilation_bessel_upper,
    contour_three_dilation_bessel_upper,
    crude_prime_upper,
    even_archimedean_rational_upper,
    even_archimedean_crude_upper,
    exact_two_dilation_square,
    exact_dilation_square,
    jacobi_moment,
    l2_extended_prime_upper,
    l2_factor_upper,
    l1_extended_prime_upper,
    l1_factor_upper,
    split_extended_prime_upper,
    split_l1_factor_upper,
    rational_bessel_factor_upper,
    robust_three_by_three_determinant_lower,
    three_split_prime_upper,
    odd_upper_polynomial,
    odd_archimedean_crude_upper,
    normalized_jacobi_coefficients,
    pfaff_hypergeometric_ratio,
    pfaff_hypergeometric_upper,
    pfaff_mangoldt_moment_upper,
    pfaff_mangoldt_tail_upper,
    pfaff_prime_upper,
    tail_entry_abs_upper,
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


def test_contour_width_92_budget_and_uniformity() -> None:
    assert LAMBDA_LOWER**2 < Fraction(1, 2) < LAMBDA_UPPER**2
    assert SQRT_TWO_UPPER**2 > 2
    assert LAMBDA_UPPER < CONTOUR_RADIUS < 1
    for m, gap in (
        (TAIL_START, 2),
        (TAIL_START, 8),
        (TAIL_START, 68),
        (TAIL_START, 92),
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
    assert max(totals) < Fraction(9, 5)
    assert totals.index(max(totals)) + 1 == 92
    assert (
        contour_prime_upper(TAIL_START, CONTOUR_EXTENDED_GAP + 1)
        + odd_archimedean_crude_upper(
            TAIL_START,
            CONTOUR_EXTENDED_GAP + 1,
        )
        > 2
    )


def test_l2_width_96_budget_and_uniformity() -> None:
    totals = []
    for gap in range(1, L2_EXTENDED_GAP + 1):
        archimedean = (
            odd_archimedean_crude_upper(TAIL_START, gap)
            if gap % 2
            else even_archimedean_crude_upper(TAIL_START, gap)
        )
        totals.append(
            l2_extended_prime_upper(TAIL_START, gap) + archimedean
        )
        if gap > CONTOUR_EXTENDED_GAP:
            assert l2_factor_upper(gap) < 1
            assert exact_two_dilation_square(TAIL_START, gap) < (
                contour_two_dilation_l2_upper(TAIL_START, gap) ** 2
            )
            assert l2_extended_prime_upper(TAIL_START + 1, gap) < (
                l2_extended_prime_upper(TAIL_START, gap)
            )
    assert max(totals) < Fraction(9, 5)
    assert totals.index(max(totals)) + 1 == 92
    assert (
        l2_extended_prime_upper(TAIL_START, L2_EXTENDED_GAP + 1)
        + odd_archimedean_crude_upper(TAIL_START, L2_EXTENDED_GAP + 1)
        > 2
    )


def test_l1_width_101_budget_and_uniformity() -> None:
    assert L1_LAMBDA_LOWER**2 < Fraction(1, 2) < L1_LAMBDA_UPPER**2
    assert L1_SQRT_TWO_UPPER**2 > 2
    totals = []
    for gap in range(1, L1_EXTENDED_GAP + 1):
        archimedean = (
            odd_archimedean_crude_upper(TAIL_START, gap)
            if gap % 2
            else even_archimedean_crude_upper(TAIL_START, gap)
        )
        totals.append(
            l1_extended_prime_upper(TAIL_START, gap) + archimedean
        )
        if gap > L2_EXTENDED_GAP:
            assert l1_factor_upper(gap) < 1
            assert exact_two_dilation_square(TAIL_START, gap) < (
                contour_two_dilation_l1_upper(TAIL_START, gap) ** 2
            )
            assert l1_extended_prime_upper(TAIL_START + 1, gap) < (
                l1_extended_prime_upper(TAIL_START, gap)
            )
    assert max(totals) < Fraction(9, 5)
    assert totals.index(max(totals)) + 1 == 101
    assert (
        l1_extended_prime_upper(TAIL_START, L1_EXTENDED_GAP + 1)
        + even_archimedean_crude_upper(TAIL_START, L1_EXTENDED_GAP + 1)
        > Fraction(9, 5)
    )


def test_split_width_106_budget_and_uniformity() -> None:
    totals = []
    for gap in range(1, SPLIT_EXTENDED_GAP + 1):
        archimedean = (
            odd_archimedean_crude_upper(TAIL_START, gap)
            if gap % 2
            else even_archimedean_crude_upper(TAIL_START, gap)
        )
        totals.append(
            split_extended_prime_upper(TAIL_START, gap) + archimedean
        )
        if gap > L1_EXTENDED_GAP:
            assert split_l1_factor_upper(gap) < 1
            assert exact_two_dilation_square(TAIL_START, gap) < (
                contour_two_dilation_split_upper(TAIL_START, gap) ** 2
            )
            assert split_extended_prime_upper(TAIL_START + 1, gap) < (
                split_extended_prime_upper(TAIL_START, gap)
            )
    assert max(totals) < Fraction(9, 5)
    assert totals.index(max(totals)) + 1 == 106
    assert (
        split_extended_prime_upper(TAIL_START, SPLIT_EXTENDED_GAP + 1)
        + odd_archimedean_crude_upper(TAIL_START, SPLIT_EXTENDED_GAP + 1)
        > Fraction(9, 5)
    )


def test_bessel_width_109_budget_and_uniformity() -> None:
    totals = []
    for gap in range(1, BESSEL_EXTENDED_GAP + 1):
        archimedean = (
            odd_archimedean_crude_upper(TAIL_START, gap)
            if gap % 2
            else even_archimedean_crude_upper(TAIL_START, gap)
        )
        totals.append(
            bessel_extended_prime_upper(TAIL_START, gap) + archimedean
        )
        if gap > SPLIT_EXTENDED_GAP:
            assert rational_bessel_factor_upper(gap) < 1
            assert exact_two_dilation_square(TAIL_START, gap) < (
                contour_two_dilation_bessel_upper(TAIL_START, gap) ** 2
            )
            assert bessel_extended_prime_upper(TAIL_START + 1, gap) < (
                bessel_extended_prime_upper(TAIL_START, gap)
            )
    assert max(totals) < Fraction(9, 5)
    assert totals.index(max(totals)) + 1 == 106
    assert (
        bessel_extended_prime_upper(TAIL_START, BESSEL_EXTENDED_GAP + 1)
        + even_archimedean_crude_upper(TAIL_START, BESSEL_EXTENDED_GAP + 1)
        > Fraction(9, 5)
    )


def test_three_split_contours_through_113() -> None:
    for gap in range(BESSEL_EXTENDED_GAP + 2, THREE_SPLIT_EXTENDED_GAP + 1):
        assert exact_two_dilation_square(TAIL_START, gap) < (
            contour_two_dilation_bessel_upper(TAIL_START, gap) ** 2
        )
        assert exact_dilation_square(TAIL_START, gap, 3) < (
            contour_three_dilation_bessel_upper(TAIL_START, gap) ** 2
        )
        assert three_split_prime_upper(TAIL_START + 1, gap) < (
            three_split_prime_upper(TAIL_START, gap)
        )


def test_robust_triple_width_113() -> None:
    entry_bounds = {
        gap: tail_entry_abs_upper(TAIL_START, gap)
        for gap in range(1, ROBUST_TRIPLE_DIAMETER + 1)
    }
    assert max(entry_bounds.values()) < TAIL_DIAGONAL_LOWER
    certificates = []
    for diameter in range(2, ROBUST_TRIPLE_DIAMETER + 1):
        for left_gap in range(1, diameter):
            certificate = robust_three_by_three_determinant_lower(
                left_gap,
                diameter - left_gap,
            )
            assert certificate > 0
            certificates.append((certificate, diameter, left_gap))
    certificate, diameter, left_gap = min(certificates)
    assert diameter == ROBUST_TRIPLE_DIAMETER
    assert left_gap in (1, ROBUST_TRIPLE_DIAMETER - 1)
    assert certificate > 3

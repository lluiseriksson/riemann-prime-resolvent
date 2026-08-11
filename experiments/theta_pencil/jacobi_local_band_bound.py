"""Exact audit for the local Jacobi tail bounds.

This module checks the terminating beta-sum identities and the rational
inequalities used to control the tail bands.  It also implements the Pfaff
majorant which extends the three-point positivity theorem from width 45 to
width 68.  The infinite-in-m part is analytic; the finite checks below audit
its exact cutoff constants without zero data or floating-point quadrature.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, factorial

try:
    from experiments.theta_pencil.jacobi_dilation_connection import rising
except ModuleNotFoundError:  # Direct ``python path/to/script.py`` execution.
    from jacobi_dilation_connection import rising


TAIL_START = 232
MAX_GAP = 29
EXTENDED_GAP = 45
PFAFF_EXTENDED_GAP = 68
PFAFF_NORM_UPPER = Fraction(8, 7)
CONTOUR_EXTENDED_GAP = 92
CONTOUR_RADIUS = Fraction(89, 100)
CONTOUR_RADIUS_OVERRIDES = {
    86: Fraction(9, 10),
    87: Fraction(181, 200),
    88: Fraction(91, 100),
    89: Fraction(229, 250),
    90: Fraction(461, 500),
    91: Fraction(116, 125),
    92: Fraction(187, 200),
    93: Fraction(943, 1000),
}
LAMBDA_LOWER = Fraction(7071, 10_000)
LAMBDA_UPPER = Fraction(7072, 10_000)
SQRT_TWO_UPPER = Fraction(14_143, 10_000)
CONTOUR_NORM_UPPER = Fraction(6, 5)
L2_EXTENDED_GAP = 96
L2_RADIUS_OVERRIDES = {
    93: Fraction(469, 500),
    94: Fraction(473, 500),
    95: Fraction(477, 500),
    96: Fraction(963, 1000),
    97: Fraction(971, 1000),
}
L2_FACTOR_UPPERS = {
    93: Fraction(179, 500),
    94: Fraction(183, 500),
    95: Fraction(47, 125),
    96: Fraction(49, 125),
    97: Fraction(103, 250),
}
L1_EXTENDED_GAP = 101
L1_LAMBDA_LOWER = Fraction(70_710_678, 100_000_000)
L1_LAMBDA_UPPER = Fraction(70_710_679, 100_000_000)
L1_SQRT_TWO_UPPER = Fraction(141_421_357, 100_000_000)
L1_RADIUS_OVERRIDES = {
    97: Fraction(481, 500),
    98: Fraction(969, 1000),
    99: Fraction(487, 500),
    100: Fraction(489, 500),
    101: Fraction(491, 500),
    102: Fraction(9841, 10_000),
}
L1_FACTOR_UPPERS = {
    97: Fraction(2133, 10_000),
    98: Fraction(2311, 10_000),
    99: Fraction(31, 125),
    100: Fraction(166, 625),
    101: Fraction(2893, 10_000),
    102: Fraction(3047, 10_000),
}
SPLIT_EXTENDED_GAP = 106
SPLIT_NORM_UPPER = Fraction(61, 50)
SPLIT_RADIUS_OVERRIDES = {
    102: Fraction(491, 500),
    103: Fraction(123, 125),
    104: Fraction(197, 200),
    105: Fraction(493, 500),
    106: Fraction(987, 1000),
    107: Fraction(247, 250),
}
SPLIT_MAIN_FACTOR_UPPERS = {
    102: Fraction(509, 2500),
    103: Fraction(1069, 5000),
    104: Fraction(137, 625),
    105: Fraction(2253, 10_000),
    106: Fraction(2321, 10_000),
    107: Fraction(1199, 5000),
}
BESSEL_EXTENDED_GAP = 109
BESSEL_RADIUS_OVERRIDES = {
    107: Fraction(9897, 10_000),
    108: Fraction(619, 625),
    109: Fraction(9911, 10_000),
    110: Fraction(2479, 2500),
}
BESSEL_I0_ORDER = 16
BESSEL_EXP_ORDER = 24


def beta_integer(left: int, right: int) -> Fraction:
    """Exact beta(left,right) for positive integers."""

    return Fraction(
        factorial(left - 1) * factorial(right - 1),
        factorial(left + right - 1),
    )


def normalized_jacobi_coefficients(m: int, gap: int) -> list[Fraction]:
    """Coefficients of H_(m,d)=2F1(1-d,2m+d+2;2m+2;u)."""

    degree = gap - 1
    return [
        Fraction(
            (-1) ** j * comb(degree, j) * rising(2 * m + gap + 2, j),
            rising(2 * m + 2, j),
        )
        for j in range(degree + 1)
    ]


def jacobi_moment(m: int, gap: int, order: int) -> Fraction:
    """Exact J_order = integral u^(m-1)(1-u)^order H_(m,d)(u) du."""

    return sum(
        (
            coefficient * beta_integer(m + power, order + 1)
            for power, coefficient in enumerate(
                normalized_jacobi_coefficients(m, gap)
            )
        ),
        Fraction(0),
    )


def closed_j_one(m: int, gap: int) -> Fraction:
    """Saalschutz evaluation of J_1."""

    return Fraction(
        factorial(gap) * factorial(2 * m + 1),
        m * (m + 1) * factorial(2 * m + gap),
    )


def closed_j_zero_ratio(m: int, gap: int) -> Fraction:
    """Closed parity formula for J_0/J_1."""

    if gap % 2 == 0:
        return Fraction(1)
    half = (gap + 1) // 2
    center = m + half
    return Fraction(center * center + half * (half - 1), gap * center)


def odd_upper_polynomial(m: int, gap: int) -> int:
    """Positive numerator proving the odd-band archimedean bound < 1/d."""

    assert gap % 2 == 1
    return (
        14 * gap * m * m
        + 7 * gap * (gap + 1) * m
        - (gap - 1) * (gap + 1) ** 2
    )


def even_archimedean_rational_upper(m: int, gap: int) -> Fraction:
    """Rational majorant for the even-band archimedean contribution."""

    assert gap % 2 == 0
    # sqrt((2m+1)(2m+2d+1)) <= 2m+d+1.
    return Fraction(15 * (2 * m + gap + 1), 8 * m * (m + 1))


def odd_archimedean_crude_upper(m: int, gap: int) -> Fraction:
    """Monotone-in-m absolute upper bound for an odd archimedean band."""

    assert gap % 2 == 1
    half = (gap + 1) // 2
    correction = half * (half - 1)
    norm_upper = Fraction(2, m) + Fraction(gap + 1, m * m)
    bracket_upper = (
        Fraction(m, 2 * gap)
        + Fraction(half, 2 * gap)
        + Fraction(correction, 2 * gap * m)
        + Fraction(13, 4)
    )
    return norm_upper * bracket_upper


def even_archimedean_crude_upper(m: int, gap: int) -> Fraction:
    """Monotone-in-m absolute upper bound for an even archimedean band."""

    assert gap % 2 == 0
    norm_upper = Fraction(2, m) + Fraction(gap + 1, m * m)
    return Fraction(15, 8) * norm_upper


def crude_prime_upper(m: int, gap: int) -> Fraction:
    """Elementary prime-band bound using e<3 and Lambda(r)<=log(r)."""

    # binom(2m+d,d) <= (e(2m+d)/d)^d, the square-root norm ratio is <2,
    # and the entire Mangoldt moment is <2^-m.
    return (
        Fraction(2, 2**m)
        * Fraction(3 * (2 * m + gap), gap) ** gap
    )


def pfaff_hypergeometric_ratio(m: int, gap: int) -> Fraction:
    """Chu--Vandermonde factor in the Pfaff bound for H_(m,d)."""

    assert gap >= 1
    base = 2 * m + 2
    return Fraction(
        rising(base + gap, gap - 1),
        rising(base, gap - 1),
    )


def pfaff_hypergeometric_upper(
    m: int,
    gap: int,
    denominator: int,
) -> Fraction:
    """Upper bound for abs(H_(m,d)(1/denominator)) from Pfaff."""

    assert denominator >= 2
    return (
        Fraction(denominator - 1, denominator) ** (gap - 1)
        * pfaff_hypergeometric_ratio(m, gap)
    )


def pfaff_mangoldt_moment_upper(m: int, gap: int) -> Fraction:
    """Rational upper bound for the Pfaff-weighted Mangoldt moment.

    This bounds

        sum_(r>=2) log(r) r^(-m-1) (1-1/r)^gap.

    The r=2,3 terms are kept separately.  The decreasing remainder is
    bounded by its integral from 3 to infinity, split after u=1/x at 1/4.
    We use log(2)<1 and log(3),log(4)<3/2.
    """

    assert m >= 2
    assert 1 <= gap < 2 * (m - 1)
    at_two = Fraction(1, 2 ** (m + 1 + gap))
    return at_two + pfaff_mangoldt_tail_upper(m, gap)


def pfaff_mangoldt_tail_upper(m: int, gap: int) -> Fraction:
    """The same rational Mangoldt bound with the r=2 term removed."""

    assert m >= 2
    assert 1 <= gap < 2 * (m - 1)
    at_three = Fraction(3, 2) * Fraction(
        2**gap,
        3 ** (m + 1 + gap),
    )
    integral_zero_quarter = Fraction(1, 4**m) * (
        Fraction(3, 2 * m) + Fraction(1, m * m)
    )
    logarithmic_slope = Fraction(3 * (m - 1), 1) - Fraction(3 * gap, 2)
    integral_quarter_third = (
        Fraction(3, 2)
        * Fraction(2**gap, 3 ** (m - 1 + gap))
        / logarithmic_slope
    )
    return at_three + integral_zero_quarter + integral_quarter_third


def pfaff_prime_upper(m: int, gap: int) -> Fraction:
    """Prime-band bound retaining the Pfaff exponential factor.

    The normalization factor is at most 8/7 in the registered range.  The
    assertion records that requirement explicitly, so this helper cannot be
    silently used outside its proved normalization window.
    """

    norm_square = Fraction(2 * m + 2 * gap + 1, 2 * m + 1)
    assert norm_square < PFAFF_NORM_UPPER**2
    return (
        PFAFF_NORM_UPPER
        * comb(2 * m + gap, gap)
        * pfaff_hypergeometric_ratio(m, gap)
        * pfaff_mangoldt_moment_upper(m, gap)
    )


def binomial_one_step_ratio(m: int, gap: int) -> Fraction:
    """C(2(m+1)+d,d) / C(2m+d,d)."""

    return Fraction(
        (2 * m + gap + 2) * (2 * m + gap + 1),
        (2 * m + 2) * (2 * m + 1),
    )


def direct_contour_upper(m: int, gap: int, radius: Fraction) -> Fraction:
    """Direct rational circle-maximum bound at a specified radius."""

    norm_square = Fraction(2 * m + 2 * gap + 1, 2 * m + 1)
    assert norm_square < CONTOUR_NORM_UPPER**2
    assert LAMBDA_UPPER < radius < 1
    return (
        CONTOUR_NORM_UPPER
        * Fraction(2 * m + 1, gap)
        * SQRT_TWO_UPPER
        * radius ** (2 * m + gap + 1)
        * (1 - LAMBDA_LOWER * radius) ** gap
        / (radius - LAMBDA_UPPER) ** gap
    )


def contour_two_dilation_upper(m: int, gap: int) -> Fraction:
    """Rational contour bound for abs(Q_(m,m+d)(1/2)).

    This is the Szehr--Zarouf integral estimate at lambda=1/sqrt(2),
    alpha=0 and beta=1.  A short list of rational contour radii retains the
    cancellation through gap 92.  Rational brackets for lambda and sqrt(2)
    make the returned certificate exact.
    """

    assert gap >= 2
    radius = CONTOUR_RADIUS_OVERRIDES.get(gap, CONTOUR_RADIUS)
    return direct_contour_upper(m, gap, radius)


def l2_concentration_lower(gap: int) -> Fraction:
    """Rational lower bound for the angular concentration constant c."""

    radius = L2_RADIUS_OVERRIDES[gap]
    return (
        LAMBDA_LOWER
        * radius
        * (1 - radius * radius)
        / (
            (1 - LAMBDA_LOWER * radius) ** 2
            * (radius + LAMBDA_UPPER) ** 2
        )
    )


def l2_factor_upper(gap: int) -> Fraction:
    """Rational upper bound for (pi/(8*d*c))^(1/4)."""

    factor = L2_FACTOR_UPPERS[gap]
    # pi < 22/7, so pi/(8*d*c) < 11/(28*d*c).
    assert factor**4 > Fraction(11, 28 * gap) / l2_concentration_lower(gap)
    return factor


def contour_two_dilation_l2_upper(m: int, gap: int) -> Fraction:
    """Circle-L2 bound retaining the Gaussian angular concentration."""

    radius = L2_RADIUS_OVERRIDES[gap]
    return direct_contour_upper(m, gap, radius) * l2_factor_upper(gap)


def direct_contour_tight_upper(m: int, gap: int, radius: Fraction) -> Fraction:
    """Direct contour bound using the tighter L1 algebraic brackets."""

    norm_square = Fraction(2 * m + 2 * gap + 1, 2 * m + 1)
    assert norm_square < CONTOUR_NORM_UPPER**2
    assert L1_LAMBDA_UPPER < radius < 1
    return (
        CONTOUR_NORM_UPPER
        * Fraction(2 * m + 1, gap)
        * L1_SQRT_TWO_UPPER
        * radius ** (2 * m + gap + 1)
        * (1 - L1_LAMBDA_LOWER * radius) ** gap
        / (radius - L1_LAMBDA_UPPER) ** gap
    )


def l1_concentration_lower(gap: int) -> Fraction:
    """Tight rational lower bound for the angular concentration c."""

    radius = L1_RADIUS_OVERRIDES[gap]
    return (
        L1_LAMBDA_LOWER
        * radius
        * (1 - radius * radius)
        / (
            (1 - L1_LAMBDA_LOWER * radius) ** 2
            * (radius + L1_LAMBDA_UPPER) ** 2
        )
    )


def l1_factor_upper(gap: int) -> Fraction:
    """Rational upper bound for sqrt(pi/(4*d*c))."""

    factor = L1_FACTOR_UPPERS[gap]
    # pi < 22/7, so pi/(4*d*c) < 11/(14*d*c).
    assert factor**2 > Fraction(11, 14 * gap) / l1_concentration_lower(gap)
    return factor


def contour_two_dilation_l1_upper(m: int, gap: int) -> Fraction:
    """Circle-L1 bound retaining the full Gaussian peak width."""

    radius = L1_RADIUS_OVERRIDES[gap]
    return direct_contour_tight_upper(m, gap, radius) * l1_factor_upper(gap)


def split_concentration_lower(gap: int) -> Fraction:
    """Tight concentration lower bound at the split-contour radius."""

    radius = SPLIT_RADIUS_OVERRIDES[gap]
    return (
        L1_LAMBDA_LOWER
        * radius
        * (1 - radius * radius)
        / (
            (1 - L1_LAMBDA_LOWER * radius) ** 2
            * (radius + L1_LAMBDA_UPPER) ** 2
        )
    )


def split_main_factor_upper(gap: int) -> Fraction:
    """Rational upper bound for sqrt(pi/(8*d*c))."""

    factor = SPLIT_MAIN_FACTOR_UPPERS[gap]
    assert factor**2 > Fraction(11, 28 * gap) / split_concentration_lower(gap)
    return factor


def split_tail_factor_upper(gap: int) -> Fraction:
    """Rational upper bound for exp(-d*c/2)/2."""

    exponent = Fraction(gap, 2) * split_concentration_lower(gap)
    exponential_denominator = (
        1
        + exponent
        + exponent**2 / 2
        + exponent**3 / 6
        + exponent**4 / 24
    )
    return Fraction(1, 2) / exponential_denominator


def split_l1_factor_upper(gap: int) -> Fraction:
    """Main Gaussian arc plus the complementary exponential tail."""

    return split_main_factor_upper(gap) + split_tail_factor_upper(gap)


def contour_two_dilation_split_upper(m: int, gap: int) -> Fraction:
    """Split-arc L1 bound with a sharper quadratic constant near zero."""

    radius = SPLIT_RADIUS_OVERRIDES[gap]
    norm_square = Fraction(2 * m + 2 * gap + 1, 2 * m + 1)
    assert norm_square < SPLIT_NORM_UPPER**2
    direct = (
        SPLIT_NORM_UPPER
        * Fraction(2 * m + 1, gap)
        * L1_SQRT_TWO_UPPER
        * radius ** (2 * m + gap + 1)
        * (1 - L1_LAMBDA_LOWER * radius) ** gap
        / (radius - L1_LAMBDA_UPPER) ** gap
    )
    return direct * split_l1_factor_upper(gap)


def bessel_concentration_lower(gap: int) -> Fraction:
    """Tight concentration lower bound at the Bessel-contour radius."""

    radius = BESSEL_RADIUS_OVERRIDES[gap]
    return (
        L1_LAMBDA_LOWER
        * radius
        * (1 - radius * radius)
        / (
            (1 - L1_LAMBDA_LOWER * radius) ** 2
            * (radius + L1_LAMBDA_UPPER) ** 2
        )
    )


def rational_bessel_factor_upper(gap: int) -> Fraction:
    """Rational upper bound for exp(-a) I_0(a), a=d*c/2."""

    a = Fraction(gap, 2) * bessel_concentration_lower(gap)
    a_square = a * a

    term = Fraction(1)
    i_zero_partial = term
    for index in range(1, BESSEL_I0_ORDER + 1):
        term *= a_square / (4 * index * index)
        i_zero_partial += term
    next_term = term * a_square / (
        4 * (BESSEL_I0_ORDER + 1) ** 2
    )
    tail_ratio = a_square / (4 * (BESSEL_I0_ORDER + 2) ** 2)
    assert tail_ratio < 1
    i_zero_upper = i_zero_partial + next_term / (1 - tail_ratio)

    term = Fraction(1)
    exponential_partial = term
    for index in range(1, BESSEL_EXP_ORDER + 1):
        term *= a / index
        exponential_partial += term
    return i_zero_upper / exponential_partial


def contour_two_dilation_bessel_upper(m: int, gap: int) -> Fraction:
    """Contour bound retaining the full angular exponential integral."""

    radius = BESSEL_RADIUS_OVERRIDES[gap]
    norm_square = Fraction(2 * m + 2 * gap + 1, 2 * m + 1)
    assert norm_square < SPLIT_NORM_UPPER**2
    direct = (
        SPLIT_NORM_UPPER
        * Fraction(2 * m + 1, gap)
        * L1_SQRT_TWO_UPPER
        * radius ** (2 * m + gap + 1)
        * (1 - L1_LAMBDA_LOWER * radius) ** gap
        / (radius - L1_LAMBDA_UPPER) ** gap
    )
    return direct * rational_bessel_factor_upper(gap)


def exact_two_dilation_square(m: int, gap: int) -> Fraction:
    """Exact square of Q_(m,m+d)(1/2), avoiding every square root."""

    value = sum(
        (
            coefficient * Fraction(1, 2) ** power
            for power, coefficient in enumerate(
                normalized_jacobi_coefficients(m, gap)
            )
        ),
        Fraction(0),
    )
    norm_square = (
        comb(2 * m + gap, gap) ** 2
        * Fraction(2 * m + 2 * gap + 1, 2 * m + 1)
    )
    return norm_square * Fraction(1, 2 ** (2 * m + 2)) * value * value


def contour_prime_upper(m: int, gap: int) -> Fraction:
    """Prime-band bound using the contour estimate for p=2."""

    if gap == 1:
        return pfaff_prime_upper(m, gap)
    tail = (
        CONTOUR_NORM_UPPER
        * comb(2 * m + gap, gap)
        * pfaff_hypergeometric_ratio(m, gap)
        * pfaff_mangoldt_tail_upper(m, gap)
    )
    # Lambda(2)/2 < 1/2 because log(2)<1.
    return contour_two_dilation_upper(m, gap) / 2 + tail


def l2_extended_prime_upper(m: int, gap: int) -> Fraction:
    """Prime bound extended past gap 92 using angular L2 concentration."""

    if gap <= CONTOUR_EXTENDED_GAP:
        return contour_prime_upper(m, gap)
    tail = (
        CONTOUR_NORM_UPPER
        * comb(2 * m + gap, gap)
        * pfaff_hypergeometric_ratio(m, gap)
        * pfaff_mangoldt_tail_upper(m, gap)
    )
    return contour_two_dilation_l2_upper(m, gap) / 2 + tail


def l1_extended_prime_upper(m: int, gap: int) -> Fraction:
    """Prime bound extended past gap 96 using angular L1 concentration."""

    if gap <= L2_EXTENDED_GAP:
        return l2_extended_prime_upper(m, gap)
    tail = (
        CONTOUR_NORM_UPPER
        * comb(2 * m + gap, gap)
        * pfaff_hypergeometric_ratio(m, gap)
        * pfaff_mangoldt_tail_upper(m, gap)
    )
    return contour_two_dilation_l1_upper(m, gap) / 2 + tail


def split_extended_prime_upper(m: int, gap: int) -> Fraction:
    """Prime bound extended past gap 101 by splitting the angular arc."""

    if gap <= L1_EXTENDED_GAP:
        return l1_extended_prime_upper(m, gap)
    tail = (
        SPLIT_NORM_UPPER
        * comb(2 * m + gap, gap)
        * pfaff_hypergeometric_ratio(m, gap)
        * pfaff_mangoldt_tail_upper(m, gap)
    )
    return contour_two_dilation_split_upper(m, gap) / 2 + tail


def bessel_extended_prime_upper(m: int, gap: int) -> Fraction:
    """Prime bound retaining the full angular integral past gap 106."""

    if gap <= SPLIT_EXTENDED_GAP:
        return split_extended_prime_upper(m, gap)
    tail = (
        SPLIT_NORM_UPPER
        * comb(2 * m + gap, gap)
        * pfaff_hypergeometric_ratio(m, gap)
        * pfaff_mangoldt_tail_upper(m, gap)
    )
    return contour_two_dilation_bessel_upper(m, gap) / 2 + tail


def main() -> None:
    identity_checks = 0
    for m in range(4, 20):
        for gap in range(1, 14):
            j_zero = jacobi_moment(m, gap, 0)
            j_one = jacobi_moment(m, gap, 1)
            assert j_one == closed_j_one(m, gap)
            assert j_zero == j_one * closed_j_zero_ratio(m, gap)
            previous = j_one
            assert previous > 0
            for order in range(2, 7):
                current = jacobi_moment(m, gap, order)
                assert 0 < current < previous
                previous = current
            identity_checks += 1

    for gap in range(1, MAX_GAP + 1, 2):
        assert odd_upper_polynomial(TAIL_START, gap) > 0
        assert Fraction(TAIL_START, gap) > Fraction(19, 4)

    for gap in range(2, MAX_GAP + 1, 2):
        assert even_archimedean_rational_upper(TAIL_START, gap) < Fraction(1, 50)

    prime_bounds = [
        crude_prime_upper(TAIL_START, gap)
        for gap in range(1, MAX_GAP + 1)
    ]
    assert max(prime_bounds) < Fraction(1, 10**20)
    assert prime_bounds.index(max(prime_bounds)) + 1 == MAX_GAP

    # The cutoff bound decreases with m: at the worst gap the one-step ratio
    # is already below one, and it decreases thereafter.
    for gap in range(1, MAX_GAP + 1):
        current = crude_prime_upper(TAIL_START, gap)
        following = crude_prime_upper(TAIL_START + 1, gap)
        assert following < current

    for gap in range(1, EXTENDED_GAP + 1, 2):
        assert odd_archimedean_crude_upper(TAIL_START, gap) < Fraction(21, 20)
    for gap in range(2, EXTENDED_GAP + 1, 2):
        assert even_archimedean_crude_upper(TAIL_START, gap) < Fraction(1, 20)

    extended_prime_bounds = [
        crude_prime_upper(TAIL_START, gap)
        for gap in range(1, EXTENDED_GAP + 1)
    ]
    assert max(extended_prime_bounds) < Fraction(1, 4)
    assert extended_prime_bounds.index(max(extended_prime_bounds)) + 1 == EXTENDED_GAP
    for gap in range(1, EXTENDED_GAP + 1):
        assert crude_prime_upper(TAIL_START + 1, gap) < (
            crude_prime_upper(TAIL_START, gap)
        )

    # Pfaff retains (1-1/r)^d and crosses the old gap-46 frontier.  Check
    # the hypergeometric inequality itself on small exact instances.
    for m in (4, 9, 17):
        for gap in range(1, 11):
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

    # All normalization and growth constants are uniform for m>=232 and
    # d<=68.  The binomial ratio decreases with m, the Pfaff ratio decreases
    # with m, and every summand in the moment bound loses at least a factor
    # two per unit increase of m.  The exact cutoff checks below record the
    # rational constants used by that analytic monotonicity argument.
    for gap in range(1, PFAFF_EXTENDED_GAP + 1):
        norm_square = Fraction(
            2 * TAIL_START + 2 * gap + 1,
            2 * TAIL_START + 1,
        )
        assert norm_square < PFAFF_NORM_UPPER**2
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

    odd_pfaff_bounds = [
        pfaff_prime_upper(TAIL_START, gap)
        for gap in range(1, PFAFF_EXTENDED_GAP + 1, 2)
    ]
    even_pfaff_bounds = [
        pfaff_prime_upper(TAIL_START, gap)
        for gap in range(2, PFAFF_EXTENDED_GAP + 1, 2)
    ]
    assert max(odd_pfaff_bounds) < Fraction(1, 3)
    assert max(even_pfaff_bounds) < Fraction(8, 5)
    assert 2 * odd_pfaff_bounds.index(max(odd_pfaff_bounds)) + 1 == 67
    assert 2 * (even_pfaff_bounds.index(max(even_pfaff_bounds)) + 1) == 68
    for gap in range(1, PFAFF_EXTENDED_GAP + 1, 2):
        assert odd_archimedean_crude_upper(TAIL_START, gap) < Fraction(21, 20)
    for gap in range(2, PFAFF_EXTENDED_GAP + 1, 2):
        assert even_archimedean_crude_upper(TAIL_START, gap) < Fraction(1, 20)

    # The same Pfaff--Chu majorant no longer fits the diagonal budget at the
    # next gap.  This registers a method frontier, not a matrix obstruction.
    assert pfaff_prime_upper(TAIL_START, PFAFF_EXTENDED_GAP + 1) > 7

    # The central p=2 term admits a much sharper contour estimate.  First
    # audit all rational enclosures used to remove sqrt(2).
    assert LAMBDA_LOWER**2 < Fraction(1, 2) < LAMBDA_UPPER**2
    assert SQRT_TWO_UPPER**2 > 2
    assert LAMBDA_UPPER < CONTOUR_RADIUS < 1
    for m, gap in (
        (TAIL_START, 2),
        (TAIL_START, 7),
        (TAIL_START, 68),
        (TAIL_START, 92),
    ):
        assert exact_two_dilation_square(m, gap) < (
            contour_two_dilation_upper(m, gap) ** 2
        )

    contour_totals = []
    for gap in range(1, CONTOUR_EXTENDED_GAP + 1):
        norm_square = Fraction(
            2 * TAIL_START + 2 * gap + 1,
            2 * TAIL_START + 1,
        )
        assert norm_square < CONTOUR_NORM_UPPER**2
        assert binomial_one_step_ratio(TAIL_START, gap) < Fraction(3, 2)
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
        contour_totals.append(
            contour_prime_upper(TAIL_START, gap) + archimedean
        )
    assert max(contour_totals) < Fraction(9, 5)
    assert contour_totals.index(max(contour_totals)) + 1 == 92

    next_archimedean = odd_archimedean_crude_upper(
        TAIL_START,
        CONTOUR_EXTENDED_GAP + 1,
    )
    assert (
        contour_prime_upper(TAIL_START, CONTOUR_EXTENDED_GAP + 1)
        + next_archimedean
        > 2
    )

    # Cauchy--Schwarz on the circle retains the angular width of the peak.
    # Exact fourth-power comparisons remove both pi and the fourth root.
    for gap in range(CONTOUR_EXTENDED_GAP + 1, L2_EXTENDED_GAP + 2):
        assert l2_factor_upper(gap) < 1
        assert exact_two_dilation_square(TAIL_START, gap) < (
            contour_two_dilation_l2_upper(TAIL_START, gap) ** 2
        )
        assert l2_extended_prime_upper(TAIL_START + 1, gap) < (
            l2_extended_prime_upper(TAIL_START, gap)
        )

    l2_totals = list(contour_totals)
    for gap in range(CONTOUR_EXTENDED_GAP + 1, L2_EXTENDED_GAP + 1):
        archimedean = (
            odd_archimedean_crude_upper(TAIL_START, gap)
            if gap % 2
            else even_archimedean_crude_upper(TAIL_START, gap)
        )
        l2_totals.append(
            l2_extended_prime_upper(TAIL_START, gap) + archimedean
        )
    assert max(l2_totals) < Fraction(9, 5)
    assert l2_totals.index(max(l2_totals)) + 1 == 92
    l2_next_archimedean = odd_archimedean_crude_upper(
        TAIL_START,
        L2_EXTENDED_GAP + 1,
    )
    assert (
        l2_extended_prime_upper(TAIL_START, L2_EXTENDED_GAP + 1)
        + l2_next_archimedean
        > 2
    )

    # Direct L1 integration improves d^(-1/4) to d^(-1/2).  The tighter
    # algebraic brackets are independently certified by squaring.
    assert L1_LAMBDA_LOWER**2 < Fraction(1, 2) < L1_LAMBDA_UPPER**2
    assert L1_SQRT_TWO_UPPER**2 > 2
    for gap in range(L2_EXTENDED_GAP + 1, L1_EXTENDED_GAP + 2):
        assert l1_factor_upper(gap) < 1
        assert exact_two_dilation_square(TAIL_START, gap) < (
            contour_two_dilation_l1_upper(TAIL_START, gap) ** 2
        )
        assert l1_extended_prime_upper(TAIL_START + 1, gap) < (
            l1_extended_prime_upper(TAIL_START, gap)
        )

    l1_totals = list(l2_totals)
    for gap in range(L2_EXTENDED_GAP + 1, L1_EXTENDED_GAP + 1):
        archimedean = (
            odd_archimedean_crude_upper(TAIL_START, gap)
            if gap % 2
            else even_archimedean_crude_upper(TAIL_START, gap)
        )
        l1_totals.append(
            l1_extended_prime_upper(TAIL_START, gap) + archimedean
        )
    assert max(l1_totals) < Fraction(9, 5)
    assert l1_totals.index(max(l1_totals)) + 1 == 101
    l1_next_archimedean = even_archimedean_crude_upper(
        TAIL_START,
        L1_EXTENDED_GAP + 1,
    )
    assert (
        l1_extended_prime_upper(TAIL_START, L1_EXTENDED_GAP + 1)
        + l1_next_archimedean
        > Fraction(9, 5)
    )

    # A half-circle split doubles the quadratic constant near zero.  The
    # complementary arc is bounded by a fourth-order exponential series.
    for gap in range(L1_EXTENDED_GAP + 1, SPLIT_EXTENDED_GAP + 2):
        assert split_l1_factor_upper(gap) < 1
        assert exact_two_dilation_square(TAIL_START, gap) < (
            contour_two_dilation_split_upper(TAIL_START, gap) ** 2
        )
        assert split_extended_prime_upper(TAIL_START + 1, gap) < (
            split_extended_prime_upper(TAIL_START, gap)
        )

    split_totals = list(l1_totals)
    for gap in range(L1_EXTENDED_GAP + 1, SPLIT_EXTENDED_GAP + 1):
        archimedean = (
            odd_archimedean_crude_upper(TAIL_START, gap)
            if gap % 2
            else even_archimedean_crude_upper(TAIL_START, gap)
        )
        split_totals.append(
            split_extended_prime_upper(TAIL_START, gap) + archimedean
        )
    assert max(split_totals) < Fraction(9, 5)
    assert split_totals.index(max(split_totals)) + 1 == 106
    split_next_archimedean = odd_archimedean_crude_upper(
        TAIL_START,
        SPLIT_EXTENDED_GAP + 1,
    )
    assert (
        split_extended_prime_upper(TAIL_START, SPLIT_EXTENDED_GAP + 1)
        + split_next_archimedean
        > Fraction(9, 5)
    )

    # The full angular majorant integrates to exp(-a) I_0(a).  Both
    # factors are enclosed by finite rational series with rigorous tails.
    for gap in range(SPLIT_EXTENDED_GAP + 1, BESSEL_EXTENDED_GAP + 2):
        assert rational_bessel_factor_upper(gap) < 1
        assert exact_two_dilation_square(TAIL_START, gap) < (
            contour_two_dilation_bessel_upper(TAIL_START, gap) ** 2
        )
        assert bessel_extended_prime_upper(TAIL_START + 1, gap) < (
            bessel_extended_prime_upper(TAIL_START, gap)
        )

    bessel_totals = list(split_totals)
    for gap in range(SPLIT_EXTENDED_GAP + 1, BESSEL_EXTENDED_GAP + 1):
        archimedean = (
            odd_archimedean_crude_upper(TAIL_START, gap)
            if gap % 2
            else even_archimedean_crude_upper(TAIL_START, gap)
        )
        bessel_totals.append(
            bessel_extended_prime_upper(TAIL_START, gap) + archimedean
        )
    assert max(bessel_totals) < Fraction(9, 5)
    assert bessel_totals.index(max(bessel_totals)) + 1 == 106
    bessel_next_archimedean = even_archimedean_crude_upper(
        TAIL_START,
        BESSEL_EXTENDED_GAP + 1,
    )
    assert (
        bessel_extended_prime_upper(TAIL_START, BESSEL_EXTENDED_GAP + 1)
        + bessel_next_archimedean
        > Fraction(9, 5)
    )

    print(f"exact_moment_identity_checks={identity_checks}")
    print(f"max_prime_bound={float(max(prime_bounds)):.12e}")
    print("odd_archimedean_bound=1/gap")
    print("even_archimedean_bound=1/50")
    print("tail_local_diameter=29")
    print(f"extended_prime_bound={float(max(extended_prime_bounds)):.12e}")
    print("extended_tail_local_diameter=45")
    print(f"pfaff_odd_prime_bound={float(max(odd_pfaff_bounds)):.12e}")
    print(f"pfaff_even_prime_bound={float(max(even_pfaff_bounds)):.12e}")
    print("pfaff_tail_local_diameter=68")
    print(f"contour_total_bound={float(max(contour_totals)):.12e}")
    print("contour_tail_local_diameter=92")
    print(f"l2_total_bound={float(max(l2_totals)):.12e}")
    print("l2_tail_local_diameter=96")
    print(f"l1_total_bound={float(max(l1_totals)):.12e}")
    print("l1_tail_local_diameter=101")
    print(f"split_total_bound={float(max(split_totals)):.12e}")
    print("split_tail_local_diameter=106")
    print(
        "bessel_new_gap_bound="
        f"{float(bessel_extended_prime_upper(TAIL_START, 109) + odd_archimedean_crude_upper(TAIL_START, 109)):.12e}"
    )
    print("bessel_tail_local_diameter=109")


if __name__ == "__main__":
    main()

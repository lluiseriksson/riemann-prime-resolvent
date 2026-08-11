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
CONTOUR_EXTENDED_GAP = 85
CONTOUR_RADIUS = Fraction(89, 100)
LAMBDA_LOWER = Fraction(7071, 10_000)
LAMBDA_UPPER = Fraction(7072, 10_000)
SQRT_TWO_UPPER = Fraction(14_143, 10_000)
CONTOUR_NORM_UPPER = Fraction(6, 5)


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


def contour_two_dilation_upper(m: int, gap: int) -> Fraction:
    """Rational contour bound for abs(Q_(m,m+d)(1/2)).

    This is the Szehr--Zarouf integral estimate at lambda=1/sqrt(2),
    alpha=0, beta=1 and the fixed contour radius x=89/100.  Rational
    brackets for lambda and sqrt(2) make the returned certificate exact.
    """

    assert gap >= 2
    norm_square = Fraction(2 * m + 2 * gap + 1, 2 * m + 1)
    assert norm_square < CONTOUR_NORM_UPPER**2
    radius = CONTOUR_RADIUS
    assert LAMBDA_UPPER < radius < 1
    return (
        CONTOUR_NORM_UPPER
        * Fraction(2 * m + 1, gap)
        * SQRT_TWO_UPPER
        * radius ** (2 * m + gap + 1)
        * (1 + LAMBDA_UPPER * radius) ** 2
        * (1 - LAMBDA_LOWER * radius) ** (gap - 2)
        / (radius - LAMBDA_UPPER) ** gap
    )


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
        (TAIL_START, 85),
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
    assert max(contour_totals) < Fraction(17, 10)
    assert contour_totals.index(max(contour_totals)) + 1 == 85

    next_archimedean = even_archimedean_crude_upper(
        TAIL_START,
        CONTOUR_EXTENDED_GAP + 1,
    )
    assert (
        contour_prime_upper(TAIL_START, CONTOUR_EXTENDED_GAP + 1)
        + next_archimedean
        > 2
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
    print("contour_tail_local_diameter=85")


if __name__ == "__main__":
    main()

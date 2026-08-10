import math
from fractions import Fraction

import numpy as np
import pytest

from experiments.theta_pencil.arb_adjacent_full_map import (
    _build_separated_full_matrix,
    _wigner_zero_square,
    build_arb_adjacent_full_map,
    certify_adjacent_analytic_tail,
)
from experiments.theta_pencil.arb_cut_dominant import (
    _cross_block_rectangular,
)


def test_wigner_zero_square_known_values():
    assert _wigner_zero_square(0, 7, 7) == Fraction(1, 15)
    assert _wigner_zero_square(1, 1, 0) == Fraction(1, 3)
    assert _wigner_zero_square(2, 2, 2) == Fraction(2, 35)
    assert _wigner_zero_square(1, 1, 1) == 0

    for left in range(6):
        for right in range(6):
            for middle in range(abs(left - right), left + right + 1, 2):
                semiperimeter = (left + middle + right) // 2
                numerator = (
                    math.factorial(2 * semiperimeter - 2 * left)
                    * math.factorial(2 * semiperimeter - 2 * middle)
                    * math.factorial(2 * semiperimeter - 2 * right)
                    * math.factorial(semiperimeter) ** 2
                )
                denominator = (
                    math.factorial(2 * semiperimeter + 1)
                    * math.factorial(semiperimeter - left) ** 2
                    * math.factorial(semiperimeter - middle) ** 2
                    * math.factorial(semiperimeter - right) ** 2
                )
                assert _wigner_zero_square(left, middle, right) == Fraction(
                    numerator, denominator
                )


def test_adjacent_full_map_matches_direct_exact_moments():
    flint = pytest.importorskip("flint")
    target_length = 0.21
    source_length = 0.73
    count = 3
    first = 5
    last = 11
    result = build_arb_adjacent_full_map(
        target_length,
        source_length,
        count,
        first,
        last,
        precision=384,
    )
    direct = _cross_block_rectangular(
        flint.arb,
        flint.arb_mat,
        flint.arb(str(target_length)),
        flint.arb(str(source_length)),
        flint.arb(0),
        first,
        last,
        0,
        count,
    )
    for row in range(last - first):
        for column in range(count):
            midpoint = float(direct[row, column].mid())
            radius = float(direct[row, column].rad())
            assert abs(result.midpoint[row, column] - midpoint) <= (
                result.radius[row, column] + radius + 1e-45
            )
    assert np.max(result.radius) < 1e-35


def test_recombined_analytic_tail_avoids_polynomial_extrapolation_loss():
    pytest.importorskip("flint")
    result = certify_adjacent_analytic_tail(
        0.73,
        0.0062,
        source_degree_count=4,
        first_degree=128,
        precision=256,
    )
    assert 0 < result.geometric_ratio_upper < 1
    assert result.frobenius_upper < 1e-2


def test_separated_full_map_matches_direct_exact_moments():
    flint = pytest.importorskip("flint")
    target_length = flint.arb("0.21")
    source_length = flint.arb("0.37")
    gap = flint.arb("0.12")
    first = 4
    last = 9
    count = 3
    actual = _build_separated_full_matrix(
        flint.arb,
        flint.arb_mat,
        flint.acb,
        target_length,
        source_length,
        gap,
        count,
        first,
        last,
    )
    direct = _cross_block_rectangular(
        flint.arb,
        flint.arb_mat,
        target_length,
        source_length,
        gap,
        first,
        last,
        0,
        count,
    )
    for row in range(last - first):
        for column in range(count):
            assert (actual[row, column] - direct[row, column]).contains(0)

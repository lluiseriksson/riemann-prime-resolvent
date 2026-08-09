import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss, legvander

from experiments.theta_pencil.arb_cut_smooth import (
    _absolute_distance_moment,
    _power_block,
    _separated_distance_moment,
    build_arb_cut_smooth_matrix,
)
from experiments.theta_pencil.cut_adapted_prime_basis import first_prime_partition
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_remainder_series_coefficients,
)


def test_distance_power_moments_have_required_symmetries():
    flint = pytest.importorskip("flint")
    arb = flint.arb
    for power in range(6):
        for p in range(4):
            for q in range(4):
                same_left = _absolute_distance_moment(
                    arb, p, q, power, arb("0.7")
                )
                same_right = _absolute_distance_moment(
                    arb, q, p, power, arb("0.7")
                )
                assert (same_left - same_right).contains(0)
                separated_left = _separated_distance_moment(
                    arb, p, q, power, arb("0.6"), arb("0.8"), arb("0.3")
                )
                separated_right = _separated_distance_moment(
                    arb, q, p, power, arb("0.8"), arb("0.6"), arb("0.3")
                )
                assert (separated_left - separated_right).contains(0)


def test_cut_smooth_matrix_matches_direct_truncated_kernel():
    pytest.importorskip("flint")
    half_width = 0.5
    degree_count = 3
    maximum_power = 9
    result = build_arb_cut_smooth_matrix(
        half_width, degree_count, maximum_power, 256
    )
    partition = first_prime_partition(half_width)
    intervals = (partition.left, partition.center, partition.right)
    nodes, weights = leggauss(500)

    def local(interval):
        lo, hi = interval
        length = hi - lo
        x = length * nodes / 2 + (hi + lo) / 2
        w = weights * length / 2
        basis = legvander(nodes, degree_count - 1).T
        basis *= np.sqrt((2 * np.arange(degree_count) + 1) / length)[:, None]
        return x, w, basis

    coefficients = smooth_remainder_series_coefficients(maximum_power)
    data = [local(interval) for interval in intervals]
    for left_block in range(3):
        for right_block in range(3):
            x, wx, bx = data[left_block]
            y, wy, by = data[right_block]
            distance = np.abs(x[:, None] - y[None, :])
            kernel = np.zeros_like(distance)
            for power, coefficient in enumerate(coefficients):
                kernel += (
                    -half_width
                    * float(coefficient)
                    * (half_width * distance) ** power
                )
            direct = (bx * wx) @ kernel @ (by * wy).T
            row = slice(left_block * degree_count, (left_block + 1) * degree_count)
            column = slice(
                right_block * degree_count, (right_block + 1) * degree_count
            )
            assert np.max(np.abs(result.midpoint[row, column] - direct)) < 2e-6
            assert np.max(result.radius[row, column]) < 1e-60


def test_constant_power_block_has_expected_rank_one_mass():
    flint = pytest.importorskip("flint")
    length = flint.arb("0.7")
    block = _power_block(
        flint.arb,
        flint.arb_mat,
        length,
        length,
        flint.arb(0),
        3,
        0,
        True,
    )
    assert (block[0, 0] - length).contains(0)
    for left in range(3):
        for right in range(3):
            if (left, right) != (0, 0):
                assert block[left, right].contains(0)

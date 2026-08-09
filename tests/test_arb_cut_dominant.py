import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss, legvander

from experiments.theta_pencil.arb_cut_dominant import (
    _inverse_distance_moment,
    build_arb_cut_dominant_matrix,
)
from experiments.theta_pencil.cut_adapted_prime_basis import first_prime_partition
from experiments.theta_pencil.legendre_log_matrix import dominant_operator_matrix


def test_inverse_distance_moments_are_symmetric():
    flint = pytest.importorskip("flint")
    arb = flint.arb
    for gap in (arb(0), arb("0.7")):
        for p in range(4):
            for q in range(4):
                left = _inverse_distance_moment(
                    arb, p, q, arb("0.6"), arb("0.8"), gap
                )
                right = _inverse_distance_moment(
                    arb, q, p, arb("0.8"), arb("0.6"), gap
                )
                assert (left - right).contains(0)


def test_cut_dominant_cross_blocks_match_high_order_gauss():
    pytest.importorskip("flint")
    degree_count = 3
    result = build_arb_cut_dominant_matrix(0.5, degree_count, 256)
    partition = first_prime_partition(0.5)
    intervals = (partition.left, partition.center, partition.right)
    nodes, weights = leggauss(1200)

    def local(interval):
        lo, hi = interval
        length = hi - lo
        x = length * nodes / 2 + (hi + lo) / 2
        w = weights * length / 2
        basis = legvander(nodes, degree_count - 1).T
        basis *= np.sqrt((2 * np.arange(degree_count) + 1) / length)[:, None]
        return x, w, basis

    data = [local(interval) for interval in intervals]
    for left_block, right_block in ((0, 1), (0, 2), (1, 2)):
        x, wx, bx = data[left_block]
        y, wy, by = data[right_block]
        direct = -0.5 * (bx * wx) @ (1.0 / (y[None, :] - x[:, None])) @ (by * wy).T
        row = slice(left_block * degree_count, (left_block + 1) * degree_count)
        column = slice(right_block * degree_count, (right_block + 1) * degree_count)
        assert np.max(np.abs(result.midpoint[row, column] - direct)) < 2e-5
        assert np.max(result.radius[row, column]) < 1e-60


def test_cut_dominant_diagonal_blocks_have_exact_scaling_shift():
    pytest.importorskip("flint")
    degree_count = 7
    result = build_arb_cut_dominant_matrix(0.5, degree_count, 256)
    partition = first_prime_partition(0.5)
    intervals = (partition.left, partition.center, partition.right)
    standard = dominant_operator_matrix(degree_count)
    for block, interval in enumerate(intervals):
        length = interval[1] - interval[0]
        expected = standard - np.log(length / 2.0) * np.eye(degree_count)
        indices = slice(block * degree_count, (block + 1) * degree_count)
        assert np.max(np.abs(result.midpoint[indices, indices] - expected)) < 2e-14
        assert np.max(result.radius[indices, indices]) < 1e-60

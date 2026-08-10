import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss, legvander

from experiments.theta_pencil.arb_cut_smooth import _power_block_rectangular
from experiments.theta_pencil.arb_second_window_source import (
    build_arb_second_window_dominant,
    build_arb_second_window_source,
)
from experiments.theta_pencil.cut_adapted_prime_basis import (
    second_prime_partition,
)


def _local_data(interval, degree_count, nodes, weights):
    lower, upper = interval
    length = upper - lower
    points = length * nodes / 2 + (upper + lower) / 2
    scaled_weights = weights * length / 2
    basis = legvander(nodes, degree_count - 1).T
    basis *= np.sqrt((2 * np.arange(degree_count) + 1) / length)[:, None]
    return points, scaled_weights, basis


def test_rectangular_power_block_matches_gauss():
    flint = pytest.importorskip("flint")
    block = _power_block_rectangular(
        flint.arb,
        flint.arb_mat,
        flint.arb("0.6"),
        flint.arb("0.8"),
        flint.arb("0.3"),
        2,
        3,
        4,
        False,
    )
    nodes, weights = leggauss(20)
    left = 0.6 * (nodes + 1) / 2
    right = 0.8 * (nodes + 1) / 2
    left_basis = legvander(-nodes, 1).T * np.sqrt(
        (2 * np.arange(2) + 1)[:, None] / 0.6
    )
    right_basis = legvander(nodes, 2).T * np.sqrt(
        (2 * np.arange(3) + 1)[:, None] / 0.8
    )
    kernel = (0.3 + left[:, None] + right[None, :]) ** 4
    direct = (
        (left_basis * (weights * 0.3))
        @ kernel
        @ (right_basis * (weights * 0.4)).T
    )
    midpoint = np.array(
        [[float(block[row, column].mid()) for column in range(3)] for row in range(2)]
    )
    assert np.max(np.abs(midpoint - direct)) < 2e-13


def test_second_window_dominant_cross_block_matches_gauss():
    pytest.importorskip("flint")
    half_width = 0.56
    degree = 2
    result = build_arb_second_window_dominant(
        half_width, degree, degree, degree, 256
    )
    intervals = second_prime_partition(half_width).intervals
    nodes, weights = leggauss(800)
    data = [_local_data(interval, degree, nodes, weights) for interval in intervals]
    for left_block, right_block in ((0, 1), (0, 3), (1, 6), (3, 4)):
        x, wx, bx = data[left_block]
        y, wy, by = data[right_block]
        direct = -0.5 * (bx * wx) @ (1 / (y[None, :] - x[:, None])) @ (by * wy).T
        row = slice(result.offsets[left_block], result.offsets[left_block + 1])
        column = slice(
            result.offsets[right_block], result.offsets[right_block + 1]
        )
        assert np.max(np.abs(result.midpoint[row, column] - direct)) < 2e-5


def test_second_window_reflection_blocks_reconstruct_full_spectrum():
    pytest.importorskip("flint")
    result = build_arb_second_window_source(
        0.56, 2, 2, 2, maximum_power=7, precision=256
    )
    total = result.offsets[-1]
    reflection = np.zeros((total, total))
    for block in range(7):
        mirror = 6 - block
        for degree in range(result.interval_degrees[block]):
            reflection[
                result.offsets[mirror] + degree,
                result.offsets[block] + degree,
            ] = -1.0 if degree % 2 else 1.0
    assert np.max(
        np.abs(reflection.T @ result.midpoint @ reflection - result.midpoint)
    ) < 2e-14
    full = np.linalg.eigvalsh(result.midpoint)
    parity = np.sort(
        np.concatenate(
            (
                np.linalg.eigvalsh(result.even_midpoint),
                np.linalg.eigvalsh(result.odd_midpoint),
            )
        )
    )
    assert np.max(np.abs(full - parity)) < 2e-14

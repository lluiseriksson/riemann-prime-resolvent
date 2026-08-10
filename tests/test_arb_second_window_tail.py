import numpy as np
import pytest

from experiments.theta_pencil.arb_second_window_tail import (
    certify_second_window_regularized_tail,
)
from experiments.theta_pencil.arb_second_green_tail import (
    certify_second_green_adjacent_constant_geometric_tail,
    certify_second_green_separated_geometric_tail,
)
from experiments.theta_pencil.arb_cut_dominant import _cross_block_rectangular


def test_second_window_tail_comparison_respects_reflection_and_norm():
    pytest.importorskip("flint")
    result = certify_second_window_regularized_tail(
        0.62,
        2,
        3,
        2,
        first_degree=16,
        derivative_order=3,
        explicit_end=64,
        subdivisions=16,
        precision=192,
        moment_order=3,
    )
    reflection = result.comparison_matrix[::-1, ::-1]
    assert np.max(np.abs(result.comparison_matrix - reflection)) < 1e-12
    assert np.linalg.norm(result.comparison_matrix, 2) < result.spectral_norm_upper
    assert result.spectral_norm_upper <= result.row_column_upper


def test_geometric_separated_tail_dominates_an_explicit_finite_band():
    flint = pytest.importorskip("flint")
    previous_precision = flint.ctx.prec
    try:
        flint.ctx.prec = 256
        target = flint.arb("0.6")
        source = flint.arb("0.8")
        gap = flint.arb("0.2")
        # Keep the independent monomial construction at low degree; at high
        # degree that implementation is deliberately not the certified route
        # because interval dependency makes its radii explode.
        first = 4
        end = 10
        degree_count = 3
        block = _cross_block_rectangular(
            flint.arb,
            flint.arb_mat,
            target,
            source,
            gap,
            first,
            end,
            0,
            degree_count,
        )
        explicit_square = flint.arb(0)
        for row, degree in enumerate(range(first, end)):
            eigenvalue = degree * (degree + 1)
            for column in range(degree_count):
                explicit_square += (
                    eigenvalue * block[row, column]
                ).abs_upper() ** 2
        result = certify_second_green_separated_geometric_tail(
            target, source, gap, first_degree=first, precision=256
        )
        assert float(explicit_square.sqrt().upper()) < result.total_upper
    finally:
        flint.ctx.prec = previous_precision


def test_adjacent_constant_geometric_tail_dominates_flux_removed_band():
    flint = pytest.importorskip("flint")
    previous_precision = flint.ctx.prec
    try:
        flint.ctx.prec = 256
        target = flint.arb("0.7")
        source = flint.arb("0.03")
        first = 4
        end = 10
        block = _cross_block_rectangular(
            flint.arb,
            flint.arb_mat,
            target,
            source,
            flint.arb(0),
            first,
            end,
            0,
            1,
        )
        explicit_square = flint.arb(0)
        for row, degree in enumerate(range(first, end)):
            eigenvalue = degree * (degree + 1)
            flux = -(target / source).sqrt() * flint.arb(2 * degree + 1).sqrt() / 2
            remainder = eigenvalue * block[row, 0] - flux
            explicit_square += remainder.abs_upper() ** 2
        result = certify_second_green_adjacent_constant_geometric_tail(
            target, source, first_degree=first, precision=256
        )
        assert float(explicit_square.sqrt().upper()) < result.total_upper
    finally:
        flint.ctx.prec = previous_precision

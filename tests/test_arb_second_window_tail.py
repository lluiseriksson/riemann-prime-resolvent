import numpy as np
import pytest

from experiments.theta_pencil.arb_second_window_tail import (
    certify_second_window_regularized_tail,
)


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

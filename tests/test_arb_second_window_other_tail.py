import numpy as np
import pytest

from experiments.theta_pencil.arb_second_window_other_tail import (
    certify_second_window_other_tail,
)


def test_second_window_other_tail_is_reflection_symmetric_and_small():
    pytest.importorskip("flint")
    result = certify_second_window_other_tail(
        0.551,
        edge_degree=3,
        bridge_degree=3,
        center_degree=3,
        first_degree=256,
        explicit_end=512,
        precision=256,
    )
    reflection = result.comparison_matrix[::-1, ::-1]
    assert np.max(np.abs(reflection - result.comparison_matrix)) < 1e-14
    assert result.spectral_norm_upper <= result.row_column_upper * (1 + 1e-12)
    assert result.spectral_norm_upper < 1e-3


def test_registered_other_tail_is_below_the_schur_budget():
    pytest.importorskip("flint")
    result = certify_second_window_other_tail(
        0.551,
        edge_degree=16,
        bridge_degree=16,
        center_degree=16,
        first_degree=640,
        explicit_end=4096,
        precision=512,
    )
    assert 6.49e-6 < result.spectral_norm_upper < 6.50e-6

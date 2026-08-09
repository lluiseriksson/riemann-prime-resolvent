import numpy as np
import pytest

from experiments.theta_pencil.arb_smooth_kernel import build_arb_smooth_matrix
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_matrix,
)


def test_arb_smooth_matrix_encloses_series_midpoint():
    pytest.importorskip("flint")
    result = build_arb_smooth_matrix(0.4, 8, 16, 9, 192)
    direct = smooth_kernel_series_matrix(0.4, 16, 9)[:8]
    assert np.max(np.abs(result.midpoint - direct)) < 2e-14
    assert np.max(result.radius) < 1e-40


import numpy as np
import pytest

from experiments.theta_pencil.arb_cut_dominant import build_arb_cut_dominant_matrix
from experiments.theta_pencil.arb_cut_dominant_cross import (
    build_arb_cut_dominant_cross,
)


def test_rectangular_dominant_cross_matches_square_source():
    pytest.importorskip("flint")
    d = 3
    end = 7
    rectangular = build_arb_cut_dominant_cross(0.5, d, end, 384)
    square = build_arb_cut_dominant_matrix(0.5, end, 384)
    low = np.concatenate([np.arange(d) + block * end for block in range(3)])
    high = np.concatenate(
        [np.arange(d, end) + block * end for block in range(3)]
    )
    expected = square.midpoint[np.ix_(low, high)]
    assert np.max(np.abs(rectangular.midpoint - expected)) < 2e-14
    assert np.max(rectangular.radius) < 1e-80

import numpy as np
import pytest

from experiments.theta_pencil.arb_second_window_dominant_cross import (
    build_arb_second_window_dominant_cross,
)
from experiments.theta_pencil.arb_second_window_source import (
    build_arb_second_window_dominant,
)


def test_second_window_cross_agrees_with_one_larger_finite_matrix():
    pytest.importorskip("flint")
    low_degree = 2
    high_end = 5
    cross = build_arb_second_window_dominant_cross(
        0.62, low_degree, low_degree, low_degree, high_end, 512
    )
    full = build_arb_second_window_dominant(
        0.62, high_end, high_end, high_end, 512
    )
    for low_block in range(7):
        for high_block in range(7):
            rows = slice(low_block * low_degree, (low_block + 1) * low_degree)
            columns = slice(
                high_block * (high_end - low_degree),
                (high_block + 1) * (high_end - low_degree),
            )
            full_rows = slice(high_end * low_block, high_end * low_block + low_degree)
            full_columns = slice(
                high_end * high_block + low_degree,
                high_end * (high_block + 1),
            )
            assert np.max(
                np.abs(
                    cross.midpoint[rows, columns]
                    - full.midpoint[full_rows, full_columns]
                )
            ) < 2e-14

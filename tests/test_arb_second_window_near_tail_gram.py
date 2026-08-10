import numpy as np
import pytest

from experiments.theta_pencil.arb_second_window_near_tail_gram import (
    build_arb_second_window_near_tail_gram,
)


def test_second_window_near_tail_gram_respects_reflection_and_is_psd():
    pytest.importorskip("flint")
    result = build_arb_second_window_near_tail_gram(
        0.56,
        edge_degree=2,
        bridge_degree=2,
        center_degree=2,
        first_degree=2,
        last_degree=8,
        precision=256,
    )
    reflection = np.zeros_like(result.midpoint)
    for block in range(7):
        for degree in range(2):
            reflection[(6 - block) * 2 + degree, block * 2 + degree] = (
                -1.0 if degree % 2 else 1.0
            )
    assert np.max(
        np.abs(reflection.T @ result.midpoint @ reflection - result.midpoint)
    ) < 1e-12
    assert np.linalg.eigvalsh(result.midpoint)[0] > -1e-12
    full = np.linalg.eigvalsh(result.midpoint)
    parity = np.sort(
        np.concatenate(
            (
                np.linalg.eigvalsh(result.even_midpoint),
                np.linalg.eigvalsh(result.odd_midpoint),
            )
        )
    )
    assert np.max(np.abs(full - parity)) < 1e-12
    assert np.max(result.radius) < 1e-30


def test_smooth_rows_are_added_before_the_outer_product():
    pytest.importorskip("flint")
    dominant = build_arb_second_window_near_tail_gram(
        0.56, 2, 2, 2, 2, 6, 256
    )
    combined = build_arb_second_window_near_tail_gram(
        0.56, 2, 2, 2, 2, 6, 256, maximum_smooth_power=3
    )
    assert np.linalg.norm(combined.midpoint - dominant.midpoint) > 1e-8
    assert np.linalg.eigvalsh(combined.midpoint)[0] > -1e-12

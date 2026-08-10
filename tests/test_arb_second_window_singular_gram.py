import numpy as np
import pytest

from experiments.theta_pencil.arb_second_window_singular_gram import (
    build_arb_second_window_singular_gram,
)


def test_second_window_singular_gram_respects_reflection_and_is_psd():
    pytest.importorskip("flint")
    result = build_arb_second_window_singular_gram(
        0.56,
        edge_degree=2,
        bridge_degree=2,
        center_degree=2,
        first_degree=4,
        last_degree=16,
        moment_order=2,
        precision=256,
    )
    degree = 2
    reflection = np.zeros_like(result.midpoint)
    for block in range(7):
        for local_degree in range(degree):
            reflection[(6 - block) * degree + local_degree, block * degree + local_degree] = (
                -1.0 if local_degree % 2 else 1.0
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
    assert result.remainder_norm_upper > 0

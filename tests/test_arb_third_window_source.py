import numpy as np
import pytest

from experiments.theta_pencil.arb_third_window_source import (
    build_arb_third_window_source,
)


def test_third_window_reflection_blocks_reconstruct_full_spectrum():
    pytest.importorskip("flint")
    result = build_arb_third_window_source(
        0.7, 1, 1, 1, maximum_power=7, precision=256
    )
    total = result.offsets[-1]
    reflection = np.zeros((total, total))
    for block in range(13):
        mirror = 12 - block
        for degree in range(result.interval_degrees[block]):
            reflection[
                result.offsets[mirror] + degree,
                result.offsets[block] + degree,
            ] = -1.0 if degree % 2 else 1.0
    assert np.max(
        np.abs(reflection.T @ result.midpoint @ reflection - result.midpoint)
    ) < 3e-14
    full = np.linalg.eigvalsh(result.midpoint)
    parity = np.sort(
        np.concatenate(
            (
                np.linalg.eigvalsh(result.even_midpoint),
                np.linalg.eigvalsh(result.odd_midpoint),
            )
        )
    )
    assert np.max(np.abs(full - parity)) < 3e-14


def test_third_window_source_has_outward_rounded_entries():
    pytest.importorskip("flint")
    result = build_arb_third_window_source(
        0.7, 2, 1, 1, maximum_power=9, precision=256
    )
    assert np.all(np.isfinite(result.midpoint))
    assert np.all(result.radius >= 0)
    assert result.smooth_remainder > 0

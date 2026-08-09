import numpy as np
import pytest
from scipy.linalg import eigvalsh

from experiments.theta_pencil.arb_cut_source import build_arb_cut_finite_source


def test_cut_source_parity_blocks_reconstruct_full_spectrum():
    pytest.importorskip("flint")
    source = build_arb_cut_finite_source(0.5, 5, 9, 256)
    full = eigvalsh(source.midpoint)
    parity = np.sort(
        np.concatenate(
            (eigvalsh(source.even_midpoint), eigvalsh(source.odd_midpoint))
        )
    )
    assert np.max(np.abs(full - parity)) < 2e-14
    # The source deliberately re-wraps exported doubles with one ulp before
    # the parity transform, so its final balls retain that round-trip debt.
    assert np.max(source.radius) < 1e-14
    assert np.max(source.even_radius) < 1e-14
    assert np.max(source.odd_radius) < 1e-14


def test_cut_source_has_expected_low_parity_ritz_values():
    pytest.importorskip("flint")
    source = build_arb_cut_finite_source(0.5, 8, 23, 256)
    even = eigvalsh(source.even_midpoint)
    odd = eigvalsh(source.odd_midpoint)
    assert 0.0 < even[0] < 2e-6
    assert 0.01 < even[1]
    assert 0.0 < odd[0] < 3e-4
    assert 0.3 < odd[1]

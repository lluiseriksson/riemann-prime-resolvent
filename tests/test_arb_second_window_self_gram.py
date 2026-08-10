import numpy as np
import pytest

from experiments.theta_pencil.arb_second_window_self_gram import (
    build_arb_second_window_self_gram,
)


def test_directional_self_gram_is_positive_and_parity_split():
    pytest.importorskip("flint")
    result = build_arb_second_window_self_gram(4, 12, 40, 100, 256)
    assert result.even_midpoint.shape == (14, 14)
    assert result.odd_midpoint.shape == (14, 14)
    assert np.linalg.eigvalsh(result.even_midpoint)[0] > -1e-18
    assert np.linalg.eigvalsh(result.odd_midpoint)[0] > -1e-18
    # The exact self map preserves local Legendre parity.
    assert result.even_midpoint[0, 1] == 0.0
    assert result.remainder_norm_upper > 0.0

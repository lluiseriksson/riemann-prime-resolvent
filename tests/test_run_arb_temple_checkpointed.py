import numpy as np
import pytest

from experiments.theta_pencil.run_arb_temple_checkpointed import (
    _load_or_build_prime_action,
)


def test_prime_action_checkpoint_roundtrip_and_metadata_guard(tmp_path):
    cache = tmp_path / "prime-action.npz"
    coefficients = np.array([1.0, 0.0, -0.125, 0.0])
    first = _load_or_build_prime_action(cache, 0.4, coefficients, 8, 512)
    second = _load_or_build_prime_action(cache, 0.4, coefficients, 8, 512)

    assert cache.exists()
    assert np.array_equal(first.midpoint, second.midpoint)
    assert np.array_equal(first.radius, second.radius)

    changed = coefficients.copy()
    changed[2] = -0.25
    with pytest.raises(ValueError, match="metadata does not match"):
        _load_or_build_prime_action(cache, 0.4, changed, 8, 512)

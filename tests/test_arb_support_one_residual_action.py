import hashlib
import json

import numpy as np
import pytest

from experiments.theta_pencil.arb_prime_translation import ArbPrimeAction
from experiments.theta_pencil.run_arb_support_one_residual_action import (
    run_arb_support_one_residual_action,
)
from experiments.theta_pencil.support_one_residual_endpoint_audit import (
    run_support_one_residual_endpoint_audit,
)


def _digest(array):
    return hashlib.sha256(np.asarray(array, dtype=np.float64).tobytes()).hexdigest()


def _write_trial(path):
    even = np.zeros((12, 2))
    odd = np.zeros((12, 2))
    even[4::2] = ((1.0, 2.0), (3.0, 4.0), (5.0, 6.0), (7.0, 8.0))
    odd[5::2] = ((-1.0, -2.0), (-3.0, -4.0), (-5.0, -6.0), (-7.0, -8.0))
    even_right = np.array(((1.0, 0.0), (0.0, 1.0)))
    odd_right = np.array(((2.0, 0.0), (0.0, 2.0)))
    metadata = {
        "format": 1,
        "architecture": "support-one-residual-schur-trial",
        "trial_rank": 2,
        "source_dimension": 4,
        "finite_dimension": 12,
        "quadrature_order": 64,
        "maximum_smooth_power": 5,
        "parities": {
            "even": {
                "action_vectors_sha256": _digest(even),
                "right_factor_sha256": _digest(even_right),
            },
            "odd": {
                "action_vectors_sha256": _digest(odd),
                "right_factor_sha256": _digest(odd_right),
            },
        },
    }
    np.savez(
        path,
        metadata=np.array(json.dumps(metadata, sort_keys=True)),
        even_action_vectors=even,
        even_right_factor=even_right,
        even_low_indices=np.array((0, 2), dtype=np.int64),
        even_high_indices=np.array((4, 6, 8, 10), dtype=np.int64),
        odd_action_vectors=odd,
        odd_right_factor=odd_right,
        odd_low_indices=np.array((1, 3), dtype=np.int64),
        odd_high_indices=np.array((5, 7, 9, 11), dtype=np.int64),
    )


def test_atomic_residual_action_validates_trial_and_reuses_output(tmp_path):
    trial = tmp_path / "trial.npz"
    output = tmp_path / "action.npz"
    _write_trial(trial)
    calls = []

    def fake_builder(half_width, prime, coefficients, maximum_degree, precision):
        calls.append((half_width, prime, coefficients.copy(), precision))
        midpoint = np.arange(maximum_degree, dtype=float)
        radius = np.full(maximum_degree, 0.125)
        return ArbPrimeAction(midpoint, radius, precision)

    first = run_arb_support_one_residual_action(
        trial, output, "even", 1, 3, 16, 512, builder=fake_builder
    )
    second = run_arb_support_one_residual_action(
        trial, output, "even", 1, 3, 16, 512, builder=fake_builder
    )
    assert first == second
    assert len(calls) == 1
    assert np.all(calls[0][2][1::2] == 0.0)
    assert first["coefficient_sha256"] == _digest(calls[0][2])
    assert first["maximum_radius"] == 0.125


def test_residual_action_rejects_tampered_trial_hash(tmp_path):
    trial = tmp_path / "trial.npz"
    _write_trial(trial)
    with np.load(trial, allow_pickle=False) as payload:
        arrays = {key: np.array(payload[key]) for key in payload.files}
    arrays["even_action_vectors"][4, 0] += 1.0
    np.savez(trial, **arrays)
    with pytest.raises(ValueError, match="hash"):
        run_arb_support_one_residual_action(
            trial, tmp_path / "action.npz", "even", 0, 2, 16, 512
        )


def test_residual_endpoint_audit_detects_a_surviving_jump(tmp_path):
    trial = tmp_path / "trial.npz"
    _write_trial(trial)
    result = run_support_one_residual_endpoint_audit(
        trial, first_degree=256, last_degree=320
    )
    assert result.even.residual_endpoint_norm > 0.0
    assert result.odd.residual_endpoint_norm > 0.0
    assert result.even.triangular_correction_upper > 0.0
    assert result.odd.signed_leading_jet_band_norm > 0.0

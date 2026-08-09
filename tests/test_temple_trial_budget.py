import numpy as np

from experiments.theta_pencil.temple_trial_budget import (
    _legendre_transform_on_interval,
    run_temple_trial_audit,
)


def test_streaming_legendre_transform_recovers_constant():
    nodes, weights = np.polynomial.legendre.leggauss(32)
    coefficients = _legendre_transform_on_interval(nodes, weights, 20)
    assert abs(coefficients[0] - np.sqrt(2.0)) < 2e-14
    assert np.linalg.norm(coefficients[1:]) < 2e-13


def test_small_temple_audit_has_consistent_nonnegative_components():
    audit = run_temple_trial_audit(
        trial_dimension=24, residual_end=128, second_floor=0.005
    )
    assert audit.rayleigh > 0.0
    assert audit.finite_high_residual > 0.0
    assert audit.jump_tail > 0.0
    assert len(audit.coefficients) == 24


def test_odd_trial_stays_in_the_odd_block():
    audit = run_temple_trial_audit(
        trial_dimension=24,
        residual_end=128,
        second_floor=0.5,
        trial_parity=1,
    )
    assert audit.trial_parity == 1
    assert (audit.coefficients[::2] == 0.0).all()

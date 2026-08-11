import numpy as np

from experiments.theta_pencil.block_temple import (
    block_temple_audit,
    generalized_block_temple_audit,
    inflate_residual_gram,
)
from experiments.theta_pencil.arb_block_temple import (
    certify_arb_block_temple_from_residual_gram,
    certify_arb_generalized_block_temple,
)


def test_block_temple_lower_matrix_matches_coordinate_schur_bound():
    compression = np.array([[2.0, 0.1], [0.1, 1.5]])
    cross = np.array([[0.2, -0.1], [0.05, 0.15]])
    complement = np.array([[3.0, 0.2], [0.2, 2.5]])
    operator = np.block([[compression, cross], [cross.T, complement]])
    trial = np.eye(4)[:, :2]
    beta = float(np.linalg.eigvalsh(complement)[0])
    audit = block_temple_audit(operator, trial, beta)
    expected = compression - cross @ cross.T / beta
    assert np.max(np.abs(audit.lower_matrix - expected)) < 2e-15
    assert audit.lower_eigenvalues[0] > 0.0
    assert np.linalg.eigvalsh(operator)[0] > 0.0


def test_exact_invariant_trial_has_zero_residual():
    operator = np.diag([0.2, 0.4, 2.0, 3.0])
    trial = np.eye(4)[:, :2]
    audit = block_temple_audit(operator, trial, 2.0)
    assert audit.residual_norm == 0.0
    assert np.array_equal(audit.lower_matrix, np.diag([0.2, 0.4]))


def test_generalized_formula_is_congruent_to_isometric_formula():
    operator = np.array(
        [
            [1.4, 0.1, 0.2, 0.0],
            [0.1, 1.1, -0.1, 0.15],
            [0.2, -0.1, 3.0, 0.2],
            [0.0, 0.15, 0.2, 2.8],
        ]
    )
    isometry = np.eye(4)[:, :2]
    change = np.array([[2.0, 0.25], [-0.5, 1.5]])
    trial = isometry @ change
    gram = trial.T @ trial
    compression = trial.T @ operator @ trial
    action_gram = trial.T @ operator @ operator @ trial
    beta = float(np.linalg.eigvalsh(operator[2:, 2:])[0])
    generalized = generalized_block_temple_audit(
        gram, compression, action_gram, beta
    )

    direct = block_temple_audit(operator, isometry, beta)
    congruent = change.T @ direct.lower_matrix @ change
    assert np.max(np.abs(generalized.lower_matrix - congruent)) < 5e-15
    assert generalized.lower_eigenvalues[0] > 0.0


def test_arb_generalized_certificate_when_flint_is_available():
    try:
        import flint  # noqa: F401
    except ImportError:
        return
    operator = np.array(
        [
            [1.4, 0.1, 0.2, 0.0],
            [0.1, 1.1, -0.1, 0.15],
            [0.2, -0.1, 3.0, 0.2],
            [0.0, 0.15, 0.2, 2.8],
        ]
    )
    trial = np.eye(4)[:, :2] @ np.array([[2.0, 0.25], [-0.5, 1.5]])
    gram = trial.T @ trial
    compression = trial.T @ operator @ trial
    action = trial.T @ operator @ operator @ trial
    beta = float(np.linalg.eigvalsh(operator[2:, 2:])[0])
    certificate = certify_arb_generalized_block_temple(
        gram,
        1e-30,
        compression,
        1e-30,
        action,
        1e-30,
        beta,
        precision=256,
    )
    assert certificate.trial_gram_lower > 0.0
    assert certificate.lower_certificate.original_spectral_lower > 0.0

    inverse_gram = np.linalg.inv(gram)
    residual = action - compression @ inverse_gram @ compression
    direct = certify_arb_block_temple_from_residual_gram(
        gram,
        1e-30,
        compression,
        1e-30,
        residual,
        1e-29,
        beta,
        precision=256,
    )
    assert direct.lower_certificate.original_spectral_lower > 0.0


def test_scalar_residual_inflation_dominates_every_cross_term():
    explicit = np.array([[0.2, -0.1], [0.4, 0.3], [-0.2, 0.5]])
    omitted = np.array([[0.01, -0.02], [0.0, 0.015], [-0.01, 0.0]])
    delta = float(np.linalg.norm(omitted, 2))
    inflated, amount = inflate_residual_gram(explicit.T @ explicit, delta)
    exact = (explicit + omitted).T @ (explicit + omitted)
    assert amount > 0.0
    assert np.linalg.eigvalsh(inflated - exact)[0] > -2e-16

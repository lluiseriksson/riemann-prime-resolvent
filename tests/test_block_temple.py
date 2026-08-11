import numpy as np

from experiments.theta_pencil.block_temple import (
    block_temple_audit,
    generalized_block_temple_audit,
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

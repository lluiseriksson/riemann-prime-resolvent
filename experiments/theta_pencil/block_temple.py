"""Block Kato--Temple/Schur certificate for a low spectral cluster.

Let ``V`` be an isometry and ``Q = I - V V*``.  If the exact operator obeys
``Q T Q >= beta Q``, then

    V* T V - (Q T V)* (Q T V) / beta > 0

implies ``T > 0``.  This is the cluster analogue of the one-vector Temple
test used by the existing localized certificates.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BlockTempleAudit:
    compression: np.ndarray
    residual_gram: np.ndarray
    lower_matrix: np.ndarray
    lower_eigenvalues: np.ndarray
    residual_norm: float
    complement_floor: float


def block_temple_audit(
    operator: np.ndarray,
    trial_isometry: np.ndarray,
    complement_floor: float,
    orthogonality_tolerance: float = 1.0e-11,
) -> BlockTempleAudit:
    """Form the finite matrices entering the block Temple theorem.

    The routine does not establish the complement floor; that is a separate
    analytic/interval obligation.  It does verify symmetry and the isometry
    condition before calculating the residual Gram.
    """

    matrix = np.asarray(operator, dtype=float)
    trial = np.asarray(trial_isometry, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("operator must be square")
    if trial.ndim != 2 or trial.shape[0] != matrix.shape[0] or trial.shape[1] < 1:
        raise ValueError("trial vectors must be a nonempty compatible matrix")
    if complement_floor <= 0.0:
        raise ValueError("complement floor must be positive")
    if not np.allclose(matrix, matrix.T, atol=orthogonality_tolerance, rtol=0.0):
        raise ValueError("operator must be symmetric")
    gram = trial.T @ trial
    if not np.allclose(
        gram, np.eye(trial.shape[1]), atol=orthogonality_tolerance, rtol=0.0
    ):
        raise ValueError("trial vectors must be orthonormal")

    compression = trial.T @ matrix @ trial
    compression = 0.5 * (compression + compression.T)
    residual = matrix @ trial - trial @ compression
    residual_gram = residual.T @ residual
    residual_gram = 0.5 * (residual_gram + residual_gram.T)
    lower = compression - residual_gram / complement_floor
    lower = 0.5 * (lower + lower.T)
    return BlockTempleAudit(
        compression=compression,
        residual_gram=residual_gram,
        lower_matrix=lower,
        lower_eigenvalues=np.linalg.eigvalsh(lower),
        residual_norm=float(np.linalg.norm(residual, 2)),
        complement_floor=complement_floor,
    )

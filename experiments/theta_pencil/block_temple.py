"""Block Kato--Temple/Schur certificate for a low spectral cluster.

Let ``V`` be an isometry and ``Q = I - V V*``.  If the exact operator obeys
``Q T Q >= beta Q``, then

    V* T V - (Q T V)* (Q T V) / beta > 0

implies ``T > 0``.  This is the cluster analogue of the one-vector Temple
test used by the existing localized certificates.
"""

from __future__ import annotations

import math
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


@dataclass(frozen=True)
class GeneralizedBlockTempleAudit:
    trial_gram: np.ndarray
    compression: np.ndarray
    action_gram: np.ndarray
    residual_gram: np.ndarray
    lower_matrix: np.ndarray
    lower_eigenvalues: np.ndarray
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


def generalized_block_temple_audit(
    trial_gram: np.ndarray,
    compression: np.ndarray,
    action_gram: np.ndarray,
    complement_floor: float,
    symmetry_tolerance: float = 1.0e-11,
) -> GeneralizedBlockTempleAudit:
    """Block Temple matrix in a nonorthonormal trial basis.

    For an injective trial map ``V``, the inputs are

    ``G = V* V``, ``A = V* T V``, and ``K = V* T^2 V``.

    The orthogonal residual Gram is exactly ``K - A G^-1 A``.  Positivity of
    ``A - residual/beta`` is congruent to the isometric block criterion and
    can be checked without treating a floating QR factorization as data.
    """

    gram = np.asarray(trial_gram, dtype=float)
    source = np.asarray(compression, dtype=float)
    action = np.asarray(action_gram, dtype=float)
    if gram.ndim != 2 or gram.shape[0] != gram.shape[1] or gram.shape[0] < 1:
        raise ValueError("trial Gram must be nonempty and square")
    if source.shape != gram.shape or action.shape != gram.shape:
        raise ValueError("all three matrices must have the same shape")
    if complement_floor <= 0.0:
        raise ValueError("complement floor must be positive")
    for matrix in (gram, source, action):
        if not np.allclose(
            matrix, matrix.T, atol=symmetry_tolerance, rtol=0.0
        ):
            raise ValueError("input matrices must be symmetric")
    if np.linalg.eigvalsh(gram)[0] <= 0.0:
        raise ValueError("trial Gram must be positive definite")

    projected_action = source @ np.linalg.solve(gram, source)
    residual = action - projected_action
    residual = 0.5 * (residual + residual.T)
    lower = source - residual / complement_floor
    lower = 0.5 * (lower + lower.T)
    return GeneralizedBlockTempleAudit(
        trial_gram=gram,
        compression=source,
        action_gram=action,
        residual_gram=residual,
        lower_matrix=lower,
        lower_eigenvalues=np.linalg.eigvalsh(lower),
        complement_floor=complement_floor,
    )


def inflate_residual_gram(
    explicit_residual_gram: np.ndarray, remainder_operator_norm: float
) -> tuple[np.ndarray, float]:
    """Add a scalar upper bound for an omitted residual operator.

    If ``R = R0 + E`` and ``||E|| <= delta``, then

    ``R*R <= R0*R0 + (2 ||R0|| delta + delta^2) I``.

    The returned scalar is the diagonal inflation.
    """

    gram = np.asarray(explicit_residual_gram, dtype=float)
    if gram.ndim != 2 or gram.shape[0] != gram.shape[1] or gram.shape[0] < 1:
        raise ValueError("residual Gram must be nonempty and square")
    if remainder_operator_norm < 0.0:
        raise ValueError("remainder norm must be nonnegative")
    gram = 0.5 * (gram + gram.T)
    maximum = max(0.0, float(np.linalg.eigvalsh(gram)[-1]))
    inflation = (
        2.0 * math.sqrt(maximum) * remainder_operator_norm
        + remainder_operator_norm**2
    )
    return gram + inflation * np.eye(len(gram)), inflation

"""Canonical intermediate shifts for the two-channel Weyl programme."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import eigh

from experiments.theta_pencil.finite_weyl_ratio import canonical_weyl_from_channels


@dataclass(frozen=True)
class GapNormalizedWeylValue:
    ground_eigenvalue: float
    first_gap: float
    gap_multiple: float
    shift: float
    canonical_weyl: complex


def gap_normalized_weyl_value(
    operator: np.ndarray,
    metric: np.ndarray,
    plus_vector: np.ndarray,
    minus_vector: np.ndarray,
    observation: np.ndarray,
    z: complex,
    gap_multiple: float,
) -> GapNormalizedWeylValue:
    """Evaluate the Weyl function at a scale-free admissible shift.

    If ``mu0 < mu1`` are the first generalized eigenvalues, use

    ``shift = mu0 - gap_multiple * (mu1-mu0)``.

    The pencil is positive with spectral margin
    ``gap_multiple * (mu1-mu0)``. Its common gap scale cancels from the
    quotient, so the result only depends on the normalized operator
    ``(A-mu0*G)/(mu1-mu0)``. In particular it is invariant under
    ``A -> alpha*A + beta*G`` for ``alpha > 0``.
    """

    matrix = np.asarray(operator, dtype=float)
    gram = np.asarray(metric, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("operator must be square")
    if gram.shape != matrix.shape:
        raise ValueError("metric has the wrong shape")
    if not np.allclose(matrix, matrix.T, atol=1.0e-12, rtol=0.0):
        raise ValueError("operator must be self-adjoint")
    if not np.allclose(gram, gram.T, atol=1.0e-12, rtol=0.0):
        raise ValueError("metric must be self-adjoint")
    if gap_multiple <= 0.0:
        raise ValueError("gap_multiple must be positive")
    dimension = matrix.shape[0]
    plus = np.asarray(plus_vector, dtype=float)
    minus = np.asarray(minus_vector, dtype=float)
    functional = np.asarray(observation, dtype=complex)
    if plus.shape != (dimension,) or minus.shape != (dimension,):
        raise ValueError("channel vectors have the wrong shape")
    if functional.shape != (dimension,):
        raise ValueError("observation has the wrong shape")

    eigenvalues = eigh(
        matrix,
        gram,
        eigvals_only=True,
        subset_by_index=(0, 1),
    )
    ground = float(eigenvalues[0])
    gap = float(eigenvalues[1] - eigenvalues[0])
    if gap <= 0.0:
        raise ValueError("the first generalized eigenvalue must be simple")
    shift = ground - gap_multiple * gap
    pencil = matrix - shift * gram
    plus_solution = np.linalg.solve(pencil, plus)
    minus_solution = np.linalg.solve(pencil, minus)
    plus_transform = complex(functional @ plus_solution)
    minus_transform = complex(functional @ minus_solution)
    value = canonical_weyl_from_channels(plus_transform, minus_transform, z)
    return GapNormalizedWeylValue(
        ground_eigenvalue=ground,
        first_gap=gap,
        gap_multiple=gap_multiple,
        shift=shift,
        canonical_weyl=value,
    )

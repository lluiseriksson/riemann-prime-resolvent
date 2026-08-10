"""A reproducible order-four obstruction beyond the rapidity Lipschitz gate."""

from __future__ import annotations

import itertools
import math

import numpy as np


def linear_rapidity_increment(left: float, right: float, length: float) -> float:
    """Integrate tanh(g) when g is linear between two endpoint values."""

    slope = (right - left) / length
    if abs(slope) < 1.0e-15:
        return length * math.tanh(left)
    return (math.log(math.cosh(right)) - math.log(math.cosh(left))) / slope


def endpoint_partial_correlation(correlation: np.ndarray) -> float:
    """Return the partial correlation of endpoints conditional on nodes 2,3."""

    matrix = np.asarray(correlation, dtype=float)
    if matrix.shape != (4, 4):
        raise ValueError("correlation must be 4 by 4")
    middle = matrix[1:3, 1:3]
    left = matrix[0, 1:3]
    right = matrix[1:3, 3]
    inverse = np.linalg.inv(middle)
    left_variance = 1.0 - left @ inverse @ left
    right_variance = 1.0 - right @ inverse @ right
    covariance = matrix[0, 3] - left @ inverse @ right
    return float(covariance / math.sqrt(left_variance * right_variance))


def counterexample() -> dict[str, object]:
    """Construct and audit the piecewise-linear rapidity counterexample."""

    spacing = 0.6
    rapidities = np.asarray((0.7, 0.01, 1.1, 2.2))
    slopes = np.diff(rapidities) / spacing
    increments = np.asarray(
        [
            linear_rapidity_increment(rapidities[index], rapidities[index + 1], spacing)
            for index in range(3)
        ]
    )
    times = spacing * np.arange(4)
    values = np.concatenate(([0.0], np.cumsum(increments)))
    correlation = np.cosh(values[:, None] - values[None, :]) / np.cosh(
        times[:, None] - times[None, :]
    )
    determinant = float(np.linalg.det(correlation))
    triple_determinants = tuple(
        float(np.linalg.det(correlation[np.ix_(indices, indices)]))
        for indices in itertools.combinations(range(4), 3)
    )
    partial = endpoint_partial_correlation(correlation)
    assert np.max(np.abs(slopes)) < 2.0
    assert min(triple_determinants) > 0.0
    assert determinant < -1.62e-4
    assert partial > 1.23
    return {
        "slopes": tuple(float(value) for value in slopes),
        "increments": tuple(float(value) for value in increments),
        "determinant": determinant,
        "triple_determinants": triple_determinants,
        "endpoint_partial_correlation": partial,
    }


if __name__ == "__main__":
    print(counterexample())

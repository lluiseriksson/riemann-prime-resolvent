"""Arb verifier for the generalized block Temple criterion.

Source construction is intentionally separate.  This module accepts
entrywise enclosures of

    G = W*W,  A = W*T*W,  K = W*T^2*W

and certifies positivity of ``A - (K - A G^-1 A) / beta``.  All matrix
operations, including inversion of ``G``, are performed with Arb balls.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.interval_inertia import (
    ArbPositiveDefiniteCongruence,
    certify_arb_positive_definite_by_congruence,
)


@dataclass(frozen=True)
class ArbBlockTempleCertificate:
    dimension: int
    complement_floor: float
    trial_gram_lower: float
    lower_midpoint: np.ndarray
    lower_radius: np.ndarray
    lower_certificate: ArbPositiveDefiniteCongruence
    precision: int


def _radius_array(radius: float | np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    values = np.asarray(radius, dtype=float)
    if values.ndim == 0:
        if float(values) < 0.0:
            raise ValueError("entry radius must be nonnegative")
        return np.full(shape, float(values))
    if values.shape != shape or np.any(values < 0.0):
        raise ValueError("entry radii must be nonnegative and match the matrix")
    return values


def _ball_matrix(arb, arb_mat, midpoint, radius):
    center = np.asarray(midpoint, dtype=float)
    if center.ndim != 2 or center.shape[0] != center.shape[1]:
        raise ValueError("midpoint must be square")
    radii = _radius_array(radius, center.shape)
    rows = []
    for left in range(len(center)):
        row = []
        for right in range(len(center)):
            pad = math.ulp(float(center[left, right]))
            row.append(
                arb(
                    float(center[left, right]),
                    float(radii[left, right]) + pad,
                )
            )
        rows.append(row)
    matrix = arb_mat(rows)
    return (matrix + matrix.transpose()) / 2


def _arb_inverse(matrix, arb, arb_mat):
    """Gauss--Jordan inverse with interval-safe pivot rejection."""

    if matrix.nrows() != matrix.ncols() or matrix.nrows() < 1:
        raise ValueError("matrix must be nonempty and square")
    size = matrix.nrows()
    left = [
        [arb(matrix[row, column]) for column in range(size)]
        for row in range(size)
    ]
    right = [
        [arb(int(row == column)) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        candidates = [
            row
            for row in range(column, size)
            if left[row][column].lower() > 0 or left[row][column].upper() < 0
        ]
        if not candidates:
            raise ArithmeticError("every interval pivot candidate contained zero")
        pivot_row = max(
            candidates,
            key=lambda row: abs(float(left[row][column].mid())),
        )
        if pivot_row != column:
            left[column], left[pivot_row] = left[pivot_row], left[column]
            right[column], right[pivot_row] = right[pivot_row], right[column]

        pivot = arb(left[column][column])
        for index in range(size):
            left[column][index] /= pivot
            right[column][index] /= pivot
        for row in range(size):
            if row == column:
                continue
            factor = arb(left[row][column])
            for index in range(size):
                left[row][index] -= factor * left[column][index]
                right[row][index] -= factor * right[column][index]
    return arb_mat(right)


def certify_arb_generalized_block_temple(
    trial_gram_midpoint: np.ndarray,
    trial_gram_radius: float | np.ndarray,
    compression_midpoint: np.ndarray,
    compression_radius: float | np.ndarray,
    action_gram_midpoint: np.ndarray,
    action_gram_radius: float | np.ndarray,
    complement_floor: float,
    precision: int = 512,
) -> ArbBlockTempleCertificate:
    """Certify the basis-free block Temple matrix with outward rounding."""

    if complement_floor <= 0.0:
        raise ValueError("complement floor must be a certified positive lower bound")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        gram = _ball_matrix(
            arb, arb_mat, trial_gram_midpoint, trial_gram_radius
        )
        source = _ball_matrix(
            arb, arb_mat, compression_midpoint, compression_radius
        )
        action = _ball_matrix(
            arb, arb_mat, action_gram_midpoint, action_gram_radius
        )
        if not (
            gram.nrows() == source.nrows() == action.nrows()
            and gram.ncols() == source.ncols() == action.ncols()
        ):
            raise ValueError("all three interval matrices must have the same shape")

        gram_certificate = certify_arb_positive_definite_by_congruence(
            gram, precision
        )
        inverse = _arb_inverse(gram, arb, arb_mat)
        residual = action - source * inverse * source
        residual = (residual + residual.transpose()) / 2
        lower = source - residual / arb(str(complement_floor))
        lower = (lower + lower.transpose()) / 2
        lower_certificate = certify_arb_positive_definite_by_congruence(
            lower, precision
        )

        dimension = lower.nrows()
        midpoint = np.empty((dimension, dimension), dtype=float)
        radius = np.empty_like(midpoint)
        for row in range(dimension):
            for column in range(dimension):
                midpoint[row, column] = float(lower[row, column].mid())
                radius[row, column] = _arb_radius_as_float(lower[row, column])
    finally:
        ctx.prec = previous_precision

    return ArbBlockTempleCertificate(
        dimension=dimension,
        complement_floor=complement_floor,
        trial_gram_lower=gram_certificate.original_spectral_lower,
        lower_midpoint=midpoint,
        lower_radius=radius,
        lower_certificate=lower_certificate,
        precision=precision,
    )


def certify_arb_block_temple_from_residual_gram(
    trial_gram_midpoint: np.ndarray,
    trial_gram_radius: float | np.ndarray,
    compression_midpoint: np.ndarray,
    compression_radius: float | np.ndarray,
    residual_gram_midpoint: np.ndarray,
    residual_gram_radius: float | np.ndarray,
    complement_floor: float,
    precision: int = 512,
) -> ArbBlockTempleCertificate:
    """Certify block Temple when the residual Gram is supplied directly.

    This is the stable entry point for degree-resolved source builders: finite
    residual bands and endpoint-jet tails can be accumulated as Grams before
    any scalar remainder inflation is added.
    """

    if complement_floor <= 0.0:
        raise ValueError("complement floor must be a certified positive lower bound")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        gram = _ball_matrix(
            arb, arb_mat, trial_gram_midpoint, trial_gram_radius
        )
        source = _ball_matrix(
            arb, arb_mat, compression_midpoint, compression_radius
        )
        residual = _ball_matrix(
            arb, arb_mat, residual_gram_midpoint, residual_gram_radius
        )
        if not (
            gram.nrows() == source.nrows() == residual.nrows()
            and gram.ncols() == source.ncols() == residual.ncols()
        ):
            raise ValueError("all three interval matrices must have the same shape")

        gram_certificate = certify_arb_positive_definite_by_congruence(
            gram, precision
        )
        lower = source - residual / arb(str(complement_floor))
        lower = (lower + lower.transpose()) / 2
        lower_certificate = certify_arb_positive_definite_by_congruence(
            lower, precision
        )

        dimension = lower.nrows()
        midpoint = np.empty((dimension, dimension), dtype=float)
        radius = np.empty_like(midpoint)
        for row in range(dimension):
            for column in range(dimension):
                midpoint[row, column] = float(lower[row, column].mid())
                radius[row, column] = _arb_radius_as_float(lower[row, column])
    finally:
        ctx.prec = previous_precision

    return ArbBlockTempleCertificate(
        dimension=dimension,
        complement_floor=complement_floor,
        trial_gram_lower=gram_certificate.original_spectral_lower,
        lower_midpoint=midpoint,
        lower_radius=radius,
        lower_certificate=lower_certificate,
        precision=precision,
    )

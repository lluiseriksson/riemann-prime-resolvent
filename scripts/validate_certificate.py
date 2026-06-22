#!/usr/bin/env python3
"""Deterministically validate the exact-rational demo certificate structure."""
from __future__ import annotations

import argparse
import json
import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


class CertificateError(ValueError):
    pass


def rational(value: Any, field: str) -> Fraction:
    if not isinstance(value, str) or re.fullmatch(r"-?[0-9]+(?:/[1-9][0-9]*)?", value) is None:
        raise CertificateError(f"{field}: expected exact rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise CertificateError(f"{field}: invalid rational {value!r}") from exc


def mat_vec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((a * b for a, b in zip(row, vector, strict=True)), Fraction(0)) for row in matrix]


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def matrix_square(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    dim = len(matrix)
    return [
        [sum((matrix[i][k] * matrix[k][j] for k in range(dim)), Fraction(0)) for j in range(dim)]
        for i in range(dim)
    ]


def inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    """Invert a square rational matrix by deterministic Gauss--Jordan elimination."""
    dim = len(matrix)
    augmented = [
        row[:] + [Fraction(int(i == j)) for j in range(dim)]
        for i, row in enumerate(matrix)
    ]
    for column in range(dim):
        pivot = next((row for row in range(column, dim) if augmented[row][column] != 0), None)
        if pivot is None:
            raise CertificateError("squared-resolvent matrix is singular")
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(dim):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor != 0:
                augmented[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(augmented[row], augmented[column], strict=True)
                ]
    return [row[dim:] for row in augmented]


def half_squared_resolvent_trace(matrix: list[list[Fraction]], x: Fraction) -> Fraction:
    """Compute `(1/2) * Tr((A^2 + x I)^-1)` exactly over the rationals."""
    squared = matrix_square(matrix)
    shifted = [
        [squared[i][j] + (x if i == j else 0) for j in range(len(matrix))]
        for i in range(len(matrix))
    ]
    inv = inverse(shifted)
    return sum((inv[i][i] for i in range(len(matrix))), Fraction(0)) / 2


def validate(data: dict[str, Any]) -> dict[str, Any]:
    required = {
        "format_version", "certificate_kind", "lambda", "N", "matrix", "trial_vector",
        "rayleigh_value", "residual_upper", "separation_lower", "galerkin_tail_upper",
        "resolvent_grid", "provenance",
    }
    unknown = set(data) - required
    missing = required - set(data)
    if missing:
        raise CertificateError(f"missing fields: {sorted(missing)}")
    if unknown:
        raise CertificateError(f"unknown fields: {sorted(unknown)}")
    if data["format_version"] != "0.3.0":
        raise CertificateError("format_version must be 0.3.0")
    if data["certificate_kind"] != "exact-rational-structural":
        raise CertificateError("unsupported certificate_kind")

    lam = rational(data["lambda"], "lambda")
    if lam <= 1:
        raise CertificateError("lambda must be > 1")
    if not isinstance(data["N"], int) or isinstance(data["N"], bool) or data["N"] < 1:
        raise CertificateError("N must be an integer >= 1")

    raw_matrix = data["matrix"]
    if not isinstance(raw_matrix, list) or not raw_matrix:
        raise CertificateError("matrix must be a nonempty array")
    dim = len(raw_matrix)
    matrix: list[list[Fraction]] = []
    for i, raw_row in enumerate(raw_matrix):
        if not isinstance(raw_row, list) or len(raw_row) != dim:
            raise CertificateError("matrix must be square")
        matrix.append([rational(value, f"matrix[{i}][{j}]") for j, value in enumerate(raw_row)])
    for i in range(dim):
        for j in range(dim):
            if matrix[i][j] != matrix[j][i]:
                raise CertificateError(f"matrix is not symmetric at ({i},{j})")

    raw_vector = data["trial_vector"]
    if not isinstance(raw_vector, list) or len(raw_vector) != dim:
        raise CertificateError("trial_vector length must equal matrix dimension")
    vector = [rational(value, f"trial_vector[{i}]") for i, value in enumerate(raw_vector)]
    norm_sq = dot(vector, vector)
    if norm_sq != 1:
        raise CertificateError(f"trial_vector must have exact squared norm 1, got {norm_sq}")

    rayleigh = rational(data["rayleigh_value"], "rayleigh_value")
    av = mat_vec(matrix, vector)
    computed_rayleigh = dot(vector, av)
    if computed_rayleigh != rayleigh:
        raise CertificateError(f"rayleigh_value mismatch: declared {rayleigh}, computed {computed_rayleigh}")
    residual = [entry - rayleigh * component for entry, component in zip(av, vector, strict=True)]
    residual_sq = dot(residual, residual)
    residual_upper = rational(data["residual_upper"], "residual_upper")
    if residual_upper < 0 or residual_sq > residual_upper * residual_upper:
        raise CertificateError(f"residual bound failed: squared residual {residual_sq} > {residual_upper**2}")

    separation = rational(data["separation_lower"], "separation_lower")
    tail = rational(data["galerkin_tail_upper"], "galerkin_tail_upper")
    if separation <= 0:
        raise CertificateError("separation_lower must be positive")
    if tail < 0:
        raise CertificateError("galerkin_tail_upper must be nonnegative")

    grid = data["resolvent_grid"]
    if not isinstance(grid, list):
        raise CertificateError("resolvent_grid must be an array")
    previous_x: Fraction | None = None
    for index, point in enumerate(grid):
        if not isinstance(point, dict) or set(point) != {"x", "lower", "upper"}:
            raise CertificateError(f"resolvent_grid[{index}] has invalid fields")
        x = rational(point["x"], f"resolvent_grid[{index}].x")
        lower = rational(point["lower"], f"resolvent_grid[{index}].lower")
        upper = rational(point["upper"], f"resolvent_grid[{index}].upper")
        if x <= 0:
            raise CertificateError(f"resolvent_grid[{index}].x must be positive")
        if previous_x is not None and x <= previous_x:
            raise CertificateError("resolvent_grid x values must be strictly increasing")
        previous_x = x
        if lower > upper:
            raise CertificateError(f"resolvent_grid[{index}] lower > upper")
        exact = half_squared_resolvent_trace(matrix, x)
        if not lower <= exact <= upper:
            raise CertificateError(
                f"resolvent_grid[{index}] does not enclose exact half trace {exact}"
            )

    provenance = data["provenance"]
    if not isinstance(provenance, dict) or set(provenance) != {"generator", "purpose", "input_sha256"}:
        raise CertificateError("provenance fields are invalid")
    if not all(isinstance(provenance[key], str) and provenance[key] for key in ("generator", "purpose")):
        raise CertificateError("provenance generator and purpose must be nonempty strings")
    digest = provenance["input_sha256"]
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise CertificateError("provenance.input_sha256 must be 64 lowercase hex characters")

    return {"dimension": dim, "lambda": str(lam), "rayleigh": str(rayleigh), "residual_sq": str(residual_sq), "grid_points": len(grid)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.certificate.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise CertificateError("certificate root must be an object")
        summary = validate(data)
    except (OSError, json.JSONDecodeError, CertificateError) as exc:
        print(f"Certificate check FAILED: {exc}", file=sys.stderr)
        return 1
    print("Certificate check passed:", json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

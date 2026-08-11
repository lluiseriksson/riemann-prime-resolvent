"""Certify one fixed support-one residual-trial action with Arb.

Production is deliberately split by parity, trial column and prime power.
Every output verifies the hashes embedded in the frozen rank-factor trial and
can therefore be resumed without silently changing the floating design.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Callable

import numpy as np

from experiments.theta_pencil.arb_prime_translation import (
    ArbPrimeAction,
    build_arb_prime_action,
)


def _array_sha256(array: np.ndarray) -> str:
    payload = np.asarray(array, dtype=np.float64).tobytes()
    return hashlib.sha256(payload).hexdigest()


def _atomic_save_npz(path: Path, **arrays) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as stream:
        np.savez(stream, **arrays)
    os.replace(temporary, path)


def _load_trial_column(
    trial: Path, parity: str, column: int
) -> tuple[np.ndarray, dict]:
    if parity not in {"even", "odd"}:
        raise ValueError("parity must be even or odd")
    with np.load(trial, allow_pickle=False) as payload:
        metadata = json.loads(str(payload["metadata"].item()))
        if metadata.get("architecture") != "support-one-residual-schur-trial":
            raise ValueError("the input is not a support-one residual trial")
        action_vectors = np.array(payload[f"{parity}_action_vectors"], dtype=float)
        right_factor = np.array(payload[f"{parity}_right_factor"], dtype=float)

    parity_metadata = metadata.get("parities", {}).get(parity)
    if parity_metadata is None:
        raise ValueError("the trial has no metadata for the selected parity")
    if _array_sha256(action_vectors) != parity_metadata.get(
        "action_vectors_sha256"
    ):
        raise ValueError("the trial action-vector hash does not match")
    if _array_sha256(right_factor) != parity_metadata.get("right_factor_sha256"):
        raise ValueError("the trial right-factor hash does not match")
    trial_rank = int(metadata["trial_rank"])
    finite_dimension = int(metadata["finite_dimension"])
    if action_vectors.shape != (finite_dimension, trial_rank):
        raise ValueError("the trial action-vector shape does not match metadata")
    if right_factor.shape[0] != trial_rank:
        raise ValueError("the trial right-factor rank does not match metadata")
    if not 0 <= column < trial_rank:
        raise ValueError("the trial column is out of range")
    opposite = 1 if parity == "even" else 0
    if np.any(action_vectors[opposite::2] != 0.0):
        raise ValueError("the selected trial vectors are not parity-pure")
    coefficients = action_vectors[:, column].copy()
    provenance = {
        "trial_format": int(metadata["format"]),
        "trial_rank": trial_rank,
        "source_dimension": int(metadata["source_dimension"]),
        "finite_dimension": finite_dimension,
        "quadrature_order": int(metadata["quadrature_order"]),
        "maximum_smooth_power": int(metadata["maximum_smooth_power"]),
        "action_vectors_sha256": parity_metadata["action_vectors_sha256"],
        "right_factor_sha256": parity_metadata["right_factor_sha256"],
        "coefficient_sha256": _array_sha256(coefficients),
    }
    return coefficients, provenance


def _load_matching_output(path: Path, request: dict) -> dict | None:
    if not path.exists():
        return None
    with np.load(path, allow_pickle=False) as payload:
        metadata = json.loads(str(payload["metadata"].item()))
        midpoint = np.array(payload["midpoint"], dtype=float)
        radius = np.array(payload["radius"], dtype=float)
    for key, value in request.items():
        if metadata.get(key) != value:
            raise ValueError(f"existing action output mismatches request field {key}")
    if not np.all(np.isfinite(midpoint)) or not np.all(np.isfinite(radius)):
        raise ValueError("existing action output is not finite")
    if np.any(radius < 0.0):
        raise ValueError("existing action output has a negative radius")
    if _array_sha256(midpoint) != metadata.get("midpoint_sha256"):
        raise ValueError("existing action midpoint hash does not match")
    if _array_sha256(radius) != metadata.get("radius_sha256"):
        raise ValueError("existing action radius hash does not match")
    return metadata


def run_arb_support_one_residual_action(
    trial: Path,
    output: Path,
    parity: str,
    column: int,
    prime: int,
    maximum_degree: int,
    precision: int,
    half_width: float = 1.0,
    builder: Callable[..., ArbPrimeAction] | None = None,
) -> dict:
    """Build or validate one atomic prime-power action checkpoint."""

    coefficients, provenance = _load_trial_column(trial, parity, column)
    if maximum_degree < len(coefficients):
        raise ValueError("maximum_degree must cover every trial coefficient")
    request = {
        "format": 1,
        "architecture": "support-one-residual-prime-action",
        "parity": parity,
        "column": column,
        "prime": prime,
        "half_width": repr(half_width),
        "maximum_degree": maximum_degree,
        "precision": precision,
        **provenance,
    }
    cached = _load_matching_output(output, request)
    if cached is not None:
        return cached

    action_builder = build_arb_prime_action if builder is None else builder
    action = action_builder(
        half_width, prime, coefficients, maximum_degree, precision
    )
    midpoint = np.asarray(action.midpoint, dtype=float)
    radius = np.asarray(action.radius, dtype=float)
    if midpoint.shape != (maximum_degree,) or radius.shape != (maximum_degree,):
        raise ValueError("the Arb action has the wrong shape")
    if not np.all(np.isfinite(midpoint)) or not np.all(np.isfinite(radius)):
        raise ArithmeticError("the Arb action is not finite")
    if np.any(radius < 0.0) or not math.isfinite(float(np.sum(radius))):
        raise ArithmeticError("the Arb action has invalid radii")
    metadata = {
        **request,
        "midpoint_sha256": _array_sha256(midpoint),
        "radius_sha256": _array_sha256(radius),
        "maximum_radius": float(np.max(radius)),
    }
    _atomic_save_npz(
        output,
        midpoint=midpoint,
        radius=radius,
        metadata=np.array(json.dumps(metadata, sort_keys=True)),
    )
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trial", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--parity", choices=("even", "odd"), required=True)
    parser.add_argument("--column", type=int, required=True)
    parser.add_argument("--prime", type=int, required=True)
    parser.add_argument("--maximum-degree", type=int, required=True)
    parser.add_argument("--precision", type=int, required=True)
    parser.add_argument("--half-width", type=float, default=1.0)
    args = parser.parse_args()
    metadata = run_arb_support_one_residual_action(
        trial=args.trial,
        output=args.output,
        parity=args.parity,
        column=args.column,
        prime=args.prime,
        maximum_degree=args.maximum_degree,
        precision=args.precision,
        half_width=args.half_width,
    )
    print(json.dumps(metadata, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

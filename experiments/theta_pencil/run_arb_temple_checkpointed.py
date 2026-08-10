"""Run a long Arb Temple certificate with a recoverable prime-action cache."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import asdict
from pathlib import Path

import numpy as np

from experiments.theta_pencil.arb_prime_translation import (
    ArbPrimeAction,
    build_arb_prime_two_action,
)
from experiments.theta_pencil.arb_temple_certificate import (
    _trial_build_residual_end,
    certify_temple_trial,
)
from experiments.theta_pencil.temple_trial_budget import run_temple_trial_audit


def _coefficient_hash(coefficients: np.ndarray) -> str:
    payload = np.asarray(coefficients, dtype=np.float64).tobytes()
    return hashlib.sha256(payload).hexdigest()


def _atomic_save_npz(path: Path, **arrays) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as stream:
        np.savez(stream, **arrays)
    os.replace(temporary, path)


def _atomic_save_json(path: Path, payload: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def _trial_coefficients(
    half_width: float,
    parity: int,
    dimension: int,
    residual_end: int,
    second_floor: float,
) -> np.ndarray:
    floating = run_temple_trial_audit(
        half_width=half_width,
        trial_dimension=dimension,
        residual_end=_trial_build_residual_end(dimension, residual_end),
        second_floor=second_floor,
        trial_parity=parity,
    )
    coefficients = floating.coefficients.copy()
    coefficients[1 - parity :: 2] = 0.0
    return coefficients


def _load_or_build_prime_action(
    cache: Path,
    half_width: float,
    coefficients: np.ndarray,
    residual_end: int,
    precision: int,
) -> ArbPrimeAction:
    digest = _coefficient_hash(coefficients)
    if cache.exists():
        with np.load(cache, allow_pickle=False) as data:
            metadata = json.loads(str(data["metadata"].item()))
            expected = {
                "half_width": half_width,
                "residual_end": residual_end,
                "precision": precision,
                "coefficient_hash": digest,
            }
            if metadata != expected:
                raise ValueError("the prime-action cache metadata does not match")
            action = ArbPrimeAction(
                midpoint=np.array(data["midpoint"], dtype=float),
                radius=np.array(data["radius"], dtype=float),
                precision=precision,
            )
            if not np.all(np.isfinite(action.midpoint)) or not np.all(
                np.isfinite(action.radius)
            ):
                raise ValueError("the prime-action cache is not finite")
            return action

    action = build_arb_prime_two_action(
        half_width, coefficients, residual_end, precision
    )
    metadata = {
        "half_width": half_width,
        "residual_end": residual_end,
        "precision": precision,
        "coefficient_hash": digest,
    }
    _atomic_save_npz(
        cache,
        midpoint=action.midpoint,
        radius=action.radius,
        metadata=np.array(json.dumps(metadata, sort_keys=True)),
    )
    return action


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--half-width", type=float, required=True)
    parser.add_argument("--parity", type=int, choices=(0, 1), required=True)
    parser.add_argument("--dimension", type=int, required=True)
    parser.add_argument("--residual-end", type=int, required=True)
    parser.add_argument("--second-floor", type=float, required=True)
    parser.add_argument("--variation-partitions", type=int, required=True)
    parser.add_argument("--precision", type=int, required=True)
    parser.add_argument("--prime-precision", type=int, required=True)
    parser.add_argument("--prime-cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    coefficients = _trial_coefficients(
        args.half_width,
        args.parity,
        args.dimension,
        args.residual_end,
        args.second_floor,
    )
    prime = _load_or_build_prime_action(
        args.prime_cache,
        args.half_width,
        coefficients,
        args.residual_end,
        args.prime_precision,
    )
    certificate = certify_temple_trial(
        half_width=args.half_width,
        trial_parity=args.parity,
        dimension=args.dimension,
        residual_end=args.residual_end,
        second_floor=args.second_floor,
        variation_partitions=args.variation_partitions,
        precision=args.precision,
        prime_precision=args.prime_precision,
        prime_action=prime,
    )
    _atomic_save_json(args.output, asdict(certificate))
    print(json.dumps(asdict(certificate), sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

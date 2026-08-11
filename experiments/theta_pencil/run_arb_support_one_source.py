"""Reproduce the support-one raw-source positive-subspace certificate."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict
from pathlib import Path

from experiments.theta_pencil.arb_support_one_source import (
    build_arb_support_one_source,
    certify_arb_support_one_positive_subspaces,
)


def _atomic_write_json(path: Path, payload: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, default=58)
    parser.add_argument("--maximum-smooth-power", type=int, default=95)
    parser.add_argument("--precision", type=int, default=512)
    parser.add_argument("--prime-precision", type=int, default=2048)
    parser.add_argument("--even-positive-count", type=int, default=26)
    parser.add_argument("--odd-positive-count", type=int, default=26)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    started = time.perf_counter()
    source = build_arb_support_one_source(
        dimension=args.dimension,
        maximum_smooth_power=args.maximum_smooth_power,
        precision=args.precision,
        prime_precision=args.prime_precision,
    )
    built = time.perf_counter()
    certificate = certify_arb_support_one_positive_subspaces(
        source,
        even_positive_count=args.even_positive_count,
        odd_positive_count=args.odd_positive_count,
        precision=args.precision,
    )
    finished = time.perf_counter()
    payload = {
        "source": {
            "dimension": source.dimension,
            "maximum_smooth_power": args.maximum_smooth_power,
            "smooth_remainder": source.smooth_remainder,
            "precision": source.precision,
            "prime_precision": source.prime_precision,
            "active_prime_powers": source.active_prime_powers,
        },
        "certificate": asdict(certificate),
        "timing_seconds": {
            "build": built - started,
            "certify": finished - built,
            "total": finished - started,
        },
    }
    if args.output is not None:
        _atomic_write_json(args.output, payload)
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

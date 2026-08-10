"""Build registered near-tail bands with resumable cross-map checkpoints."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np

from experiments.theta_pencil.arb_third_window_near_tail_gram import (
    build_arb_third_window_near_tail_gram,
)


def _atomic_save_npz(path: Path, **arrays) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as stream:
        np.savez_compressed(stream, **arrays)
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--half-width", type=float, required=True)
    parser.add_argument("--degree", type=int, required=True)
    parser.add_argument("--boundaries", type=int, nargs="+", required=True)
    parser.add_argument("--precision", type=int, required=True)
    parser.add_argument("--maximum-smooth-power", type=int, required=True)
    parser.add_argument("--cross-map-cache-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    boundaries = tuple(args.boundaries)
    bands = build_arb_third_window_near_tail_gram(
        half_width=args.half_width,
        edge_degree=args.degree,
        bridge_degree=args.degree,
        center_degree=args.degree,
        first_degree=boundaries[0],
        last_degree=boundaries[-1],
        precision=args.precision,
        maximum_smooth_power=args.maximum_smooth_power,
        band_boundaries=boundaries,
        cross_map_cache_dir=args.cross_map_cache_dir,
    )
    metadata = {
        "format": 1,
        "architecture": "third-window-near-tail-bands",
        "half_width": repr(args.half_width),
        "degree": args.degree,
        "boundaries": list(boundaries),
        "precision": args.precision,
        "working_precision": bands[0].working_precision,
        "maximum_smooth_power": args.maximum_smooth_power,
    }
    arrays = {"metadata": np.array(json.dumps(metadata, sort_keys=True))}
    for index, band in enumerate(bands):
        arrays[f"band_{index}_even_midpoint"] = band.even_midpoint
        arrays[f"band_{index}_even_radius"] = band.even_radius
        arrays[f"band_{index}_odd_midpoint"] = band.odd_midpoint
        arrays[f"band_{index}_odd_radius"] = band.odd_radius
    _atomic_save_npz(args.output, **arrays)
    print(json.dumps(metadata, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

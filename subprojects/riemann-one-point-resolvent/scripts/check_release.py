#!/usr/bin/env python3
"""Validate manifest hashes and the exact toy certificate without extra packages."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRACTION = re.compile(r"^-?\d+(?:/\d+)?$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_fraction(value: str) -> None:
    if not FRACTION.fullmatch(value):
        raise ValueError(f"not an exact integer/fraction string: {value!r}")
    Fraction(value)


def check_certificate() -> None:
    path = ROOT / "data/certificates/exact_atomic_certificate.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "status",
        "x0",
        "spectrum",
        "weights",
        "compactified_points",
        "moments",
        "signed_differences",
        "hankel_matrix",
        "localizing_matrix",
    }
    missing = required - data.keys()
    if missing:
        raise ValueError(f"certificate missing fields: {sorted(missing)}")
    check_fraction(data["x0"])
    for key in ["spectrum", "weights", "compactified_points", "moments"]:
        for value in data[key]:
            check_fraction(value)
    for value in data["signed_differences"].values():
        check_fraction(value)
        if Fraction(value) < 0:
            raise ValueError("negative signed difference")
    for key in ["hankel_matrix", "localizing_matrix"]:
        matrix = data[key]
        if not matrix or any(len(row) != len(matrix) for row in matrix):
            raise ValueError(f"{key} is not square")
        for row in matrix:
            for value in row:
                check_fraction(value)


def check_manifest() -> None:
    manifest_path = ROOT / "MANIFEST.json"
    if not manifest_path.exists():
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for record in manifest["files"]:
        path = ROOT / record["path"]
        if not path.exists():
            raise FileNotFoundError(record["path"])
        if path.stat().st_size != record["bytes"]:
            raise ValueError(f"size mismatch: {record['path']}")
        if sha256(path) != record["sha256"]:
            raise ValueError(f"hash mismatch: {record['path']}")


def main() -> int:
    check_certificate()
    check_manifest()
    print("Release/certificate checks: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

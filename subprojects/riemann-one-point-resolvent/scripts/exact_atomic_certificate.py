#!/usr/bin/env python3
"""Generate exact rational Hausdorff/Hankel certificates for a toy spectrum."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp


def moment(weights: list[Fraction], points: list[Fraction], n: int) -> Fraction:
    return sum((w * p**n for w, p in zip(weights, points, strict=True)), Fraction(0))


def signed_difference(seq: list[Fraction], k: int, n: int) -> Fraction:
    current = seq[:]
    for _ in range(k):
        current = [current[j] - current[j + 1] for j in range(len(current) - 1)]
    return current[n]


def fraction_text(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def sympy_matrix_to_text(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("data/certificates"))
    parser.add_argument("--order", type=int, default=5)
    args = parser.parse_args()
    if args.order < 2:
        raise ValueError("order must be at least 2")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    x0 = Fraction(1)
    spectrum = [Fraction(1), Fraction(4), Fraction(9)]
    weights = [1 / (lam + x0) for lam in spectrum]
    points = [x0 / (lam + x0) for lam in spectrum]
    max_index = 2 * args.order + args.order + 4
    moments = [moment(weights, points, n) for n in range(max_index)]

    differences: dict[str, str] = {}
    for k in range(args.order + 1):
        for n in range(args.order + 1):
            value = signed_difference(moments, k, n)
            if value < 0:
                raise AssertionError(f"negative signed difference at k={k}, n={n}: {value}")
            differences[f"k={k},n={n}"] = fraction_text(value)

    size = args.order
    hankel = sp.Matrix(
        size,
        size,
        lambda i, j: sp.Rational(moments[i + j].numerator, moments[i + j].denominator),
    )
    localizing = sp.Matrix(
        size,
        size,
        lambda i, j: sp.Rational(
            (moments[i + j] - moments[i + j + 1]).numerator,
            (moments[i + j] - moments[i + j + 1]).denominator,
        ),
    )

    hankel_minors = [sp.factor(hankel[:k, :k].det()) for k in range(1, size + 1)]
    localizing_minors = [sp.factor(localizing[:k, :k].det()) for k in range(1, size + 1)]
    if any(v < 0 for v in hankel_minors + localizing_minors):
        raise AssertionError("a principal minor is negative")

    payload = {
        "status": "exact toy certificate; not an RH certificate",
        "x0": fraction_text(x0),
        "spectrum": [fraction_text(q) for q in spectrum],
        "weights": [fraction_text(q) for q in weights],
        "compactified_points": [fraction_text(q) for q in points],
        "moments": [fraction_text(q) for q in moments[: 2 * size + 1]],
        "signed_differences": differences,
        "hankel_matrix": sympy_matrix_to_text(hankel),
        "localizing_matrix": sympy_matrix_to_text(localizing),
        "hankel_leading_principal_minors": [str(v) for v in hankel_minors],
        "localizing_leading_principal_minors": [str(v) for v in localizing_minors],
        "rank_hankel": int(hankel.rank()),
        "rank_localizing": int(localizing.rank()),
    }

    out = args.output_dir / "exact_atomic_certificate.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

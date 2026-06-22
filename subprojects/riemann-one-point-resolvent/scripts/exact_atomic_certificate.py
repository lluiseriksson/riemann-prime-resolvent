#!/usr/bin/env python3
"""Generate a deterministic exact-rational finite Hausdorff certificate."""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def encode(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    if not matrix:
        return Fraction(1)
    a = [row[:] for row in matrix]
    det = Fraction(1)
    n = len(a)
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        p = a[col][col]
        det *= p
        a[col] = [v / p for v in a[col]]
        for r in range(col + 1, n):
            factor = a[r][col]
            if factor:
                a[r] = [v - factor * w for v, w in zip(a[r], a[col], strict=True)]
    return det


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--order', type=int, default=8)
    args = parser.parse_args()

    x0 = Fraction(1)
    spectrum = [Fraction(1), Fraction(4), Fraction(9)]
    weights = [1 / (lam + x0) for lam in spectrum]
    points = [x0 / (lam + x0) for lam in spectrum]

    max_moment = max(args.order, 10)
    moments = [sum(w * p**n for w, p in zip(weights, points, strict=True)) for n in range(max_moment + 1)]

    def diff(k: int, n: int) -> Fraction:
        return sum(w * p**n * (1 - p)**k for w, p in zip(weights, points, strict=True))

    signed = {f'{k},{n}': encode(diff(k, n)) for k in range(5) for n in range(5)}
    size = 4
    hankel = [[moments[i + j] for j in range(size)] for i in range(size)]
    localizing = [[moments[i + j] - moments[i + j + 1] for j in range(size)] for i in range(size)]

    data = {
        'format_version': '0.3.0',
        'status': 'exact-finite-toy-certificate-not-evidence-for-RH',
        'x0': encode(x0),
        'spectrum': [encode(x) for x in spectrum],
        'weights': [encode(x) for x in weights],
        'compactified_points': [encode(x) for x in points],
        'moments': [encode(x) for x in moments],
        'signed_differences': signed,
        'hankel_matrix': [[encode(x) for x in row] for row in hankel],
        'localizing_matrix': [[encode(x) for x in row] for row in localizing],
        'hankel_leading_principal_minors': [encode(determinant([row[:n] for row in hankel[:n]])) for n in range(1, size + 1)],
        'localizing_leading_principal_minors': [encode(determinant([row[:n] for row in localizing[:n]])) for n in range(1, size + 1)],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(data, indent=2, sort_keys=True) + '\n').encode('utf-8'))
    print(args.output)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Recompute and validate the exact finite atomic certificate."""
from __future__ import annotations

import argparse
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

FRACTION = re.compile(r'^-?\d+(?:/[1-9]\d*)?$')


def frac(value: str) -> Fraction:
    if not isinstance(value, str) or not FRACTION.fullmatch(value):
        raise ValueError(f'invalid exact fraction: {value!r}')
    return Fraction(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.certificate.read_text(encoding='utf-8'))
        x0 = frac(data['x0'])
        spectrum = [frac(x) for x in data['spectrum']]
        weights = [frac(x) for x in data['weights']]
        points = [frac(x) for x in data['compactified_points']]
        if weights != [1 / (lam + x0) for lam in spectrum]:
            raise ValueError('weight formula mismatch')
        if points != [x0 / (lam + x0) for lam in spectrum]:
            raise ValueError('compactification formula mismatch')
        moments = [frac(x) for x in data['moments']]
        for n, value in enumerate(moments):
            expected = sum(w * p**n for w, p in zip(weights, points, strict=True))
            if value != expected:
                raise ValueError(f'moment {n} mismatch')
        for key, encoded in data['signed_differences'].items():
            k, n = map(int, key.split(','))
            value = frac(encoded)
            expected = sum(w * p**n * (1 - p)**k for w, p in zip(weights, points, strict=True))
            if value != expected or value < 0:
                raise ValueError(f'signed difference {key} invalid')
        size = len(data['hankel_matrix'])
        expected_h = [[moments[i + j] for j in range(size)] for i in range(size)]
        actual_h = [[frac(x) for x in row] for row in data['hankel_matrix']]
        if actual_h != expected_h:
            raise ValueError('Hankel matrix mismatch')
        expected_l = [[moments[i + j] - moments[i + j + 1] for j in range(size)] for i in range(size)]
        actual_l = [[frac(x) for x in row] for row in data['localizing_matrix']]
        if actual_l != expected_l:
            raise ValueError('localizing matrix mismatch')
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f'Certificate audit FAILED: {exc}', file=sys.stderr)
        return 1
    print('Exact certificate audit passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

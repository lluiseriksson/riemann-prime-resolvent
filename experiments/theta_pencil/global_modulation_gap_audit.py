"""Finite exact-structure audit for the global modulation--gap gate.

The analytic theorem concerns the localized Weil form.  This script checks
the operator identity, the spectral-gap lower bound, the off-diagonal source
formula, and recovery of the double commutator on a three-point model.  It is
not numerical evidence for RH.
"""

from __future__ import annotations

import cmath
import math


POINTS = (-1.0, 0.0, 1.0)
WITNESS = (1.0, 1.0, 1.0)
OPERATOR = (
    (2.0, -1.0, -1.0),
    (-1.0, 2.0, -1.0),
    (-1.0, -1.0, 2.0),
)
GAP = 3.0


def inner(left: tuple[complex, ...], right: tuple[complex, ...]) -> complex:
    return sum(value.conjugate() * other for value, other in zip(left, right))


def apply(matrix, vector: tuple[complex, ...]) -> tuple[complex, ...]:
    return tuple(sum(row[j] * vector[j] for j in range(3)) for row in matrix)


def modulated(t: float) -> tuple[complex, ...]:
    return tuple(w * cmath.exp(1j * t * x) for x, w in zip(POINTS, WITNESS))


def energy(t: float) -> float:
    vector = modulated(t)
    return float(inner(vector, apply(OPERATOR, vector)).real)


def source_energy(t: float) -> float:
    total = 0.0
    for i in range(3):
        for j in range(3):
            if i != j:
                phase = t * (POINTS[j] - POINTS[i])
                total += OPERATOR[i][j] * WITNESS[i] * WITNESS[j] * (
                    math.cos(phase) - 1
                )
    return total


def projected_distance_squared(t: float) -> float:
    vector = modulated(t)
    norm_squared = inner(WITNESS, WITNESS).real
    overlap = inner(WITNESS, vector)
    return float(inner(vector, vector).real - abs(overlap) ** 2 / norm_squared)


def double_commutator_expectation() -> float:
    total = 0.0
    for i in range(3):
        for j in range(3):
            difference = POINTS[i] - POINTS[j]
            total -= (
                OPERATOR[i][j]
                * WITNESS[i]
                * WITNESS[j]
                * difference**2
            )
    return total


def radial_source(s: float) -> float:
    total = 0.0
    for i in range(3):
        for j in range(3):
            if i != j:
                difference = POINTS[j] - POINTS[i]
                total -= (
                    OPERATOR[i][j]
                    * WITNESS[i]
                    * WITNESS[j]
                    * difference**2
                    / (s**2 + difference**2)
                )
    return total


def radial_gap_margin(s: float) -> float:
    norm_squared = inner(WITNESS, WITNESS).real
    total = 0.0
    for i in range(3):
        for j in range(3):
            difference = POINTS[j] - POINTS[i]
            total += (
                WITNESS[i] ** 2
                * WITNESS[j] ** 2
                * difference**2
                / (s**2 + difference**2)
            )
    return GAP * total / norm_squared


def audit() -> None:
    assert apply(OPERATOR, WITNESS) == (0.0, 0.0, 0.0)
    for t in (0.1, 0.7, 1.9, 4.2):
        direct = energy(t)
        source = source_energy(t)
        lower = GAP * projected_distance_squared(t)
        assert abs(direct - source) < 1e-12
        assert abs(direct - lower) < 1e-12  # A is exactly GAP times Q.
        assert direct > 0

    step = 1e-4
    numerical_second = (energy(step) - 2 * energy(0.0) + energy(-step)) / step**2
    commutator = double_commutator_expectation()
    assert abs(numerical_second - commutator) < 1e-6
    for s in (0.2, 1.0, 3.0, 10.0):
        assert abs(radial_source(s) - radial_gap_margin(s)) < 1e-12
        assert radial_source(s) > 0
    print("GLOBAL-MODULATION-GAP-AUDIT: PASS")


if __name__ == "__main__":
    audit()

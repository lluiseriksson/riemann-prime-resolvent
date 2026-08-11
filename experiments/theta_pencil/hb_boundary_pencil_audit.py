"""Lightweight algebra audit for Proposition 4.9.

This script checks only the elementary factorization and the finite-dimensional
spectral-projector limit used in the boundary Hermite--Biehler pencil.  The
real-zero input is Suzuki's Theorem 1.5, not a numerical claim made here.
The script is intentionally local-light: one process, negligible memory, and
well below one second on the desk machine.
"""

from __future__ import annotations

from fractions import Fraction


def parity_factorization(
    y: Fraction, deficiency: Fraction, even: Fraction, odd: Fraction
) -> None:
    left = (y + deficiency) ** 2 * (even + odd) ** 2 - (
        y - deficiency
    ) ** 2 * (even - odd) ** 2
    right = 4 * (y * even + deficiency * odd) * (
        deficiency * even + y * odd
    )
    assert left == right


def projector_limit() -> None:
    # Diagonal model for epsilon (A + epsilon I)^(-1) -> P_ker(A).
    eigenvalues = [Fraction(0), Fraction(0), Fraction(7, 10), Fraction(21, 10)]
    vector = [Fraction(2), Fraction(-3), Fraction(5), Fraction(11)]
    projection = vector[:2] + [Fraction(0), Fraction(0)]
    errors = []
    for epsilon in [Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000)]:
        scaled_resolvent = [
            epsilon * value / (eigenvalue + epsilon)
            for eigenvalue, value in zip(eigenvalues, vector, strict=True)
        ]
        error = sum(abs(x - y) for x, y in zip(scaled_resolvent, projection, strict=True))
        errors.append(error)
    assert errors[2] < errors[1] < errors[0]


def main() -> None:
    for y in [Fraction(1, 7), Fraction(1), Fraction(5, 2), Fraction(13)]:
        for deficiency in [Fraction(1, 5), Fraction(1), Fraction(11, 3)]:
            for even, odd in [
                (Fraction(2), Fraction(3)),
                (Fraction(-5, 4), Fraction(7, 9)),
                (Fraction(0), Fraction(11, 6)),
            ]:
                parity_factorization(y, deficiency, even, odd)
    projector_limit()
    print("HB-PENCIL-AUDIT: PASS (exact rational algebra; spectral sanity check)")


if __name__ == "__main__":
    main()

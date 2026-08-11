"""Lightweight algebra audit for Proposition 4.9.

This script checks only the elementary factorization and the finite-dimensional
spectral-projector limit used in the boundary Hermite--Biehler pencil.  The
real-zero input is Suzuki's Theorem 1.5, not a numerical claim made here.
The script is intentionally local-light: one process, negligible memory, and
well below one second on the desk machine.
"""

from __future__ import annotations

from fractions import Fraction

Gaussian = tuple[Fraction, Fraction]


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gdiv(left: Gaussian, right: Gaussian) -> Gaussian:
    denominator = right[0] ** 2 + right[1] ** 2
    return (
        (left[0] * right[0] + left[1] * right[1]) / denominator,
        (left[1] * right[0] - left[0] * right[1]) / denominator,
    )


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


def simple_kernel_cayley_check() -> None:
    one: Gaussian = Fraction(1), Fraction(0)
    imaginary_unit: Gaussian = Fraction(0), Fraction(1)
    for z in [Fraction(-7, 3), Fraction(2, 5), Fraction(11, 2)]:
        for c in [Fraction(1, 7), Fraction(3, 2), Fraction(9)]:
            z_gaussian: Gaussian = z, Fraction(0)
            ic: Gaussian = Fraction(0), c
            base_theta = gdiv(gsub(z_gaussian, ic), gadd(z_gaussian, ic))
            even_m = gmul(
                imaginary_unit,
                gdiv(gadd(one, base_theta), gsub(one, base_theta)),
            )
            odd_theta = -base_theta[0], -base_theta[1]
            odd_m = gmul(
                imaginary_unit,
                gdiv(gadd(one, odd_theta), gsub(one, odd_theta)),
            )
            assert even_m == (z / c, Fraction(0))
            assert odd_m == (-c / z, Fraction(0))


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
    simple_kernel_cayley_check()
    print("HB-PENCIL-AUDIT: PASS (exact rational algebra; spectral sanity check)")


if __name__ == "__main__":
    main()

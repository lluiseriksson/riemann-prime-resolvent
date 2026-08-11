"""Exact finite algebra for the arithmetic non-Blaschke Pick sequence.

The script audits (E93)--(E98a).  It does not test or assume RH.  Rational
weights stand in for arbitrary positive prime-power weights because every
identity checked here is coefficientwise in those weights.
"""

from __future__ import annotations

import math
from fractions import Fraction


def inner_product(
    left: list[Fraction], right: list[Fraction]
) -> Fraction:
    """L2(0,1) inner product of polynomials with no constant term."""

    return sum(
        left_degree * right_degree * Fraction(1, i + j + 1)
        for i, left_degree in enumerate(left, start=1)
        for j, right_degree in enumerate(right, start=1)
    )


def dilation(coefficients: list[Fraction], scale: Fraction) -> list[Fraction]:
    """Coefficients of p(scale*t)."""

    return [
        coefficient * scale**degree
        for degree, coefficient in enumerate(coefficients, start=1)
    ]


def moments(
    weighted_atoms: list[tuple[Fraction, Fraction]], count: int
) -> list[Fraction]:
    """Return m_n=sum weight*u^n for n=1,...,count."""

    return [
        sum(weight * atom**degree for atom, weight in weighted_atoms)
        for degree in range(1, count + 1)
    ]


def hilbert_anticommutator_quadratic(
    coefficients: list[Fraction], multiplier: list[Fraction]
) -> Fraction:
    """Evaluate c^T(D_l C+C D_l)c exactly."""

    return sum(
        ci
        * cj
        * (multiplier[i - 1] + multiplier[j - 1])
        * Fraction(1, i + j + 1)
        for i, ci in enumerate(coefficients, start=1)
        for j, cj in enumerate(coefficients, start=1)
    )


def prime_block_determinant(first: Fraction, second: Fraction) -> Fraction:
    """Determinant of P_ij=(m_i+m_j)/(i+j+1), i,j=1,2."""

    return (
        Fraction(2, 3) * first * Fraction(2, 5) * second
        - (first + second) ** 2 * Fraction(1, 16)
    )


def archimedean_two_by_two_upper() -> Fraction:
    """Rigorous rational upper bound for the determinant in (E98a)."""

    scale = 10**16
    euler_lower = Fraction(5_772_156_649_015_328, scale)
    euler_upper = Fraction(5_772_156_649_015_329, scale)
    log_two_lower = Fraction(6_931_471_805_599_453, scale)
    log_two_upper = Fraction(6_931_471_805_599_454, scale)
    log_pi_lower = Fraction(11_447_298_858_494_001, scale)
    log_pi_upper = Fraction(11_447_298_858_494_002, scale)

    a_one_lower = Fraction(3, 2) - (euler_upper + log_pi_upper) / 2
    a_one_upper = Fraction(3, 2) - (euler_lower + log_pi_lower) / 2
    a_two_lower = (
        Fraction(11, 6)
        - (euler_upper + log_pi_upper) / 2
        - log_two_upper
    )
    a_two_upper = (
        Fraction(11, 6)
        - (euler_lower + log_pi_lower) / 2
        - log_two_lower
    )
    assert Fraction(6_390, 10_000) < a_one_lower < a_one_upper < Fraction(6_391, 10_000)
    assert Fraction(2_792, 10_000) < a_two_lower < a_two_upper < Fraction(2_793, 10_000)
    return (
        Fraction(4, 15) * a_one_upper * a_two_upper
        - Fraction(1, 16) * (a_one_lower + a_two_lower) ** 2
    )


def audit() -> dict[str, object]:
    """Verify the exact multiplier identities and the size-two obstruction."""

    coefficients = [
        Fraction(3, 2),
        Fraction(-5, 3),
        Fraction(7, 4),
        Fraction(-2, 5),
    ]
    archimedean = [
        Fraction(11, 7),
        Fraction(13, 8),
        Fraction(17, 9),
        Fraction(19, 10),
    ]
    # All atoms lie in (0,1/2], exactly as u=1/r does for prime powers.
    weighted_atoms = [
        (Fraction(1, 2), Fraction(3, 1)),
        (Fraction(1, 3), Fraction(5, 2)),
        (Fraction(1, 5), Fraction(7, 3)),
        (Fraction(1, 8), Fraction(11, 4)),
    ]
    prime_moments = moments(weighted_atoms, len(coefficients))
    euler_multiplier = [
        arch - prime
        for arch, prime in zip(archimedean, prime_moments, strict=True)
    ]

    direct = hilbert_anticommutator_quadratic(coefficients, euler_multiplier)
    arch_form = inner_product(
        coefficients,
        [
            coefficient * value
            for coefficient, value in zip(coefficients, archimedean, strict=True)
        ],
    )
    prime_form = sum(
        weight * inner_product(coefficients, dilation(coefficients, atom))
        for atom, weight in weighted_atoms
    )
    operator_form = 2 * (arch_form - prime_form)
    assert direct == operator_form

    first, second = prime_moments[:2]
    ratio = second / first
    determinant = prime_block_determinant(first, second)
    factored = first**2 * (-15 * ratio**2 + 34 * ratio - 15) / 240
    assert determinant == factored
    assert 0 < ratio <= Fraction(1, 2)
    assert determinant < 0

    archimedean_determinant_upper = archimedean_two_by_two_upper()
    assert archimedean_determinant_upper < Fraction(-509, 100_000)

    partial_blaschke = sum(
        (n - 0.5) / (1.0 + (n - 0.5) ** 2) for n in range(1, 100_001)
    )
    return {
        "exact_operator_identity": direct == operator_form,
        "prime_moment_ratio": str(ratio),
        "prime_block_determinant": str(determinant),
        "prime_block_is_indefinite": determinant < 0,
        "archimedean_block_determinant_upper": str(
            archimedean_determinant_upper
        ),
        "archimedean_block_is_indefinite": True,
        "non_blaschke_partial_sum_N_100000": partial_blaschke,
        "partial_sum_over_log_N": partial_blaschke / math.log(100_000),
    }


if __name__ == "__main__":
    print(audit())

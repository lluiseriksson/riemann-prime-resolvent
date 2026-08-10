"""Audit the verified two-orbit Gram floor and off-line perturbation formula."""

from __future__ import annotations

import math

import numpy as np


def on_line_orbit_kernel(nodes: np.ndarray, zero_height: float) -> np.ndarray:
    """Return the rank-two kernel contributed by one on-line zero height."""

    points = np.asarray(nodes, dtype=float)
    gamma = float(zero_height)
    square = gamma * gamma
    return 2.0 * (points[:, None] * points[None, :] + square) / (
        (points[:, None] ** 2 + square) * (points[None, :] ** 2 + square)
    )


def two_orbit_gram_determinant_formula(
    nodes: np.ndarray, first_height: float, second_height: float
) -> float:
    """Return the exact Cauchy--Vandermonde determinant formula (E38)."""

    points = np.asarray(nodes, dtype=float)
    if points.shape != (4,) or np.any(np.diff(points) <= 0.0):
        raise ValueError("nodes must be four strictly increasing points")
    first = float(first_height)
    second = float(second_height)
    first_square = first * first
    second_square = second * second
    vandermonde = math.prod(
        points[right] - points[left]
        for left in range(4)
        for right in range(left + 1, 4)
    )
    denominator = float(
        np.prod((points * points + first_square) * (points * points + second_square))
    )
    root = (
        4.0
        * first
        * second
        * (second_square - first_square) ** 2
        * vandermonde
        / denominator
    )
    return root * root


def off_line_mass_perturbation(
    node: float, centered_real_part: float, zero_height: float
) -> float:
    """Difference between one off-line pair and two on-line surrogates."""

    x = float(node)
    alpha = float(centered_real_part)
    gamma = float(zero_height)
    a = alpha * alpha
    g = gamma * gamma
    base = x * x + g
    denominator = (base - a) ** 2 + 4.0 * a * g
    return 4.0 * x / base * a * (x * x - 3.0 * g - a) / denominator


def rational_zero_quadratic(
    nodes: np.ndarray, coefficients: np.ndarray, spectral_parameter: complex
) -> complex:
    """Return Q_c(w)=F_c(w)^2+w^2*G_c(w)^2 from (E42)."""

    points = np.asarray(nodes, dtype=float)
    vector = np.asarray(coefficients, dtype=float)
    parameter = complex(spectral_parameter)
    denominators = points * points + parameter * parameter
    first = np.sum(vector * points / denominators)
    second = np.sum(vector / denominators)
    return complex(first * first + parameter * parameter * second * second)


def grouped_off_line_kernel(
    nodes: np.ndarray, centered_real_part: float, zero_height: float
) -> np.ndarray:
    """Return the real kernel of one grouped off-line conjugate pair."""

    points = np.asarray(nodes, dtype=float)
    alpha = float(centered_real_part)
    gamma = float(zero_height)
    centered_zero = alpha + 1j * gamma
    denominators = points * points - centered_zero * centered_zero
    single = 2.0 * (
        points[:, None] * points[None, :] - centered_zero * centered_zero
    ) / (denominators[:, None] * denominators[None, :])
    return 2.0 * np.real(single)


def common_denominator_polynomials(
    nodes: np.ndarray, coefficients: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return ascending coefficients of P, A, B, S from (E45)."""

    points = np.asarray(nodes, dtype=float)
    vector = np.asarray(coefficients, dtype=float)
    factors = [np.asarray((point * point, 1.0)) for point in points]
    denominator = np.asarray((1.0,))
    for factor in factors:
        denominator = np.polynomial.polynomial.polymul(denominator, factor)
    first_numerator = np.zeros(4)
    second_numerator = np.zeros(4)
    for index, factor in enumerate(factors):
        quotient, remainder = np.polynomial.polynomial.polydiv(denominator, factor)
        assert np.max(np.abs(remainder)) < 1.0e-8
        first_numerator[: len(quotient)] += vector[index] * quotient
        second_numerator[: len(quotient)] += vector[index] * points[index] * quotient
    first_square = np.polynomial.polynomial.polymul(first_numerator, first_numerator)
    second_square = np.polynomial.polynomial.polymul(second_numerator, second_numerator)
    shifted_first_square = np.concatenate(([0.0], first_square))
    if len(second_square) < len(shifted_first_square):
        second_square = np.pad(
            second_square, (0, len(shifted_first_square) - len(second_square))
        )
    numerator = second_square + shifted_first_square
    return denominator, first_numerator, second_numerator, numerator


def audit() -> dict[str, float]:
    """Check (E38) and (E39) at representative nonsingular values."""

    nodes = np.asarray((0.6, 1.2, 3.0, 7.0))
    first = 14.134725
    second = 21.022040
    gram = on_line_orbit_kernel(nodes, first) + on_line_orbit_kernel(nodes, second)
    direct = float(np.linalg.det(gram))
    formula = two_orbit_gram_determinant_formula(nodes, first, second)
    assert math.isclose(direct, formula, rel_tol=3.0e-9)

    x, alpha, gamma = 3.0, 0.2, 100.0
    a, g = alpha * alpha, gamma * gamma
    base = x * x + g
    true_mass = 4.0 * x * (base - a) / ((base - a) ** 2 + 4.0 * a * g)
    surrogate_mass = 4.0 * x / base
    perturbation = off_line_mass_perturbation(x, alpha, gamma)
    assert math.isclose(true_mass - surrogate_mass, perturbation, rel_tol=1.0e-10)

    coefficients = np.asarray((0.7, -1.2, 0.4, 1.1))
    grouped = grouped_off_line_kernel(nodes, alpha, gamma)
    direct_quadratic = float(coefficients @ grouped @ coefficients)
    shifted_quadratic = 4.0 * rational_zero_quadratic(
        nodes, coefficients, gamma - 1j * alpha
    ).real
    assert math.isclose(direct_quadratic, shifted_quadratic, rel_tol=1.0e-12)

    denominator, _, _, numerator = common_denominator_polynomials(
        nodes, coefficients
    )
    parameter = 17.3
    square = parameter * parameter
    rational_from_polynomials = np.polynomial.polynomial.polyval(
        square, numerator
    ) / np.polynomial.polynomial.polyval(square, denominator) ** 2
    rational_direct = rational_zero_quadratic(nodes, coefficients, parameter).real
    assert math.isclose(rational_from_polynomials, rational_direct, rel_tol=1.0e-12)
    assert len(numerator) <= 8
    return {
        "direct_gram_determinant": direct,
        "formula_gram_determinant": formula,
        "mass_perturbation": perturbation,
        "grouped_off_line_quadratic": direct_quadratic,
        "complex_shift_quadratic": shifted_quadratic,
        "degree_seven_rational_check": rational_from_polynomials,
    }


if __name__ == "__main__":
    print(audit())

"""Finite algebra behind the signed prime-side Euler-axis Pick identity."""

from __future__ import annotations

import math

import numpy as np


def cauchy_dual(nodes: np.ndarray, coefficients: np.ndarray) -> np.ndarray:
    """Return d_i = sum_j c_j/(x_i+x_j)."""

    x = np.asarray(nodes, dtype=float)
    c = np.asarray(coefficients, dtype=float)
    return (1.0 / (x[:, None] + x[None, :])) @ c


def exponential_test(
    nodes: np.ndarray, coefficients: np.ndarray, coordinate: float
) -> float:
    """Return phi_c(t) from (E73)."""

    x = np.asarray(nodes, dtype=float)
    c = np.asarray(coefficients, dtype=float)
    dual = cauchy_dual(x, c)
    return float(np.dot(c * dual, np.exp(-x * coordinate)))


def resolvent_square(
    nodes: np.ndarray, coefficients: np.ndarray, frequency: complex
) -> complex:
    """Return the analytic Q_c(w)=F_c(w)^2+w^2 G_c(w)^2."""

    x = np.asarray(nodes, dtype=float)
    c = np.asarray(coefficients, dtype=float)
    denominator = x**2 + frequency**2
    f_value = np.sum(c * x / denominator)
    g_value = np.sum(c / denominator)
    return complex(f_value**2 + frequency**2 * g_value**2)


def cosine_transform_closed_form(
    nodes: np.ndarray, coefficients: np.ndarray, frequency: complex
) -> complex:
    """Evaluate 2 integral phi(t) cos(wt) dt in closed form."""

    x = np.asarray(nodes, dtype=float)
    c = np.asarray(coefficients, dtype=float)
    dual = cauchy_dual(x, c)
    return complex(2.0 * np.sum(c * dual * x / (x**2 + frequency**2)))


def finite_prime_quadratic(
    nodes: np.ndarray,
    coefficients: np.ndarray,
    logarithms: np.ndarray,
    weights: np.ndarray,
) -> tuple[float, float]:
    """Evaluate a finite prime block both as a matrix and through phi."""

    x = np.asarray(nodes, dtype=float)
    c = np.asarray(coefficients, dtype=float)
    logs = np.asarray(logarithms, dtype=float)
    mass = np.asarray(weights, dtype=float)
    matrix = np.zeros((len(x), len(x)))
    for coordinate, weight in zip(logs, mass, strict=True):
        decay = np.exp(-x * coordinate)
        matrix += weight * (
            decay[:, None] + decay[None, :]
        ) / (x[:, None] + x[None, :])
    direct = float(c @ matrix @ c)
    transformed = float(
        2.0
        * sum(
            weight * exponential_test(x, c, coordinate)
            for coordinate, weight in zip(logs, mass, strict=True)
        )
    )
    return direct, transformed


def centered_test_mass(
    nodes: np.ndarray, coefficients: np.ndarray
) -> tuple[float, float]:
    """Return both sides of the exact mass identity (E80)."""

    x = np.asarray(nodes, dtype=float)
    c = np.asarray(coefficients, dtype=float)
    dual = cauchy_dual(x, c)
    amplitudes = c * dual
    # Integral of -(x_i+1/2) a_i u^(-x_i-3/2) from one to infinity.
    integrated = float(np.sum(-(x + 0.5) * amplitudes / (x + 0.5)))
    return integrated, -float(np.sum(amplitudes))


def audit() -> dict[str, float]:
    """Check (E74)--(E76) on deterministic finite data."""

    nodes = np.array([0.7, 1.0, 1.4, 2.1, 3.0])
    coefficients = np.array([0.8, -1.2, 0.4, 1.1, -0.6])
    real_frequency = 7.25
    complex_frequency = 7.25 - 0.31j

    real_error = abs(
        resolvent_square(nodes, coefficients, real_frequency)
        - cosine_transform_closed_form(nodes, coefficients, real_frequency)
    )
    complex_error = abs(
        resolvent_square(nodes, coefficients, complex_frequency)
        - cosine_transform_closed_form(nodes, coefficients, complex_frequency)
    )
    prime_direct, prime_transformed = finite_prime_quadratic(
        nodes,
        coefficients,
        np.log(np.array([2.0, 3.0, 4.0, 5.0, 7.0])),
        np.array(
            [math.log(2.0), math.log(3.0), math.log(2.0), math.log(5.0), math.log(7.0)]
        )
        / np.sqrt(np.array([2.0, 3.0, 4.0, 5.0, 7.0])),
    )
    prime_error = abs(prime_direct - prime_transformed)
    integrated_mass, expected_mass = centered_test_mass(nodes, coefficients)
    mass_error = abs(integrated_mass - expected_mass)
    cauchy_mass = exponential_test(nodes, coefficients, 0.0)
    assert real_error < 1.0e-14
    assert complex_error < 1.0e-14
    assert prime_error < 1.0e-14
    assert mass_error < 1.0e-14
    assert cauchy_mass > 0.0
    return {
        "real_cosine_identity_error": real_error,
        "complex_cosine_identity_error": complex_error,
        "finite_prime_identity_error": prime_error,
        "centered_mass_identity_error": mass_error,
        "positive_cauchy_mass": cauchy_mass,
    }


if __name__ == "__main__":
    print(audit())

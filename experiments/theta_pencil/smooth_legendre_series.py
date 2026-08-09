"""Exact-power Legendre expansion of Suzuki's smooth convolution kernel."""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np


def _multiply_by_x(vector: np.ndarray) -> np.ndarray:
    result = np.zeros_like(vector)
    degrees = np.arange(len(vector) - 1)
    links = (degrees + 1.0) / np.sqrt(
        (2.0 * degrees + 1.0) * (2.0 * degrees + 3.0)
    )
    result[:-1] += links * vector[1:]
    result[1:] += links * vector[:-1]
    return result


def _monomial_vectors(maximum_power: int, size: int) -> list[np.ndarray]:
    vectors = [np.zeros(size)]
    vectors[0][0] = math.sqrt(2.0)
    for _ in range(maximum_power):
        vectors.append(_multiply_by_x(vectors[-1]))
    return vectors


def _definite_integral_standard_legendre(vector: np.ndarray) -> np.ndarray:
    """Coefficients of integral_-1^x f in the unnormalized P_n basis."""
    result = np.zeros(len(vector) + 1)
    result[0] += vector[0]
    result[1] += vector[0]
    for degree in range(1, len(vector)):
        result[degree + 1] += vector[degree] / (2 * degree + 1)
        result[degree - 1] -= vector[degree] / (2 * degree + 1)
    return result


def absolute_power_matrix(power: int, size: int) -> np.ndarray:
    """Matrix of the kernel integral operator |x-y|^power on (-1,1)."""
    if power < 0:
        raise ValueError("power must be nonnegative")
    if size < 1:
        raise ValueError("size must be positive")
    work_size = size + power + 2
    monomials = _monomial_vectors(power, work_size)
    result = np.zeros((size, size))

    # Polynomial kernel (x-y)^power.  It is the whole answer for even power,
    # and the correction to twice the left Volterra integral for odd power.
    polynomial = np.zeros_like(result)
    for left_power in range(power + 1):
        right_power = power - left_power
        coefficient = math.comb(power, left_power) * (-1.0) ** right_power
        polynomial += coefficient * np.outer(
            monomials[left_power][:size],
            monomials[right_power][:size],
        )
    if power % 2 == 0:
        return 0.5 * (polynomial + polynomial.T)

    for input_degree in range(size):
        standard = np.zeros(input_degree + 1)
        standard[input_degree] = math.sqrt((2 * input_degree + 1) / 2.0)
        for _ in range(power + 1):
            standard = _definite_integral_standard_legendre(standard)
        standard *= 2.0 * math.factorial(power)
        limit = min(size, len(standard))
        output_degrees = np.arange(limit)
        normalizations = np.sqrt((2.0 * output_degrees + 1.0) / 2.0)
        result[:limit, input_degree] = standard[:limit] / normalizations
    result -= polynomial
    return 0.5 * (result + result.T)


def _bernoulli_numbers(maximum: int) -> list[Fraction]:
    numbers: list[Fraction] = []
    work = [Fraction(0) for _ in range(maximum + 1)]
    for m in range(maximum + 1):
        work[m] = Fraction(1, m + 1)
        for j in range(m, 0, -1):
            work[j - 1] = j * (work[j - 1] - work[j])
        numbers.append(work[0])
    if maximum >= 1:
        numbers[1] = Fraction(-1, 2)
    return numbers


def _bernoulli_polynomial(n: int, x: Fraction) -> Fraction:
    numbers = _bernoulli_numbers(n)
    return sum(
        Fraction(math.comb(n, j)) * numbers[j] * x ** (n - j)
        for j in range(n + 1)
    )


def smooth_remainder_series_coefficients(maximum_power: int) -> tuple[Fraction, ...]:
    """Taylor coefficients of r''(t) for t >= 0 through given power."""
    coefficients = []
    for power in range(maximum_power + 1):
        n = power + 1
        h_coefficient = (
            _bernoulli_polynomial(n, Fraction(3, 4))
            * 2**power
            / math.factorial(n)
        )
        cosh_coefficient = Fraction(0)
        if power % 2 == 0:
            cosh_coefficient = -Fraction(2, 2**power * math.factorial(power))
        coefficients.append(h_coefficient + cosh_coefficient)
    return tuple(coefficients)


def smooth_kernel_series_matrix(
    half_width: float, size: int, maximum_power: int = 23
) -> np.ndarray:
    """Truncated exact-power matrix of -a r''(a|x-y|)."""
    coefficients = smooth_remainder_series_coefficients(maximum_power)
    result = np.zeros((size, size))
    for power, coefficient in enumerate(coefficients):
        result += (
            -half_width
            * float(coefficient)
            * half_width**power
            * absolute_power_matrix(power, size)
        )
    return 0.5 * (result + result.T)


def smooth_kernel_series_remainder_bound(
    half_width: float, maximum_power: int = 23
) -> float:
    """Certified Schur-norm bound for omitted powers when 2a <= 4/5."""
    if not 0.0 < half_width <= 0.4:
        raise ValueError("the registered rational tail bound applies for a <= 2/5")
    if maximum_power < 1:
        raise ValueError("maximum_power must be positive")
    # Bernoulli-polynomial Fourier bound with pi > 3 and 2a/pi <= 4/15.
    ratio = Fraction(4, 15)
    h_tail = Fraction(2, 3) * ratio ** (maximum_power + 1) / (1 - ratio)

    first_even = maximum_power + 1
    if first_even % 2:
        first_even += 1
    z = Fraction(2, 5)  # upper bound for t/2
    first_term = Fraction(2) * z**first_even / math.factorial(first_even)
    next_ratio = z * z / ((first_even + 1) * (first_even + 2))
    cosh_tail = first_term / (1 - next_ratio)
    kernel_supremum = half_width * float(h_tail + cosh_tail)
    return 2.0 * kernel_supremum


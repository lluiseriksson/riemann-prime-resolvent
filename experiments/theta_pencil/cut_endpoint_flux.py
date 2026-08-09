"""Endpoint-flux term in the cut-basis logarithmic residual."""

from __future__ import annotations

import math

import numpy as np

from experiments.theta_pencil.cut_adapted_prime_basis import first_prime_partition


def endpoint_flux_maps(half_width: float, degree_count: int) -> np.ndarray:
    """Return the (F_plus,F_minus) row maps for all three intervals.

    Coordinates are ordered left, center, right.  The maps include the
    sqrt(length/2) factor converting normalized Legendre coefficients on
    (-1,1) to normalized local coefficients on the physical interval.
    """

    if degree_count < 1:
        raise ValueError("degree_count must be positive")
    partition = first_prime_partition(half_width)
    intervals = (partition.left, partition.center, partition.right)
    lengths = np.array([right - left for left, right in intervals])
    endpoint_minus = []
    endpoint_plus = []
    degrees = np.arange(degree_count)
    for block, length in enumerate(lengths):
        minus = np.zeros(3 * degree_count)
        plus = np.zeros(3 * degree_count)
        normalization = np.sqrt((2 * degrees + 1) / length)
        interval = slice(block * degree_count, (block + 1) * degree_count)
        minus[interval] = normalization * (-1.0) ** degrees
        plus[interval] = normalization
        endpoint_minus.append(minus)
        endpoint_plus.append(plus)

    flux = np.empty((3, 2, 3 * degree_count))
    flux[0, 0] = math.sqrt(lengths[0] / 2.0) * (
        endpoint_plus[0] - endpoint_minus[1]
    )
    flux[0, 1] = -math.sqrt(lengths[0] / 2.0) * endpoint_minus[0]
    flux[1, 0] = math.sqrt(lengths[1] / 2.0) * (
        endpoint_plus[1] - endpoint_minus[2]
    )
    flux[1, 1] = math.sqrt(lengths[1] / 2.0) * (
        endpoint_plus[0] - endpoint_minus[1]
    )
    flux[2, 0] = math.sqrt(lengths[2] / 2.0) * endpoint_plus[2]
    flux[2, 1] = math.sqrt(lengths[2] / 2.0) * (
        endpoint_plus[1] - endpoint_minus[2]
    )
    return flux


def endpoint_flux_tail_psd_upper(
    half_width: float, degree_count: int, first_degree: int
) -> np.ndarray:
    """PSD upper bound for the infinite leading-flux Gram matrix.

    Integration by parts gives coefficient weight

      w_n^2 = (2n+1)/(2 n^2 (n+1)^2)
            = (1/2)(n^-2-(n+1)^-2).

    Hence sum_{n>=N} w_n^2=1/(2N^2).  Applying
    |F_plus-(-1)^n F_minus|^2 <= 2(|F_plus|^2+|F_minus|^2)
    yields the returned matrix in Loewner order.
    """

    if first_degree < 1:
        raise ValueError("first_degree must be positive")
    flux = endpoint_flux_maps(half_width, degree_count)
    gram = np.zeros((3 * degree_count, 3 * degree_count))
    for plus, minus in flux:
        gram += (
            np.outer(plus, plus) + np.outer(minus, minus)
        ) / first_degree**2
    return 0.5 * (gram + gram.T)

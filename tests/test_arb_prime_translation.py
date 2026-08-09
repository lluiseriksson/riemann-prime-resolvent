import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss

from experiments.theta_pencil.arb_prime_translation import (
    build_arb_prime_two_matrix,
)
from experiments.theta_pencil.legendre_feshbach import normalized_legendre_values


def test_arb_prime_matrix_encloses_independent_gauss_values():
    pytest.importorskip("flint")
    low = 8
    maximum = 32
    result = build_arb_prime_two_matrix(0.4, low, maximum, precision=512)
    shift = np.log(2.0) / 0.4
    cut = 1.0 - shift
    nodes, weights = leggauss(40)
    x = (cut + 1.0) * nodes / 2.0 + (cut - 1.0) / 2.0
    scaled = weights * (cut + 1.0) / 2.0
    at_x = normalized_legendre_values(x, maximum)
    at_shift = normalized_legendre_values(x + shift, maximum)
    direct = -np.log(2.0) / np.sqrt(2.0) * (
        (at_shift[:low] * scaled) @ at_x.T
        + (at_x[:low] * scaled) @ at_shift.T
    )
    error = np.abs(result.midpoint - direct)
    assert np.max(error) < 2e-13
    assert np.max(result.radius) < 1e-40


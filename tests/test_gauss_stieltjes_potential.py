import math

import numpy as np

from experiments.theta_pencil.gauss_stieltjes_potential import (
    chebyshev_multiplication_compression,
    chebyshev_multiplication_compression_gauss,
    endpoint_value,
    gauss_stieltjes_chebyshev,
    gauss_stieltjes_increment,
    gauss_stieltjes_jacobi_value,
    gauss_stieltjes_rational_value,
    harmonic,
    markov_remainder_value,
)


def test_gauss_endpoint_is_harmonic_before_uniform_subtraction():
    data = gauss_stieltjes_chebyshev(8, 128)
    assert abs((endpoint_value(data) + data.uniform_error) - harmonic(8)) < 2e-14
    assert 0.0 < data.uniform_error < 2e-16


def test_enlarged_jacobi_and_degree_exact_gauss_compressions_agree():
    data = gauss_stieltjes_chebyshev(5, 24)
    jacobi = chebyshev_multiplication_compression(data.coefficients, 18)
    gauss = chebyshev_multiplication_compression_gauss(data.coefficients, 18)
    assert np.max(np.abs(jacobi - gauss)) < 5e-14


def test_markov_remainder_factorization():
    points = np.array([0.1, 0.35, 0.7, 0.9, 0.97])
    direct = -0.5 * np.log1p(-points**2) - gauss_stieltjes_rational_value(
        points, 8
    )
    markov = markov_remainder_value(points, 8, 320)
    assert np.all(markov > 0.0)
    assert np.max(np.abs(direct - markov)) < 4e-14


def test_markov_remainder_starts_at_the_predicted_order():
    order = 3
    x1 = 0.01
    x2 = 0.02
    first = float(markov_remainder_value(x1, order, 128))
    second = float(markov_remainder_value(x2, order, 128))
    predicted_ratio = (x2 / x1) ** (4 * order + 2)
    assert math.isclose(second / first, predicted_ratio, rel_tol=2e-3)


def test_jacobi_resolvent_equals_gauss_rule():
    for order in (1, 2, 4, 8):
        for point in (0.2, 0.6, 0.93):
            direct = float(gauss_stieltjes_rational_value(point, order))
            jacobi = gauss_stieltjes_jacobi_value(point, order)
            assert math.isclose(jacobi, direct, rel_tol=2e-14, abs_tol=2e-15)


def test_added_jacobi_dimension_is_an_exact_positive_square():
    for order in (1, 2, 4, 8):
        for point in (0.2, 0.6, 0.93):
            increment = gauss_stieltjes_increment(point, order)
            direct = gauss_stieltjes_jacobi_value(
                point, order + 1
            ) - gauss_stieltjes_jacobi_value(point, order)
            assert increment > 0.0
            assert math.isclose(increment, direct, rel_tol=2e-11, abs_tol=2e-15)

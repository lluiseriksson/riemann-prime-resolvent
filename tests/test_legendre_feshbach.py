import numpy as np
import pytest

from experiments.theta_pencil.legendre_feshbach import (
    build_legendre_weil_components,
    feshbach_audit,
    normalized_legendre_values,
    smooth_remainder_second_array,
)


def test_normalized_legendre_basis_is_orthonormal_under_gauss_rule():
    nodes, weights = np.polynomial.legendre.leggauss(32)
    basis = normalized_legendre_values(nodes, 16)
    gram = (basis * weights) @ basis.T
    assert gram == pytest.approx(np.eye(16), abs=2e-14)


def test_remainder_second_removable_value_and_symmetry():
    values = np.array([-0.3, -1e-8, 0.0, 1e-8, 0.3])
    result = smooth_remainder_second_array(values)
    assert result == pytest.approx(result[::-1], abs=1e-14)
    assert result[2] == -7.0 / 4.0


def test_first_prime_activates_across_threshold():
    below = build_legendre_weil_components(0.34, 8, 64)
    above = build_legendre_weil_components(0.4, 8, 64)
    assert below.active_prime_powers == ()
    assert above.active_prime_powers == (2,)
    assert np.linalg.norm(below.prime) == 0.0
    assert np.linalg.norm(above.prime) > 0.0


def test_finite_feshbach_identity_and_scalar_bound_gap():
    audit = feshbach_audit(0.4, 32, 16, 128)
    assert audit.full_ritz > 0.0
    assert audit.tail_ritz > 0.0
    assert audit.scalar_schur_bound < 0.0
    assert audit.exact_finite_schur_ritz > 0.0


import numpy as np
import pytest

from experiments.theta_pencil.arb_support_one_source import (
    ACTIVE_SUPPORT_ONE_PRIME_POWERS,
    build_arb_support_one_source,
    certify_arb_support_one_positive_subspaces,
)
from experiments.theta_pencil.legendre_feshbach import (
    build_legendre_weil_components,
)
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_matrix,
)


def test_small_arb_support_one_source_matches_point_builder():
    pytest.importorskip("flint")
    source = build_arb_support_one_source(
        dimension=4,
        maximum_smooth_power=3,
        precision=192,
        prime_precision=256,
    )
    components = build_legendre_weil_components(1.0, 4, 32)
    target = (
        components.dominant
        + components.scalar
        + components.prime
        + smooth_kernel_series_matrix(1.0, 4, 3)
    )
    assert source.active_prime_powers == ACTIVE_SUPPORT_ONE_PRIME_POWERS
    assert np.max(np.abs(source.midpoint - target)) < 1.0e-12
    assert np.all(source.radius >= 0.0)
    assert np.max(np.abs(source.even_midpoint - source.even_midpoint.T)) == 0.0
    assert np.max(np.abs(source.odd_midpoint - source.odd_midpoint.T)) == 0.0


def test_small_arb_source_certifies_selected_positive_subspaces():
    pytest.importorskip("flint")
    source = build_arb_support_one_source(
        dimension=6,
        maximum_smooth_power=5,
        precision=256,
        prime_precision=384,
    )
    certificate = certify_arb_support_one_positive_subspaces(
        source,
        even_positive_count=1,
        odd_positive_count=1,
        precision=256,
    )
    assert certificate.even_certificate.original_spectral_lower > 0.0
    assert certificate.odd_certificate.original_spectral_lower > 0.0
    assert "Schur correction is omitted" in certificate.context

    with pytest.raises(ValueError, match="not positive even at the midpoint"):
        certify_arb_support_one_positive_subspaces(
            source,
            even_positive_count=2,
            odd_positive_count=1,
            precision=256,
        )

import numpy as np
import pytest

from experiments.theta_pencil.arb_third_window_flux_gram import (
    build_arb_third_window_flux_gram,
)
from experiments.theta_pencil.arb_third_window_self_gram import (
    _self_cache_metadata,
    build_arb_third_window_self_gram,
    load_third_window_self_gram,
)
from experiments.theta_pencil.arb_third_window_singular_gram import (
    build_arb_third_window_singular_gram,
)
from experiments.theta_pencil.arb_third_window_near_tail_gram import (
    build_arb_third_window_near_tail_gram,
)
from experiments.theta_pencil.arb_third_window_other_tail import (
    certify_third_window_other_tail,
)


@pytest.mark.parametrize(
    "builder,kwargs",
    [
        (
            build_arb_third_window_flux_gram,
            dict(
                half_width=0.7,
                edge_degree=2,
                bridge_degree=2,
                center_degree=2,
                first_degree=4,
                explicit_end=32,
                precision=256,
            ),
        ),
        (
            build_arb_third_window_self_gram,
            dict(
                edge_degree=2,
                bridge_degree=2,
                center_degree=2,
                first_degree=4,
                explicit_end=32,
                remainder_end=128,
                precision=256,
            ),
        ),
        (
            build_arb_third_window_singular_gram,
            dict(
                half_width=0.7,
                edge_degree=2,
                bridge_degree=2,
                center_degree=2,
                first_degree=4,
                last_degree=32,
                moment_order=3,
                precision=256,
            ),
        ),
    ],
)
def test_third_window_directional_grams_are_positive_semidefinite(builder, kwargs):
    pytest.importorskip("flint")
    result = builder(**kwargs)
    for midpoint, radius in (
        (result.even_midpoint, result.even_radius),
        (result.odd_midpoint, result.odd_radius),
    ):
        assert np.max(np.abs(midpoint - midpoint.T)) < 1e-14
        assert np.min(np.linalg.eigvalsh(midpoint)) > -1e-14
        assert np.all(radius >= 0)
    assert result.remainder_norm_upper >= 0


def test_third_window_near_tail_keeps_complete_rows_before_squaring():
    pytest.importorskip("flint")
    result = build_arb_third_window_near_tail_gram(
        half_width=0.7,
        edge_degree=1,
        bridge_degree=1,
        center_degree=1,
        first_degree=2,
        last_degree=8,
        precision=256,
        maximum_smooth_power=3,
    )
    for midpoint, radius in (
        (result.even_midpoint, result.even_radius),
        (result.odd_midpoint, result.odd_radius),
    ):
        assert np.max(np.abs(midpoint - midpoint.T)) < 1e-13
        assert np.min(np.linalg.eigvalsh(midpoint)) > -1e-12
        assert np.all(radius >= 0)
    assert result.working_precision >= result.precision


def test_third_window_other_tail_is_finite_after_directional_extraction():
    pytest.importorskip("flint")
    result = certify_third_window_other_tail(
        half_width=0.7,
        edge_degree=2,
        bridge_degree=2,
        center_degree=2,
        first_degree=16,
        explicit_end=64,
        precision=256,
        include_self_blocks=False,
    )
    assert result.comparison_matrix.shape == (13, 13)
    assert np.all(result.comparison_matrix >= 0)
    assert 0 <= result.spectral_norm_upper <= result.row_column_upper


def test_third_window_self_gram_cache_round_trip(tmp_path):
    pytest.importorskip("flint")
    cache = tmp_path / "self-tail.npz"
    first = build_arb_third_window_self_gram(
        2, 2, 2, 8, 16, 32, 192, cache
    )
    metadata = _self_cache_metadata(2, 2, 2, 8, 16, 32, 192)
    loaded = load_third_window_self_gram(cache, metadata)
    assert loaded is not None
    assert loaded.remainder_norm_upper == first.remainder_norm_upper
    assert np.array_equal(loaded.even_midpoint, first.even_midpoint)
    second = build_arb_third_window_self_gram(
        2, 2, 2, 8, 16, 32, 192, cache
    )
    assert np.array_equal(second.odd_radius, first.odd_radius)

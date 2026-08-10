import numpy as np
import pytest

from experiments.theta_pencil.arb_second_window_flux_gram import (
    build_arb_second_window_flux_gram,
)


def _reflection(degree: int) -> np.ndarray:
    matrix = np.zeros((7 * degree, 7 * degree))
    for block in range(7):
        for local_degree in range(degree):
            matrix[
                (6 - block) * degree + local_degree,
                block * degree + local_degree,
            ] = -1.0 if local_degree % 2 else 1.0
    return matrix


def test_second_window_flux_gram_respects_reflection_and_is_psd():
    pytest.importorskip("flint")
    result = build_arb_second_window_flux_gram(
        0.56,
        edge_degree=2,
        bridge_degree=2,
        center_degree=2,
        first_degree=4,
        explicit_end=32,
        precision=256,
    )
    reflection = _reflection(2)
    assert np.max(
        np.abs(reflection.T @ result.midpoint @ reflection - result.midpoint)
    ) < 1e-12
    assert np.linalg.eigvalsh(result.midpoint)[0] > -1e-12
    full = np.linalg.eigvalsh(result.midpoint)
    parity = np.sort(
        np.concatenate(
            (
                np.linalg.eigvalsh(result.even_midpoint),
                np.linalg.eigvalsh(result.odd_midpoint),
            )
        )
    )
    assert np.max(np.abs(full - parity)) < 1e-12
    assert result.remainder_norm_upper > 0


def test_second_window_flux_gram_dominates_a_longer_direct_sum():
    pytest.importorskip("flint")
    from flint import arb, arb_mat, ctx

    from experiments.theta_pencil.arb_second_window_flux_gram import (
        _endpoint_rows,
    )
    from experiments.theta_pencil.arb_second_window_source import (
        _arb_lengths,
        _degree_pattern,
        _offsets,
    )

    result = build_arb_second_window_flux_gram(
        0.56,
        edge_degree=2,
        bridge_degree=2,
        center_degree=2,
        first_degree=4,
        explicit_end=32,
        precision=256,
    )
    previous_precision = ctx.prec
    try:
        ctx.prec = 256
        _, lengths = _arb_lengths(arb, 0.56)
        degrees = _degree_pattern(2, 2, 2)
        rows = _endpoint_rows(
            arb, arb_mat, lengths, degrees, _offsets(degrees)
        )
        direct = np.zeros_like(result.midpoint)
        for degree in range(4, 20_000):
            weight = (2 * degree + 1) / (
                2.0 * degree**2 * (degree + 1) ** 2
            )
            for positive, negative in rows:
                row = np.array(
                    [
                        float(
                            (
                                positive[0, index]
                                - (-1 if degree % 2 else 1)
                                * negative[0, index]
                            ).mid()
                        )
                        for index in range(result.midpoint.shape[0])
                    ]
                )
                direct += weight * np.outer(row, row)
    finally:
        ctx.prec = previous_precision

    rng = np.random.default_rng(314159)
    for _ in range(12):
        vector = rng.normal(size=result.midpoint.shape[0])
        assert vector @ direct @ vector <= (
            vector @ result.midpoint @ vector + 2e-12
        )

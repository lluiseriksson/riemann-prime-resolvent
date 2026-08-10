import pytest

from experiments.theta_pencil.harmonic_schur_stratification import (
    build_harmonic_schur_stratification,
)


def test_harmonic_stratification_has_registered_relative_overcharge():
    result = build_harmonic_schur_stratification(
        12, 8192, 0.220973215897795, 0.25
    )
    assert result.boundaries[0] == 12
    assert result.boundaries[-1] == 8192
    assert result.maximum_denominator_ratio <= 1.25
    assert len(result.denominator_starts) <= result.band_count_logarithmic_upper
    assert len(result.denominator_starts) == 14


@pytest.mark.parametrize(
    "arguments",
    [
        (0, 10, 1.0, 0.1),
        (10, 10, 1.0, 0.1),
        (1, 10, 0.0, 0.1),
        (1, 10, 1.0, 0.0),
    ],
)
def test_harmonic_stratification_rejects_invalid_inputs(arguments):
    with pytest.raises(ValueError):
        build_harmonic_schur_stratification(*arguments)

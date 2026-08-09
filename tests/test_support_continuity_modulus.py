import numpy as np

from experiments.theta_pencil.support_continuity_modulus import (
    HLOG_FROM_DOMINANT_CONSTANT,
    hlog_energy_from_dominant,
    log10_displacement_for_resolution,
    required_logarithmic_resolution,
    translation_difference_upper,
)


def test_pointwise_fourier_multiplier_inequality():
    for delta in (1e-6, 1e-3, 0.1, 0.7):
        frequencies = np.geomspace(1e-8, 1e8, 10000)
        left = np.minimum(4.0, delta**2 * frequencies**2)
        right = (
            4.0
            * np.log1p(frequencies**2)
            / np.log1p(delta**-2)
        )
        assert np.max(left - right) < 1e-12


def test_registered_support_modulus_is_quantitatively_too_weak():
    dominant = 5.047850307074702 + 7.42373609443714e-5
    energy = hlog_energy_from_dominant(dominant)
    assert abs(HLOG_FROM_DOMINANT_CONSTANT - 0.8119553954920423) < 1e-15
    assert abs(energy - 10.907804484363336) < 1e-14
    coefficient = np.log(2.0) / np.sqrt(2.0)
    required = required_logarithmic_resolution(
        coefficient, energy, 7.117220758560887e-5
    )
    assert 8.27e9 < required < 8.28e9
    assert log10_displacement_for_resolution(required) < -1.79e9


def test_translation_modulus_vanishes_only_logarithmically():
    assert translation_difference_upper(0.0, 3.0) == 0.0
    assert translation_difference_upper(1e-100, 3.0) > 0.1

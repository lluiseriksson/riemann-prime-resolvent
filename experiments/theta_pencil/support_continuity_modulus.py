"""Quantitative H^log modulus for the moving prime-translation cut."""

from __future__ import annotations

import math

from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA


HLOG_FROM_DOMINANT_CONSTANT = (
    4.0 / math.pi - 2.0 * EULER_GAMMA + math.log(2.0)
)


def hlog_energy_from_dominant(
    dominant_energy: float, norm_squared: float = 1.0
) -> float:
    """Bound the log(1+xi^2) Fourier energy of a function on [-1,1]."""
    if dominant_energy < 0.0 or norm_squared < 0.0:
        raise ValueError("energies and squared norms must be nonnegative")
    return (
        2.0 * dominant_energy
        + HLOG_FROM_DOMINANT_CONSTANT * norm_squared
    )


def translation_difference_upper(
    displacement_difference: float,
    hlog_energy: float,
    norm: float = 1.0,
) -> float:
    """Bound the quadratic-form change of tau_h + tau_h^*.

    The result is ``4 norm sqrt(E_log / log(1 + delta^-2))``.  It controls
    the zero-extended translations and therefore their compressions to
    ``L^2(-1,1)``.
    """
    delta = abs(displacement_difference)
    if delta == 0.0:
        return 0.0
    if hlog_energy < 0.0 or norm < 0.0:
        raise ValueError("energy and norm must be nonnegative")
    logarithm = math.log1p(delta ** -2)
    return 4.0 * norm * math.sqrt(hlog_energy / logarithm)


def required_logarithmic_resolution(
    coefficient: float,
    hlog_energy: float,
    margin: float,
    norm: float = 1.0,
) -> float:
    """Required value of log(1+delta^-2) to protect ``margin``."""
    if coefficient < 0.0 or hlog_energy < 0.0 or norm < 0.0:
        raise ValueError("coefficient, energy, and norm must be nonnegative")
    if margin <= 0.0:
        raise ValueError("margin must be positive")
    return (4.0 * coefficient * norm) ** 2 * hlog_energy / margin**2


def log10_displacement_for_resolution(required_logarithm: float) -> float:
    """Return log10 of the largest delta allowed by a logarithmic budget."""
    if required_logarithm <= 0.0:
        raise ValueError("required logarithm must be positive")
    if required_logarithm > 50.0:
        natural_log_delta = -0.5 * required_logarithm
    else:
        natural_log_delta = -0.5 * math.log(math.expm1(required_logarithm))
    return natural_log_delta / math.log(10.0)

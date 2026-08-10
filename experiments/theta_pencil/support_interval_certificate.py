"""A quantitative open support interval from one localized positivity point."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from experiments.theta_pencil.smooth_legendre_series import (
    smooth_remainder_series_coefficients,
)


@dataclass(frozen=True)
class SupportIntervalCertificate:
    center: float
    neighborhood_lower: float
    neighborhood_upper: float
    point_lower: float
    certified_interval_lower: float
    smooth_kernel_supremum_upper: float
    smooth_radial_derivative_upper: float
    bounded_perturbation_upper: float
    hlog_constant_upper: float
    prime_coefficient_upper: float
    relative_eta: float
    required_logarithm: float
    regular_radius_lower: float
    decimal_radius_exponent: int
    precision: int


def _float_upper(value) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def _float_lower(value) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def _smooth_series_supremum(
    maximum_argument: float,
    *,
    radial_derivative: bool,
    maximum_power: int = 23,
) -> float:
    """Bound ``|r''|`` or ``|r'' + t r'''|`` on ``[0,T]``.

    The finite Taylor coefficients are exact rationals.  The omitted
    Bernoulli-polynomial part uses ``|c_p| <= (2/3) 3^-p`` and the cosh part
    uses its factorial series.  Multiplication by ``p+1`` gives the radial
    derivative bound.
    """

    if not 0.0 < maximum_argument < 3.0:
        raise ValueError("the series majorant requires 0 < T < 3")
    if maximum_power < 3:
        raise ValueError("maximum_power must be at least three")
    t = Fraction(str(maximum_argument))
    coefficients = smooth_remainder_series_coefficients(maximum_power)
    finite = Fraction(0)
    for power, coefficient in enumerate(coefficients):
        weight = power + 1 if radial_derivative else 1
        finite += weight * abs(coefficient) * t**power

    first = maximum_power + 1
    ratio = t / 3
    if radial_derivative:
        bernoulli_tail = (
            Fraction(2, 3)
            * ratio**first
            * (first + 1 - first * ratio)
            / (1 - ratio) ** 2
        )
    else:
        bernoulli_tail = Fraction(2, 3) * ratio**first / (1 - ratio)

    z = t / 2
    if radial_derivative:
        first_cosh = (
            2 * (first + 1) * z**first / math.factorial(first)
        )
        next_ratio = z * Fraction(first + 2, (first + 1) ** 2)
    else:
        first_cosh = 2 * z**first / math.factorial(first)
        next_ratio = z / (first + 1)
    cosh_tail = first_cosh / (1 - next_ratio)
    return math.nextafter(float(finite + bernoulli_tail + cosh_tail), math.inf)


def certify_support_054_interval(
    point_lower: float = 7.13337959131472e-9,
    precision: int = 256,
) -> SupportIntervalCertificate:
    """Certify positivity on an explicit (very small) interval about 0.54.

    If ``N`` is the returned ``decimal_radius_exponent``, the conclusion is
    ``A_a >= certified_interval_lower I`` whenever
    ``|a-0.54| <= 10^-N``.  The tiny radius is a theorem, not a claim that the
    true positive interval is comparably small.
    """

    if point_lower <= 0:
        raise ValueError("point_lower must be positive")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        center = arb("0.54")
        lower = arb("0.53")
        upper = arb("0.545")
        margin = arb(str(point_lower))
        log_two = arb.const_log2()
        prime = log_two / arb(2).sqrt()
        hlog_constant = 4 / arb.pi() - 2 * arb.const_euler() + log_two
        if not hlog_constant.lower() > 0:
            raise ArithmeticError("the H-log comparison constant was unresolved")

        maximum_argument = 2 * _float_upper(upper)
        smooth_supremum = _smooth_series_supremum(
            maximum_argument, radial_derivative=False
        )
        smooth_radial = _smooth_series_supremum(
            maximum_argument, radial_derivative=True
        )

        scalar = -center.log() - (2 * arb.pi()).log() - arb.const_euler()
        perturbation = (
            scalar.abs_upper()
            + 2 * prime.abs_upper()
            + 2 * center * arb(str(smooth_supremum))
        )
        perturbation_upper = _float_upper(perturbation)
        perturbation_ball = arb(str(perturbation_upper))

        # Four losses receive one fifth of the point margin: the relative
        # scale-free-form term, the Young term, the H-log scalar term, and the
        # ordinary scalar/smooth parameter variation. One fifth remains.
        eta_ball = margin / (5 * (margin + perturbation_ball))
        eta = _float_lower(eta_ball)
        if eta <= 0:
            raise ArithmeticError("the relative-form parameter was unresolved")
        eta_lower = arb(str(eta))
        prime_upper = arb(str(_float_upper(prime)))
        hlog_upper = arb(str(_float_upper(hlog_constant)))
        young_resolution = 40 * prime_upper**2 / (eta_lower * margin)
        scalar_resolution = (
            20 * prime_upper * hlog_upper.sqrt() / margin
        ) ** 2
        required_logarithm = max(
            _float_upper(young_resolution), _float_upper(scalar_resolution)
        )
        registered_resolution = arb(str(required_logarithm))
        budget_piece = margin / 5
        relative_loss = eta_lower * (margin + perturbation_ball)
        young_loss = 8 * prime_upper**2 / (
            eta_lower * registered_resolution
        )
        scalar_loss = (
            4 * prime_upper * hlog_upper.sqrt() / registered_resolution.sqrt()
        )
        for name, loss in (
            ("relative", relative_loss),
            ("Young", young_loss),
            ("H-log scalar", scalar_loss),
        ):
            if not loss.upper() <= budget_piece.lower():
                raise ArithmeticError(f"the {name} continuity budget did not close")

        ordinary_lipschitz = 1 / lower + 2 * arb(str(smooth_radial))
        regular_radius = margin / (5 * ordinary_lipschitz)
        regular_radius_lower = _float_lower(regular_radius)
        if regular_radius_lower <= 0:
            raise ArithmeticError("the ordinary parameter radius was unresolved")

        # For |a-a0| <= r inside the registered neighbourhood,
        # |log(2)/a-log(2)/a0| <= log(2) r/(a_min a0).
        conversion = lower * center / log_two
        exponent_translation = (
            arb(str(required_logarithm)) / 2 - conversion.log()
        ) / arb(10).log()
        exponent_regular = -regular_radius.log() / arb(10).log()
        exponent_neighborhood = -(arb("0.005").log()) / arb(10).log()
        exponent = max(
            exponent_translation, exponent_regular, exponent_neighborhood
        )
        exponent_upper = math.nextafter(float(exponent.upper()), math.inf)
        decimal_exponent = math.ceil(exponent_upper)
        if not arb(decimal_exponent).lower() >= exponent.upper():
            raise ArithmeticError("the decimal radius exponent was not outward")
        certified_lower = _float_lower(margin / 5)
    finally:
        ctx.prec = previous_precision

    return SupportIntervalCertificate(
        center=0.54,
        neighborhood_lower=0.53,
        neighborhood_upper=0.545,
        point_lower=point_lower,
        certified_interval_lower=certified_lower,
        smooth_kernel_supremum_upper=smooth_supremum,
        smooth_radial_derivative_upper=smooth_radial,
        bounded_perturbation_upper=perturbation_upper,
        hlog_constant_upper=_float_upper(hlog_constant),
        prime_coefficient_upper=_float_upper(prime),
        relative_eta=eta,
        required_logarithm=required_logarithm,
        regular_radius_lower=regular_radius_lower,
        decimal_radius_exponent=decimal_exponent,
        precision=precision,
    )

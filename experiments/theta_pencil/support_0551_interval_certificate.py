"""Open support interval after both prime two and prime three activate."""

from __future__ import annotations

import math
from dataclasses import dataclass

from experiments.theta_pencil.support_interval_certificate import (
    _float_lower,
    _float_upper,
    _smooth_series_supremum,
)


@dataclass(frozen=True)
class TwoPrimeSupportIntervalCertificate:
    center: float
    neighborhood_lower: float
    neighborhood_upper: float
    point_lower: float
    certified_interval_lower: float
    smooth_kernel_supremum_upper: float
    smooth_radial_derivative_upper: float
    bounded_perturbation_upper: float
    hlog_constant_upper: float
    prime_coefficient_sum_upper: float
    relative_eta: float
    required_logarithm: float
    regular_radius_lower: float
    decimal_radius_exponent: int
    precision: int


# Backward-compatible public name for the first registered two-prime anchor.
Support0551IntervalCertificate = TwoPrimeSupportIntervalCertificate


def certify_support_0551_interval(
    point_lower: float = 1.3163321231312722e-9,
    precision: int = 256,
) -> TwoPrimeSupportIntervalCertificate:
    """Certify a two-prime open interval around ``a = 0.551``.

    If ``N`` is the returned decimal exponent, then
    ``A_a >= point_lower / 5`` for ``|a - 0.551| <= 10^-N``.  The registered
    neighbourhood lies strictly between the prime-three and prime-four
    activation thresholds, so its arithmetic part contains exactly the
    translations attached to 2 and 3.
    """

    return _certify_two_prime_support_interval(
        center_text="0.551",
        lower_text="0.55",
        upper_text="0.56",
        point_lower=point_lower,
        precision=precision,
    )


def _certify_two_prime_support_interval(
    *,
    center_text: str,
    lower_text: str,
    upper_text: str,
    point_lower: float,
    precision: int,
) -> TwoPrimeSupportIntervalCertificate:
    """Common continuation theorem inside the fixed two-prime window."""

    if point_lower <= 0:
        raise ValueError("point_lower must be positive")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        center = arb(center_text)
        lower = arb(lower_text)
        upper = arb(upper_text)
        if not lower.upper() < center.lower() or not center.upper() < upper.lower():
            raise ValueError("the centre must lie inside the neighbourhood")
        if not lower.lower() > (arb(3).log() / 2).upper():
            raise ArithmeticError("the neighbourhood crosses the prime-three threshold")
        if not upper.upper() < arb.const_log2().lower():
            raise ArithmeticError("the neighbourhood crosses the prime-four threshold")

        margin = arb(str(point_lower))
        log_two = arb.const_log2()
        log_three = arb(3).log()
        prime_two = log_two / arb(2).sqrt()
        prime_three = log_three / arb(3).sqrt()
        prime_sum = prime_two + prime_three
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
            + 2 * prime_sum
            + 2 * center * arb(str(smooth_supremum))
        )
        perturbation_upper = _float_upper(perturbation)
        perturbation_ball = arb(str(perturbation_upper))

        # As in the first-window continuation theorem, four independent
        # losses receive one fifth of the point margin.  Both prime terms are
        # combined before Young's inequality through p_2 + p_3.
        eta_ball = margin / (5 * (margin + perturbation_ball))
        eta = _float_lower(eta_ball)
        if eta <= 0:
            raise ArithmeticError("the relative-form parameter was unresolved")
        eta_lower = arb(str(eta))
        prime_upper = arb(str(_float_upper(prime_sum)))
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
        losses = (
            ("relative", eta_lower * (margin + perturbation_ball)),
            (
                "Young",
                8 * prime_upper**2 / (eta_lower * registered_resolution),
            ),
            (
                "H-log scalar",
                4 * prime_upper * hlog_upper.sqrt() / registered_resolution.sqrt(),
            ),
        )
        for name, loss in losses:
            if not loss.upper() <= budget_piece.lower():
                raise ArithmeticError(f"the {name} continuity budget did not close")

        ordinary_lipschitz = 1 / lower + 2 * arb(str(smooth_radial))
        regular_radius = margin / (5 * ordinary_lipschitz)
        regular_radius_lower = _float_lower(regular_radius)
        if regular_radius_lower <= 0:
            raise ArithmeticError("the ordinary parameter radius was unresolved")

        # For n=2,3, the largest displacement change is the n=3 one:
        # |log(n)/a-log(n)/a0| <= log(3) |a-a0|/(a_min a0).
        conversion = lower * center / log_three
        exponent_translation = (
            arb(str(required_logarithm)) / 2 - conversion.log()
        ) / arb(10).log()
        exponent_regular = -regular_radius.log() / arb(10).log()
        neighborhood_radius = min(center - lower, upper - center)
        exponent_neighborhood = -neighborhood_radius.log() / arb(10).log()
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

    return TwoPrimeSupportIntervalCertificate(
        center=float(center_text),
        neighborhood_lower=float(lower_text),
        neighborhood_upper=float(upper_text),
        point_lower=point_lower,
        certified_interval_lower=certified_lower,
        smooth_kernel_supremum_upper=smooth_supremum,
        smooth_radial_derivative_upper=smooth_radial,
        bounded_perturbation_upper=perturbation_upper,
        hlog_constant_upper=_float_upper(hlog_constant),
        prime_coefficient_sum_upper=_float_upper(prime_sum),
        relative_eta=eta,
        required_logarithm=required_logarithm,
        regular_radius_lower=regular_radius_lower,
        decimal_radius_exponent=decimal_exponent,
        precision=precision,
    )

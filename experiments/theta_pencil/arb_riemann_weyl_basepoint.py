"""Arb certificate for the Riemann Weyl target at the base point ``z=i``."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class RiemannWeylBasepointCertificate:
    precision_bits: int
    xi_value: object
    xi_first_derivative: object
    xi_second_derivative: object
    normalized_weyl_derivative: object
    odd_even_balance: object
    target_fourier_parity_ratio: object


@dataclass(frozen=True)
class RiemannFourierParityTargetCertificate:
    precision_bits: int
    imaginary_height: object
    normalized_reciprocal_log_derivative: object
    target_fourier_parity_ratio: object


@dataclass(frozen=True)
class RiemannSchwarzPickExcessCertificate:
    precision_bits: int
    imaginary_height: object
    odd_even_balance: object
    target_fourier_parity_ratio: object
    lower_extremal: object
    upper_extremal: object
    target_excess: object
    upper_slack: object


def _xi_series_at(variable, arb):
    pi = arb.pi()
    return (
        variable
        * (variable - 1)
        * ((-variable / 2) * pi.log()).exp()
        * (variable / 2).gamma()
        * variable.zeta()
    )


def certify_riemann_weyl_basepoint(
    precision_bits: int = 200,
) -> RiemannWeylBasepointCertificate:
    """Certify ``F_Xi'(i)`` and ``kappa_Xi`` using Arb power series.

    For ``F_Xi=(Xi/Xi') / ((Xi/Xi')(i)/i)`` and
    ``Xi(z)=xi(1/2-iz)``, direct differentiation gives

    ``F_Xi'(i) = xi'(3/2)/xi(3/2) - xi''(3/2)/xi'(3/2)``.

    The returned ``odd_even_balance`` is
    ``(1+F_Xi'(i))/(1-F_Xi'(i))``.
    """

    if precision_bits < 80:
        raise ValueError("precision_bits must be at least 80")
    from flint import arb, arb_series, ctx

    old_precision = ctx.prec
    try:
        ctx.prec = precision_bits
        variable = arb_series([arb(3) / 2, 1, 0], 3)
        xi_series = _xi_series_at(variable, arb)
        xi_value = xi_series[0]
        xi_first = xi_series[1]
        xi_second = 2 * xi_series[2]
        derivative = xi_first / xi_value - xi_second / xi_first
        balance = (1 + derivative) / (1 - derivative)
        return RiemannWeylBasepointCertificate(
            precision_bits=precision_bits,
            xi_value=xi_value,
            xi_first_derivative=xi_first,
            xi_second_derivative=xi_second,
            normalized_weyl_derivative=derivative,
            odd_even_balance=balance,
            target_fourier_parity_ratio=-balance,
        )
    finally:
        ctx.prec = old_precision


def certify_riemann_fourier_parity_target(
    imaginary_height: float | str,
    precision_bits: int = 200,
) -> RiemannFourierParityTargetCertificate:
    """Certify ``r_Xi(i*eta)`` wholly in the Euler-product half-plane."""

    if precision_bits < 80:
        raise ValueError("precision_bits must be at least 80")
    from flint import arb, arb_series, ctx

    old_precision = ctx.prec
    try:
        ctx.prec = precision_bits
        eta = arb(str(imaginary_height))
        if not eta.lower() > arb("0.5"):
            raise ValueError("imaginary_height must exceed one half")
        base_variable = arb_series([arb(3) / 2, 1], 2)
        base_xi = _xi_series_at(base_variable, arb)
        base_scale = base_xi[0] / base_xi[1]

        variable = arb_series([arb(1) / 2 + eta, 1], 2)
        xi_series = _xi_series_at(variable, arb)
        normalized = (xi_series[0] / xi_series[1]) / base_scale
        denominator = eta - normalized
        if denominator.contains(0):
            raise ZeroDivisionError("the target parity ratio denominator overlaps zero")
        target = (1 - eta * normalized) / denominator
        return RiemannFourierParityTargetCertificate(
            precision_bits=precision_bits,
            imaginary_height=eta,
            normalized_reciprocal_log_derivative=normalized,
            target_fourier_parity_ratio=target,
        )
    finally:
        ctx.prec = old_precision


def certify_riemann_schwarz_pick_excess(
    imaginary_height: float | str,
    precision_bits: int = 200,
) -> RiemannSchwarzPickExcessCertificate:
    """Certify the target's position in the calibrated Schwarz--Pick interval.

    For ``eta >= 1`` and ``kappa`` fixed by the derivative at ``i``, every
    calibrated real-symmetric Herglotz function obeys

    ``-eta*kappa <= r(i*eta) <= -kappa/eta``.

    The returned ``target_excess`` and ``upper_slack`` rigorously measure the
    distances of the normalized Riemann target from the two endpoints.
    """

    if precision_bits < 80:
        raise ValueError("precision_bits must be at least 80")
    from flint import arb, ctx

    old_precision = ctx.prec
    try:
        ctx.prec = precision_bits
        eta = arb(str(imaginary_height))
        if eta.lower() < arb(1):
            raise ValueError("imaginary_height must be at least one")
        base = certify_riemann_weyl_basepoint(precision_bits)
        target = certify_riemann_fourier_parity_target(
            imaginary_height, precision_bits
        )
        lower = -eta * base.odd_even_balance
        upper = -base.odd_even_balance / eta
        excess = target.target_fourier_parity_ratio - lower
        upper_slack = upper - target.target_fourier_parity_ratio
        return RiemannSchwarzPickExcessCertificate(
            precision_bits=precision_bits,
            imaginary_height=eta,
            odd_even_balance=base.odd_even_balance,
            target_fourier_parity_ratio=target.target_fourier_parity_ratio,
            lower_extremal=lower,
            upper_extremal=upper,
            target_excess=excess,
            upper_slack=upper_slack,
        )
    finally:
        ctx.prec = old_precision


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", type=int, default=200)
    parser.add_argument("--eta", default=None)
    args = parser.parse_args()
    result = certify_riemann_weyl_basepoint(args.precision)
    parity_target = (
        certify_riemann_fourier_parity_target(args.eta, args.precision)
        if args.eta is not None
        else None
    )
    from flint import ctx

    old_precision = ctx.prec
    try:
        ctx.prec = result.precision_bits
        print(
            json.dumps(
                {
                    "precision_bits": result.precision_bits,
                    "xi_value": str(result.xi_value),
                    "xi_first_derivative": str(result.xi_first_derivative),
                    "xi_second_derivative": str(result.xi_second_derivative),
                    "normalized_weyl_derivative": str(
                        result.normalized_weyl_derivative
                    ),
                    "odd_even_balance": str(result.odd_even_balance),
                    "target_fourier_parity_ratio": str(
                        result.target_fourier_parity_ratio
                    ),
                },
                indent=2,
            )
        )
        if parity_target is not None:
            print(
                json.dumps(
                    {
                        "imaginary_height": str(parity_target.imaginary_height),
                        "normalized_reciprocal_log_derivative": str(
                            parity_target.normalized_reciprocal_log_derivative
                        ),
                        "target_fourier_parity_ratio": str(
                            parity_target.target_fourier_parity_ratio
                        ),
                    },
                    indent=2,
                )
            )
    finally:
        ctx.prec = old_precision


if __name__ == "__main__":
    main()

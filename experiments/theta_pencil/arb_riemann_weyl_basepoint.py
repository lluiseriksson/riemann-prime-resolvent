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
        pi = arb.pi()
        xi_series = (
            variable
            * (variable - 1)
            * ((-variable / 2) * pi.log()).exp()
            * (variable / 2).gamma()
            * variable.zeta()
        )
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
        )
    finally:
        ctx.prec = old_precision


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", type=int, default=200)
    args = parser.parse_args()
    result = certify_riemann_weyl_basepoint(args.precision)
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
                },
                indent=2,
            )
        )
    finally:
        ctx.prec = old_precision


if __name__ == "__main__":
    main()

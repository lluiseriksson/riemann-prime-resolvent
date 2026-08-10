from flint import arb, ctx

from experiments.theta_pencil.arb_riemann_weyl_basepoint import (
    certify_riemann_weyl_basepoint,
)


def test_riemann_weyl_basepoint_values_are_rigorously_enclosed():
    old_precision = ctx.prec
    try:
        certificate = certify_riemann_weyl_basepoint(160)
        ctx.prec = 160
        assert certificate.normalized_weyl_derivative.upper() < arb("-0.9968019520324008")
        assert certificate.normalized_weyl_derivative.lower() > arb("-0.9968019520324010")
        assert certificate.odd_even_balance.lower() > arb("0.0016015849565571")
        assert certificate.odd_even_balance.upper() < arb("0.0016015849565573")
    finally:
        ctx.prec = old_precision

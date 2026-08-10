import pytest
from flint import arb, ctx

from experiments.theta_pencil.arb_riemann_weyl_basepoint import (
    certify_riemann_fourier_parity_target,
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
        assert certificate.target_fourier_parity_ratio.overlaps(
            -certificate.odd_even_balance
        )
        assert certificate.target_fourier_parity_ratio.upper() < 0
    finally:
        ctx.prec = old_precision


def test_riemann_fourier_parity_target_is_certified_at_three_i():
    old_precision = ctx.prec
    try:
        certificate = certify_riemann_fourier_parity_target("3", 160)
        ctx.prec = 160
        assert certificate.normalized_reciprocal_log_derivative.lower() > arb(
            "0.33752251372035"
        )
        assert certificate.normalized_reciprocal_log_derivative.upper() < arb(
            "0.33752251372037"
        )
        assert certificate.target_fourier_parity_ratio.lower() > arb(
            "-0.00472024316670"
        )
        assert certificate.target_fourier_parity_ratio.upper() < arb(
            "-0.00472024316667"
        )
    finally:
        ctx.prec = old_precision


def test_riemann_fourier_parity_target_rejects_the_non_euler_region():
    with pytest.raises(ValueError):
        certify_riemann_fourier_parity_target("0.5", 100)

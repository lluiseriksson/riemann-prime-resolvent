"""Audit the constants in the low-type Kadec sampling obstruction.

This is a constant-only check.  It performs no zero search and no spectral
computation.  The mathematical inputs are the explicit coefficient 0.10076 in
the Bellotti--Wong zero-counting bound and the complex Kadec constant
from Avantaggiati--Loreti--Vellucci.
"""

from __future__ import annotations

import json
import math


ZERO_COUNT_LOG_COEFFICIENT = 0.10076


def oseen_parameter() -> float:
    """Return the positive root of exp(x) = 2*x + 1 by Newton iteration."""

    x = 1.25
    for _ in range(12):
        x -= (math.exp(x) - 2.0 * x - 1.0) / (math.exp(x) - 2.0)
    return x


def main() -> None:
    alpha = oseen_parameter()
    limiting_interval = 4.0 * math.pi * ZERO_COUNT_LOG_COEFFICIENT
    limiting_displacement = math.hypot(limiting_interval / 2.0, 0.5)
    scaled_kadec_radius = math.sqrt(3.0 * alpha / 8.0)
    critical_type = scaled_kadec_radius / limiting_displacement

    def paired_margin(pw_type: float) -> float:
        phase = pw_type * limiting_interval / 2.0
        kadec_defect = 1.0 - math.cos(phase) + math.sin(phase)
        even_vertical_defect = math.cosh(pw_type / 2.0) - 1.0
        return (
            (1.0 - kadec_defect)
            - (1.0 + kadec_defect) * even_vertical_defect
        )

    def centered_paired_margin(pw_type: float) -> float:
        """Margin after centering every even vertical coefficient.

        For |y_n| <= 1/2, the coefficient y_n^(2k) lies in
        [0, 2^(-2k)]. Subtracting its midpoint halves the worst coefficient
        error. The common midpoint series is the positive multiplier
        (1 + cosh(t/2))/2, whose minimum on the real interval is one.
        """

        phase = pw_type * limiting_interval / 2.0
        kadec_defect = 1.0 - math.cos(phase) + math.sin(phase)
        centered_vertical_defect = 0.5 * (
            math.cosh(pw_type / 2.0) - 1.0
        )
        return (
            (1.0 - kadec_defect)
            - (1.0 + kadec_defect) * centered_vertical_defect
        )

    def max_gap_centered_margin(pw_type: float) -> float:
        """Centered-pair margin from the direct max-gap sampling frame."""

        gap_defect = pw_type * limiting_interval / math.pi
        centered_vertical_defect = 0.5 * (
            math.cosh(pw_type / 2.0) - 1.0
        )
        return (
            (1.0 - gap_defect)
            - (1.0 + gap_defect) * centered_vertical_defect
        )

    def max_gap_linear_centered_margin(pw_type: float) -> float:
        """Margin with piecewise-linear lower sampling reconstruction."""

        gap_defect = pw_type * limiting_interval / math.pi
        centered_vertical_defect = 0.5 * (
            math.cosh(pw_type / 2.0) - 1.0
        )
        return (
            (1.0 - gap_defect * gap_defect)
            - (1.0 + gap_defect) * centered_vertical_defect
        )

    paired_lo = 0.0
    paired_hi = math.pi / (2.0 * limiting_interval)
    for _ in range(80):
        paired_mid = (paired_lo + paired_hi) / 2.0
        if paired_margin(paired_mid) > 0.0:
            paired_lo = paired_mid
        else:
            paired_hi = paired_mid

    centered_lo = 0.0
    centered_hi = math.pi / (2.0 * limiting_interval)
    for _ in range(80):
        centered_mid = (centered_lo + centered_hi) / 2.0
        if centered_paired_margin(centered_mid) > 0.0:
            centered_lo = centered_mid
        else:
            centered_hi = centered_mid

    max_gap_lo = 0.0
    max_gap_hi = math.pi / limiting_interval
    for _ in range(80):
        max_gap_mid = (max_gap_lo + max_gap_hi) / 2.0
        if max_gap_centered_margin(max_gap_mid) > 0.0:
            max_gap_lo = max_gap_mid
        else:
            max_gap_hi = max_gap_mid

    max_gap_linear_lo = 0.0
    max_gap_linear_hi = math.pi / limiting_interval
    for _ in range(80):
        max_gap_linear_mid = (max_gap_linear_lo + max_gap_linear_hi) / 2.0
        if max_gap_linear_centered_margin(max_gap_linear_mid) > 0.0:
            max_gap_linear_lo = max_gap_linear_mid
        else:
            max_gap_linear_hi = max_gap_linear_mid

    # A strict, usable pair on the proved side of the limiting inequalities.
    test_interval = 1.27
    test_type = 0.84
    test_displacement = math.hypot(test_interval / 2.0, 0.5)

    result = {
        "oseen_parameter": alpha,
        "zero_count_interval_infimum": limiting_interval,
        "limiting_complex_displacement": limiting_displacement,
        "scaled_complex_kadec_radius": scaled_kadec_radius,
        "critical_paley_wiener_type": critical_type,
        "conjugate_pair_paley_wiener_type": paired_lo,
        "centered_conjugate_pair_paley_wiener_type": centered_lo,
        "real_kadec_type_ceiling": math.pi / (2.0 * limiting_interval),
        "max_gap_centered_pair_paley_wiener_type": max_gap_lo,
        "max_gap_linear_centered_pair_paley_wiener_type": max_gap_linear_lo,
        "max_gap_sampling_type_ceiling": math.pi / limiting_interval,
        "strict_test": {
            "interval_length": test_interval,
            "type": test_type,
            "zero_count_leading_margin": (
                test_interval / (2.0 * math.pi)
                - 2.0 * ZERO_COUNT_LOG_COEFFICIENT
            ),
            "kadec_margin": (
                scaled_kadec_radius - test_type * test_displacement
            ),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    assert abs(math.exp(alpha) - 2.0 * alpha - 1.0) < 1e-14
    assert result["strict_test"]["zero_count_leading_margin"] > 0.0
    assert result["strict_test"]["kadec_margin"] > 0.0
    assert 0.8508 < critical_type < 0.8510
    assert 0.9908 < paired_lo < 0.9910
    assert paired_margin(0.99) > 0.0
    assert paired_margin(1.00) < 0.0
    assert 1.0839 < centered_lo < 1.0841
    assert centered_paired_margin(1.08) > 0.0
    assert centered_paired_margin(1.09) < 0.0
    assert 1.6904 < max_gap_lo < 1.6907
    assert max_gap_centered_margin(1.69) > 0.0
    assert max_gap_centered_margin(1.70) < 0.0
    assert 1.8867 < max_gap_linear_lo < 1.8870
    assert max_gap_linear_centered_margin(1.88) > 0.0
    assert max_gap_linear_centered_margin(1.89) < 0.0


if __name__ == "__main__":
    main()

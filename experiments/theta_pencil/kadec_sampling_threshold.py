"""Audit the constants in the low-type Kadec sampling obstruction.

This is a constant-only check.  It performs no zero search and no spectral
computation.  The mathematical inputs are the explicit coefficient 0.1038 in
the Hasanalizade--Shen--Wong zero-counting bound and the complex Kadec constant
from Avantaggiati--Loreti--Vellucci.
"""

from __future__ import annotations

import json
import math


ZERO_COUNT_LOG_COEFFICIENT = 0.1038


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

    # A strict, usable pair on the proved side of the limiting inequalities.
    test_interval = 1.31
    test_type = 0.83
    test_displacement = math.hypot(test_interval / 2.0, 0.5)

    result = {
        "oseen_parameter": alpha,
        "zero_count_interval_infimum": limiting_interval,
        "limiting_complex_displacement": limiting_displacement,
        "scaled_complex_kadec_radius": scaled_kadec_radius,
        "critical_paley_wiener_type": critical_type,
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
    assert 0.8352 < critical_type < 0.8353


if __name__ == "__main__":
    main()

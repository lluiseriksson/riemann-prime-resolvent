"""Explicit unconditional small-support bound for the Weil--Suzuki form."""

from __future__ import annotations

import math

from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA

LOG_LAPLACIAN_GAP = (5.0 - math.sqrt(19.0)) / 6.0
MAX_CERTIFIED_HALF_WIDTH = 1.0 / 14.0


def smooth_remainder_second(t: float) -> float:
    """Return r''(t) in Suzuki's prime-free local decomposition.

    The removable value at zero is -7/4.  The formula is used only as a
    numerical regression check; the accompanying note proves the bound by
    elementary exponential inequalities.
    """
    t = abs(t)
    if t == 0.0:
        return -7.0 / 4.0
    return (
        -math.exp(t / 2.0)
        - math.exp(-t / 2.0)
        + math.exp(-t / 2.0) / (-math.expm1(-2.0 * t))
        - 1.0 / (2.0 * t)
    )


def coercivity_constant(half_width: float) -> float:
    """Certified analytic coefficient from the |r''| <= 2 Schur bound."""
    if not 0.0 < half_width <= MAX_CERTIFIED_HALF_WIDTH:
        raise ValueError("the registered proof applies only on 0 < a <= 1/14")
    return (
        -math.log(half_width)
        - math.log(2.0 * math.pi)
        - EULER_GAMMA
        + LOG_LAPLACIAN_GAP
        - 4.0 * half_width
    )


def main() -> None:
    endpoint = MAX_CERTIFIED_HALF_WIDTH
    samples = [
        smooth_remainder_second((2.0 * endpoint) * k / 1000.0)
        for k in range(1001)
    ]
    print(f"a={endpoint:.12g}")
    print(f"coercivity={coercivity_constant(endpoint):.15g}")
    print(f"sampled rpp range=[{min(samples):.15g}, {max(samples):.15g}]")


if __name__ == "__main__":
    main()

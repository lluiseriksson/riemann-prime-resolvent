"""Colab-only exploratory audit of Chebyshev-cardinal L1 derivative norms.

Do not run this sweep on the local Windows desk.  Its output is numerical
evidence for choosing an analytic lemma, never proof of that lemma.

Suggested Colab Pro+ commands, prepared before connecting::

    !git clone https://github.com/lluiseriksson/riemann-prime-resolvent.git
    %cd riemann-prime-resolvent
    !git checkout research/rh-reboot-2026
    !python experiments/theta_pencil/chebyshev_cardinal_l1_colab.py \
        --orders 8 16 32 64 128 256 512 --points-per-mode 4000 \
        --checkpoint /content/chebyshev-cardinal-l1-colab.json

The integration is streamed one cardinal polynomial at a time.  The grid is
uniform in theta, so endpoint layers of width O(m^-2) in x are resolved with
O(m) theta samples rather than an O(m^2) uniform-x grid.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
from numpy.polynomial.chebyshev import chebder, chebval


def cardinal_second_derivative_l1(m: int, points_per_mode: int) -> dict[str, float]:
    """Numerically integrate every first-kind cardinal second derivative."""

    count = max(200_000, points_per_mode * m)
    theta_grid = np.linspace(0.0, math.pi, count + 1)
    x_grid = np.cos(theta_grid)
    jacobian = np.sin(theta_grid)
    frequencies = np.arange(1, m, dtype=float)
    values: list[float] = []
    started = time.monotonic()
    for index in range(m):
        theta = (2 * index + 1) * math.pi / (2 * m)
        coefficients = np.empty(m)
        coefficients[0] = 1.0 / m
        coefficients[1:] = 2.0 / m * np.cos(frequencies * theta)
        second = chebder(coefficients, 2)
        integrand = np.abs(chebval(x_grid, second)) * jacobian
        values.append(float(np.trapezoid(integrand, theta_grid)))
    maximum = max(values)
    argmax = values.index(maximum)
    return {
        "m": m,
        "theta_intervals": count,
        "max_l1": maximum,
        "max_l1_over_m2": maximum / m**2,
        "argmax_k": argmax,
        "elapsed_seconds": time.monotonic() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orders", nargs="+", type=int, required=True)
    parser.add_argument("--points-per-mode", type=int, default=4000)
    parser.add_argument("--checkpoint", type=Path, required=True)
    arguments = parser.parse_args()
    payload: dict[str, object] = {
        "status": "exploratory_only_not_a_proof",
        "points_per_mode": arguments.points_per_mode,
        "rows": [],
    }
    for order in arguments.orders:
        row = cardinal_second_derivative_l1(order, arguments.points_per_mode)
        payload["rows"].append(row)  # type: ignore[union-attr]
        arguments.checkpoint.write_text(json.dumps(payload, indent=2) + "\n")
        print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()

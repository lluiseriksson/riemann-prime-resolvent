"""Checks for the one-prime semilocal moments in arXiv:2403.01247.

The module deliberately does not evaluate zeta zeros and does not claim a
Weil-sign theorem.
"""

from __future__ import annotations

import argparse
import math


def alpha(index: int) -> float:
    """Return (-4)^(-index) * binomial(2*index, index)."""
    if index < 0:
        raise ValueError("index must be nonnegative")
    value = 1.0
    for ell in range(index):
        value *= -(2 * ell + 1) / (2 * ell + 2)
    return value


def sigma_direct(p: int, t: float, terms: int = 100) -> float:
    """Evaluate Sigma_p(t) from its sum over positive powers of p."""
    if p < 2:
        raise ValueError("p must be at least 2")
    q = 1.0 / p
    scale = math.exp(-t / 2)
    radial = math.exp(-2 * t)
    return scale * sum(
        q**n / math.sqrt(1.0 + q ** (2 * n) * radial)
        for n in range(1, terms + 1)
    )


def sigma_lambert(p: int, t: float, terms: int = 100) -> float:
    """Evaluate Sigma_p(t) from the Lambert expansion (L1)."""
    if p < 2:
        raise ValueError("p must be at least 2")
    q = 1.0 / p
    total = 0.0
    coefficient = 1.0
    for ell in range(terms):
        odd = 2 * ell + 1
        total += (
            coefficient
            * math.exp(-2 * ell * t)
            * q**odd
            / (1.0 - q**odd)
        )
        coefficient *= -(2 * ell + 1) / (2 * ell + 2)
    return math.exp(-t / 2) * total


def lambert_moment_correction(p: int, k: int, terms: int = 100) -> float:
    """Return (-1)^k L_{f_k}(1/p), the finite-prime part of c(2k,p)."""
    if p < 2:
        raise ValueError("p must be at least 2")
    if k < 0:
        raise ValueError("k must be nonnegative")
    q = 1.0 / p
    total = 0.0
    coefficient = 1.0
    for ell in range(terms):
        odd = 2 * ell + 1
        frequency = 0.5 + 2 * ell
        total += (
            2.0
            * frequency ** (2 * k)
            * coefficient
            * q**odd
            / (1.0 - q**odd)
        )
        coefficient *= -(2 * ell + 1) / (2 * ell + 2)
    return (-1.0) ** k * total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=2)
    parser.add_argument("--terms", type=int, default=80)
    args = parser.parse_args()

    print(f"one-prime Lambert audit: p={args.prime}, terms={args.terms}")
    for t in (-0.25, 0.0, 0.25, 0.75):
        direct = sigma_direct(args.prime, t, args.terms)
        lambert = sigma_lambert(args.prime, t, args.terms)
        print(
            f"t={t:+.2f} direct={direct:.16e} "
            f"lambert={lambert:.16e} abs_error={abs(direct-lambert):.3e}"
        )
    for k in range(4):
        correction = lambert_moment_correction(args.prime, k, args.terms)
        print(f"prime correction to c({2*k},p): {correction:.16e}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Reproducible numerical illustration for the prime–resolvent programme.

This script is not part of a proof.  It compares three scalar functions on a
compact interval:

1. the completed-zeta logarithmic-derivative target S_Xi(x);
2. a von-Mangoldt truncation P_X(x);
3. a partial sum over the first K critical-line zeros.

The output is a CSV, a JSON metadata file, and PDF/PNG figures.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np


def von_mangoldt_table(limit: int) -> np.ndarray:
    """Return Lambda(n) for 0 <= n <= limit using a prime-power sieve."""
    if limit < 2:
        return np.zeros(limit + 1, dtype=float)
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[:2] = False
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            is_prime[p * p : limit + 1 : p] = False
    lam = np.zeros(limit + 1, dtype=float)
    for p in np.flatnonzero(is_prime):
        value = math.log(int(p))
        power = int(p)
        while power <= limit:
            lam[power] = value
            if power > limit // int(p):
                break
            power *= int(p)
    return lam


def xi_resolvent_target(x: float) -> mp.mpf:
    y = mp.sqrt(x)
    sigma = mp.mpf("0.5") + y
    zeta_log_derivative = mp.diff(mp.zeta, sigma) / mp.zeta(sigma)
    xi_log_derivative = (
        1 / sigma
        + 1 / (sigma - 1)
        - mp.log(mp.pi) / 2
        + mp.digamma(sigma / 2) / 2
        + zeta_log_derivative
    )
    return xi_log_derivative / (2 * y)


def prime_truncation(x: float, lam: np.ndarray) -> mp.mpf:
    y = mp.sqrt(x)
    sigma = mp.mpf("0.5") + y
    n = np.arange(2, len(lam), dtype=float)
    arithmetic = mp.mpf(str(float(np.sum(lam[2:] * np.power(n, -float(sigma))))))
    archimedean = (
        1 / sigma
        + 1 / (sigma - 1)
        - mp.log(mp.pi) / 2
        + mp.digamma(sigma / 2) / 2
    )
    return (archimedean - arithmetic) / (2 * y)


def spectral_partial(x: float, ordinates: list[mp.mpf]) -> mp.mpf:
    xx = mp.mpf(x)
    return mp.fsum(1 / (gamma * gamma + xx) for gamma in ordinates)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("data/demo"))
    parser.add_argument("--prime-cutoff", type=int, default=20_000)
    parser.add_argument("--zeros", type=int, default=40)
    parser.add_argument("--points", type=int, default=70)
    parser.add_argument("--xmin", type=float, default=1.0)
    parser.add_argument("--xmax", type=float, default=25.0)
    parser.add_argument("--dps", type=int, default=50)
    args = parser.parse_args()

    if args.xmin <= 0.25:
        raise ValueError("xmin must be greater than 1/4")
    if args.xmax <= args.xmin:
        raise ValueError("xmax must exceed xmin")
    if args.zeros < 1 or args.points < 2 or args.prime_cutoff < 3:
        raise ValueError("invalid numerical parameters")

    mp.mp.dps = args.dps
    args.output_dir.mkdir(parents=True, exist_ok=True)

    lam = von_mangoldt_table(args.prime_cutoff)
    ordinates = [mp.im(mp.zetazero(k)) for k in range(1, args.zeros + 1)]
    xs = np.linspace(args.xmin, args.xmax, args.points)

    rows: list[dict[str, float]] = []
    for x in xs:
        target = xi_resolvent_target(float(x))
        prime = prime_truncation(float(x), lam)
        spectral = spectral_partial(float(x), ordinates)
        rows.append(
            {
                "x": float(x),
                "target": float(target),
                "prime_truncation": float(prime),
                "spectral_partial": float(spectral),
                "prime_abs_error": float(abs(prime - target)),
                "spectral_abs_error": float(abs(spectral - target)),
            }
        )

    csv_path = args.output_dir / "resolvent_comparison.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.plot(xs, [r["target"] for r in rows], label=r"$\mathcal{S}_{\Xi}(x)$", linewidth=2)
    ax.plot(xs, [r["prime_truncation"] for r in rows], "--", label="prime truncation")
    ax.plot(xs, [r["spectral_partial"] for r in rows], ":", label="first critical zeros")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel("resolvent observable")
    ax.set_title("Prime and spectral approximations to the resolvent target")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    pdf_path = args.output_dir / "resolvent_comparison.pdf"
    png_path = args.output_dir / "resolvent_comparison.png"
    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.semilogy(xs, [max(r["prime_abs_error"], 1e-30) for r in rows], label="prime error")
    ax.semilogy(
        xs,
        [max(r["spectral_abs_error"], 1e-30) for r in rows],
        label="finite-zero tail error",
    )
    ax.set_xlabel(r"$x$")
    ax.set_ylabel("absolute error")
    ax.set_title("Illustrative approximation errors")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    error_pdf = args.output_dir / "resolvent_errors.pdf"
    error_png = args.output_dir / "resolvent_errors.png"
    fig.savefig(error_pdf)
    fig.savefig(error_png, dpi=180)
    plt.close(fig)

    metadata = {
        "status": "numerical illustration only; not evidence constituting a proof",
        "parameters": vars(args) | {"output_dir": str(args.output_dir)},
        "first_zero": str(ordinates[0]),
        "last_zero": str(ordinates[-1]),
        "max_prime_abs_error": max(r["prime_abs_error"] for r in rows),
        "max_spectral_abs_error": max(r["spectral_abs_error"] for r in rows),
        "python": sys.version,
        "platform": platform.platform(),
        "mpmath": mp.__version__,
        "numpy": np.__version__,
        "outputs": {},
    }
    for path in [csv_path, pdf_path, png_path, error_pdf, error_png]:
        metadata["outputs"][path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}

    metadata_path = args.output_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote {csv_path}")
    print(f"Wrote {pdf_path}")
    print(f"Wrote {metadata_path}")


if __name__ == "__main__":
    main()

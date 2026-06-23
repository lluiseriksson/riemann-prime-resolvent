#!/usr/bin/env python3
"""Run generated-artifact commands twice and require byte-identical output."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]


class GeneratedArtifactError(RuntimeError):
    """Raised when generated output is missing or not byte reproducible."""


@dataclass(frozen=True)
class ProjectConfig:
    label: str
    commands: tuple[tuple[str, ...], ...]
    patterns: tuple[str, ...]


def discover_project(root: Path) -> ProjectConfig:
    python = sys.executable
    if (root / "RiemannPrimeResolvent").is_dir():
        return ProjectConfig(
            "construction",
            ((python, "scripts/generate_figures.py"),),
            (
                "docs/assets/images/*.png",
                "docs/assets/images/*.svg",
                "figures/data/*.csv",
            ),
        )
    if (root / "OnePointResolvent").is_dir():
        return ProjectConfig(
            "criterion",
            (
                (
                    python,
                    "scripts/exact_atomic_certificate.py",
                    "--output",
                    "docs/assets/data/exact_atomic_certificate.json",
                ),
                (python, "scripts/generate_figures.py"),
            ),
            (
                "docs/assets/data/exact_atomic_certificate.json",
                "docs/assets/data/finite_signed_differences.csv",
                "docs/assets/images/*.png",
                "docs/assets/images/*.svg",
            ),
        )
    raise GeneratedArtifactError("cannot identify construction or criterion project layout")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot(root: Path, patterns: Iterable[str]) -> dict[str, tuple[int, str]]:
    result: dict[str, tuple[int, str]] = {}
    for pattern in patterns:
        matches = sorted(root.glob(pattern))
        if not matches:
            raise GeneratedArtifactError(f"generated-artifact pattern matched nothing: {pattern}")
        for path in matches:
            if path.is_symlink() or not path.is_file():
                raise GeneratedArtifactError(f"generated artifact is not a regular file: {path}")
            relative = path.relative_to(root).as_posix()
            result[relative] = (path.stat().st_size, sha256_file(path))
    return dict(sorted(result.items()))


def run_commands(root: Path, commands: Sequence[Sequence[str]], *, mpl_config: Path) -> None:
    environment = os.environ.copy()
    environment.update(
        {
            "MPLBACKEND": "Agg",
            "MPLCONFIGDIR": str(mpl_config),
            "PYTHONHASHSEED": "0",
            "SOURCE_DATE_EPOCH": "0",
            "TZ": "UTC",
        }
    )
    for command in commands:
        result = subprocess.run(
            list(command),
            cwd=root,
            env=environment,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            rendered = " ".join(command)
            raise GeneratedArtifactError(
                f"generator failed ({result.returncode}): {rendered}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )


def verify_reproducible(
    root: Path,
    commands: Sequence[Sequence[str]],
    patterns: Iterable[str],
) -> dict[str, tuple[int, str]]:
    root = root.resolve()
    with tempfile.TemporaryDirectory(prefix="rpr-mpl-first-") as first_config:
        run_commands(root, commands, mpl_config=Path(first_config))
    first = snapshot(root, patterns)
    with tempfile.TemporaryDirectory(prefix="rpr-mpl-second-") as second_config:
        run_commands(root, commands, mpl_config=Path(second_config))
    second = snapshot(root, patterns)
    if first != second:
        paths = sorted(set(first) | set(second))
        changed = [path for path in paths if first.get(path) != second.get(path)]
        details = ", ".join(changed[:20])
        if len(changed) > 20:
            details += f" … and {len(changed) - 20} more"
        raise GeneratedArtifactError(
            "generated artifacts are not byte reproducible across two clean runs: " + details
        )
    return second


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        config = discover_project(root)
        artifacts = verify_reproducible(root, config.commands, config.patterns)
    except (OSError, UnicodeError, GeneratedArtifactError) as exc:
        print(f"Generated-artifact reproducibility FAILED: {exc}", file=sys.stderr)
        return 1
    print(
        f"Generated-artifact reproducibility passed for {config.label}: "
        f"{len(artifacts)} files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

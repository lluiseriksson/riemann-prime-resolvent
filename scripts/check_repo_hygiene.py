#!/usr/bin/env python3
"""Repository hygiene checks that are cheap, local and cross-platform.

The release manifest already checks payload completeness.  This script catches
problems that usually appear only after moving between Linux, macOS and Windows:
case-insensitive path collisions, CRLF drift in normalized text files, unsafe
control characters in file names, and accidentally committed local cache files.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path, PurePosixPath
from typing import Iterable

TEXT_SUFFIXES = {
    ".cff", ".csv", ".dot", ".json", ".lean", ".md", ".py", ".sh",
    ".svg", ".toml", ".txt", ".yaml", ".yml",
}
EXCLUDED_DIRS = {
    ".git", ".lake", ".mypy_cache", ".nox", ".pytest_cache", ".ruff_cache",
    ".tox", ".venv", "__pycache__", "build", "dist", "release", "site", "venv",
}
FORBIDDEN_NAMES = {".DS_Store", "Thumbs.db"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


class HygieneError(RuntimeError):
    pass


def iter_files(root: Path) -> Iterable[Path]:
    root = root.resolve()
    for directory, directory_names, file_names in os.walk(root, topdown=True, followlinks=False):
        directory_names[:] = [name for name in sorted(directory_names) if name not in EXCLUDED_DIRS]
        base = Path(directory)
        for name in sorted(file_names):
            yield base / name


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def audit(root: Path) -> list[str]:
    root = root.resolve()
    failures: list[str] = []
    if not root.is_dir():
        return [f"not a directory: {root}"]

    seen_casefold: dict[str, str] = {}
    for path in iter_files(root):
        relative = rel(path, root)
        pure = PurePosixPath(relative)
        folded = relative.casefold()
        previous = seen_casefold.setdefault(folded, relative)
        if previous != relative:
            failures.append(f"case-insensitive path collision: {previous} <-> {relative}")
        if any(ord(ch) < 32 for ch in relative):
            failures.append(f"control character in path: {relative!r}")
        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            failures.append(f"forbidden generated/local file: {relative}")
        if path.is_symlink():
            failures.append(f"included symlink is forbidden: {relative}")
            continue
        if pure.suffix.lower() in TEXT_SUFFIXES:
            try:
                data = path.read_bytes()
            except OSError as exc:
                failures.append(f"cannot read {relative}: {exc}")
                continue
            if b"\r\n" in data:
                failures.append(f"CRLF line endings in normalized text file: {relative}")
            try:
                data.decode("utf-8")
            except UnicodeDecodeError as exc:
                failures.append(f"normalized text file is not UTF-8: {relative}: {exc}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    failures = audit(args.root)
    if failures:
        print("Repository hygiene FAILED:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1
    print("Repository hygiene passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

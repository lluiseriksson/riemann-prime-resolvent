#!/usr/bin/env python3
"""Audit GitHub Actions workflows for supply-chain-safe references.

The repository intentionally pins third-party Actions by full commit SHA.  This
keeps release and documentation workflows reproducible and prevents a mutable tag
from changing CI behavior between two commits.  Local reusable actions may still
be referenced with ``./`` paths.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_GLOBS = (".github/workflows/*.yml", ".github/workflows/*.yaml")
FULL_SHA_RE = re.compile(r"\A[0-9a-f]{40}\Z")
USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)")
FORBIDDEN_EVENT_RE = re.compile(r"^\s*pull_request_target\s*:", re.MULTILINE)
NETWORK_PIPE_RE = re.compile(r"\b(?:curl|wget)\b[^\n|]*\|\s*(?:sh|bash|python|python3)\b")


def workflow_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for directory in [root, root / "subprojects/riemann-one-point-resolvent"]:
        if directory.is_dir():
            for pattern in WORKFLOW_GLOBS:
                files.extend(directory.glob(pattern))
    return sorted(set(files))


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def audit_text(path: Path, text: str, root: Path) -> list[str]:
    failures: list[str] = []
    rel = _relative(path, root)
    if FORBIDDEN_EVENT_RE.search(text):
        failures.append(f"{rel}: pull_request_target is forbidden")
    if NETWORK_PIPE_RE.search(text):
        failures.append(f"{rel}: network download piped to interpreter is forbidden")

    for lineno, line in enumerate(text.splitlines(), start=1):
        match = USES_RE.match(line)
        if not match:
            continue
        reference = match.group(1).strip('"\'')
        if reference.startswith("./"):
            continue
        if "@" not in reference:
            failures.append(f"{rel}:{lineno}: action reference has no @ ref: {reference}")
            continue
        action, ref = reference.rsplit("@", 1)
        if not action or not ref:
            failures.append(f"{rel}:{lineno}: malformed action reference: {reference}")
            continue
        if FULL_SHA_RE.fullmatch(ref) is None:
            failures.append(
                f"{rel}:{lineno}: action must be pinned by 40-char commit SHA, not {ref!r}"
            )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    failures: list[str] = []
    files = workflow_files(root)
    if not files:
        failures.append("no GitHub workflow files found")
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"{_relative(path, root)}: not UTF-8: {exc}")
            continue
        failures.extend(audit_text(path, text, root))
    if failures:
        print("Workflow audit FAILED:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1
    print(f"Workflow audit passed for {len(files)} workflow files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

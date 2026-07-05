#!/usr/bin/env python3
"""Audit remote documentation assets for HTTPS and immutable version pins."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"https?://[^\s\"']+")
JSDELIVR_NPM_RE = re.compile(r"https://cdn\.jsdelivr\.net/npm/([^@/]+)@([^/]+)/")
EXACT_SEMVER_RE = re.compile(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?\Z")
MUTABLE_MARKERS = ("@latest/", "@main/", "@master/", "/latest/")


def config_files(root: Path) -> list[Path]:
    root = root.resolve()
    files = [root / "mkdocs.yml"]
    nested = root / "subprojects/riemann-one-point-resolvent/mkdocs.yml"
    if nested.is_file():
        files.append(nested)
    return files


def audit_file(path: Path, root: Path) -> list[str]:
    failures: list[str] = []
    relative = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{relative}: cannot read UTF-8 configuration: {exc}"]

    urls = URL_RE.findall(text)
    for url in urls:
        cleaned = url.rstrip(",)]}")
        if not cleaned.startswith("https://"):
            failures.append(f"{relative}: remote asset must use HTTPS: {cleaned}")
        if any(marker in cleaned for marker in MUTABLE_MARKERS):
            failures.append(f"{relative}: mutable remote asset reference: {cleaned}")
        # Match the package/version prefix; the URL continues with an asset path.
        match = JSDELIVR_NPM_RE.match(cleaned)
        if match and EXACT_SEMVER_RE.fullmatch(match.group(2)) is None:
            failures.append(
                f"{relative}: jsDelivr npm asset requires exact semantic version, "
                f"got {match.group(1)}@{match.group(2)}"
            )
    return failures


def audit(root: Path) -> list[str]:
    root = root.resolve()
    failures: list[str] = []
    files = config_files(root)
    for path in files:
        if path.is_symlink() or not path.is_file():
            failures.append(f"missing regular MkDocs configuration: {path}")
            continue
        failures.extend(audit_file(path, root))
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    failures = audit(args.root)
    if failures:
        print("Documentation asset audit FAILED:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1
    print(f"Documentation asset audit passed for {len(config_files(args.root))} configuration(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

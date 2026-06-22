#!/usr/bin/env python3
"""Fail on proof placeholders or project axiom declarations in Lean sources."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = [
    re.compile(r"\bsorry\b"),
    re.compile(r"\badmit\b"),
    re.compile(r"^\s*axiom\s+", re.MULTILINE),
]


def strip_comments(text: str) -> str:
    text = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    text = re.sub(r"--.*?$", "", text, flags=re.MULTILINE)
    return text


def main() -> int:
    failures: list[str] = []
    for path in sorted(ROOT.rglob("*.lean")):
        if ".lake" in path.parts:
            continue
        clean = strip_comments(path.read_text(encoding="utf-8"))
        for pattern in PATTERNS:
            if pattern.search(clean):
                failures.append(f"{path.relative_to(ROOT)} matches {pattern.pattern!r}")
    if failures:
        print("Placeholder/axiom scan failed:")
        print("\n".join(failures))
        return 1
    print("Lean placeholder scan: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())

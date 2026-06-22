#!/usr/bin/env python3
"""Fail on proof placeholders or project axiom declarations in Lean sources.

The scanner removes nested block comments, line comments, and strings before
checking tokens.  `#print axioms` is allowed; an `axiom` declaration is not.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_FILES = [ROOT / "RiemannPrimeResolvent.lean"] + sorted(
    (ROOT / "RiemannPrimeResolvent").rglob("*.lean")
)


def strip_lean_comments_and_strings(text: str) -> str:
    out: list[str] = []
    i = 0
    depth = 0
    in_string = False
    while i < len(text):
        if depth > 0:
            if text.startswith("/-", i):
                depth += 1
                i += 2
            elif text.startswith("-/", i):
                depth -= 1
                i += 2
            else:
                if text[i] == "\n":
                    out.append("\n")
                i += 1
            continue
        if in_string:
            if text[i] == "\\":
                i += 2
            elif text[i] == '"':
                in_string = False
                out.append('"')
                i += 1
            else:
                if text[i] == "\n":
                    out.append("\n")
                i += 1
            continue
        if text.startswith("/-", i):
            depth = 1
            i += 2
        elif text.startswith("--", i):
            j = text.find("\n", i)
            if j < 0:
                break
            out.append("\n")
            i = j + 1
        elif text[i] == '"':
            in_string = True
            out.append('"')
            i += 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


patterns = {
    "sorry": re.compile(r"\bsorry\b"),
    "admit": re.compile(r"\badmit\b"),
    "axiom declaration": re.compile(r"(?m)^\s*(?:private\s+)?axiom\b"),
    "unsafe declaration": re.compile(r"(?m)^\s*unsafe\s+(?:def|theorem|opaque)\b"),
}

failures: list[str] = []
for path in LEAN_FILES:
    text = strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
    for label, pattern in patterns.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            failures.append(f"{path.relative_to(ROOT)}:{line}: forbidden {label}")

if failures:
    print("Consistency check FAILED", file=sys.stderr)
    print("\n".join(failures), file=sys.stderr)
    raise SystemExit(1)

print(f"Consistency check passed: {len(LEAN_FILES)} Lean files scanned.")

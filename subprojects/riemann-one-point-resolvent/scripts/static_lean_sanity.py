#!/usr/bin/env python3
"""Very small non-authoritative Lean source sanity checks.

This is not a substitute for the Lean compiler. It catches missing local imports,
unbalanced delimiters outside comments/strings, and duplicate top-level declaration names.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECL = re.compile(r"^\s*(?:noncomputable\s+)?(?:def|theorem|lemma|corollary|abbrev|structure|class|instance)\s+([A-Za-z0-9_'.]+)", re.MULTILINE)
IMPORT = re.compile(r"^\s*import\s+([A-Za-z0-9_.]+)\s*$", re.MULTILINE)


def strip_comments_and_strings(text: str) -> str:
    text = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    text = re.sub(r"--.*?$", "", text, flags=re.MULTILINE)
    text = re.sub(r'"(?:\\.|[^"\\])*"', '""', text)
    return text


def module_path(module: str) -> Path:
    return ROOT / (module.replace(".", "/") + ".lean")


def main() -> int:
    errors: list[str] = []
    declarations: dict[str, Path] = {}
    for path in sorted(ROOT.rglob("*.lean")):
        if ".lake" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        clean = strip_comments_and_strings(text)
        stack: list[str] = []
        pairs = {")": "(", "]": "[", "}": "{"}
        for char in clean:
            if char in "([{":
                stack.append(char)
            elif char in pairs:
                if not stack or stack.pop() != pairs[char]:
                    errors.append(f"{path.relative_to(ROOT)}: unbalanced {char}")
                    break
        if stack:
            errors.append(f"{path.relative_to(ROOT)}: unclosed delimiters {stack[-10:]}")
        for module in IMPORT.findall(text):
            if module.startswith("PrimeResolvent") and not module_path(module).exists():
                errors.append(f"{path.relative_to(ROOT)}: missing local import {module}")
        for name in DECL.findall(clean):
            full = name if "." in name else f"PrimeResolvent.{name}"
            if full in declarations:
                errors.append(
                    f"duplicate declaration candidate {full}: {declarations[full]} and {path}"
                )
            declarations[full] = path
    if errors:
        print("Static Lean sanity failed:")
        print("\n".join(errors))
        return 1
    print(f"Static Lean sanity: passed ({len(declarations)} declarations scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

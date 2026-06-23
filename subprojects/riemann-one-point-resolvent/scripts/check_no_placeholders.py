#!/usr/bin/env python3
"""Reject proof placeholders and project-level axiom shortcuts in Lean sources.

The scanner masks nested Lean comments and string literals while preserving line
positions.  Interpolated string expressions remain visible to the audit, so a
placeholder cannot be hidden inside ``s!\"{...}\"``.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCLUDED_LEAN_DIRECTORIES = frozenset(
    {
        ".git",
        ".lake",
        ".mypy_cache",
        ".nox",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "release",
        "site",
        "venv",
    }
)

PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("sorry", re.compile(r"\bsorry\b")),
    ("admit", re.compile(r"\badmit\b")),
    ("axiom", re.compile(r"\baxiom\b")),
    # Lean's `constant` command is an axiom-like declaration and must not bypass
    # the project policy merely by using the synonym instead of `axiom`.
    ("constant", re.compile(r"\bconstant\b")),
    # Any `unsafe` declaration is outside the trusted publication surface.
    ("unsafe", re.compile(r"\bunsafe\b")),
)


class LeanLexError(ValueError):
    """Raised when the lightweight scanner finds an unterminated construct."""


@dataclass(frozen=True, order=True)
class Finding:
    path: str
    line: int
    column: int
    label: str

    def render(self) -> str:
        return f"{self.path}:{self.line}:{self.column}: {self.label}"


def _mask_char(output: list[str], text: str, index: int) -> None:
    if text[index] not in "\r\n":
        output[index] = " "


def _line_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    previous_newline = text.rfind("\n", 0, offset)
    column = offset + 1 if previous_newline < 0 else offset - previous_newline
    return line, column


def mask_lean_source(text: str) -> str:
    """Return ``text`` with comments/string literals replaced by spaces.

    Newlines are retained exactly, making regex match offsets useful for stable
    diagnostics. Lean block comments are nested. Within an interpolated string,
    expressions between braces are scanned as Lean code.
    """

    output = list(text)
    # Frames are [kind, data]. A code frame's data is None outside interpolation
    # or the current brace depth inside an interpolated string expression.
    frames: list[list[object]] = [["code", None]]
    index = 0
    length = len(text)

    while index < length:
        kind = frames[-1][0]

        if kind == "string":
            interpolated = bool(frames[-1][1])
            char = text[index]
            _mask_char(output, text, index)

            if char == "\\":
                if index + 1 < length:
                    _mask_char(output, text, index + 1)
                    index += 2
                else:
                    index += 1
                continue

            if char == '"':
                frames.pop()
                index += 1
                continue

            if interpolated and char == "{":
                # Lean uses doubled opening braces for a literal brace.
                if index + 1 < length and text[index + 1] == "{":
                    _mask_char(output, text, index + 1)
                    index += 2
                else:
                    frames.append(["code", 1])
                    index += 1
                continue

            index += 1
            continue

        # Code frame.
        interpolation_depth = frames[-1][1]

        if text.startswith("--", index):
            _mask_char(output, text, index)
            _mask_char(output, text, index + 1)
            index += 2
            while index < length and text[index] not in "\r\n":
                _mask_char(output, text, index)
                index += 1
            continue

        if text.startswith("/-", index):
            start = index
            depth = 1
            _mask_char(output, text, index)
            _mask_char(output, text, index + 1)
            index += 2
            while index < length and depth:
                if text.startswith("/-", index):
                    _mask_char(output, text, index)
                    _mask_char(output, text, index + 1)
                    depth += 1
                    index += 2
                elif text.startswith("-/", index):
                    _mask_char(output, text, index)
                    _mask_char(output, text, index + 1)
                    depth -= 1
                    index += 2
                else:
                    _mask_char(output, text, index)
                    index += 1
            if depth:
                line, column = _line_column(text, start)
                raise LeanLexError(f"unterminated block comment at {line}:{column}")
            continue

        char = text[index]
        if char == '"':
            interpolated = index >= 2 and text[index - 2:index] == "s!"
            _mask_char(output, text, index)
            frames.append(["string", interpolated])
            index += 1
            continue

        if interpolation_depth is not None:
            depth = int(interpolation_depth)
            if char == "{":
                frames[-1][1] = depth + 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    _mask_char(output, text, index)
                    frames.pop()
                else:
                    frames[-1][1] = depth
            index += 1
            continue

        index += 1

    for kind, data in frames[1:]:
        if kind == "string":
            raise LeanLexError("unterminated string literal")
        if kind == "code" and data is not None:
            raise LeanLexError("unterminated interpolated-string expression")
    return "".join(output)


def audit_text(text: str, *, path: str = "<memory>") -> list[Finding]:
    masked = mask_lean_source(text)
    findings: list[Finding] = []
    for label, pattern in PATTERNS:
        for match in pattern.finditer(masked):
            line, column = _line_column(text, match.start())
            findings.append(Finding(path, line, column, label))
    return sorted(findings)


def lean_files(root: Path) -> list[Path]:
    """Discover every repository Lean source while pruning generated/vendor trees.

    Restricting the scan to the conventional library directory would let a new
    imported root or support module bypass the placeholder policy.  Walking the
    complete source tree closes that gap while explicitly excluding build caches.
    """

    root = root.resolve()
    candidates: list[Path] = []
    for directory, directory_names, file_names in os.walk(
        root, topdown=True, followlinks=False
    ):
        directory_names[:] = sorted(
            name for name in directory_names if name not in EXCLUDED_LEAN_DIRECTORIES
        )
        base = Path(directory)
        for name in sorted(file_names):
            if not name.endswith(".lean"):
                continue
            path = base / name
            if path.is_file():
                candidates.append(path)

    return sorted(set(candidates))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()

    files = lean_files(root)
    failures: list[str] = []
    if not files:
        failures.append("no Lean source files found")

    for path in files:
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
            failures.extend(finding.render() for finding in audit_text(text, path=relative))
        except (OSError, UnicodeError, LeanLexError) as exc:
            failures.append(f"{relative}: scanner error: {exc}")

    if failures:
        print("Placeholder/axiom audit FAILED:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1
    print(f"Placeholder/axiom audit passed for {len(files)} Lean files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

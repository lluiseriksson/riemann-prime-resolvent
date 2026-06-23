#!/usr/bin/env python3
"""Keep public Lean theorems, axiom oracles and theorem ledgers synchronized."""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from check_no_placeholders import LeanLexError, lean_files, mask_lean_source

ROOT = Path(__file__).resolve().parents[1]
LEAN_NAME = r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*"
PRINT_AXIOMS_RE = re.compile(
    r"(?m)^[ \t]*#print[ \t]+axioms[ \t]+"
    rf"({LEAN_NAME})[ \t]*$"
)
PRINT_AXIOMS_LINE_RE = re.compile(r"(?m)^[ \t]*#print[ \t]+axioms\b.*$")
LEDGER_ROW_RE = re.compile(
    r"^\|\s*`([^`]+)`\s*\|\s*([A-Za-z][A-Za-z0-9_-]*)\s*\|",
    re.MULTILINE,
)
NAMESPACE_RE = re.compile(rf"^[ \t]*namespace[ \t]+({LEAN_NAME})[ \t]*$")
SECTION_RE = re.compile(rf"^[ \t]*section(?:[ \t]+({LEAN_NAME}))?[ \t]*$")
END_RE = re.compile(rf"^[ \t]*end(?:[ \t]+({LEAN_NAME}))?[ \t]*$")
DECLARATION_RE = re.compile(
    rf"^[ \t]*(?:@\[[^\]\n]*\][ \t]*)*"
    rf"(?P<modifiers>(?:(?:private|protected|local|noncomputable)[ \t]+)*)"
    rf"(?P<kind>theorem|lemma)[ \t]+(?P<name>{LEAN_NAME})\b"
)


class OracleCoverageError(RuntimeError):
    """Raised when source declarations, the oracle and the ledger disagree."""


@dataclass(frozen=True)
class ProjectSpec:
    label: str
    namespace: str
    aggregate_import: str
    oracle: Path
    ledger: Path


def discover_project(root: Path) -> ProjectSpec:
    root = root.resolve()
    if (root / "RiemannPrimeResolvent").is_dir():
        return ProjectSpec(
            label="construction",
            namespace="RiemannPrimeResolvent.",
            aggregate_import="RiemannPrimeResolvent",
            oracle=root / "oracle_check.lean",
            ledger=root / "docs/THEOREM-LEDGER.md",
        )
    if (root / "OnePointResolvent").is_dir():
        return ProjectSpec(
            label="criterion",
            namespace="OnePointResolvent.",
            aggregate_import="OnePointResolvent",
            oracle=root / "OnePointResolvent/Oracle.lean",
            ledger=root / "docs/THEOREM_LEDGER.md",
        )
    raise OracleCoverageError("cannot identify construction or criterion project layout")


def parse_oracle(spec: ProjectSpec) -> list[str]:
    try:
        text = spec.oracle.read_text(encoding="utf-8")
        masked = mask_lean_source(text)
    except (OSError, UnicodeError, LeanLexError) as exc:
        raise OracleCoverageError(f"cannot scan {spec.oracle}: {exc}") from exc

    imports = re.findall(r"(?m)^[ \t]*import[ \t]+([A-Za-z0-9_.]+)[ \t]*$", masked)
    if imports != [spec.aggregate_import]:
        raise OracleCoverageError(
            f"{spec.oracle.name}: expected exactly `import {spec.aggregate_import}`, got {imports}"
        )

    declarations = PRINT_AXIOMS_RE.findall(masked)
    command_lines = PRINT_AXIOMS_LINE_RE.findall(masked)
    if len(declarations) != len(command_lines):
        raise OracleCoverageError(f"{spec.oracle.name}: malformed `#print axioms` command")
    if not declarations:
        raise OracleCoverageError(f"{spec.oracle.name}: no `#print axioms` declarations")
    if len(set(declarations)) != len(declarations):
        raise OracleCoverageError(f"{spec.oracle.name}: duplicate `#print axioms` declaration")
    unqualified = [name for name in declarations if not name.startswith(spec.namespace)]
    if unqualified:
        raise OracleCoverageError(
            f"{spec.oracle.name}: declarations outside {spec.namespace}: {', '.join(unqualified)}"
        )
    return declarations


def parse_ledger(spec: ProjectSpec) -> list[str]:
    try:
        text = spec.ledger.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise OracleCoverageError(f"cannot read {spec.ledger}: {exc}") from exc

    rows = LEDGER_ROW_RE.findall(text)
    if not rows:
        raise OracleCoverageError(f"{spec.ledger.name}: no machine-readable declaration rows")

    verified: list[str] = []
    for declaration, status in rows:
        normalized_status = status.casefold()
        if normalized_status != "verified":
            continue
        if "*" in declaration or "…" in declaration or declaration.endswith("."):
            raise OracleCoverageError(
                f"{spec.ledger.name}: verified declaration must be exact, got {declaration!r}"
            )
        if not declaration.startswith(spec.namespace):
            raise OracleCoverageError(
                f"{spec.ledger.name}: verified declaration outside {spec.namespace}: {declaration}"
            )
        verified.append(declaration)

    if not verified:
        raise OracleCoverageError(f"{spec.ledger.name}: no verified declaration rows")
    if len(set(verified)) != len(verified):
        raise OracleCoverageError(f"{spec.ledger.name}: duplicate verified declaration")
    return verified


def _source_declarations(path: Path, spec: ProjectSpec) -> list[str]:
    try:
        masked = mask_lean_source(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, LeanLexError) as exc:
        raise OracleCoverageError(f"cannot scan {path}: {exc}") from exc

    scopes: list[tuple[str, str | None]] = []
    declarations: list[str] = []
    for line in masked.splitlines():
        namespace = NAMESPACE_RE.fullmatch(line)
        if namespace:
            scopes.append(("namespace", namespace.group(1)))
            continue
        section = SECTION_RE.fullmatch(line)
        if section:
            scopes.append(("section", section.group(1)))
            continue
        if END_RE.fullmatch(line):
            if scopes:
                scopes.pop()
            continue

        declaration = DECLARATION_RE.match(line)
        if not declaration:
            continue
        modifiers = declaration.group("modifiers").split()
        if "private" in modifiers or "local" in modifiers:
            continue
        name = declaration.group("name")
        namespace_parts = [
            scope_name
            for scope_kind, scope_name in scopes
            if scope_kind == "namespace" and scope_name
        ]
        prefix = ".".join(namespace_parts)
        if name.startswith(spec.namespace):
            qualified = name
        elif prefix:
            qualified = f"{prefix}.{name}"
        else:
            qualified = name
        if qualified.startswith(spec.namespace):
            declarations.append(qualified)
    return declarations


def parse_source_declarations(root: Path, spec: ProjectSpec) -> list[str]:
    """Enumerate public theorem/lemma commands in the project namespace."""

    declarations: list[str] = []
    locations: dict[str, str] = {}
    root = root.resolve()
    for path in lean_files(root):
        for declaration in _source_declarations(path, spec):
            relative = path.relative_to(root).as_posix()
            previous = locations.get(declaration)
            if previous is not None:
                raise OracleCoverageError(
                    f"duplicate public Lean declaration {declaration}: {previous}, {relative}"
                )
            locations[declaration] = relative
            declarations.append(declaration)
    if not declarations:
        raise OracleCoverageError(
            f"no public theorem/lemma declarations found in {spec.namespace}"
        )
    return declarations


def audit(root: Path) -> list[str]:
    root = root.resolve()
    try:
        spec = discover_project(root)
        oracle = parse_oracle(spec)
        ledger = parse_ledger(spec)
        source = parse_source_declarations(root, spec)
    except OracleCoverageError as exc:
        return [str(exc)]

    failures: list[str] = []
    oracle_set = set(oracle)
    ledger_set = set(ledger)
    source_set = set(source)
    missing = [name for name in oracle if name not in ledger_set]
    extra = [name for name in ledger if name not in oracle_set]
    uncovered = sorted(source_set - oracle_set)
    stale = [name for name in oracle if name not in source_set]
    if missing:
        failures.append("oracle declarations missing from ledger: " + ", ".join(missing))
    if extra:
        failures.append("verified ledger declarations missing from oracle: " + ", ".join(extra))
    if not missing and not extra and oracle != ledger:
        failures.append("verified ledger rows must follow the oracle declaration order")
    if uncovered:
        failures.append("public source declarations missing from oracle: " + ", ".join(uncovered))
    if stale:
        failures.append("oracle declarations missing from public source: " + ", ".join(stale))
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    failures = audit(args.root)
    if failures:
        print("Lean oracle coverage FAILED:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1
    spec = discover_project(args.root)
    count = len(parse_oracle(spec))
    print(
        f"Lean oracle coverage passed for {spec.label}: "
        f"{count} public declarations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

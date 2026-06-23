#!/usr/bin/env python3
"""Audit release metadata, version pins and monorepo project coherence."""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+\-]*\Z")
MATHLIB_REV_RE = re.compile(
    r"mathlib4\.git[\s\S]{0,240}?[\"']([0-9a-f]{40})[\"']"
)
TOOLCHAIN_RE = re.compile(r"leanprover/lean4:v[0-9A-Za-z._+\-]+\Z")


@dataclass(frozen=True)
class ProjectSpec:
    label: str
    root: Path
    title: str
    repository: str
    cff_license: str
    codemeta_license: str


@dataclass(frozen=True)
class ProjectState:
    spec: ProjectSpec
    version: str
    released: str
    toolchain: str
    mathlib_revision: str


def _unquote_scalar(raw: str) -> str:
    value = raw.strip()
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid quoted CFF scalar {value!r}") from exc
        if not isinstance(parsed, str):
            raise ValueError(f"CFF scalar is not a string: {value!r}")
        return parsed
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value.split(" #", 1)[0].strip()


def parse_cff_top_level(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z0-9_-]+):(?:\s*(.*))?", line)
        if not match:
            continue
        key, raw_value = match.group(1), match.group(2) or ""
        if key in values:
            raise ValueError(f"{path.name}:{line_number}: duplicate top-level key {key!r}")
        values[key] = _unquote_scalar(raw_value)
    return values


def _regular_file(path: Path, errors: list[str], label: str) -> bool:
    if path.is_symlink() or not path.is_file():
        errors.append(f"{label}: missing required regular file {path.name}")
        return False
    return True


def _read_canonical_line(path: Path, errors: list[str], label: str) -> str:
    try:
        data = path.read_bytes()
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{label}: cannot read {path.name} as UTF-8: {exc}")
        return ""
    value = text.strip()
    if text != value + "\n":
        errors.append(f"{label}: {path.name} must contain one LF-terminated line")
    return value


def _required_scalar(
    mapping: dict[str, Any], key: str, expected: Any, errors: list[str], label: str
) -> None:
    observed = mapping.get(key)
    if observed != expected:
        errors.append(f"{label}: {key} mismatch: expected {expected!r}, got {observed!r}")


def _discover_projects(root: Path) -> list[ProjectSpec]:
    construction = root / "RiemannPrimeResolvent"
    criterion = root / "OnePointResolvent"
    subproject = root / "subprojects/riemann-one-point-resolvent"

    projects: list[ProjectSpec] = []
    if construction.is_dir():
        projects.append(
            ProjectSpec(
                "construction",
                root,
                "Riemann Prime–Resolvent Programme",
                "https://github.com/lluiseriksson/riemann-prime-resolvent",
                "AGPL-3.0-or-later",
                "https://spdx.org/licenses/AGPL-3.0-or-later.html",
            )
        )
        if (subproject / "OnePointResolvent").is_dir():
            projects.append(
                ProjectSpec(
                    "criterion",
                    subproject,
                    "One-Point Resolvent–Hausdorff Programme",
                    "https://github.com/lluiseriksson/riemann-prime-resolvent/tree/main/subprojects/riemann-one-point-resolvent",
                    "Apache-2.0",
                    "https://spdx.org/licenses/Apache-2.0.html",
                )
            )
    elif criterion.is_dir():
        projects.append(
            ProjectSpec(
                "criterion",
                root,
                "One-Point Resolvent–Hausdorff Programme",
                "https://github.com/lluiseriksson/riemann-prime-resolvent/tree/main/subprojects/riemann-one-point-resolvent",
                "Apache-2.0",
                "https://spdx.org/licenses/Apache-2.0.html",
            )
        )
    return projects


def audit_project(spec: ProjectSpec) -> tuple[ProjectState | None, list[str]]:
    errors: list[str] = []
    root = spec.root
    required = [
        root / "VERSION",
        root / "CITATION.cff",
        root / "codemeta.json",
        root / "CHANGELOG.md",
        root / "lean-toolchain",
        root / "lakefile.lean",
    ]
    if not all(_regular_file(path, errors, spec.label) for path in required):
        return None, errors

    version = _read_canonical_line(root / "VERSION", errors, spec.label)
    if VERSION_RE.fullmatch(version) is None:
        errors.append(f"{spec.label}: unsafe VERSION value {version!r}")

    try:
        cff = parse_cff_top_level(root / "CITATION.cff")
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        errors.append(f"{spec.label}: invalid CITATION.cff: {exc}")
        cff = {}

    _required_scalar(cff, "cff-version", "1.2.0", errors, spec.label)
    _required_scalar(cff, "title", spec.title, errors, spec.label)
    _required_scalar(cff, "version", version, errors, spec.label)
    _required_scalar(cff, "repository-code", spec.repository, errors, spec.label)
    _required_scalar(cff, "license", spec.cff_license, errors, spec.label)
    _required_scalar(cff, "type", "software", errors, spec.label)

    released = cff.get("date-released", "")
    try:
        date.fromisoformat(released)
    except ValueError:
        errors.append(f"{spec.label}: date-released is not an ISO date: {released!r}")

    try:
        codemeta = json.loads((root / "codemeta.json").read_text(encoding="utf-8"))
        if not isinstance(codemeta, dict):
            raise ValueError("top-level value must be an object")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"{spec.label}: invalid codemeta.json: {exc}")
        codemeta = {}

    _required_scalar(
        codemeta, "@context", "https://doi.org/10.5063/schema/codemeta-2.0", errors, spec.label
    )
    _required_scalar(codemeta, "@type", "SoftwareSourceCode", errors, spec.label)
    _required_scalar(codemeta, "name", spec.title, errors, spec.label)
    _required_scalar(codemeta, "version", version, errors, spec.label)
    _required_scalar(codemeta, "codeRepository", spec.repository, errors, spec.label)
    _required_scalar(codemeta, "license", spec.codemeta_license, errors, spec.label)
    modified = codemeta.get("dateModified", "")
    try:
        modified_date = date.fromisoformat(modified)
        released_date = date.fromisoformat(released)
        if modified_date < released_date:
            errors.append(
                f"{spec.label}: dateModified {modified!r} predates date-released {released!r}"
            )
    except (TypeError, ValueError):
        errors.append(f"{spec.label}: dateModified is not an ISO date: {modified!r}")
    languages = codemeta.get("programmingLanguage")
    if not isinstance(languages, list) or not {"Lean 4", "Python"}.issubset(set(languages)):
        errors.append(f"{spec.label}: programmingLanguage must include Lean 4 and Python")

    try:
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
        if re.search(rf"(?m)^##\s+{re.escape(version)}(?:\s|$)", changelog) is None:
            errors.append(f"{spec.label}: CHANGELOG.md has no section for {version}")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{spec.label}: cannot read CHANGELOG.md: {exc}")

    pyproject_path = root / "pyproject.toml"
    if pyproject_path.is_file():
        try:
            pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
            project_table = pyproject.get("project")
            if isinstance(project_table, dict) and "version" in project_table:
                expected_python_version = version
                match = re.fullmatch(r"(\d+\.\d+\.\d+)-(.+)", version)
                if match:
                    expected_python_version = (
                        f"{match.group(1)}+" + match.group(2).replace("-", ".")
                    )
                observed_python_version = project_table.get("version")
                if observed_python_version != expected_python_version:
                    errors.append(
                        f"{spec.label}: pyproject project.version mismatch: "
                        f"expected {expected_python_version!r}, got {observed_python_version!r}"
                    )
        except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"{spec.label}: invalid pyproject.toml: {exc}")

    toolchain = _read_canonical_line(root / "lean-toolchain", errors, spec.label)
    if TOOLCHAIN_RE.fullmatch(toolchain) is None:
        errors.append(f"{spec.label}: invalid lean-toolchain value {toolchain!r}")

    try:
        lakefile = (root / "lakefile.lean").read_text(encoding="utf-8")
        revisions = MATHLIB_REV_RE.findall(lakefile)
        if len(revisions) != 1:
            errors.append(
                f"{spec.label}: lakefile.lean must contain exactly one pinned 40-char Mathlib revision"
            )
            mathlib_revision = ""
        else:
            mathlib_revision = revisions[0]
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{spec.label}: cannot read lakefile.lean: {exc}")
        mathlib_revision = ""

    state = ProjectState(spec, version, released, toolchain, mathlib_revision)
    return state, errors


def audit_repository(root: Path, *, tag: str | None = None) -> list[str]:
    root = root.resolve()
    projects = _discover_projects(root)
    if not projects:
        return ["unrecognized repository layout; no construction or criterion Lean project found"]

    errors: list[str] = []
    states: list[ProjectState] = []
    for project in projects:
        state, project_errors = audit_project(project)
        errors.extend(project_errors)
        if state is not None:
            states.append(state)

    if len(states) > 1:
        versions = {state.version for state in states}
        if len(versions) != 1:
            errors.append(f"monorepo VERSION values differ: {sorted(versions)}")
        toolchains = {state.toolchain for state in states}
        if len(toolchains) != 1:
            errors.append(f"monorepo lean-toolchain values differ: {sorted(toolchains)}")
        revisions = {state.mathlib_revision for state in states}
        if len(revisions) != 1:
            errors.append(f"monorepo Mathlib revisions differ: {sorted(revisions)}")

    if tag is not None and states:
        expected_tag = f"v{states[0].version}"
        if tag != expected_tag:
            errors.append(f"release tag mismatch: expected {expected_tag!r}, got {tag!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--tag", help="require an exact vVERSION release tag")
    args = parser.parse_args()

    errors = audit_repository(args.root, tag=args.tag)
    if errors:
        print("Metadata audit FAILED:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    project_count = len(_discover_projects(args.root.resolve()))
    print(f"Metadata audit passed for {project_count} project(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the final-release research frontier and archive policy."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IDS = ("RF-1", "RF-2", "RF-3", "RF-4")
HEX40 = re.compile(r"^[0-9a-f]{40}$")


class FrontierError(RuntimeError):
    """Raised when the closeout frontier is malformed."""


def load_frontier(root: Path) -> dict:
    path = root / "docs/research-frontier.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FrontierError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise FrontierError("research-frontier.json must contain an object")
    return value


def validate_frontier(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    try:
        data = load_frontier(root)
    except FrontierError as exc:
        return [str(exc)]

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("closure_state") != "engineering-complete-research-open":
        errors.append("closure_state must be engineering-complete-research-open")

    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot read VERSION: {exc}")
        version = ""
    expected_tag = f"v{version}" if version else ""
    if data.get("release_tag") != expected_tag:
        errors.append(
            f"release_tag must match VERSION: expected {expected_tag!r}, "
            f"got {data.get('release_tag')!r}"
        )

    prepared = data.get("prepared_from_commit")
    if not isinstance(prepared, str) or HEX40.fullmatch(prepared) is None:
        errors.append("prepared_from_commit must be a lowercase 40-character SHA")

    items = data.get("frontiers")
    if not isinstance(items, list):
        errors.append("frontiers must be an array")
        items = []

    ids = [item.get("id") for item in items if isinstance(item, dict)]
    if tuple(ids) != EXPECTED_IDS:
        errors.append(f"frontier IDs must be ordered exactly as {EXPECTED_IDS}")
    if len(ids) != len(set(ids)):
        errors.append("frontier IDs must be unique")

    id_set = set(ids)
    graph: dict[str, list[str]] = {}
    for item in items:
        if not isinstance(item, dict):
            errors.append("each frontier entry must be an object")
            continue
        frontier_id = item.get("id")
        if item.get("status") != "open-research":
            errors.append(f"{frontier_id}: status must be open-research")
        for field in ("title", "area", "summary"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{frontier_id}: {field} must be non-empty")
        for field in ("acceptance_criteria", "non_goals", "related_files", "depends_on"):
            value = item.get(field)
            if not isinstance(value, list):
                errors.append(f"{frontier_id}: {field} must be an array")
                continue
            if field in {"acceptance_criteria", "related_files"} and not value:
                errors.append(f"{frontier_id}: {field} must not be empty")
            if any(not isinstance(entry, str) or not entry.strip() for entry in value):
                errors.append(f"{frontier_id}: {field} entries must be non-empty strings")
        dependencies = item.get("depends_on", [])
        if isinstance(dependencies, list):
            unknown = [dep for dep in dependencies if dep not in id_set]
            if unknown:
                errors.append(f"{frontier_id}: unknown dependencies {unknown}")
            if frontier_id in dependencies:
                errors.append(f"{frontier_id}: self-dependency is forbidden")
            graph[str(frontier_id)] = [str(dep) for dep in dependencies]

        for relative in item.get("related_files", []):
            if isinstance(relative, str) and not (root / relative).exists():
                errors.append(f"{frontier_id}: related file does not exist: {relative}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            errors.append(f"dependency cycle contains {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in graph.get(node, []):
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)

    markdown_files = {
        "RF-1": "docs/research-frontier/issues/RF-1-prime-tail.md",
        "RF-2": "docs/research-frontier/issues/RF-2-slit-plane.md",
        "RF-3": "docs/research-frontier/issues/RF-3-spectral-model.md",
        "RF-4": "docs/research-frontier/issues/RF-4-convergence.md",
    }
    try:
        frontier_md = (root / "docs/RESEARCH-FRONTIER.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot read docs/RESEARCH-FRONTIER.md: {exc}")
        frontier_md = ""
    for frontier_id, relative in markdown_files.items():
        if f"## {frontier_id}" not in frontier_md:
            errors.append(f"RESEARCH-FRONTIER.md is missing section {frontier_id}")
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read {relative}: {exc}")
            continue
        if f"<!-- frontier-id: {frontier_id} -->" not in text:
            errors.append(f"{relative}: missing stable frontier marker")
        if "## Acceptance criteria" not in text:
            errors.append(f"{relative}: missing acceptance criteria")

    try:
        final_release = (root / "docs/FINAL-RELEASE.md").read_text(encoding="utf-8")
        maintenance = (root / "MAINTENANCE.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot read closeout policy documents: {exc}")
        final_release = maintenance = ""
    if expected_tag and expected_tag not in final_release:
        errors.append("FINAL-RELEASE.md must name the VERSION-derived tag")
    if "does **not** prove" not in final_release:
        errors.append("FINAL-RELEASE.md must contain the mathematical non-claim")
    if "Archive gate" not in maintenance:
        errors.append("MAINTENANCE.md must contain an archive gate")
    if data.get("archive_policy", {}).get("recommended_now") is not False:
        errors.append("archive_policy.recommended_now must be false while frontiers are open")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate_frontier(args.root)
    if errors:
        print("Research-frontier closeout FAILED:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("Research-frontier closeout passed for RF-1 through RF-4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

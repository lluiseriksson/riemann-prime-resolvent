from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_research_frontier import validate_frontier  # noqa: E402


def test_repository_frontier_is_consistent() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_frontier(root) == []


def _fixture(tmp_path: Path) -> Path:
    source = Path(__file__).resolve().parents[1]
    root = tmp_path / "project"
    for relative in [
        "VERSION",
        "MAINTENANCE.md",
        "docs/FINAL-RELEASE.md",
        "docs/RESEARCH-FRONTIER.md",
        "docs/research-frontier.json",
    ]:
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, destination)
    for path in (source / "docs/research-frontier/issues").glob("*.md"):
        destination = root / "docs/research-frontier/issues" / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    data = json.loads((root / "docs/research-frontier.json").read_text(encoding="utf-8"))
    for item in data["frontiers"]:
        for relative in item["related_files"]:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("fixture\n", encoding="utf-8")
    return root


def test_release_tag_must_match_version(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    path = root / "docs/research-frontier.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["release_tag"] = "v9.9.9"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("release_tag must match VERSION" in error for error in validate_frontier(root))


def test_dependency_cycle_is_rejected(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    path = root / "docs/research-frontier.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["frontiers"][0]["depends_on"] = ["RF-4"]
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("dependency cycle" in error for error in validate_frontier(root))


def test_missing_issue_marker_is_rejected(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    path = root / "docs/research-frontier/issues/RF-2-slit-plane.md"
    path.write_text(path.read_text(encoding="utf-8").replace(
        "<!-- frontier-id: RF-2 -->", ""
    ), encoding="utf-8")
    assert any("missing stable frontier marker" in error for error in validate_frontier(root))

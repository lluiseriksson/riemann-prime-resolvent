from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from check_workflows import audit_text  # noqa: E402


SHA = "34e114876b0b11c390a56381ad16ebd13914f8d5"


def _path(tmp_path: Path) -> Path:
    return tmp_path / ".github/workflows/ci.yml"


def test_pinned_remote_and_local_actions_are_allowed(tmp_path: Path) -> None:
    text = f"""
name: test
jobs:
  job:
    steps:
      - uses: actions/checkout@{SHA} # v4
      - uses: ./local-action
"""
    assert audit_text(_path(tmp_path), text, tmp_path) == []


@pytest.mark.parametrize(
    "reference",
    [
        "actions/checkout@v4",
        "actions/setup-python@main",
        "docker/login-action@latest",
        "actions/upload-artifact",
    ],
)
def test_mutable_or_missing_action_refs_are_rejected(tmp_path: Path, reference: str) -> None:
    text = f"""
name: test
jobs:
  job:
    steps:
      - uses: {reference}
"""
    failures = audit_text(_path(tmp_path), text, tmp_path)
    assert failures


def test_pull_request_target_is_rejected(tmp_path: Path) -> None:
    text = """
on:
  pull_request_target:
jobs:
  job:
    steps:
      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5
"""
    assert any("pull_request_target" in failure for failure in audit_text(_path(tmp_path), text, tmp_path))


def test_network_pipe_to_shell_is_rejected(tmp_path: Path) -> None:
    text = """
jobs:
  job:
    steps:
      - run: curl https://example.invalid/install.sh | bash
"""
    assert any("piped" in failure for failure in audit_text(_path(tmp_path), text, tmp_path))

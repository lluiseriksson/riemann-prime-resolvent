from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from check_workflows import audit_repository, audit_text  # noqa: E402

SHA = "34e114876b0b11c390a56381ad16ebd13914f8d5"


def _path(tmp_path: Path) -> Path:
    return tmp_path / ".github/workflows/ci.yml"


def _valid_workflow(extra_steps: str = "") -> str:
    return f"""
name: test
on: [push]
permissions:
  contents: read
jobs:
  job:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@{SHA} # v4
        with:
          persist-credentials: false
      - uses: ./local-action
{extra_steps}
"""


def test_pinned_remote_and_local_actions_are_allowed(tmp_path: Path) -> None:
    assert audit_text(_path(tmp_path), _valid_workflow(), tmp_path) == []


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
    text = _valid_workflow(
        f"      - uses: {reference}\n"
        + ("        with:\n          persist-credentials: false\n" if reference.startswith("actions/checkout@") else "")
    )
    assert audit_text(_path(tmp_path), text, tmp_path)


def test_pull_request_target_is_rejected(tmp_path: Path) -> None:
    text = _valid_workflow().replace("on: [push]", "on:\n  pull_request_target:")
    assert any("pull_request_target" in failure for failure in audit_text(_path(tmp_path), text, tmp_path))


def test_network_pipe_to_shell_is_rejected(tmp_path: Path) -> None:
    text = _valid_workflow("      - run: curl https://example.invalid/install.sh | bash\n")
    assert any("interpreter" in failure for failure in audit_text(_path(tmp_path), text, tmp_path))


def test_mutable_runner_alias_is_rejected(tmp_path: Path) -> None:
    text = _valid_workflow().replace("ubuntu-24.04", "ubuntu-latest")
    assert any("fixed image label" in failure for failure in audit_text(_path(tmp_path), text, tmp_path))


def test_top_level_permissions_are_required(tmp_path: Path) -> None:
    text = _valid_workflow().replace("permissions:\n  contents: read\n", "")
    assert any("top-level permissions" in failure for failure in audit_text(_path(tmp_path), text, tmp_path))


def test_checkout_must_not_persist_credentials(tmp_path: Path) -> None:
    text = _valid_workflow().replace("persist-credentials: false", "persist-credentials: true")
    assert any("persist-credentials" in failure for failure in audit_text(_path(tmp_path), text, tmp_path))


def test_repository_audit_scans_dockerfile_and_shell_scripts(tmp_path: Path) -> None:
    workflow = _path(tmp_path)
    workflow.parent.mkdir(parents=True)
    workflow.write_text(_valid_workflow(), encoding="utf-8")
    (tmp_path / "Dockerfile").write_text(
        "FROM ubuntu:24.04\nRUN wget https://example.invalid/i | sh\n", encoding="utf-8"
    )
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/ok.sh").write_text("#!/bin/sh\necho ok\n", encoding="utf-8")
    _, failures = audit_repository(tmp_path)
    assert any("Dockerfile" in failure and "interpreter" in failure for failure in failures)


def test_mutable_raw_github_reference_is_rejected(tmp_path: Path) -> None:
    dockerfile = tmp_path / "Dockerfile"
    text = "RUN curl -O https://raw.githubusercontent.com/example/tool/main/install.sh\n"
    assert any("main/master" in failure for failure in audit_text(dockerfile, text, tmp_path))

def test_job_timeout_is_required_and_bounded(tmp_path: Path) -> None:
    missing = _valid_workflow().replace("    timeout-minutes: 10\n", "")
    assert any("timeout-minutes" in failure for failure in audit_text(_path(tmp_path), missing, tmp_path))

    excessive = _valid_workflow().replace("timeout-minutes: 10", "timeout-minutes: 999")
    assert any("between 1 and 120" in failure for failure in audit_text(_path(tmp_path), excessive, tmp_path))

def test_comment_only_installer_examples_are_ignored(tmp_path: Path) -> None:
    dockerfile = tmp_path / "Dockerfile"
    text = "# Never use: curl https://example.invalid/install.sh | sh\nFROM ubuntu:24.04\n"
    assert audit_text(dockerfile, text, tmp_path) == []

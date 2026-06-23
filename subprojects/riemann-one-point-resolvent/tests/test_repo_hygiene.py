from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from check_repo_hygiene import audit  # noqa: E402


def _write_lf(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


def _skip_if_case_insensitive(root: Path) -> None:
    probe = root / "CaseProbe"
    probe.write_bytes(b"x")
    try:
        if (root / "caseprobe").exists():
            pytest.skip("filesystem is case-insensitive")
    finally:
        probe.unlink(missing_ok=True)


def test_clean_minimal_tree_passes(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    _write_lf(tmp_path / "docs/index.md", "# ok\n")
    _write_lf(tmp_path / "script.py", "print('ok')\n")
    assert audit(tmp_path) == []


def test_crlf_text_file_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_bytes(b"# bad\r\n")
    failures = audit(tmp_path)
    assert any("CRLF" in failure for failure in failures)


def test_casefold_collision_is_rejected(tmp_path: Path) -> None:
    _skip_if_case_insensitive(tmp_path)
    _write_lf(tmp_path / "Alpha.txt", "a\n")
    _write_lf(tmp_path / "alpha.txt", "b\n")
    failures = audit(tmp_path)
    assert any("case-insensitive" in failure for failure in failures)


def test_generated_cache_file_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "x.pyc").write_bytes(b"cache")
    failures = audit(tmp_path)
    assert any("forbidden" in failure for failure in failures)

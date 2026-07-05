from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_docs_assets import audit  # noqa: E402


def _project(tmp_path: Path, url: str) -> Path:
    root = tmp_path / "project"
    root.mkdir()
    (root / "mkdocs.yml").write_text(
        "site_name: test\nextra_javascript:\n  - " + url + "\n",
        encoding="utf-8",
    )
    return root


def test_exact_jsdelivr_version_passes(tmp_path: Path) -> None:
    root = _project(
        tmp_path,
        "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js",
    )
    assert audit(root) == []


def test_major_only_jsdelivr_version_is_rejected(tmp_path: Path) -> None:
    root = _project(
        tmp_path,
        "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js",
    )
    assert any("exact semantic version" in failure for failure in audit(root))


def test_latest_reference_is_rejected(tmp_path: Path) -> None:
    root = _project(
        tmp_path,
        "https://cdn.jsdelivr.net/npm/mathjax@latest/es5/tex-mml-chtml.js",
    )
    failures = audit(root)
    assert any("mutable" in failure for failure in failures)


def test_http_reference_is_rejected(tmp_path: Path) -> None:
    root = _project(tmp_path, "http://example.invalid/asset.js")
    assert any("must use HTTPS" in failure for failure in audit(root))

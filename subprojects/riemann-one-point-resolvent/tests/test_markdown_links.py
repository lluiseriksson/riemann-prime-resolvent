from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from check_markdown_links import audit_markdown_links, markdown_destination  # noqa: E402


def test_markdown_destination_supports_angle_paths_and_titles() -> None:
    assert markdown_destination("<assets/a file.svg>") == "assets/a file.svg"
    assert markdown_destination('docs/index.md "Documentation"') == "docs/index.md"


def test_angle_destination_with_spaces_is_checked(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    assets = docs / "assets"
    assets.mkdir(parents=True)
    (assets / "a file.svg").write_text("<svg/>", encoding="utf-8")
    (docs / "index.md").write_text("[figure](<assets/a file.svg>)\n", encoding="utf-8")

    checked, failures = audit_markdown_links(tmp_path)

    assert checked == 1
    assert failures == []


def test_percent_encoded_target_and_title_are_supported(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a file.md").write_text("ok\n", encoding="utf-8")
    (docs / "index.md").write_text(
        '[encoded](a%20file.md "local title")\n', encoding="utf-8"
    )

    checked, failures = audit_markdown_links(tmp_path)

    assert checked == 1
    assert failures == []


def test_missing_and_escaping_targets_are_reported(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "index.md").write_text(
        "[missing](missing.md)\n[escape](../../outside.md)\n", encoding="utf-8"
    )

    checked, failures = audit_markdown_links(tmp_path)

    assert checked == 2
    assert failures == [
        "docs/index.md: missing missing.md",
        "docs/index.md: escapes repository: ../../outside.md",
    ]


def test_external_and_fragment_only_targets_are_skipped(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "[web](https://example.com/a) [mail](mailto:a@example.com) [local](#section)\n",
        encoding="utf-8",
    )

    checked, failures = audit_markdown_links(tmp_path)

    assert checked == 0
    assert failures == []

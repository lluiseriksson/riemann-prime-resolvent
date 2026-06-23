from __future__ import annotations

import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from check_metadata import audit_repository  # noqa: E402

VERSION = "1.2.3"
REVISION = "a" * 40
TOOLCHAIN = "leanprover/lean4:v4.31.0"


def _write_lf(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


def _write_project(root: Path, *, criterion: bool = False) -> None:
    marker = root / ("OnePointResolvent" if criterion else "RiemannPrimeResolvent")
    marker.mkdir(parents=True)
    if criterion:
        title = "One-Point Resolvent–Hausdorff Programme"
        repository = (
            "https://github.com/lluiseriksson/riemann-prime-resolvent/"
            "tree/main/subprojects/riemann-one-point-resolvent"
        )
        cff_license = "Apache-2.0"
        codemeta_license = "https://spdx.org/licenses/Apache-2.0.html"
    else:
        title = "Riemann Prime–Resolvent Programme"
        repository = "https://github.com/lluiseriksson/riemann-prime-resolvent"
        cff_license = "AGPL-3.0-or-later"
        codemeta_license = "https://spdx.org/licenses/AGPL-3.0-or-later.html"

    root.mkdir(parents=True, exist_ok=True)
    _write_lf(root / "VERSION", f"{VERSION}\n")
    _write_lf(root / "lean-toolchain", f"{TOOLCHAIN}\n")
    _write_lf(
        root / "lakefile.lean",
        'require mathlib from git\n  "https://github.com/leanprover-community/mathlib4.git" @\n'
        f'    "{REVISION}"\n',
    )
    _write_lf(root / "CHANGELOG.md", f"# Changelog\n\n## {VERSION} — 2026-06-23\n")
    _write_lf(
        root / "CITATION.cff",
        f'''cff-version: 1.2.0
title: "{title}"
version: "{VERSION}"
date-released: "2026-06-23"
repository-code: "{repository}"
license: {cff_license}
type: software
''',
    )
    _write_lf(
        root / "codemeta.json",
        json.dumps(
            {
                "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
                "@type": "SoftwareSourceCode",
                "name": title,
                "version": VERSION,
                "codeRepository": repository,
                "license": codemeta_license,
                "dateModified": "2026-06-23",
                "programmingLanguage": ["Lean 4", "Python"],
            },
            ensure_ascii=False,
        )
        + "\n",
    )


def test_valid_construction_metadata_passes(tmp_path: Path) -> None:
    _write_project(tmp_path)
    assert audit_repository(tmp_path) == []


def test_citation_version_drift_is_rejected(tmp_path: Path) -> None:
    _write_project(tmp_path)
    citation = tmp_path / "CITATION.cff"
    _write_lf(
        citation,
        citation.read_text(encoding="utf-8").replace('version: "1.2.3"', 'version: "9.9.9"'),
    )
    assert any("version mismatch" in error for error in audit_repository(tmp_path))


def test_release_tag_must_match_version_exactly(tmp_path: Path) -> None:
    _write_project(tmp_path)
    assert audit_repository(tmp_path, tag="v1.2.3") == []
    assert any("release tag mismatch" in error for error in audit_repository(tmp_path, tag="v1.2"))


def test_monorepo_toolchain_and_mathlib_pins_must_match(tmp_path: Path) -> None:
    _write_project(tmp_path)
    subproject = tmp_path / "subprojects/riemann-one-point-resolvent"
    _write_project(subproject, criterion=True)
    _write_lf(subproject / "lean-toolchain", "leanprover/lean4:v4.30.0\n")
    _write_lf(
        subproject / "lakefile.lean",
        'require mathlib from git "https://github.com/leanprover-community/mathlib4.git" @\n'
        f'  "{"b" * 40}"\n',
    )
    errors = audit_repository(tmp_path)
    assert any("lean-toolchain values differ" in error for error in errors)
    assert any("Mathlib revisions differ" in error for error in errors)


def test_noncanonical_version_file_is_rejected(tmp_path: Path) -> None:
    _write_project(tmp_path)
    (tmp_path / "VERSION").write_text(VERSION, encoding="utf-8")
    assert any("LF-terminated" in error for error in audit_repository(tmp_path))

def test_codemeta_modified_date_cannot_precede_release(tmp_path: Path) -> None:
    _write_project(tmp_path)
    path = tmp_path / "codemeta.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["dateModified"] = "2026-06-22"
    _write_lf(path, json.dumps(data, ensure_ascii=False) + "\n")
    assert any("predates" in error for error in audit_repository(tmp_path))


def test_repository_version_maps_to_pep440_local_version(tmp_path: Path) -> None:
    _write_project(tmp_path)
    _write_lf(tmp_path / "VERSION", "1.2.3-docs-integrated\n")
    citation = tmp_path / "CITATION.cff"
    _write_lf(
        citation,
        citation.read_text(encoding="utf-8").replace('version: "1.2.3"', 'version: "1.2.3-docs-integrated"'),
    )
    codemeta_path = tmp_path / "codemeta.json"
    codemeta = json.loads(codemeta_path.read_text(encoding="utf-8"))
    codemeta["version"] = "1.2.3-docs-integrated"
    _write_lf(codemeta_path, json.dumps(codemeta, ensure_ascii=False) + "\n")
    changelog = tmp_path / "CHANGELOG.md"
    _write_lf(changelog, "# Changelog\n\n## 1.2.3-docs-integrated — 2026-06-23\n")
    _write_lf(
        tmp_path / "pyproject.toml",
        '[project]\nname = "demo"\nversion = "1.2.3+docs.integrated"\n',
    )
    assert audit_repository(tmp_path) == []

    _write_lf(
        tmp_path / "pyproject.toml",
        '[project]\nname = "demo"\nversion = "1.2.3"\n',
    )
    assert any("pyproject project.version mismatch" in error for error in audit_repository(tmp_path))

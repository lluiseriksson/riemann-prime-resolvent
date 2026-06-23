from __future__ import annotations

import os
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import package_release  # noqa: E402
from package_release import FIXED_ZIP_TIME, build_archive  # noqa: E402
from release_common import (  # noqa: E402
    MANIFEST_NAME,
    MIRRORED_TOOLING_FILES,
    ReleaseError,
    audit_release,
    parse_manifest,
    render_manifest,
    validate_manifest,
    validate_release_policy,
    write_manifest,
)


def _project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    (root / "docs/contracts").mkdir(parents=True)
    (root / "src").mkdir()
    (root / "scripts").mkdir()
    (root / "README.md").write_text("# Test project\n", encoding="utf-8")
    (root / "LICENSE").write_text("Test license\n", encoding="utf-8")
    (root / "VERSION").write_text("1.2.3\n", encoding="utf-8")
    (root / "docs/contracts/resolvent-interface.json").write_text(
        '{"format": "test"}\n', encoding="utf-8"
    )
    (root / "src/data.txt").write_text("alpha\n", encoding="utf-8")
    (root / "scripts/run.sh").write_text("#!/usr/bin/env bash\necho ok\n", encoding="utf-8")
    write_manifest(root)
    return root


def test_generate_manifest_check_is_read_only(tmp_path: Path) -> None:
    root = _project(tmp_path)
    shutil.copy2(SCRIPTS / "release_common.py", root / "scripts/release_common.py")
    shutil.copy2(SCRIPTS / "generate_manifest.py", root / "scripts/generate_manifest.py")
    subprocess.run([sys.executable, "scripts/generate_manifest.py"], cwd=root, check=True)

    manifest = root / MANIFEST_NAME
    before = manifest.read_bytes()
    (root / "src/data.txt").write_text("changed\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/generate_manifest.py", "--check"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "stale" in result.stderr
    assert manifest.read_bytes() == before


def test_manifest_rejects_unlisted_file(tmp_path: Path) -> None:
    root = _project(tmp_path)
    (root / "unexpected.txt").write_text("not declared\n", encoding="utf-8")
    with pytest.raises(ReleaseError, match="files missing from manifest"):
        validate_manifest(root)


def test_manifest_rejects_duplicate_and_unsafe_rows(tmp_path: Path) -> None:
    root = _project(tmp_path)
    data = (root / MANIFEST_NAME).read_bytes()
    lines = data.decode("utf-8").splitlines()
    duplicate = ("\n".join(lines + [lines[1]]) + "\n").encode("utf-8")
    with pytest.raises(ReleaseError, match="duplicate path"):
        parse_manifest(duplicate)

    unsafe = data.replace(b"LICENSE,", b"../LICENSE,", 1)
    with pytest.raises(ReleaseError, match="unsafe path|non-canonical path"):
        parse_manifest(unsafe)


def test_manifest_rejects_casefold_collisions() -> None:
    data = (
        "path,bytes,sha256\n"
        f"A.txt,0,{'0' * 64}\n"
        f"a.txt,0,{'0' * 64}\n"
    ).encode()
    with pytest.raises(ReleaseError, match="colliding paths"):
        parse_manifest(data)


def test_manifest_rejects_windows_reserved_and_non_nfc_paths() -> None:
    reserved = (
        "path,bytes,sha256\n" f"CON.txt,0,{'0' * 64}\n"
    ).encode()
    with pytest.raises(ReleaseError, match="Windows-reserved"):
        parse_manifest(reserved)

    decomposed = unicodedata.normalize("NFD", "café.txt")
    non_nfc = (
        "path,bytes,sha256\n" f"{decomposed},0,{'0' * 64}\n"
    ).encode("utf-8")
    with pytest.raises(ReleaseError, match="NFC"):
        parse_manifest(non_nfc)


def test_source_inventory_rejects_case_collisions_when_filesystem_allows_them(
    tmp_path: Path,
) -> None:
    root = _project(tmp_path)
    upper = root / "src/Case.txt"
    lower = root / "src/case.txt"
    upper.write_text("upper\n", encoding="utf-8")
    lower.write_text("lower\n", encoding="utf-8")
    if upper.samefile(lower):
        pytest.skip("filesystem is case-insensitive")
    with pytest.raises(ReleaseError, match="colliding paths"):
        render_manifest(root)


def test_contract_mirror_must_be_byte_identical(tmp_path: Path) -> None:
    root = _project(tmp_path)
    mirror = root / "subprojects/riemann-one-point-resolvent/docs/contracts"
    mirror.mkdir(parents=True)
    (mirror / "resolvent-interface.json").write_text(
        '{"format": "different"}\n', encoding="utf-8"
    )
    write_manifest(root)
    with pytest.raises(ReleaseError, match="not byte-identical"):
        validate_release_policy(root)


def test_mirrored_release_tooling_must_be_byte_identical(tmp_path: Path) -> None:
    root = _project(tmp_path)
    subproject = root / "subprojects/riemann-one-point-resolvent"
    (subproject / "docs/contracts").mkdir(parents=True)
    (subproject / "docs/contracts/resolvent-interface.json").write_bytes(
        (root / "docs/contracts/resolvent-interface.json").read_bytes()
    )
    for relative in MIRRORED_TOOLING_FILES:
        primary = root / relative
        mirror = subproject / relative
        primary.parent.mkdir(parents=True, exist_ok=True)
        mirror.parent.mkdir(parents=True, exist_ok=True)
        primary.write_text(f"same: {relative}\n", encoding="utf-8")
        mirror.write_bytes(primary.read_bytes())
    (subproject / MIRRORED_TOOLING_FILES[0]).write_text("drift\n", encoding="utf-8")

    with pytest.raises(ReleaseError, match="mirrored tooling"):
        validate_release_policy(root)


def test_empty_paper_directory_is_rejected(tmp_path: Path) -> None:
    root = _project(tmp_path)
    (root / "paper").mkdir()
    with pytest.raises(ReleaseError, match="paper directories"):
        validate_release_policy(root)


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlinks unavailable")
def test_included_symlink_is_rejected(tmp_path: Path) -> None:
    root = _project(tmp_path)
    link = root / "src/readme-link"
    try:
        link.symlink_to(root / "README.md")
    except OSError as exc:
        pytest.skip(f"cannot create symlink: {exc}")
    with pytest.raises(ReleaseError, match="symlink"):
        render_manifest(root)


def test_archive_is_manifest_driven_safe_and_byte_reproducible(tmp_path: Path) -> None:
    root = _project(tmp_path)
    audit_release(root)

    first, checksum = build_archive(root, tmp_path / "out-a", project_name="sample")
    for path in root.rglob("*"):
        if path.is_file():
            os.utime(path, (1_800_000_000, 1_800_000_000))
    second, _ = build_archive(root, tmp_path / "out-b", project_name="sample")

    assert first.read_bytes() == second.read_bytes()
    assert first.name in checksum.read_text(encoding="utf-8")
    with zipfile.ZipFile(first) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names))
        assert names[-1] == f"sample-1.2.3/{MANIFEST_NAME}"
        assert all(name.startswith("sample-1.2.3/") for name in names)
        assert all(".." not in Path(name).parts for name in names)
        assert archive.comment == b""
        assert all(info.date_time == FIXED_ZIP_TIME for info in archive.infolist())
        assert all(info.compress_type == zipfile.ZIP_STORED for info in archive.infolist())
        assert all(info.extra == b"" and info.comment == b"" for info in archive.infolist())
        script_info = archive.getinfo("sample-1.2.3/scripts/run.sh")
        assert (script_info.external_attr >> 16) & 0o777 == 0o755


def test_archive_rejects_mutation_between_audit_and_snapshot(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _project(tmp_path)
    real_audit = package_release.audit_release

    def mutating_audit(project: Path):
        entries = real_audit(project)
        (project / "src/data.txt").write_text("mutated after audit\n", encoding="utf-8")
        return entries

    monkeypatch.setattr(package_release, "audit_release", mutating_audit)
    with pytest.raises(ReleaseError, match="source changed after manifest audit"):
        build_archive(root, tmp_path / "out", project_name="sample")


def test_archive_rejects_mutation_during_archive_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _project(tmp_path)
    real_verify = package_release.verify_archive

    def mutating_verify(*args, **kwargs):
        real_verify(*args, **kwargs)
        (root / "src/data.txt").write_text("mutated during build\n", encoding="utf-8")

    monkeypatch.setattr(package_release, "verify_archive", mutating_verify)
    with pytest.raises(ReleaseError, match="source changed during archive creation"):
        build_archive(root, tmp_path / "out", project_name="sample")

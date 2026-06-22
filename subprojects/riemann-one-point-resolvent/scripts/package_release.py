#!/usr/bin/env python3
"""Build a deterministic, manifest-driven source ZIP with no external tools."""
from __future__ import annotations

import argparse
import hashlib
import os
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

from release_common import MANIFEST_NAME, ReleaseError, audit_release, load_manifest

ROOT = Path(__file__).resolve().parents[1]
PROJECT_NAME = "riemann-one-point-resolvent"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def _read_version(root: Path) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def _mode_for(relative: str, data: bytes) -> int:
    path = PurePosixPath(relative)
    executable = data.startswith(b"#!") or path.suffix.lower() == ".sh"
    return 0o755 if executable else 0o644


def _zip_info(name: str, mode: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.create_version = 20
    info.extract_version = 20
    info.external_attr = ((stat.S_IFREG | mode) & 0xFFFF) << 16
    info.internal_attr = 0
    return info


def verify_archive(
    archive: Path,
    *,
    root: Path,
    prefix: str,
    expected_paths: list[str],
    manifest_bytes: bytes,
) -> None:
    expected_names = [f"{prefix}/{path}" for path in expected_paths]
    expected_names.append(f"{prefix}/{MANIFEST_NAME}")

    with zipfile.ZipFile(archive, "r") as handle:
        names = handle.namelist()
        if len(names) != len(set(names)):
            raise ReleaseError("archive contains duplicate member names")
        if names != expected_names:
            raise ReleaseError("archive member inventory/order does not match the manifest")
        for info in handle.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts:
                raise ReleaseError(f"unsafe archive member: {info.filename}")
            if info.date_time != FIXED_ZIP_TIME:
                raise ReleaseError(f"non-deterministic timestamp for {info.filename}")
            if info.compress_type != zipfile.ZIP_STORED:
                raise ReleaseError(f"unexpected compression method for {info.filename}")

        if handle.read(f"{prefix}/{MANIFEST_NAME}") != manifest_bytes:
            raise ReleaseError("archive manifest bytes differ from the committed manifest")
        for relative in expected_paths:
            archived = handle.read(f"{prefix}/{relative}")
            local = (root / relative).read_bytes()
            if archived != local:
                raise ReleaseError(f"archive content mismatch: {relative}")


def build_archive(
    root: Path,
    output_directory: Path,
    *,
    project_name: str = PROJECT_NAME,
) -> tuple[Path, Path]:
    root = root.resolve()
    entries = audit_release(root)
    manifest_bytes, parsed_entries = load_manifest(root)
    if parsed_entries != entries:
        raise ReleaseError("internal error: audited and parsed manifest entries differ")

    version = _read_version(root)
    prefix = f"{project_name}-{version}"
    output_directory = output_directory.resolve()
    output_directory.mkdir(parents=True, exist_ok=True)
    archive = output_directory / f"{prefix}.zip"

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{archive.name}.", suffix=".tmp", dir=output_directory
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(temporary, "w", allowZip64=True) as handle:
            for entry in entries:
                data = (root / entry.path).read_bytes()
                handle.writestr(
                    _zip_info(f"{prefix}/{entry.path}", _mode_for(entry.path, data)),
                    data,
                )
            handle.writestr(
                _zip_info(f"{prefix}/{MANIFEST_NAME}", 0o644),
                manifest_bytes,
            )
        verify_archive(
            temporary,
            root=root,
            prefix=prefix,
            expected_paths=[entry.path for entry in entries],
            manifest_bytes=manifest_bytes,
        )
        os.replace(temporary, archive)
    finally:
        temporary.unlink(missing_ok=True)

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    checksum_data = f"{digest}  {archive.name}\n"
    checksum_tmp = checksum.with_name(f".{checksum.name}.tmp")
    checksum_tmp.write_text(checksum_data, encoding="utf-8")
    os.replace(checksum_tmp, checksum)
    return archive, checksum


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "release",
        help="directory for the ZIP and SHA-256 file (default: release/)",
    )
    args = parser.parse_args()
    try:
        archive, checksum = build_archive(ROOT, args.output_dir)
    except (OSError, UnicodeError, ReleaseError, zipfile.BadZipFile) as exc:
        print(f"Release packaging FAILED: {exc}", file=sys.stderr)
        return 1
    print(archive)
    print(checksum)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build a deterministic, manifest-driven source ZIP with no external tools."""
from __future__ import annotations

import argparse
import os
import re
import stat
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from release_common import (
    MANIFEST_NAME,
    ManifestEntry,
    ReleaseError,
    audit_release,
    load_manifest,
    sha256_bytes,
    sha256_file,
)

ROOT = Path(__file__).resolve().parents[1]
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
PROJECT_NAME_RE = re.compile(r"[a-z0-9][a-z0-9._-]*\Z")


@dataclass(frozen=True)
class SnapshotEntry:
    manifest: ManifestEntry
    data: bytes
    mode: int


def _default_project_name(root: Path) -> str:
    if (root / "RiemannPrimeResolvent").is_dir():
        return "riemann-prime-resolvent"
    if (root / "OnePointResolvent").is_dir():
        return "riemann-one-point-resolvent"
    return root.name.lower().replace("_", "-")


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
    info.extra = b""
    info.comment = b""
    return info


def _read_consistent_regular_file(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ReleaseError(f"source snapshot path is not a regular file: {path}")
    with path.open("rb") as handle:
        before = os.fstat(handle.fileno())
        data = handle.read()
        after = os.fstat(handle.fileno())
    identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if identity_before != identity_after:
        raise ReleaseError(f"source changed while being read: {path}")
    return data


def snapshot_entries(root: Path, entries: list[ManifestEntry]) -> list[SnapshotEntry]:
    """Read a manifest-verified immutable byte snapshot for archive creation."""

    snapshots: list[SnapshotEntry] = []
    for entry in entries:
        data = _read_consistent_regular_file(root / entry.path)
        observed_hash = sha256_bytes(data)
        if len(data) != entry.size or observed_hash != entry.sha256:
            raise ReleaseError(
                f"source changed after manifest audit: {entry.path} "
                f"(manifest size/hash {entry.size}/{entry.sha256}, "
                f"observed {len(data)}/{observed_hash})"
            )
        snapshots.append(SnapshotEntry(entry, data, _mode_for(entry.path, data)))
    return snapshots


def _validate_member_metadata(info: zipfile.ZipInfo, *, expected_mode: int) -> None:
    if info.date_time != FIXED_ZIP_TIME:
        raise ReleaseError(f"non-deterministic timestamp for {info.filename}")
    if info.compress_type != zipfile.ZIP_STORED:
        raise ReleaseError(f"unexpected compression method for {info.filename}")
    if info.create_system != 3:
        raise ReleaseError(f"archive member is not encoded with Unix metadata: {info.filename}")
    encoded_mode = (info.external_attr >> 16) & 0xFFFF
    if stat.S_IFMT(encoded_mode) != stat.S_IFREG:
        raise ReleaseError(f"archive member is not a regular file: {info.filename}")
    if stat.S_IMODE(encoded_mode) != expected_mode:
        raise ReleaseError(
            f"archive permission mismatch for {info.filename}: "
            f"expected {oct(expected_mode)}, got {oct(stat.S_IMODE(encoded_mode))}"
        )
    if info.extra or info.comment:
        raise ReleaseError(f"archive member has non-canonical extra metadata: {info.filename}")
    if info.flag_bits & 0x1:
        raise ReleaseError(f"encrypted archive member is forbidden: {info.filename}")


def verify_archive(
    archive: Path,
    *,
    prefix: str,
    snapshots: list[SnapshotEntry],
    manifest_bytes: bytes,
) -> None:
    expected_names = [f"{prefix}/{item.manifest.path}" for item in snapshots]
    manifest_name = f"{prefix}/{MANIFEST_NAME}"
    expected_names.append(manifest_name)

    with zipfile.ZipFile(archive, "r") as handle:
        if handle.comment:
            raise ReleaseError("archive comment must be empty")
        names = handle.namelist()
        if len(names) != len(set(names)):
            raise ReleaseError("archive contains duplicate member names")
        if names != expected_names:
            raise ReleaseError("archive member inventory/order does not match the manifest")

        for item in snapshots:
            name = f"{prefix}/{item.manifest.path}"
            info = handle.getinfo(name)
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or "\\" in info.filename:
                raise ReleaseError(f"unsafe archive member: {info.filename}")
            _validate_member_metadata(info, expected_mode=item.mode)
            archived = handle.read(name)
            if archived != item.data:
                raise ReleaseError(f"archive content mismatch: {item.manifest.path}")
            if info.file_size != item.manifest.size:
                raise ReleaseError(f"archive size mismatch: {item.manifest.path}")
            if sha256_bytes(archived) != item.manifest.sha256:
                raise ReleaseError(f"archive SHA-256 mismatch: {item.manifest.path}")

        manifest_info = handle.getinfo(manifest_name)
        _validate_member_metadata(manifest_info, expected_mode=0o644)
        if handle.read(manifest_name) != manifest_bytes:
            raise ReleaseError("archive manifest bytes differ from the committed manifest")
        if handle.testzip() is not None:
            raise ReleaseError("archive CRC validation failed")


def _verify_snapshot_still_matches_tree(
    root: Path, snapshots: list[SnapshotEntry], manifest_bytes: bytes
) -> None:
    if (root / MANIFEST_NAME).read_bytes() != manifest_bytes:
        raise ReleaseError("manifest changed during archive creation")
    for item in snapshots:
        data = _read_consistent_regular_file(root / item.manifest.path)
        if data != item.data:
            raise ReleaseError(f"source changed during archive creation: {item.manifest.path}")


def build_archive(
    root: Path,
    output_directory: Path,
    *,
    project_name: str | None = None,
) -> tuple[Path, Path]:
    root = root.resolve()
    entries = audit_release(root)
    manifest_bytes, parsed_entries = load_manifest(root)
    if parsed_entries != entries:
        raise ReleaseError("internal error: audited and parsed manifest entries differ")

    snapshots = snapshot_entries(root, entries)
    version_data = next(
        (item.data for item in snapshots if item.manifest.path == "VERSION"), None
    )
    if version_data is None:
        raise ReleaseError("VERSION is missing from the release snapshot")
    try:
        version = version_data.decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise ReleaseError("VERSION must be UTF-8") from exc

    resolved_name = project_name or _default_project_name(root)
    if PROJECT_NAME_RE.fullmatch(resolved_name) is None:
        raise ReleaseError(f"unsafe project name: {resolved_name!r}")
    prefix = f"{resolved_name}-{version}"

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
            for item in snapshots:
                handle.writestr(
                    _zip_info(f"{prefix}/{item.manifest.path}", item.mode),
                    item.data,
                )
            handle.writestr(
                _zip_info(f"{prefix}/{MANIFEST_NAME}", 0o644),
                manifest_bytes,
            )
        verify_archive(
            temporary,
            prefix=prefix,
            snapshots=snapshots,
            manifest_bytes=manifest_bytes,
        )
        _verify_snapshot_still_matches_tree(root, snapshots, manifest_bytes)
        os.replace(temporary, archive)
    finally:
        temporary.unlink(missing_ok=True)

    digest = sha256_file(archive)
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    checksum_data = f"{digest}  {archive.name}\n"
    checksum_tmp = checksum.with_name(f".{checksum.name}.tmp")
    checksum_tmp.write_text(checksum_data, encoding="utf-8", newline="\n")
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
    parser.add_argument(
        "--project-name",
        help="override the archive project prefix (normally auto-detected)",
    )
    args = parser.parse_args()
    try:
        archive, checksum = build_archive(
            ROOT, args.output_dir, project_name=args.project_name
        )
    except (OSError, UnicodeError, ReleaseError, zipfile.BadZipFile) as exc:
        print(f"Release packaging FAILED: {exc}", file=sys.stderr)
        return 1
    print(archive)
    print(checksum)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

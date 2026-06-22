#!/usr/bin/env python3
"""Shared, dependency-free helpers for source manifests and releases.

The release inventory is intentionally strict: every publishable regular file must
appear exactly once in ``MANIFEST-SHA256.csv`` and no symlink is accepted.  Build
products and local caches are excluded by directory/name, at any nesting depth.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterator

MANIFEST_NAME = "MANIFEST-SHA256.csv"
MANIFEST_HEADER = ("path", "bytes", "sha256")

EXCLUDED_DIRECTORY_NAMES = frozenset(
    {
        ".git",
        ".lake",
        ".mypy_cache",
        ".nox",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".upgrade-backup",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "release",
        "site",
        "venv",
    }
)
EXCLUDED_FILE_NAMES = frozenset({MANIFEST_NAME, ".coverage", ".DS_Store"})
EXCLUDED_SUFFIXES = frozenset({".pyc", ".pyo"})
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
VERSION_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+\-]*\Z")


class ReleaseError(RuntimeError):
    """Raised when the release inventory or policy is invalid."""


@dataclass(frozen=True, order=True)
class ManifestEntry:
    path: str
    size: int
    sha256: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_excluded(relative: PurePosixPath) -> bool:
    """Return whether ``relative`` is outside the source-release inventory."""

    return (
        any(part in EXCLUDED_DIRECTORY_NAMES for part in relative.parts)
        or relative.name in EXCLUDED_FILE_NAMES
        or relative.suffix.lower() in EXCLUDED_SUFFIXES
    )


def _canonical_relative_path(raw: str, *, line: int) -> str:
    if not raw or "\\" in raw or "\x00" in raw:
        raise ReleaseError(f"manifest line {line}: invalid path {raw!r}")
    candidate = PurePosixPath(raw)
    if candidate.is_absolute() or candidate.as_posix() != raw:
        raise ReleaseError(f"manifest line {line}: non-canonical path {raw!r}")
    if any(part in {"", ".", ".."} for part in candidate.parts):
        raise ReleaseError(f"manifest line {line}: unsafe path {raw!r}")
    if is_excluded(candidate):
        raise ReleaseError(f"manifest line {line}: excluded path is listed: {raw}")
    return raw


def iter_source_files(root: Path) -> Iterator[tuple[str, Path]]:
    """Yield the canonical source-release files, rejecting included symlinks."""

    root = root.resolve()
    if not root.is_dir():
        raise ReleaseError(f"repository root is not a directory: {root}")

    for directory, directory_names, file_names in os.walk(root, topdown=True, followlinks=False):
        base = Path(directory)
        kept_directories: list[str] = []
        for name in sorted(directory_names):
            child = base / name
            relative = PurePosixPath(child.relative_to(root).as_posix())
            if is_excluded(relative):
                continue
            if child.is_symlink():
                raise ReleaseError(f"included directory symlink is forbidden: {relative}")
            kept_directories.append(name)
        directory_names[:] = kept_directories

        for name in sorted(file_names):
            path = base / name
            relative = PurePosixPath(path.relative_to(root).as_posix())
            if is_excluded(relative):
                continue
            if path.is_symlink():
                raise ReleaseError(f"included file symlink is forbidden: {relative}")
            if not path.is_file():
                raise ReleaseError(f"included path is not a regular file: {relative}")
            yield relative.as_posix(), path


def inventory(root: Path) -> list[ManifestEntry]:
    entries = [
        ManifestEntry(relative, path.stat().st_size, sha256_file(path))
        for relative, path in iter_source_files(root)
    ]
    return sorted(entries)


def render_manifest(root: Path) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(MANIFEST_HEADER)
    for entry in inventory(root):
        writer.writerow((entry.path, entry.size, entry.sha256))
    return stream.getvalue().encode("utf-8")


def write_manifest(root: Path) -> bytes:
    root = root.resolve()
    output = root / MANIFEST_NAME
    data = render_manifest(root)
    temporary = output.with_name(f".{output.name}.tmp")
    temporary.write_bytes(data)
    os.replace(temporary, output)
    return data


def parse_manifest(data: bytes) -> list[ManifestEntry]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReleaseError("manifest must be UTF-8") from exc

    reader = csv.DictReader(io.StringIO(text, newline=""))
    if tuple(reader.fieldnames or ()) != MANIFEST_HEADER:
        raise ReleaseError(
            f"manifest header must be {','.join(MANIFEST_HEADER)!r}; "
            f"got {','.join(reader.fieldnames or [])!r}"
        )

    entries: list[ManifestEntry] = []
    seen: set[str] = set()
    for line, row in enumerate(reader, start=2):
        if None in row or any(value is None for value in row.values()):
            raise ReleaseError(f"manifest line {line}: malformed CSV row")
        raw_path = _canonical_relative_path(row["path"], line=line)
        raw_size = row["bytes"]
        if not raw_size.isdecimal() or str(int(raw_size)) != raw_size:
            raise ReleaseError(f"manifest line {line}: invalid byte count {raw_size!r}")
        digest = row["sha256"]
        if SHA256_RE.fullmatch(digest) is None:
            raise ReleaseError(f"manifest line {line}: invalid SHA-256 {digest!r}")
        if raw_path in seen:
            raise ReleaseError(f"manifest line {line}: duplicate path {raw_path}")
        seen.add(raw_path)
        entries.append(ManifestEntry(raw_path, int(raw_size), digest))

    if entries != sorted(entries):
        raise ReleaseError("manifest rows must be sorted lexicographically by path")
    return entries


def load_manifest(root: Path) -> tuple[bytes, list[ManifestEntry]]:
    manifest = root.resolve() / MANIFEST_NAME
    if not manifest.exists():
        raise ReleaseError(f"missing required {MANIFEST_NAME}")
    if manifest.is_symlink() or not manifest.is_file():
        raise ReleaseError(f"{MANIFEST_NAME} must be a regular file")
    data = manifest.read_bytes()
    return data, parse_manifest(data)


def _format_paths(paths: set[str], *, limit: int = 20) -> str:
    ordered = sorted(paths)
    shown = ordered[:limit]
    suffix = f" … and {len(ordered) - limit} more" if len(ordered) > limit else ""
    return ", ".join(shown) + suffix


def validate_manifest(root: Path) -> list[ManifestEntry]:
    root = root.resolve()
    _, declared = load_manifest(root)
    actual = inventory(root)
    declared_by_path = {entry.path: entry for entry in declared}
    actual_by_path = {entry.path: entry for entry in actual}

    errors: list[str] = []
    missing = set(declared_by_path) - set(actual_by_path)
    untracked = set(actual_by_path) - set(declared_by_path)
    if missing:
        errors.append(f"manifest lists missing files: {_format_paths(missing)}")
    if untracked:
        errors.append(f"files missing from manifest: {_format_paths(untracked)}")

    for path in sorted(set(declared_by_path) & set(actual_by_path)):
        expected = declared_by_path[path]
        observed = actual_by_path[path]
        if observed.size != expected.size:
            errors.append(
                f"size mismatch for {path}: manifest={expected.size}, actual={observed.size}"
            )
        if observed.sha256 != expected.sha256:
            errors.append(
                f"SHA-256 mismatch for {path}: manifest={expected.sha256}, "
                f"actual={observed.sha256}"
            )

    if errors:
        raise ReleaseError("manifest validation failed:\n- " + "\n- ".join(errors))
    return declared


def _included_directory_names(root: Path) -> Iterator[PurePosixPath]:
    root = root.resolve()
    for directory, directory_names, _ in os.walk(root, topdown=True, followlinks=False):
        base = Path(directory)
        kept: list[str] = []
        for name in sorted(directory_names):
            path = base / name
            relative = PurePosixPath(path.relative_to(root).as_posix())
            if is_excluded(relative):
                continue
            if path.is_symlink():
                raise ReleaseError(f"included directory symlink is forbidden: {relative}")
            kept.append(name)
            yield relative
        directory_names[:] = kept


def validate_release_policy(root: Path) -> None:
    root = root.resolve()
    errors: list[str] = []

    required_files = ("README.md", "LICENSE", "VERSION")
    for relative in required_files:
        path = root / relative
        if not path.is_file() or path.is_symlink():
            errors.append(f"missing required regular file: {relative}")

    version_path = root / "VERSION"
    if version_path.is_file():
        version = version_path.read_text(encoding="utf-8").strip()
        if VERSION_RE.fullmatch(version) is None:
            errors.append(f"VERSION is not a safe release identifier: {version!r}")

    try:
        paper_directories = [
            relative.as_posix()
            for relative in _included_directory_names(root)
            if relative.name.lower() == "paper"
        ]
    except ReleaseError as exc:
        errors.append(str(exc))
        paper_directories = []
    if paper_directories:
        errors.append(f"standalone paper directories are forbidden: {paper_directories}")

    try:
        pdfs = [
            relative
            for relative, _ in iter_source_files(root)
            if PurePosixPath(relative).suffix.lower() == ".pdf"
        ]
    except ReleaseError as exc:
        errors.append(str(exc))
        pdfs = []
    if pdfs:
        errors.append(f"committed PDFs are forbidden: {pdfs}")

    contract = root / "docs/contracts/resolvent-interface.json"
    try:
        parsed = json.loads(contract.read_text(encoding="utf-8"))
        if not isinstance(parsed, dict):
            raise ValueError("top-level JSON value must be an object")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"invalid interface contract: {exc}")

    mirror = root / "subprojects/riemann-one-point-resolvent/docs/contracts/resolvent-interface.json"
    if mirror.exists():
        try:
            if mirror.is_symlink() or not mirror.is_file():
                raise ValueError("mirror must be a regular file")
            if contract.read_bytes() != mirror.read_bytes():
                raise ValueError("root and criterion-subproject contracts are not byte-identical")
        except (OSError, ValueError) as exc:
            errors.append(f"invalid mirrored interface contract: {exc}")

    if errors:
        raise ReleaseError("release policy failed:\n- " + "\n- ".join(errors))


def audit_release(root: Path) -> list[ManifestEntry]:
    validate_release_policy(root)
    return validate_manifest(root)

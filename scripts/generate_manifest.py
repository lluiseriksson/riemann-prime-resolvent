#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path, PurePosixPath

root = Path(__file__).resolve().parents[1]
excluded = {".git", ".lake"}


def git(args: list[str], check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_tracked_paths() -> list[str] | None:
    probe = git(["rev-parse", "--is-inside-work-tree"], check=False)
    if probe.returncode != 0:
        return None
    result = git(["ls-files", "-z"])
    paths = [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]
    return sorted(paths, key=lambda path: PurePosixPath(path).parts)


def git_path_changed(path: str) -> bool:
    unstaged = git(["diff", "--quiet", "--", path], check=False)
    staged = git(["diff", "--cached", "--quiet", "--", path], check=False)
    if unstaged.returncode not in {0, 1} or staged.returncode not in {0, 1}:
        raise RuntimeError(f"could not inspect git status for {path}")
    return unstaged.returncode == 1 or staged.returncode == 1


def git_manifest_bytes(path: str) -> bytes:
    if git_path_changed(path) and (root / path).exists():
        oid = git(["hash-object", "-w", f"--path={path}", path]).stdout.strip()
        return git(["cat-file", "-p", oid.decode("ascii")]).stdout
    return git(["show", f":{path}"]).stdout


rows = []
tracked_paths = git_tracked_paths()
if tracked_paths is None:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in excluded for part in path.parts):
            continue
        if path.name in {"FILE_INDEX_SHA256.csv"}:
            continue
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        rows.append((path.relative_to(root).as_posix(), len(data), digest))
else:
    for rel in tracked_paths:
        if rel == "FILE_INDEX_SHA256.csv":
            continue
        data = git_manifest_bytes(rel)
        digest = hashlib.sha256(data).hexdigest()
        rows.append((rel, len(data), digest))

out = root / "FILE_INDEX_SHA256.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\r\n")
    writer.writerow(["path", "bytes", "sha256"])
    writer.writerows(rows)
print(f"Wrote {out} with {len(rows)} entries")

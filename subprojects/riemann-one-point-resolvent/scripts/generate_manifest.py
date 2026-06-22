#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".lake", "__pycache__", ".pytest_cache", "release", "logs"}
EXCLUDED_SUFFIXES = {".aux", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".log", ".out", ".toc"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def included(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    if path.name in {"MANIFEST.json", "SHA256SUMS"}:
        return False
    return path.is_file()


def main() -> None:
    records = []
    for path in sorted(p for p in ROOT.rglob("*") if included(p)):
        records.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = {
        "artifact": "riemann-one-point-resolvent",
        "version": "0.2.0",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "files": records,
    }
    (ROOT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (ROOT / "SHA256SUMS").write_text(
        "".join(f"{r['sha256']}  {r['path']}\n" for r in records), encoding="utf-8"
    )
    print(f"Manifested {len(records)} files")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / f"{ROOT.name}.zip"
EXCLUDED = {".git", ".lake", "__pycache__", ".pytest_cache", "release"}
EXCLUDED_SUFFIXES = {".aux", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".log", ".out", ".toc"}


def include(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return path.is_file() and not any(part in EXCLUDED for part in rel.parts) and path.suffix not in EXCLUDED_SUFFIXES


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if not (ROOT / "MANIFEST.json").exists():
        raise SystemExit("Run scripts/generate_manifest.py first")
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in ROOT.rglob("*") if include(p)):
            arc = Path(ROOT.name) / path.relative_to(ROOT)
            zf.write(path, arc.as_posix())
    digest = sha256(OUT)
    hash_path = OUT.with_suffix(OUT.suffix + ".sha256")
    hash_path.write_text(f"{digest}  {OUT.name}\n", encoding="utf-8")
    shutil.copy2(OUT, ROOT / "release" / OUT.name)
    shutil.copy2(hash_path, ROOT / "release" / hash_path.name)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"SHA256 {digest}")


if __name__ == "__main__":
    main()

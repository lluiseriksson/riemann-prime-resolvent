#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
excluded = {".git", ".lake"}
rows = []
for path in sorted(root.rglob("*")):
    if not path.is_file() or any(part in excluded for part in path.parts):
        continue
    if path.name in {"FILE_INDEX_SHA256.csv"}:
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append((str(path.relative_to(root)), path.stat().st_size, digest))

out = root / "FILE_INDEX_SHA256.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["path", "bytes", "sha256"])
    writer.writerows(rows)
print(f"Wrote {out} with {len(rows)} entries")

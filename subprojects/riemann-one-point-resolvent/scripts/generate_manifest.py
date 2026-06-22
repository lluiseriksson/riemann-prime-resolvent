#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'MANIFEST-SHA256.csv'
EXCLUDED_PARTS = {'.git', '.lake', 'site', '__pycache__', '.pytest_cache', 'release'}
EXCLUDED_NAMES = {'MANIFEST-SHA256.csv'}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    rows = []
    for path in sorted(ROOT.rglob('*')):
        rel = path.relative_to(ROOT)
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if path.name in EXCLUDED_NAMES:
            continue
        rows.append((rel.as_posix(), path.stat().st_size, digest(path)))
    with OUT.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['path', 'bytes', 'sha256'])
        writer.writerows(rows)
    print(f'Wrote {OUT.name} with {len(rows)} entries')


if __name__ == '__main__':
    main()

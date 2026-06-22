#!/usr/bin/env python3
"""Release policy and manifest verification."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    failures: list[str] = []
    if any(path.is_dir() and path.name.lower() == 'paper' for path in ROOT.rglob('*')):
        failures.append('standalone paper directory is forbidden')
    pdfs = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*.pdf')]
    if pdfs:
        failures.append(f'committed PDFs are forbidden: {pdfs}')
    contract = ROOT / 'docs/contracts/resolvent-interface.json'
    try:
        json.loads(contract.read_text(encoding='utf-8'))
    except Exception as exc:
        failures.append(f'invalid interface contract: {exc}')
    manifest = ROOT / 'MANIFEST-SHA256.csv'
    if manifest.exists():
        with manifest.open(newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                path = ROOT / row['path']
                if not path.exists():
                    failures.append(f'manifest missing file: {row["path"]}')
                    continue
                if path.stat().st_size != int(row['bytes']):
                    failures.append(f'manifest size mismatch: {row["path"]}')
                if digest(path) != row['sha256']:
                    failures.append(f'manifest hash mismatch: {row["path"]}')
    if failures:
        print('Release audit FAILED:', file=sys.stderr)
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print('Release audit passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

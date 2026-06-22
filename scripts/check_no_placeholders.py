#!/usr/bin/env python3
"""Reject proof placeholders and project-level axiom shortcuts in Lean sources."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_DIRS = [ROOT / 'RiemannPrimeResolvent']
EXTRA = [ROOT / 'RiemannPrimeResolvent.lean', ROOT / 'oracle_check.lean']
PATTERNS = {
    'sorry': re.compile(r'\bsorry\b'),
    'admit': re.compile(r'\badmit\b'),
    'axiom': re.compile(r'^\s*(?:protected\s+)?axiom\b', re.MULTILINE),
    'unsafe theorem': re.compile(r'\bunsafe\s+(?:theorem|lemma)\b'),
}


def strip_comments(text: str) -> str:
    text = re.sub(r'/-(?:.|\n)*?-/', '', text)
    return re.sub(r'--.*', '', text)


def main() -> int:
    files = []
    for directory in LEAN_DIRS:
        files.extend(sorted(directory.rglob('*.lean')))
    files.extend(path for path in EXTRA if path.exists())
    failures: list[str] = []
    for path in files:
        clean = strip_comments(path.read_text(encoding='utf-8'))
        for label, pattern in PATTERNS.items():
            if pattern.search(clean):
                failures.append(f'{path.relative_to(ROOT)}: {label}')
    if failures:
        print('Placeholder/axiom audit FAILED:', file=sys.stderr)
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print(f'Placeholder/axiom audit passed for {len(files)} Lean files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

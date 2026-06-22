#!/usr/bin/env python3
"""Check local Markdown links and images without making network requests."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')
SKIP_PREFIXES = ('http://', 'https://', 'mailto:', '#', 'data:')


def main() -> int:
    failures: list[str] = []
    checked = 0
    for path in sorted([ROOT / 'README.md', *ROOT.joinpath('docs').rglob('*.md')]):
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        for raw in LINK.findall(text):
            target = raw.split()[0].strip('<>')
            if target.startswith(SKIP_PREFIXES):
                continue
            target = unquote(target.split('#', 1)[0])
            if not target:
                continue
            checked += 1
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f'{path.relative_to(ROOT)}: escapes repository: {raw}')
                continue
            if not candidate.exists():
                failures.append(f'{path.relative_to(ROOT)}: missing {target}')
    if failures:
        print('Markdown link audit FAILED:', file=sys.stderr)
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print(f'Markdown link audit passed ({checked} local targets)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

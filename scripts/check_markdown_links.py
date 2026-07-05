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


def markdown_destination(raw: str) -> str:
    """Extract a Markdown destination, preserving spaces inside ``<...>``.

    CommonMark permits angle-bracket destinations specifically so paths may
    contain spaces.  A title following a plain destination is ignored.
    """

    value = raw.strip()
    if value.startswith('<'):
        closing = value.find('>')
        if closing >= 0:
            return value[1:closing]
    return value.split(maxsplit=1)[0] if value else ''


def audit_markdown_links(root: Path) -> tuple[int, list[str]]:
    """Return ``(checked_target_count, failures)`` for a repository root."""

    root = root.resolve()
    failures: list[str] = []
    checked = 0
    paths = sorted([root / 'README.md', *root.joinpath('docs').rglob('*.md')])
    for path in paths:
        if not path.exists():
            continue
        display_path = path.relative_to(root).as_posix()
        text = path.read_text(encoding='utf-8')
        for raw in LINK.findall(text):
            target = markdown_destination(raw)
            if target.startswith(SKIP_PREFIXES):
                continue
            target = unquote(target.split('#', 1)[0])
            if not target:
                continue
            checked += 1
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                failures.append(f'{display_path}: escapes repository: {raw}')
                continue
            if not candidate.exists():
                failures.append(f'{display_path}: missing {target}')
    return checked, failures


def main() -> int:
    checked, failures = audit_markdown_links(ROOT)
    if failures:
        print('Markdown link audit FAILED:', file=sys.stderr)
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print(f'Markdown link audit passed ({checked} local targets)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

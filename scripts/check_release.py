#!/usr/bin/env python3
"""Audit source-release policy and the exact manifest inventory."""
from __future__ import annotations

import sys
from pathlib import Path

from release_common import ReleaseError, audit_release

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        entries = audit_release(ROOT)
    except (OSError, UnicodeError, ReleaseError) as exc:
        print(f"Release audit FAILED: {exc}", file=sys.stderr)
        return 1
    total = sum(entry.size for entry in entries)
    print(f"Release audit passed: {len(entries)} files, {total} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

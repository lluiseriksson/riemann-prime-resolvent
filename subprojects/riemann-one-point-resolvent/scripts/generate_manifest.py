#!/usr/bin/env python3
"""Create or verify the deterministic source manifest."""
from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

from release_common import MANIFEST_NAME, ReleaseError, render_manifest, write_manifest

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed manifest without modifying it",
    )
    args = parser.parse_args()

    try:
        expected = render_manifest(ROOT)
        output = ROOT / MANIFEST_NAME
        if args.check:
            if not output.is_file() or output.is_symlink():
                raise ReleaseError(f"missing required regular file: {MANIFEST_NAME}")
            observed = output.read_bytes()
            if observed != expected:
                before = observed.decode("utf-8", errors="replace").splitlines(keepends=True)
                after = expected.decode("utf-8").splitlines(keepends=True)
                preview = "".join(
                    difflib.unified_diff(
                        before,
                        after,
                        fromfile=MANIFEST_NAME,
                        tofile=f"{MANIFEST_NAME} (expected)",
                        n=2,
                    )
                )
                if len(preview) > 12_000:
                    preview = preview[:12_000] + "\n… diff truncated …\n"
                raise ReleaseError(
                    f"{MANIFEST_NAME} is stale; run {Path(__file__).name} without --check\n{preview}"
                )
            print(f"{MANIFEST_NAME} is current ({expected.count(b'\n') - 1} entries)")
            return 0

        write_manifest(ROOT)
        print(f"Wrote {MANIFEST_NAME} with {expected.count(b'\n') - 1} entries")
        return 0
    except (OSError, ReleaseError) as exc:
        print(f"Manifest operation FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

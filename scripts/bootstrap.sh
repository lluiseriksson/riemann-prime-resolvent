#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

for cmd in git lake lean python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    echo "Install Elan/Lean first; see AGENT-ONBOARDING.md." >&2
    exit 127
  fi
done

echo "== Environment =="
date -u --iso-8601=seconds || date -u
uname -a
lean --version
lake --version

echo "== Dependency cache =="
# The manifest is already pinned.  `lake exe cache get` is idempotent.
lake exe cache get

echo "== Build =="
lake build

echo "Bootstrap completed successfully."

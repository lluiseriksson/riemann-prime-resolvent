#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
for cmd in git lake lean python3; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "Missing required command: $cmd" >&2; exit 127; }
done
lean --version
lake --version
lake exe cache get
./scripts/verify.sh
